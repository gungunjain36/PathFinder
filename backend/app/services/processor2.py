import os
import json
from typing import List, Dict
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    base_url="https://api.galadriel.com/v1",
    api_key=os.getenv("AI_API_KEY"),
)

# Define directories
DATA_DIR = "crawled_data"
RESPONSE_DIR = "processed_results"
HTML_DIR = os.path.join(DATA_DIR, "html")
PROCESSED_FILE = os.path.join(RESPONSE_DIR, "responses.json")

async def process_html_with_llm() -> Dict:
    """Process all HTML files and store results in JSON."""
    try:
        os.makedirs(RESPONSE_DIR, exist_ok=True)  # Ensure the output directory exists
        processed_events = []

        # Get all HTML files
        html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
        print(f"Found {len(html_files)} HTML files to process")

        for filename in html_files:
            filepath = os.path.join(HTML_DIR, filename)

            # Read HTML content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract URL from the first line
            url = content.split('\n')[0].replace('Source URL: ', '').strip()

            # Define the prompt for LLM
            prompt = f"""
            Extract hackathon/tech event information from this HTML content.
            Focus on finding these key details:
            1. Event title
            2. Brief description
            3. Event date/deadline
            4. Registration/application info
            5. Prize information (if available)
            6. Event type (hackathon/conference/meetup)
            7. Mode (online/offline/hybrid)
            8. Technologies/themes involved

            Return ONLY a valid JSON object with these fields (use "unknown" if info not found). Do not include any additional text or comments. Return only the JSON object:
            {{
                "title": "",
                "description": "",
                "date": "",
                "registration": "",
                "prizes": "",
                "event_type": "",
                "mode": "",
                "tech_stack": [],
                "is_active": false
            }}

            HTML Content:
            {content[:4000]}
            """

            try:
                # Process with LLM
                completion = client.chat.completions.create(
                    model="llama3.1:70b",
                    messages=[
                        {"role": "system", "content": "You are an expert at extracting tech event information from web pages. Return only valid JSON."},
                        {"role": "user", "content": prompt}
                    ]
                )

                raw_response = completion.choices[0].message.content
                print(f"Raw API response for {filename}: {raw_response}")

                # Filter and parse JSON response
                try:
                    # Remove any text before or after the JSON object
                    json_start = raw_response.find('{')
                    json_end = raw_response.rfind('}') + 1
                    json_content = raw_response[json_start:json_end]

                    # Parse JSON
                    event_info = json.loads(json_content)
                    event_info['url'] = url
                    event_info['processed_at'] = datetime.now().isoformat()
                    processed_events.append(event_info)

                except (json.JSONDecodeError, ValueError) as parse_error:
                    print(f"Error parsing JSON from {filename}: {parse_error}")
                    continue

            except Exception as api_error:
                print(f"API error for {filename}: {api_error}")
                continue

        # Save results to JSON
        with open(PROCESSED_FILE, 'w', encoding='utf-8') as outfile:
            json.dump(processed_events, outfile, indent=4)

        print(f"Processed {len(processed_events)} events. Results saved to {PROCESSED_FILE}.")
        return {"processed_events": processed_events}

    except Exception as e:
        print(f"Error processing HTML files: {str(e)}")
        return {"error": str(e)}
