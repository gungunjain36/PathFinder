from fastapi import APIRouter, HTTPException
from app.services.crawler import crawl_hackathons

router = APIRouter()

@router.post("/crawl")
async def trigger_crawl():
    """Trigger hackathon discovery and crawling"""
    try:
        result = await crawl_hackathons()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
