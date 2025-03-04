from fastapi import FastAPI, File, UploadFile, HTTPException
from src.matrix.osrm_distance_matrix import create_distance_mat
from src.tsp.tsp_route import get_route_tsp
import io
from src.logger import logging

app = FastAPI()


@app.post("/solve_tsp")
async def solve_tsp(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            logging.error("Invalid file format. Only CSV files are allowed.")
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
        
        contents = await file.read()
        df_path = io.StringIO(contents.decode("utf-8"))
        
        try:
            distance_matrix, locations = create_distance_mat(df_path)
            logging.info(f"Distance matrix loaded successfully. Locations: {locations}")
        except Exception as e:
            logging.error(f"Error loading distance matrix: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error loading distance matrix: {str(e)}")
        
        if distance_matrix.size == 0 or not locations:
            logging.error("Invalid or empty distance matrix.")
            raise HTTPException(status_code=400, detail="Invalid or empty distance matrix.")
        
        try:
            route_order, total_distance = get_route_tsp(distance_matrix, locations)
        except Exception as e:
            logging.error(f"Error solving TSP: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error solving TSP: {str(e)}")
        
        logging.info(f"TSP solved successfully. Route: {route_order}, Total Distance: {total_distance}")
        return {
            "route_order": route_order,
            "total_distance": total_distance
        }
        
    except HTTPException as http_err:
        logging.error(f"HTTP error: {str(http_err)}")
        raise http_err
    except Exception as e:
        logging.critical(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/")
def home():
    logging.info("Home endpoint accessed.")
    return {"message": "TSP Solver API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)