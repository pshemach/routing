from fastapi import APIRouter, HTTPException
from src.data_model.global_data import data

router = APIRouter()

@router.post('/add_restricted_road')
async def add_restricted_road(start_location: str, end_location: str):
    """ Add a restricted road between two locations """
    if 'restricted_roads' not in data:
        data['restricted_roads'] = []
    data['restricted_roads'].append((start_location, end_location))
    return {"message": "Restricted road added successfully", "data": data['restricted_roads']}

@router.delete('/remove_restricted_road')
async def remove_restricted_road(start_location: str, end_location: str):
    """ Remove a restricted road """
    if 'restricted_roads' in data and (start_location, end_location) in data['restricted_roads']:
        data['restricted_roads'].remove((start_location, end_location))
        return {"message": "Restricted road removed successfully", "data": data['restricted_roads']}
    raise HTTPException(status_code=404, detail="Restricted road not found.")