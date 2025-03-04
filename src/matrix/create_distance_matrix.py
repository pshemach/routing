from src.logger import logging
import pandas as pd
import numpy as np
import time
from src.utils.helper import get_osrm_distance

def create_distance_mat(df_path):
    try:
        logging.info("Loading CSV file for distance matrix computation.")
        df = pd.read_csv(df_path)
        
        # Validate required columns
        required_columns = {"ADDRESS", "LATITUDE", "LONGITUDE"}
        if not required_columns.issubset(df.columns):
            logging.error("Missing required columns in CSV file.")
            raise ValueError("CSV file must contain 'ADDRESS', 'LATITUDE', and 'LONGITUDE' columns")
        
        # Remove duplicates and extract necessary data
        unique_locations_df = df.drop_duplicates(subset=["ADDRESS"])[["ADDRESS", "LATITUDE", "LONGITUDE"]]
        location_names = unique_locations_df["ADDRESS"].to_list()
        locations_gps = list(zip(unique_locations_df["LATITUDE"], unique_locations_df["LONGITUDE"]))
        
        num_locations = len(location_names)
        distance_matrix = np.zeros((num_locations, num_locations))
        
        logging.info(f"Processing {num_locations} locations for distance matrix computation.")
        
        # Compute distance matrix
        for i in range(num_locations):
            for j in range(i + 1, num_locations):  # Avoid duplicate calculations
                try:
                    dis = get_osrm_distance(locations_gps[i], locations_gps[j])
                    distance_matrix[i, j] = dis
                    distance_matrix[j, i] = dis
                    time.sleep(0.2)  # Prevent rate limiting
                except Exception as e:
                    logging.error(f"Error computing distance between {location_names[i]} and {location_names[j]}: {str(e)}")
                    distance_matrix[i, j] = distance_matrix[j, i] = float('inf')  # Set as unreachable if an error occurs
        
        logging.info("Distance matrix computation completed successfully.")
        return pd.DataFrame(distance_matrix, index=location_names, columns=location_names)
    
    except Exception as e:
        logging.critical(f"Unexpected error in distance matrix creation: {str(e)}")
        raise