# routes/tsp.py
from fastapi import APIRouter, HTTPException
from src.data_model.global_data import data
from src.tsp.tsp_route import get_route_tsp

router = APIRouter()

@router.post("/solve_tsp")
async def solve_tsp_route():
    """ Solve TSP if valid data exists """
    if not data.get("distance_matrix") or not data.get("locations"):
        raise HTTPException(status_code=400, detail="No distance matrix found. Please upload data first.")

    try:
        route_order, total_distance = get_route_tsp(data["distance_matrix"], data["locations"], data["depot"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e

    return {"route_order": route_order, "total_distance": total_distance}
