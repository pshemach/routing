# routes/upload.py
from fastapi import APIRouter, UploadFile, HTTPException, File
from src.data_model.global_data import data
from src.matrix.osrm_distance_matrix import create_osrm_distance_mat
from src.logger import logging
import pandas as pd
import io

router = APIRouter()

@router.post('/upload_data')
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
