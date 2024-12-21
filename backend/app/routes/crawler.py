from fastapi import APIRouter, HTTPException
from app.services.crawler import crawl_hackathons
from app.services.processor import process_all_files
from typing import Dict
from app.services.create_tweet import XBot

router = APIRouter()

@router.post("/crawl")
async def trigger_crawl():
    """Trigger hackathon discovery and crawling"""
    try:
        print("Starting crawl process...")
        result = await crawl_hackathons()
        return {
            "status": "success",
            "message": "Crawling completed",
            "details": result
        }
    except Exception as e:
        print(f"Error in crawl: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def trigger_process():
    """
    Process stored HTML files with LLM
    
    This endpoint:
    1. Reads all HTML files from crawled_data/html
    2. Cleans and chunks the HTML content
    3. Processes each chunk with LLM to extract event information
    4. Deduplicates and combines results
    5. Saves processed results to responses.json
    """
    try:
        print("Starting LLM processing...")
        result = await process_all_files()
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
            
        return {
            "status": "success",
            "message": "Processing completed",
            "details": result
        }
    except Exception as e:
        print(f"Error in processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_processing_status() -> Dict:
    """Get current processing statistics"""
    try:
        import os
        from app.services.processor import HTML_DIR, OUTPUT_DIR
        
        # Count HTML files
        html_files = len([f for f in os.listdir(HTML_DIR) if f.endswith('.html')]) if os.path.exists(HTML_DIR) else 0
        
        # Check processed results
        results_file = os.path.join(OUTPUT_DIR, "responses.json")
        processed_events = []
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                import json
                processed_events = json.load(f)
        
        return {
            "crawled_files": html_files,
            "processed_events": len(processed_events),
            "event_types": {
                event_type: len([e for e in processed_events if e.get('event_type', '').lower() == event_type])
                for event_type in ['hackathon', 'conference', 'meetup']
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

@router.post("/tweet")
async def post_tweets(max_events: int = 5):
    """Post events to X.com"""
    try:
        bot = XBot()
        results = bot.post_events(max_events=max_events)
        return {
            "status": "success",
            "tweets_posted": len(results),
            "details": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))