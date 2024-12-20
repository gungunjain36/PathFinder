from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import crawler, events

app = FastAPI(title="Pathfinder API")

# Basic CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/api/events", tags=["events"])

@app.get("/")
async def root():
    return {
        "message": "Pathfinder API - Tech Crawler",
        "version": "0.1.0"
    }

"""
TODO:
- Add basic error handling
- Add simple request logging
"""
