from src.logger import logging
import pandas as pd

def load_distance_matrix(distance_matrix_path):
    try:
        logging.info("Loading distance matrix from CSV file.")
        distance_matrix_df = pd.read_csv(distance_matrix_path, index_col=0)
        
        if distance_matrix_df.empty:
            logging.error("The distance matrix CSV file is empty.")
            raise ValueError("The distance matrix CSV file is empty.")
        
        distance_matrix = distance_matrix_df.values
        locations = distance_matrix_df.index.tolist()
        
        logging.info("Distance matrix successfully loaded.")
        return distance_matrix, locations
    except FileNotFoundError as fnf:
        logging.error(f"File not found: {str(fnf)}")
        raise
    except pd.errors.EmptyDataError as ede:
        logging.error(f"Empty data error: {str(ede)}")
        raise
    except Exception as e:
        logging.critical(f"Unexpected error while loading distance matrix: {str(e)}")
        raise

