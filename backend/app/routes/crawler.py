from fastapi import APIRouter, HTTPException
from app.services.crawler import CrawlerService
from typing import List

router = APIRouter()
crawler_service = CrawlerService()

@router.post("/crawl")
async def crawl_tech_events(urls: List[str]):
    """
    Endpoint to initiate crawling of tech event websites
    
    TODO:
    1. Implement URL validation for known tech event sites
    2. Add rate limiting per domain
    3. Implement proxy rotation
    4. Add crawl status tracking
    5. Implement retry mechanism
    6. Add support for authentication for protected event pages
    """
    try:
        result = await crawler_service.crawl_events(urls)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
TODO:
1. Add endpoint to manually trigger crawling for specific sites
2. Add endpoint to view crawling status
3. Add endpoint to view crawling history
4. Add endpoint to manage crawling rules
""" 