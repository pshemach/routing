# routes/vehicles.py
from fastapi import APIRouter, HTTPException
from src.data_model.global_data import data

router = APIRouter()

@router.post('/add_vehicle')
async def add_vehicle(vehicle_name: str, vehicle_capacity: int):
    """ Add a vehicle with a specified capacity """
    if 'vehicle_capacities' not in data:
        data['vehicle_capacities'] = {}
    data['vehicle_capacities'][vehicle_name] = vehicle_capacity
    return {"message": "Vehicle added successfully", "data": data['vehicle_capacities']}

@router.delete('/remove_vehicle')
async def remove_vehicle(vehicle_name: str):
    """ Remove a vehicle by name """
    if 'vehicle_capacities' in data and vehicle_name in data['vehicle_capacities']:
        del data['vehicle_capacities'][vehicle_name]
        return {"message": "Vehicle removed successfully", "data": data['vehicle_capacities']}
    raise HTTPException(status_code=404, detail="Vehicle not found.")
