from fastapi import APIRouter, HTTPException
from src.logger import logging
from src.data_model.global_data import data
from src.vrp.vrp_route import get_vrp_solution

router = APIRouter()

@router.post('/solve_vrp')
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