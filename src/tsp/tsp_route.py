from src.logger import logging
from src.tsp.tsp_solver import get_solution

def get_route_tsp(distance_matrix, locations):
    print("get_route_tsp")
    try:
        solution, routing, manager = get_solution(distance_matrix, locations)
        
        if solution is None:
            logging.error("No solution found for the given TSP problem.")
            raise ValueError("No solution found.")
        
        index = routing.Start(0)
        total_distance = 0
        route_order = []

        while not routing.IsEnd(index):
            route_order.append(locations[manager.IndexToNode(index)])
            next_index = solution.Value(routing.NextVar(index))
            total_distance += distance_matrix[manager.IndexToNode(index)][
                manager.IndexToNode(next_index)
            ]
            index = next_index

        route_order.append(locations[manager.IndexToNode(index)])  # Return to depot
        
        logging.info(f"Optimal route found: {' -> '.join(route_order)}")
        logging.info(f"Total Distance: {total_distance:.2f} km")
        
        return route_order, total_distance
    
    except ValueError as ve:
        logging.error(f"ValueError: {str(ve)}")
        raise
    except Exception as e:
        logging.critical(f"Unexpected error in solving TSP: {str(e)}")
        raise
