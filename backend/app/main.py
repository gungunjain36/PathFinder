from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import crawler

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

"""
TODO:
- Add basic error handling
- Add simple request logging
"""
