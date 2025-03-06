from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.middleware.cors import CORSMiddleware
from src.logger import logging
from src.data_model.data_model import create_data_model
from src.matrix.osrm_distance_matrix import create_osrm_distance_mat
from src.tsp.tsp_route import get_route_tsp
from src.vrp.vrp_route import get_vrp_solution
import io
import pandas as pd
from pydantic import BaseModel

class ShopDemandUpdate(BaseModel):
    shop_name: str
    shop_demand: int

app = FastAPI()

# Allow frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Data Model
data = create_data_model()

@app.post('/upload_data')
async def upload_data(file: UploadFile = File(...)):
    """ Upload CSV data and generate distance matrix """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

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
            data['shop_demands'] = {df['ADDRESS'][i]: demand_list[i] for i in range(len(df['ADDRESS']))}
        
        return {"message": "Distance matrix updated successfully", "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e

@app.post('/solve_tsp')
async def solve_tsp_route():
    """ Solve TSP if valid data exists """
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
    """ Add a vehicle with a specified capacity """
    if 'vehicle_capacities' not in data:
        data['vehicle_capacities'] = {}
    data['vehicle_capacities'][vehicle_name] = vehicle_capacity
    return {"message": "Vehicle added successfully", "data": data['vehicle_capacities']}

@app.delete('/remove_vehicle')
async def remove_vehicle(vehicle_name: str):
    """ Remove a vehicle by name """
    if 'vehicle_capacities' in data and vehicle_name in data['vehicle_capacities']:
        del data['vehicle_capacities'][vehicle_name]
        return {"message": "Vehicle removed successfully", "data": data['vehicle_capacities']}
    raise HTTPException(status_code=404, detail="Vehicle not found.")

@app.post('/add_restricted_road')
async def add_restricted_road(start_location: str, end_location: str):
    """ Add a restricted road between two locations """
    if 'restricted_roads' not in data:
        data['restricted_roads'] = []
    data['restricted_roads'].append((start_location, end_location))
    return {"message": "Restricted road added successfully", "data": data['restricted_roads']}

@app.delete('/remove_restricted_road')
async def remove_restricted_road(start_location: str, end_location: str):
    """ Remove a restricted road """
    if 'restricted_roads' in data and (start_location, end_location) in data['restricted_roads']:
        data['restricted_roads'].remove((start_location, end_location))
        return {"message": "Restricted road removed successfully", "data": data['restricted_roads']}
    raise HTTPException(status_code=404, detail="Restricted road not found.")

@app.post('/edit_shop_demand')
async def edit_shop_demand(update: ShopDemandUpdate):
    """ Edit the demand for an existing shop """
    if 'shop_demands' not in data or update.shop_name not in data['shop_demands']:
        raise HTTPException(status_code=404, detail=f"Shop '{update.shop_name}' not found in existing data.")

    data['shop_demands'][update.shop_name] = update.shop_demand
    print(data['shop_demands'])
    return {"message": f"Shop demand for '{update.shop_name}' updated successfully!", "data": data['shop_demands']}

@app.delete('/remove_shop_demand')
async def remove_shop_demand(shop_name: str):
    """ Remove a shop's demand """
    if 'shop_demands' in data and shop_name in data['shop_demands']:
        del data['shop_demands'][shop_name]
        return {"message": "Shop demand removed successfully", "data": data['shop_demands']}
    raise HTTPException(status_code=404, detail="Shop not found.")

@app.delete('/reset_data')
async def reset_data():
    """ Reset the entire data model to default """
    global data
    data = create_data_model()
    return {"message": "All data has been reset successfully."}

@app.post('/solve_vrp')
async def solve_vrp():
    """ Solve VRP only if valid data exists """
    if not data.get('distance_matrix') or not data.get('locations'):
        logging.error("Attempted to solve VRP without uploading data.")
        raise HTTPException(status_code=400, detail="No distance matrix found. Please upload data first.")
    
    if not data.get('vehicle_capacities'):
        logging.error("Attempted to solve VRP without updating vehicle capacities.")
        raise HTTPException(status_code=400, detail="No vehicle capacities found. Please add vehicles first.")
    
    try:
        solution = get_vrp_solution(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e
    
    return solution

@app.delete('/reset')
async def reset(self):
    """ Reset the entire data model to default and log the action """
    global data
    data = create_data_model()
    logging.info('All data has been reset successfully.')
    return {"message": "All data has been reset successfully."}
@app.get('/get_data')
async def get_data():
    """ Retrieve current data model """
    return data
        
@app.get('/')
def home():
    logging.info('Home endpoint accessed.')
    return {'message': 'TSP Solver API is running!'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8088)
