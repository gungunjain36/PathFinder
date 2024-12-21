from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import crawler
import json
import os

app = FastAPI()  

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crawler.router, prefix="/api/crawler", tags=["crawler"])

@app.get("/")
async def root():
    return {
        "message": "Pathfinder API - Tech Crawler",
        "version": "0.1.0"
    }

@app.get("/results")
async def get_results():
    """Get processed results from responses.json"""
    try:
        # Path to responses.json
        results_path = os.path.join("processed_results", "responses.json")
        
        # Check if file exists
        if not os.path.exists(results_path):
            return {
                "status": "error",
                "message": "No processed results found"
            }
            
        # Read and return the results
        with open(results_path, 'r') as f:
            results = json.load(f)
            
        return {
            "status": "success",
            "data": results
        }
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error reading results: {str(e)}"
        )

