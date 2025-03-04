from ortools.constraint_solver import pywrapcp
from src.constants import DEPOT
from src.logger import logging

def tsp_manager(distance_matrix, locations):
    try:
        logging.info("Initializing TSP Manager with depot location.")
        depot_index = locations.index(DEPOT)
        
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix), 1, depot_index
        ) 
        
        logging.info("TSP Manager successfully created.")
        return manager
    except ValueError as ve:
        logging.error(f"Depot location not found in locations list: {str(ve)}")
        raise
    except Exception as e:
        logging.critical(f"Unexpected error in TSP Manager creation: {str(e)}")
        raise