from ortools.constraint_solver import pywrapcp
from src.logger import logging

def vrp_manager(data):
    try:
        logging.info("Initializing VRP Manager with depot location.")
        distance_matrix = data.get('distance_matrix')
        depot = data.get('depot')
        num_vehicles = len(data.get('vehicle_capacities'))
        manager = pywrapcp.RoutingIndexManager(
            len(distance_matrix), num_vehicles, depot
        ) 
        
        logging.info("VRP Manager successfully created.")
        return manager
    except ValueError as ve:
        logging.error(f"Depot location not found in locations list: {str(ve)}")
    except Exception as e:
        logging.critical(f"Unexpected error in TSP Manager creation: {str(e)}")