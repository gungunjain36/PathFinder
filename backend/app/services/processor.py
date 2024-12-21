"""
This processor.py file will handle the processing of crawled hackathon/tech event data. Here's a detailed breakdown:

1. Configuration & Setup:
   - Will use OpenAI API (with Galadriel endpoint) for LLM processing
   - Will define data directories for HTML storage and processed results

2. Main Functions:

   a) process_html_with_llm():
      - Will take HTML content and URL as input
      - Will use LLM to extract structured event information
      - Will return a JSON object with event details like title, description, dates, etc.
      - Will handle errors gracefully with try-except blocks

   b) format_tweet():
      - Will convert event information into Twitter-friendly format
      - Will customize emojis and hashtags based on event type
      - Will ensure tweet stays within 280 character limit
      - Will include key details like date, mode, tech stack, and prizes

   c) process_stored_files():
      - Will be main processing pipeline that handles all stored HTML files
      - Will read files from HTML directory
      - Will process each file through LLM
      - Will generate tweets for each event
      - Will save processed results to JSON
      - Will return processing statistics and sample tweets

3. Error Handling:
   - Will include comprehensive error handling throughout
   - Will provide graceful fallbacks for missing information
   - Will include detailed error logging

4. Output Format:
   - Will produce structured JSON for event information
   - Will create tweet-ready formatted text
   - Will generate processing statistics including success/failure counts

This module will be crucial for transforming raw HTML data into structured, usable event information
and preparing it for social media distribution.
"""

from fastapi import FastAPI, HTTPException
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI Client
client = OpenAI(
    base_url="https://api.galadriel.com/v1",
    api_key=os.getenv("AI_API_KEY"),
)

app = FastAPI()

# Directories for input and output
HTML_DIR = "crawled_data/html"  # Directory containing HTML files
OUTPUT_DIR = "processed_results"  # Directory to save processed results

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/process/")
async def process_html():
    responses = []

    try:
        # List all files in the HTML directory
        files = [f for f in os.listdir(HTML_DIR) if f.endswith(".html")]

        if not files:
            return {
                "message": "No HTML files found in the directory.",
                "processed_files": [],
            }

        for file_name in files:
            # try:
                # Read file content
                file_path = os.path.join(HTML_DIR, file_name)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Validate non-empty content
                if not content.strip():
                    raise ValueError(f"File '{file_name}' is empty or unreadable.")

                # Prepare the prompt for GPT
                prompt = f"""
                Extract all relevant hackathon details from the following HTML content.
                Provide the response in the following JSON format:
                {{
                    "name": "<event_name>",
                    "description": "<event_description>",
                    "prize_pool": "<prize_pool>",
                    "tech_stack": ["<tech_stack_items>"],
                    "dates": ["<start_date>", "<end_date>"],
                    "locations": ["<locations>"],
                    "mode": "<online_or_offline>",
                    "registration_link": "<registration_url>",
                    "key_deadlines": ["<deadlines>"]
                }}
                HTML Content:
                {content}
                """

                # Query the GPT API with retry mechanism
                retries = 3
                for attempt in range(retries):
                    try:
                        gpt_response = client.chat.completions.create(
                            model="llama3.1:70b",
                            messages=[
                                {"role": "system", "content": "You are an expert at extracting tech event information from web pages. Return only valid JSON."},
                                {"role": "user", "content": prompt}
                            ]
                        )

                        # Log the response to inspect it
                        print("GPT Response:", gpt_response)

                        # Parse GPT response
                        response_text = gpt_response['choices'][0]['message']['content'].strip()  # Correct access
                        try:
                            event_data = json.loads(response_text)
                        except json.JSONDecodeError:
                            event_data = {"error": "GPT response is not valid JSON", "gpt_raw": response_text}

                        # Append the result
                        responses.append({
                            "file_name": file_name,
                            "event_data": event_data,
                        })
                        break  # Break out of retry loop if successful
                    except Exception as e:
                        if attempt < retries - 1:
                            print(f"Attempt {attempt + 1} failed, retrying...")
                            time.sleep(2)  # wait before retry
                        else:
                            responses.append({
                                "file_name": file_name,
                                "error": f"Failed to process file: {str(e)}",
                            })

        # Save responses to a JSON file
        output_file = os.path.join(OUTPUT_DIR, "responses.json")
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(responses, json_file, indent=4)

        return {
            "message": "Processing completed",
            "responses_saved_in": output_file,
            "sample_responses": responses[:3],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")


