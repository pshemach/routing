from src.vrp.vrp_manager import vrp_manager
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
from src.logger import logging

def create_vehicle_cost_callback(vehicle_id, data, manager):
    """
    Returns a transit callback that accounts for:
    - Vehicle-specific restricted roads
    - General restricted roads
    - Default distance from the distance matrix
    """

    def transit_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)

        # Vehicle-specific restricted roads
        if (from_node, to_node) in data.get("vehicle_restricted_roads", {}).get(vehicle_id, []):
            logging.warning(f"Vehicle {vehicle_id} restricted from traveling {from_node} -> {to_node}. Applying high cost.")
            return int(1e6)  # High penalty cost

        # General restricted roads
        if (from_node, to_node) in data.get("restricted_roads", []):
            logging.warning(f"Route {from_node} -> {to_node} is generally restricted. Applying high cost.")
            return int(1e6)  # High penalty cost

        # Default travel cost from distance matrix
        return int(data["distance_matrix"][from_node][to_node])

    return transit_callback


def create_demand_callback(data, manager):
    """Returns a callback function to fetch shop demands correctly."""

    def demand_callback(from_index):
        """Fetches demand value for a given location index."""
        from_node = manager.IndexToNode(from_index)
        return data["shop_demands"].get(data["locations"][from_node], 0)  

    return demand_callback



def add_capacity_constraints(routing, manager, data):
    """Ensures vehicle capacity constraints are applied correctly."""
    
    demand_callback = create_demand_callback(data, manager)
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # No slack
        list(data["vehicle_capacities"].values()),  
        True,  # Start cumul to zero
        "Capacity",
    )

    logging.info("Capacity constraints added successfully.")


    logging.info("Capacity constraints added successfully.")


def add_distance_constraints(routing, transit_callback_index):
    """
    Adds distance constraints to prevent exceeding a maximum travel distance.
    """
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # No slack
        3000,  # Default vehicle max travel distance
        True,  # Start cumul to zero
        dimension_name,
    )

    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)
    
    logging.info("Distance constraints added successfully.")


def add_same_route_constraints(routing, manager, data):
    """
    Ensures that paired locations (pickup & delivery) are assigned to the same vehicle.
    If no such constraints exist, the function safely skips execution.
    """
    same_route_locations = data.get("same_route_locations", [])
    if not same_route_locations:
        logging.info("No same-route constraints provided. Skipping this step.")
        return

    for request in same_route_locations:
        try:
            pickup_index = manager.NodeToIndex(request[0])
            delivery_index = manager.NodeToIndex(request[1])
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(delivery_index)
            )
            logging.info(f"Same-route constraint added: {request[0]} <-> {request[1]}")
        except Exception as e:
            logging.error(f"Error adding same-route constraint for {request}: {str(e)}")


def add_vehicle_restrictions(routing, manager, data):
    """
    Prevents specific vehicles from visiting certain locations.
    If no such restrictions exist, the function safely skips execution.
    """
    vehicle_restricted_locations = data.get("vehicle_restricted_locations", {})
    if not vehicle_restricted_locations:
        logging.info("No vehicle-specific restricted locations provided. Skipping this step.")
        return

    for vehicle_id, locations in vehicle_restricted_locations.items():
        for location in locations:
            try:
                index = manager.NodeToIndex(location)
                routing.solver().Add(routing.VehicleVar(index) != vehicle_id)
                logging.info(f"Vehicle {vehicle_id} restricted from visiting location {location}.")
            except Exception as e:
                logging.error(f"Error restricting vehicle {vehicle_id} from location {location}: {str(e)}")


def solve_vrp(data):
    """
    Solves the Vehicle Routing Problem (VRP) given distance matrix, demands, and constraints.
    """

    # Initialize OR-Tools Manager & Routing Model
    manager = vrp_manager(data=data)
    routing = pywrapcp.RoutingModel(manager)

    num_vehicles = len(data.get("vehicle_capacities", []))
    if num_vehicles == 0:
        logging.error("No vehicles available for VRP.")
        raise ValueError("No vehicles available for VRP.")

    # Register vehicle-specific cost callbacks
    for vehicle_id in range(num_vehicles):
        transit_callback = create_vehicle_cost_callback(vehicle_id, data, manager)
        transit_callback_index = routing.RegisterTransitCallback(transit_callback)
        routing.SetArcCostEvaluatorOfVehicle(transit_callback_index, vehicle_id)

    # Apply constraints
    add_capacity_constraints(routing, manager, data)
    add_distance_constraints(routing, transit_callback_index)
    add_same_route_constraints(routing, manager, data)
    add_vehicle_restrictions(routing, manager, data)

    # Configure search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )

    logging.info("Solving VRP...")
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        logging.info("VRP Solution Found!")
    else:
        logging.warning("No solution found for VRP.")

    return manager, routing, solution
