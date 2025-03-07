# routes/shops.py
from fastapi import APIRouter, HTTPException
from src.data_model.global_data import data
from pydantic import BaseModel

class ShopDemandUpdate(BaseModel):
    shop_name: str
    shop_demand: int


router = APIRouter()

@router.post('/edit_shop_demand')
async def edit_shop_demand(update: ShopDemandUpdate):
    """ Edit the demand for an existing shop """
    if 'shop_demands' not in data or update.shop_name not in data['shop_demands']:
        raise HTTPException(status_code=404, detail=f"Shop '{update.shop_name}' not found in existing data.")

    data['shop_demands'][update.shop_name] = update.shop_demand
    print(data['shop_demands'])
    return {"message": f"Shop demand for '{update.shop_name}' updated successfully!", "data": data['shop_demands']}

@router.delete('/remove_shop_demand')
async def remove_shop_demand(shop_name: str):
    """ Remove a shop's demand """
    if 'shop_demands' in data and shop_name in data['shop_demands']:
        del data['shop_demands'][shop_name]
        return {"message": "Shop demand removed successfully", "data": data['shop_demands']}
    raise HTTPException(status_code=404, detail="Shop not found.")