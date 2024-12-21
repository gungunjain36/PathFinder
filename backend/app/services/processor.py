from fastapi import FastAPI, HTTPException
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import time
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(
    base_url="https://api.galadriel.com/v1",
    api_key=os.getenv("AI_API_KEY"),
)

# Directories setup
HTML_DIR = "crawled_data/html"
OUTPUT_DIR = "processed_results"
CHUNK_SIZE = 4000

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_html(html_content: str) -> str:
    """Clean and extract relevant content from HTML"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']):
            element.decompose()
        
        # Extract text from remaining elements
        text = soup.get_text(separator='\n', strip=True)
        
        # Basic text cleaning
        text = re.sub(r'\n+', '\n', text)  # Remove multiple newlines
        text = re.sub(r'\s+', ' ', text)   # Normalize whitespace
        
        return text
        
    except Exception as e:
        print(f"Error cleaning HTML: {str(e)}")
        return html_content

async def analyze_chunk(chunk: str) -> Dict:
    """Initial analysis of chunk content"""
    try:
        prompt = f"""
        Analyze this text chunk and tell me if it contains any tech event information.
        Return ONLY a JSON object with these exact fields:
        {{
            "has_event": true/false,
            "event_type": "hackathon/conference/meetup/unknown",
            "relevance_score": 0-10,
            "key_points": ["point1", "point2"]
        }}

        Text:
        {chunk}
        """

        completion = client.chat.completions.create(
            model="llama3.1:70b",
            messages=[
                {"role": "system", "content": "You are a JSON generator that analyzes text for tech events. Always return valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        # Get the response content
        response_text = completion.choices[0].message.content.strip()
        
        # Try to find JSON in the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                print(f"Invalid JSON in response: {json_str}")
                return {"has_event": False, "relevance_score": 0}
        else:
            print("No JSON found in response")
            return {"has_event": False, "relevance_score": 0}

    except Exception as e:
        print(f"Error analyzing chunk: {str(e)}")
        return {"has_event": False, "relevance_score": 0}

async def extract_event_details(relevant_chunks: List[str], url: str) -> List[Dict]:
    """Extract detailed event information from relevant chunks"""
    try:
        combined_text = "\n\n===CHUNK SEPARATOR===\n\n".join(relevant_chunks)
        
        prompt = f"""
        Extract tech event information from these text chunks.
        Return ONLY a JSON array where each event has this exact structure:
        [
            {{
                "title": "event title",
                "description": "brief description",
                "date": {{
                    "start": "start date or unknown",
                    "end": "end date or unknown"
                }},
                "registration": {{
                    "status": "open/closed/unknown",
                    "url": "url or unknown"
                }},
                "prizes": {{
                    "total_pool": "amount or unknown",
                    "details": "details or unknown"
                }},
                "event_type": "hackathon/conference/meetup",
                "mode": "online/offline/hybrid/unknown",
                "tech_stack": ["tech1", "tech2"],
                "eligibility": "eligibility or unknown",
                "organizer": "organizer name or unknown"
            }}
        ]

        Text:
        {combined_text}
        """

        completion = client.chat.completions.create(
            model="llama3.1:70b",
            messages=[
                {"role": "system", "content": "You are a JSON generator that extracts event information. Always return a valid JSON array."},
                {"role": "user", "content": prompt}
            ]
        )

        # Get the response content
        response_text = completion.choices[0].message.content.strip()
        
        # Try to find JSON array in the response
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            try:
                events = json.loads(json_str)
                if isinstance(events, dict):
                    events = [events]
                
                # Add metadata
                for event in events:
                    event['source_url'] = url
                    event['processed_at'] = datetime.now().isoformat()
                
                return events
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in response: {str(e)}")
                return []
        else:
            print("No JSON array found in response")
            return []

    except Exception as e:
        print(f"Error extracting event details: {str(e)}")
        return []

async def process_html_file(file_path: str) -> List[Dict]:
    """Process a single HTML file with smart chunking"""
    try:
        print(f"\nProcessing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract URL from content
        url = content.split('\n')[0].replace('Source URL: ', '').strip()
        print(f"URL: {url}")
        
        # Clean content
        cleaned_text = clean_html(content)
        print(f"Content length: {len(cleaned_text)} characters")
        
        # Only chunk if content is large
        if len(cleaned_text) > CHUNK_SIZE:
            print("Content is large, chunking...")
            # Split into paragraphs
            chunks = [chunk.strip() for chunk in cleaned_text.split('\n\n') if chunk.strip()]
            print(f"Split into {len(chunks)} chunks")
            
            # Analyze each chunk
            relevant_chunks = []
            for i, chunk in enumerate(chunks, 1):
                print(f"Analyzing chunk {i}/{len(chunks)}...")
                analysis = await analyze_chunk(chunk)
                print(f"Chunk {i} analysis: {analysis}")
                if analysis.get('has_event', False) and analysis.get('relevance_score', 0) > 5:
                    relevant_chunks.append(chunk)
            
            print(f"Found {len(relevant_chunks)} relevant chunks")
            if relevant_chunks:
                events = await extract_event_details(relevant_chunks, url)
                print(f"Extracted {len(events)} events")
                return events
        else:
            print("Processing content directly...")
            events = await extract_event_details([cleaned_text], url)
            print(f"Extracted {len(events)} events")
            return events
            
        return []
        
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return []

def deduplicate_events(events: List[Dict]) -> List[Dict]:
    """Remove duplicate events with smart matching"""
    unique_events = []
    seen = set()
    
    for event in events:
        # Create a unique key using multiple fields
        key_parts = [
            event['title'].lower() if event.get('title') else '',
            event.get('date', {}).get('start', ''),
            event.get('organizer', '').lower(),
            event.get('event_type', '').lower()
        ]
        key = '_'.join(key_parts)
        
        if key not in seen:
            seen.add(key)
            unique_events.append(event)
    
    return unique_events

async def smart_deduplicate_with_llm(events: List[Dict]) -> List[Dict]:
    """Use LLM to identify and merge duplicate events intelligently"""
    try:
        # Convert events to string representation
        events_str = json.dumps(events, indent=2)
        
        prompt = f"""
        Analyze this list of tech events and:
        1. Identify duplicate events (same event with slightly different details)
        2. Merge duplicate events keeping the most complete information
        3. Return only unique events
        4. Ensure all dates and details are consistent
        
        For events to be considered duplicates, they should have:
        - Similar titles
        - Same or overlapping dates
        - Same organizer or similar tech stack
        
        Return ONLY a JSON array of unique events, merging information from duplicates.
        Keep the most detailed version when merging.

        Events to analyze:
        {events_str}
        """

        completion = client.chat.completions.create(
            model="llama3.1:70b",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert at identifying and merging duplicate event information. Always return valid JSON array."
                },
                {"role": "user", "content": prompt}
            ]
        )

        # Get the response content
        response_text = completion.choices[0].message.content.strip()
        
        # Try to find JSON array in the response
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        
        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            try:
                deduped_events = json.loads(json_str)
                print(f"Reduced from {len(events)} to {len(deduped_events)} unique events")
                return deduped_events
            except json.JSONDecodeError as e:
                print(f"Error parsing LLM deduplication response: {str(e)}")
                return events
        else:
            print("No valid JSON array found in deduplication response")
            return events

    except Exception as e:
        print(f"Error in smart deduplication: {str(e)}")
        return events

async def process_all_files() -> Dict:
    """Process all HTML files with enhanced error handling and smart deduplication"""
    try:
        all_events = []
        processed_files = 0
        failed_files = 0
        processing_stats = {
            "total_chunks_analyzed": 0,
            "relevant_chunks_found": 0,
            "events_extracted": 0
        }
        
        html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
        
        for file_name in html_files:
            try:
                print(f"Processing {file_name}...")
                file_path = os.path.join(HTML_DIR, file_name)
                events = await process_html_file(file_path)
                
                if events:
                    all_events.extend(events)
                    processed_files += 1
                    print(f"Found {len(events)} events in {file_name}")
                else:
                    failed_files += 1
                    print(f"No events found in {file_name}")
                    
            except Exception as e:
                print(f"Error processing {file_name}: {str(e)}")
                failed_files += 1
        
        # First do basic deduplication
        unique_events = deduplicate_events(all_events)
        
        # Then do smart LLM-based deduplication
        print("\nPerforming smart deduplication...")
        final_events = await smart_deduplicate_with_llm(unique_events)
        
        # Save results
        output_file = os.path.join(OUTPUT_DIR, "responses.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_events, f, indent=2)
        
        return {
            "status": "success",
            "total_files": len(html_files),
            "processed_files": processed_files,
            "failed_files": failed_files,
            "events_found": len(final_events),
            "events_by_type": {
                event_type: len([e for e in final_events if e.get('event_type', '').lower() == event_type])
                for event_type in ['hackathon', 'conference', 'meetup']
            },
            "deduplication_stats": {
                "initial_events": len(all_events),
                "after_basic_dedup": len(unique_events),
                "final_unique_events": len(final_events)
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        } 