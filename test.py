# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import data, upload, vehicles, shops, tsp
from config import API_HOST, API_PORT

app = FastAPI()

# Allow frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(upload.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")
app.include_router(shops.router, prefix="/api")
app.include_router(tsp.router, prefix="/api")
app.include_router(data.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "TSP Solver API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)