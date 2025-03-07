from src.logger import logging
from src.vrp.solve_vrp import solve_vrp

def get_vrp_solution(data):
    """
    Extracts solution details for VRP and returns structured route paths.
    
    Returns:
        dict: Containing each vehicle's route details with distance & load.
    """
    
    manager, routing, solution = solve_vrp(data=data)

    if not solution:
        logging.error("No solution found!")
        return {"message": "No solution found!"}

    total_distance = 0
    total_load = 0
    routes = {}
    
    num_vehicles = len(data.get('vehicle_capacities'))

    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route_path = []
        route_distance = 0
        route_load = 0
        vehicle_details = {
            "vehicle_id": vehicle_id,
            "route": [],
            "total_distance": 0,
            "total_load": 0
        }

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            location_name = data['locations'][node_index]  
            demand = data['shop_demands'].get(location_name, 0)  
            route_load += demand  

            route_path.append({
                "location": location_name,  
                "current_load": route_load
            })
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

        # Add last depot stop
        route_path.append({"location": data['locations'][manager.IndexToNode(index)], "current_load": route_load})
        
        # Store route details
        vehicle_details["route"] = route_path
        vehicle_details["total_distance"] = route_distance
        vehicle_details["total_load"] = route_load
        routes[f"Vehicle {list(data.get('vehicle_capacities').keys())[vehicle_id]}"] = vehicle_details

        # Update overall totals
        total_distance += route_distance
        total_load += route_load

        logging.info(f"Route for vehicle {vehicle_id}: {route_path}")
        logging.info(f"Distance: {route_distance} km, Load: {route_load}")

    logging.info(f"Total distance of all routes: {total_distance} km")
    logging.info(f"Total load of all routes: {total_load}")

    return {
        "routes": routes,
        "total_distance": total_distance,
        "total_load": total_load
    }