import scrapy
from scrapy.crawler import CrawlerRunner
from typing import List, Dict
import json
import os
from scrapy.utils.log import configure_logging
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
import re

class TechEventSpider(scrapy.Spider):
    name = 'tech_events'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (compatible; PathfinderBot/1.0)',
        'ROBOTSTXT_OBEY': True,
        'LOG_LEVEL': 'ERROR',
        'COOKIES_ENABLED': False,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_TIMEOUT': 15,
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.results = []
        self.start_urls = kwargs.get('start_urls', [])
        self.event_type = kwargs.get('event_type', 'event')
        print(f"Initializing spider for {self.event_type} with {len(self.start_urls)} URLs")

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                errback=self.handle_error,
                dont_filter=True
            )

    def handle_error(self, failure):
        print(f"Request failed: {failure.request.url}")

    def extract_date(self, text):
        """Extract date from text using common patterns"""
        date_patterns = [
            r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()
        return None

    def clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return None
        text = ' '.join(text.split())
        return text.strip()

    def parse(self, response):
        """Enhanced event parsing"""
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try multiple selectors for title
            title = (
                self.clean_text(response.css('h1::text').get()) or
                self.clean_text(response.css('.event-title::text').get()) or
                self.clean_text(soup.find('title').get_text()) if soup.find('title') else None
            )

            # Try multiple selectors for description
            description = (
                self.clean_text(response.css('.event-description::text').get()) or
                self.clean_text(response.css('.description::text').get()) or
                self.clean_text(response.css('p::text').get())
            )

            # Look for dates
            text_content = ' '.join(response.css('*::text').getall())
            date = self.extract_date(text_content)

            if title:
                event = {
                    'title': title,
                    'description': description or 'No description available',
                    'url': response.url,
                    'type': self.event_type,
                    'date_found': date,
                    'crawled_at': datetime.now().isoformat()
                }
                print(f"Found event: {event['title']}")
                self.results.append(event)

        except Exception as e:
            print(f"Error parsing {response.url}: {str(e)}")

class CrawlerService:
    def __init__(self):
        configure_logging()
        self.runner = CrawlerRunner()
        self.data_file = 'events.json'
        self.crawl_results = []

    def save_events(self, events: List[Dict]):
        """Save events with timestamp"""
        try:
            existing = self.load_events()
            # Add new events, avoid duplicates by URL
            existing_urls = {e['url'] for e in existing}
            new_events = [e for e in events if e['url'] not in existing_urls]
            
            if new_events:
                all_events = existing + new_events
                with open(self.data_file, 'w') as f:
                    json.dump(all_events, f, indent=2)
                print(f"Saved {len(new_events)} new events")
            else:
                print("No new events to save")
                
        except Exception as e:
            print(f"Storage error: {str(e)}")

    def load_events(self) -> List[Dict]:
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading events: {str(e)}")
        return []

    def format_for_twitter(self, event: Dict) -> str:
        """Format event for X.com with better formatting"""
        date_str = f" on {event['date_found']}" if event.get('date_found') else ""
        
        if event['type'] == 'hackathon':
            return (
                f"🚀 Hackathon Alert!\n\n"
                f"{event['title']}{date_str}\n\n"
                f"{event['description'][:100]}...\n\n"
                f"Join now: {event['url']}\n"
                f"#hackathon #tech #coding"
            )
        elif event['type'] == 'meetup':
            return (
                f"👥 Tech Meetup\n\n"
                f"{event['title']}{date_str}\n\n"
                f"{event['description'][:100]}...\n\n"
                f"Join us: {event['url']}\n"
                f"#meetup #tech #community"
            )
        else:
            return (
                f"📅 Tech Event\n\n"
                f"{event['title']}{date_str}\n\n"
                f"{event['description'][:100]}...\n\n"
                f"Learn more: {event['url']}\n"
                f"#tech #event"
            )

    async def run_spider(self, spider_cls, **kwargs):
        """Run spider with better error handling"""
        def _crawl():
            return self.runner.crawl(spider_cls, **kwargs)

        try:
            deferred = await asyncio.get_event_loop().run_in_executor(None, _crawl)
            
            # Wait for the crawler to finish with timeout
            timeout = 60  # 60 seconds timeout
            start_time = asyncio.get_event_loop().time()
            
            while not deferred.called:
                if asyncio.get_event_loop().time() - start_time > timeout:
                    print("Crawler timeout reached")
                    break
                await asyncio.sleep(1)
            
            if deferred.called:
                spider = deferred.result.spider
                return spider.results
            return []
            
        except Exception as e:
            print(f"Error running spider: {str(e)}")
            return []

    async def crawl_events(self, urls: List[str] = None) -> Dict:
        """Enhanced crawling function"""
        try:
            print("Starting crawl_events function")
            self.crawl_results = []
            
            event_types = {
                'hackathon': ["tech hackathons 2024", "upcoming hackathons"],
                'meetup': ["tech meetups near me", "developer meetups"]
            }

            if not urls:
                print("No URLs provided, crawling for each type separately")
                for event_type, queries in event_types.items():
                    urls = []
                    for query in queries:
                        print(f"Searching for query: {query}")
                        from googlesearch import search
                        try:
                            urls.extend(list(search(query, num_results=5)))
                        except Exception as e:
                            print(f"Search error for {query}: {str(e)}")
                    
                    if urls:
                        print(f"Starting spider for {len(urls)} URLs")
                        results = await self.run_spider(TechEventSpider, start_urls=urls, event_type=event_type)
                        if results:
                            self.crawl_results.extend(results)
            else:
                results = await self.run_spider(TechEventSpider, start_urls=urls, event_type='event')
                if results:
                    self.crawl_results.extend(results)

            if self.crawl_results:
                self.save_events(self.crawl_results)
                
            # Generate sample X.com posts
            sample_posts = [
                self.format_for_twitter(event) 
                for event in self.crawl_results[:3]  # Sample first 3 events
            ]

            result = {
                "status": "success",
                "events_found": len(self.crawl_results),
                "types": {
                    'hackathons': len([e for e in self.crawl_results if e['type'] == 'hackathon']),
                    'meetups': len([e for e in self.crawl_results if e['type'] == 'meetup']),
                    'events': len([e for e in self.crawl_results if e['type'] == 'event'])
                },
                "sample_posts": sample_posts
            }
            print(f"Final result: {result}")
            return result
        except Exception as e:
            print(f"Error in crawl_events: {str(e)}")
            return {"status": "error", "message": str(e)}