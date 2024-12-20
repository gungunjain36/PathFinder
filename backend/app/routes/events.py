from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.crawler import CrawlerService
from datetime import datetime

router = APIRouter()
crawler_service = CrawlerService()

@router.get("/")
async def get_events(
    event_type: Optional[str] = Query(None, enum=['hackathon', 'meetup', 'event']),
    limit: int = Query(10, ge=1, le=100)
):
    """Get stored events with optional filtering"""
    try:
        events = crawler_service.load_events()
        
        if event_type:
            events = [e for e in events if e['type'] == event_type]
            
        # Sort by crawled_at date if available
        events.sort(
            key=lambda x: x.get('crawled_at', ''), 
            reverse=True
        )
        
        return {
            "total": len(events),
            "events": events[:limit],
            "sample_post": crawler_service.format_for_twitter(events[0]) if events else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/crawl")
async def trigger_crawl(urls: Optional[List[str]] = None):
    """Trigger crawling with enhanced feedback"""
    try:
        print(f"Starting crawl for URLs: {urls if urls else 'automatic search'}")
        result = await crawler_service.crawl_events(urls)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_stats():
    """Get crawling statistics"""
    events = crawler_service.load_events()
    return {
        "total_events": len(events),
        "by_type": {
            "hackathons": len([e for e in events if e['type'] == 'hackathon']),
            "meetups": len([e for e in events if e['type'] == 'meetup']),
            "events": len([e for e in events if e['type'] == 'event'])
        },
        "latest_crawl": max([e.get('crawled_at', '') for e in events]) if events else None
    }

"""
TODO:
1. Add endpoint for calendar integration
2. Add endpoint for event recommendations
3. Add endpoint for user event preferences
4. Add endpoint for event notifications
5. Add endpoint for X.com posting
""" 