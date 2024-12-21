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
        self.consumer_key = os.getenv("x_API_KEY")
        self.consumer_secret = os.getenv("X_API_KEY_SECRET")
        self.oauth = None
        self.setup_oauth()

    def setup_oauth(self):
        """Setup OAuth 1.0a authentication"""
        try:
            # Get request token
            request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
            oauth = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)

            try:
                fetch_response = oauth.fetch_request_token(request_token_url)
            except ValueError:
                print("There may have been an issue with the consumer_key or consumer_secret.")
                return

            resource_owner_key = fetch_response.get("oauth_token")
            resource_owner_secret = fetch_response.get("oauth_token_secret")
            print("Got OAuth token:", resource_owner_key)

            # Get authorization
            base_authorization_url = "https://api.twitter.com/oauth/authorize"
            authorization_url = oauth.authorization_url(base_authorization_url)
            print("\nPlease go here and authorize:", authorization_url)
            verifier = input("Paste the PIN here: ")

            # Get the access token
            access_token_url = "https://api.twitter.com/oauth/access_token"
            oauth = OAuth1Session(
                self.consumer_key,
                client_secret=self.consumer_secret,
                resource_owner_key=resource_owner_key,
                resource_owner_secret=resource_owner_secret,
                verifier=verifier,
            )
            oauth_tokens = oauth.fetch_access_token(access_token_url)

            access_token = oauth_tokens["oauth_token"]
            access_token_secret = oauth_tokens["oauth_token_secret"]

            # Create the final OAuth session
            self.oauth = OAuth1Session(
                self.consumer_key,
                client_secret=self.consumer_secret,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_secret,
            )
            print("OAuth setup completed successfully!")

        except Exception as e:
            print(f"Error setting up OAuth: {str(e)}")
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
            # Truncate while keeping URL intact
            url_index = tweet.rfind("More info:")
            if url_index > 0:
                url_part = tweet[url_index:]
                main_part = tweet[:url_index]
                tweet = main_part[:280-len(url_part)-3] + "..." + url_part

        return tweet

    def post_tweet(self, tweet_text: str) -> Dict:
        """Post a tweet using X API v2"""
        try:
            if not self.oauth:
                return {"status": "error", "message": "OAuth not set up"}

            payload = {"text": tweet_text}
            response = self.oauth.post(
                "https://api.twitter.com/2/tweets",
                json=payload,
            )

            if response.status_code != 201:
                print(f"Error posting tweet: {response.status_code}")
                print(response.text)
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

if __name__ == "__main__":
    bot = XBot()
    results = bot.post_events(max_events=3)
    print(json.dumps(results, indent=2))
