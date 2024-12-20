from fastapi import APIRouter, HTTPException
from app.services.crawler import crawl_hackathons
from app.services.processor import process_stored_files

router = APIRouter()

@router.post("/crawl")
async def trigger_crawl():
    """Trigger hackathon discovery and crawling"""
    try:
        result = await crawl_hackathons()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a /process endpoint that processes the HTML files that were previously crawled and stored.
# It uses an LLM (Language Learning Model) to extract structured information about
# hackathons and tech events from the raw HTML content. The processing is done
# asynchronously and returns the results. If any errors occur during processing,
# it will raise an HTTP 500 error with the error details.
