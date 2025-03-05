def create_data_model(
    distance_matrix=None,
    locations=None,
    depot=0,
    shop_demands=None,
    vehicle_capacities=None,
    vehicle_restricted_locations=None,
    vehicle_restricted_roads=None,
    same_route_locations=None,
):
    return {
        "distance_matrix": distance_matrix or [],
        "locations": locations or [],
        "depot": depot,
        "shop_demands": shop_demands or {},
        "vehicle_capacities": vehicle_capacities or {},
        "vehicle_restricted_locations": vehicle_restricted_locations or {},
        "vehicle_restricted_roads": vehicle_restricted_roads or {},
        "same_route_locations": same_route_locations or [],
    }
