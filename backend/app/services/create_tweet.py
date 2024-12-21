from requests_oauthlib import OAuth1Session
import os
import json
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv
import time

load_dotenv()

class XBot:
    def __init__(self):
        # Get credentials from environment variables
        self.api_key = os.getenv("x_API_KEY")
        self.api_secret = os.getenv("X_API_KEY_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        
        # Validate credentials
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Missing required X API credentials in .env file")
        
        print("Initializing with credentials:")
        print(f"API Key: {self.api_key[:8]}...")
        print(f"Access Token: {self.access_token[:8]}...")
        
        # Create OAuth1Session with stored credentials
        self.oauth = OAuth1Session(
            client_key=self.api_key,
            client_secret=self.api_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret
        )
        
        # Verify credentials
        self.verify_credentials()

    def verify_credentials(self):
        """Verify the credentials are working"""
        try:
            print("\nVerifying credentials...")
            print(f"Using API Key: {self.api_key[:8]}...")
            print(f"Using API Secret: {self.api_secret[:8]}...")
            print(f"Using Access Token: {self.access_token[:8]}...")
            print(f"Using Access Token Secret: {self.access_token_secret[:8]}...")
            
            # Test endpoint
            response = self.oauth.get(
                "https://api.twitter.com/2/users/me",
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\nResponse Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"\nSuccessfully authenticated as: {user_data.get('data', {}).get('username')}")
            else:
                print("\nAuthentication failed!")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                raise ValueError("Failed to verify credentials")
                
        except Exception as e:
            print(f"\nError verifying credentials: {str(e)}")
            raise

    def format_event_tweet(self, event: Dict) -> str:
        """Format event data into an engaging tweet"""
        # Get event details with fallbacks
        title = event.get('title', 'Upcoming Tech Event')
        date_info = event.get('date', {})
        start_date = date_info.get('start', 'TBA')
        end_date = date_info.get('end', '')
        
        prize_info = event.get('prizes', {})
        prize_pool = prize_info.get('total_pool', '')
        
        tech_stack = event.get('tech_stack', [])
        tech_tags = ' '.join([f"#{tech.replace(' ', '')}" for tech in tech_stack[:3]])
        
        event_type = event.get('event_type', '').lower()
        mode = event.get('mode', '').lower()
        
        # Emoji mapping
        type_emoji = {
            'hackathon': '🚀',
            'conference': '🎯',
            'meetup': '👥',
            'expo': '🎪',
            'workshop': '💡'
        }.get(event_type, '📅')

        # Construct tweet
        tweet = f"{type_emoji} {title}\n\n"
        
        # Add date
        if start_date and end_date and start_date != end_date:
            tweet += f"📅 {start_date} - {end_date}\n"
        else:
            tweet += f"📅 {start_date}\n"
            
        # Add mode if available
        if mode and mode != 'unknown':
            tweet += f"📍 {mode.title()}\n"
            
        # Add prize if available
        if prize_pool and prize_pool.lower() != 'unknown':
            tweet += f"🏆 Prize Pool: {prize_pool}\n"
            
        # Add tech stack tags
        if tech_tags:
            tweet += f"\n{tech_tags}"
            
        # Add general hashtags
        tweet += f" #{event_type} #tech"
        
        # Add source URL
        if event.get('source_url'):
            tweet += f"\n\nMore info: {event['source_url']}"
            
        # Ensure tweet is within character limit
        if len(tweet) > 280:
            url_index = tweet.rfind("More info:")
            if url_index > 0:
                url_part = tweet[url_index:]
                main_part = tweet[:url_index]
                tweet = main_part[:280-len(url_part)-3] + "..." + url_part

        return tweet

    def post_tweet(self, tweet_text: str) -> Dict:
        """Post a tweet using X API v2 with OAuth 1.0a"""
        try:
            # Endpoint for v2 tweets
            url = "https://api.twitter.com/2/tweets"
            
            # Prepare payload
            payload = {"text": tweet_text}

            # Add required headers
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # Make request
            response = self.oauth.post(
                url,
                json=payload,
                headers=headers
            )

            if response.status_code != 201:
                print(f"Error posting tweet: {response.status_code}")
                print(f"Response: {response.text}")
                print(f"Request payload: {payload}")
                return {"status": "error", "message": response.text}

            print(f"Tweet posted successfully!")
            return {"status": "success", "data": response.json()}

        except Exception as e:
            print(f"Error posting tweet: {str(e)}")
            return {"status": "error", "message": str(e)}

    def post_events(self, max_events: int = 5) -> List[Dict]:
        """Post multiple events as tweets"""
        results = []
        try:
            # Read events from JSON
            with open("processed_results/responses.json", "r") as f:
                events = json.load(f)

            # Sort events by date
            events.sort(key=lambda x: x.get('date', {}).get('start', ''), reverse=True)

            # Post tweets for recent events
            for event in events[:max_events]:
                tweet_text = self.format_event_tweet(event)
                result = self.post_tweet(tweet_text)
                results.append({
                    "event": event['title'],
                    "tweet": tweet_text,
                    "result": result
                })
                
                if result["status"] == "error":
                    print(f"Error posting tweet for {event['title']}")
                    continue

                # Rate limiting
                if len(results) < max_events:
                    time.sleep(2)

            return results

        except Exception as e:
            print(f"Error posting events: {str(e)}")
            return results

    def test_auth(self):
        """Test authentication with a simple tweet"""
        try:
            print("\nTesting authentication with a test tweet...")
            
            # Simple test tweet
            test_tweet = "Test tweet from Pathfinder Bot 🤖 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Endpoint for v2 tweets
            url = "https://api.twitter.com/2/tweets"
            
            # Prepare payload and headers
            payload = {"text": test_tweet}
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # Make request
            response = self.oauth.post(
                url,
                json=payload,
                headers=headers
            )

            print(f"\nResponse Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")

            return response.status_code == 201

        except Exception as e:
            print(f"\nError testing auth: {str(e)}")
            return False

if __name__ == "__main__":
    try:
        bot = XBot()
        if bot.test_auth():
            print("\nAuthentication test successful! Proceeding with event tweets...")
            results = bot.post_events(max_events=1)  # Try one tweet first
            print(json.dumps(results, indent=2))
        else:
            print("\nAuthentication test failed!")
    except Exception as e:
        print(f"\nError: {str(e)}")
