import requests

# Function to get distance from OSRM API
def get_osrm_distance(origin, destination):
    """
    Get the distance between two coordinates using OSRM API.
    :param origin: (latitude, longitude)
    :param destination: (latitude, longitude)
    :return: Distance in meters
    """
    osrm_base_url = "http://router.project-osrm.org/route/v1/car"
    url = f"{osrm_base_url}/{origin[1]},{origin[0]};{destination[1]},{destination[0]}?overview=false"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "routes" in data and len(data["routes"]) > 0:
            return data["routes"][0]["distance"] / 1000  # Convert meters to km
    return np.inf  # Return infinity if no valid route is found