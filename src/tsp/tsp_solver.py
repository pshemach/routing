from src.logger import logging
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from src.tsp.manager import tsp_manager

def get_solution(distance_matrix, locations):
    try:
        logging.info("Initializing TSP Manager.")
        manager = tsp_manager(distance_matrix, locations)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(distance_matrix[from_node][to_node])
        
        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )

        logging.info("Solving TSP with OR-Tools.")
        solution = routing.SolveWithParameters(search_parameters)

        if solution is None:
            logging.error("No solution found by OR-Tools.")
        else:
            logging.info("TSP solution successfully found.")
        
        return solution, routing, manager
    except Exception as e:
        logging.critical(f"Unexpected error in TSP solution process: {str(e)}")
        raise
