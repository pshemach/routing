from fastapi import APIRouter, HTTPException
from src.data_model.global_data import data, reset_global_data

router = APIRouter()

@router.get('/get_data')
async def get_data():
    """ Retrieve current data model """
    return data

@router.delete('/reset_data')
async def reset_data():
    """ Reset the entire data model to default """
    reset_global_data()
    return {"message": "All data has been reset successfully."}