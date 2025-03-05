from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from src.logger import logging
from src.data_model.data_model import create_data_model
from src.matrix.osrm_distance_matrix import create_osrm_distance_mat
from src.tsp.tsp_route import get_route_tsp
from src.vrp.vrp_route import get_vrp_solution
import io
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data = create_data_model()

@app.post('/upload_data')
async def solve_tsp(file: UploadFile = File(...),):
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail='Invalid file format. Please upload a CSV file.')
        
        contents = await file.read()
        df_path = io.StringIO(contents.decode("utf-8"))
        logging.info("Loading CSV file for distance matrix computation.")
        df = pd.read_csv(df_path)
        try:
            distance_matrix, locations = create_osrm_distance_mat(df)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error generating distance matrix: {str(e)}") from e
            
        data['distance_matrix'] = distance_matrix.tolist() if hasattr(distance_matrix, "tolist") else distance_matrix
        data['locations'] = locations
        
        if "DEMAND" in df.columns:
            demand_list = df['DEMAND'].to_list()
            data['shop_demands'] = {}
            for i, loc in enumerate(df['ADDRESS']):
                print(loc)
                data['shop_demands'][loc] = demand_list[i]       
        return {'message': 'Distance matrix updated successfully', 'data': data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e

@app.post('/solve_tsp')
async def solve_tsp_route():
    """ Solve TSP only if valid data is available. """
    
    # Ensure required data is available before running TSP
    if not data.get('distance_matrix') or not data.get('locations'):
        logging.error("Attempted to solve TSP without uploading data.")
        raise HTTPException(status_code=400, detail="No distance matrix found. Please upload data first.")
    
    try:
        logging.info("Solving TSP...")
        route_order, total_distance = get_route_tsp(
            distance_matrix=data['distance_matrix'], 
            locations=data['locations'],
            depot=data['depot']
        )
    except Exception as e:
        logging.error(f"Unexpected error solving TSP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e
    
    return {"route_order": route_order, "total_distance": total_distance}

@app.post('/add_vehicle')
async def add_vehicle(vehicle_name: str, vehicle_capacity: int):
    if 'vehicle_capacities' not in data:
        data['vehicle_capacities'] = {}
    data['vehicle_capacities'][vehicle_name] = vehicle_capacity
    return {"message": "Vehicle added successfully", "data": data['vehicle_capacities']}

@app.post('/add_restricted_road')
async def add_restricted_road(start_location: str, end_location: str):
    if 'restricted_roads' not in data:
        data['restricted_roads'] = []
    data['restricted_roads'].append((start_location, end_location))
    return {"message": "Restricted road added successfully", "data": data['restricted_roads']}

@app.post('/add_vehicle_restricted_location')
async def add_vehicle_restricted_location(vehicle_name: str, location: str):
    if 'vehicle_restricted_locations' not in data:
        data['vehicle_restricted_locations'] = {}
    data['vehicle_restricted_locations'][vehicle_name] = location
    return {"message": "Vehicle restricted location added successfully", "data": data['vehicle_restricted_locations']}

@app.post('/add_vehicle_restricted_road')
async def add_vehicle_restricted_road(vehicle_name: str, start_location: str, end_location: str):
    if 'vehicle_restricted_roads' not in data:
        data['vehicle_restricted_roads'] = {}
    data['vehicle_restricted_roads'][vehicle_name] = (start_location, end_location)
    return {"message": "Vehicle restricted road added successfully", "data": data['vehicle_restricted_roads']}

@app.post('/add_same_route_location')
async def add_same_route_location(locations: list[str]):
    if 'same_route_locations' not in data:
        data['same_route_locations'] = []
    data['same_route_locations'].append(locations)
    return {"message": "Same route locations added successfully", "data": data['same_route_locations']}

@app.post('/solve_vrp')
async def solve_vrp():
    if not data.get('distance_matrix') or not data.get('locations'):
        raise HTTPException(status_code=404, detail="No distance matrix found. Please upload data first.")
    
    if not data.get('vehicle_capacities'):
        raise HTTPException(status_code=400, detail="No vehicle capacities found. Please add vehicles first.")
    
    try:
        solution = get_vrp_solution(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e
    
    return solution

@app.get('/get_data')
async def get_data():
    return data
        
@app.get('/')
def home():
    logging.info('Home endpoint accessed.')
    return {'message': 'TSP Solver API is running!'}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8086)