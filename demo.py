import sqlite3
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
import io
import pickle
from uuid import uuid4
from src.matrix.osrm_distance_matrix import create_distance_mat
from src.tsp.tsp_route import get_route_tsp
from src.logger import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create SQLite Database
conn = sqlite3.connect("distance_matrices.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS matrices (
    session_id TEXT PRIMARY KEY,
    distance_matrix BLOB,
    locations TEXT
)
""")
conn.commit()

@app.post("/upload_matrix")
async def upload_matrix(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")

        contents = await file.read()
        df_path = io.StringIO(contents.decode("utf-8"))

        try:
            distance_matrix, locations = create_distance_mat(df_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error generating distance matrix: {str(e)}")

        session_id = str(uuid4())

        # Store in SQLite
        cursor.execute(
            "INSERT INTO matrices (session_id, distance_matrix, locations) VALUES (?, ?, ?)",
            (session_id, pickle.dumps(distance_matrix), ",".join(locations))
        )
        conn.commit()

        return {"message": "Distance matrix uploaded successfully", "session_id": session_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/get_matrix")
async def get_matrix(session_id: str):
    cursor.execute("SELECT distance_matrix, locations FROM matrices WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="No distance matrix found for this session.")

    return {
        "distance_matrix": pickle.loads(result[0]).tolist(),
        "locations": result[1].split(",")
    }

@app.post("/solve_tsp")
async def solve_tsp(session_id: str):
    """ Solve TSP using the stored distance matrix """
    cursor.execute("SELECT distance_matrix, locations FROM matrices WHERE session_id = ?", (session_id,))
    result = cursor.fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="No distance matrix found for this session.")

    distance_matrix = pickle.loads(result[0])
    locations = result[1].split(",")

    try:
        route_order, total_distance = get_route_tsp(distance_matrix, locations)
    except Exception as e:
        logging.error(f"Error solving TSP: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error solving TSP: {str(e)}")

    return {"route_order": route_order, "total_distance": total_distance}

@app.delete("/delete_matrix")
async def delete_matrix(session_id: str):
    """ Delete stored distance matrix """
    cursor.execute("DELETE FROM matrices WHERE session_id = ?", (session_id,))
    conn.commit()

    return {"message": f"Session {session_id} deleted successfully."}

@app.get("/")
def home():
    logging.info("Home endpoint accessed.")
    return {"message": "TSP Solver API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8085)
