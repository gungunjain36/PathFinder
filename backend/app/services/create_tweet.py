from requests_oauthlib import OAuth1Session # type: ignore
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Load Twitter API keys from environment variables
consumer_key = os.getenv("x_API_KEY")
consumer_secret = os.getenv("X_API_KEY_SECRET")

# Function to read events data from the JSON file
def read_events_from_json():
    with open("../../processed_results/responses.json", "r") as f:
        return json.load(f)

# Format event data into a tweet-friendly format
def format_event_for_tweet(event):
    title = event.get("title", "No Title")
    description = event.get("description", "No Description")
    date = event.get("date", "Date unknown")
    registration = event.get("registration", "Registration unknown")
    prizes = event.get("prizes", "Prizes unknown")
    tech_stack = ", ".join(event.get("tech_stack", [])) if event.get("tech_stack") else "No specific tech stack"
    event_url = event.get("url", "No URL")

    tweet = f"🎉 Event: {title}\n" \
            f"📝 Description: {description[:50]}...\n" \
            f"📅 Date: {date}\n" \
            f"💰 Prizes: {prizes}\n" \
            f"🛠️ Tech Stack: {tech_stack}\n" \
            f"🌐 URL: {event_url}"

    # Ensure the tweet is within Twitter's character limit (280 characters)
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."

    return tweet

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print("There may have been an issue with the consumer_key or consumer_secret you entered.")

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization URL
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request with access token
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Read events from JSON
events = read_events_from_json()

# Loop through the events and post tweets for active events
for event in events:
    if event["is_active"]:  # Only post active events
        tweet_text = format_event_for_tweet(event)
        
        # Make the request to post the tweet
        payload = {"status": tweet_text}
        response = oauth.post(
            "https://api.twitter.com/1.1/statuses/update.json",
            params=payload
        )

        if response.status_code != 200:
            print(f"Error posting tweet: {response.status_code}, {response.text}")
        else:
            print(f"Successfully posted tweet: {tweet_text}")
            json_response = response.json()
            print(json.dumps(json_response, indent=4, sort_keys=True))
