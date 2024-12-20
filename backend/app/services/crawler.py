# Import required libraries
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML content
from typing import List, Dict  # For type hints
import json  # For reading/writing JSON files
import os  # For file/directory operations
from datetime import datetime  # For timestamp handling
from googlesearch import search  # For Google search functionality
import asyncio  # For asynchronous operations
import aiohttp  # For async HTTP requests
import re  # For regular expressions
from playwright.async_api import async_playwright
from urllib.parse import urlparse

# Define browser headers to mimic real browser requests and avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Create a function to handle directory setup
def setup_directories():
    """Create necessary directories for storing crawled data"""
    try:
        # Get absolute paths
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        data_dir = os.path.join(base_dir, 'crawled_data')
        html_dir = os.path.join(data_dir, 'html')
        
        # Create directories
        for directory in [data_dir, html_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
        
        return {
            'base_dir': base_dir,
            'data_dir': data_dir,
            'html_dir': html_dir,
            'index_file': os.path.join(data_dir, 'index.json')
        }
    except Exception as e:
        print(f"Error setting up directories: {str(e)}")
        raise

# Set up directories and get paths
try:
    PATHS = setup_directories()
except Exception as e:
    print(f"Fatal error setting up directories: {str(e)}")
    raise

async def save_html_content(content: str, url: str) -> str:
    """
    Save HTML content to file with proper error handling
    
    Args:
        content: HTML content to save
        url: Source URL for generating filename
        
    Returns:
        Path to saved file or None if failed
    """
    try:
        # Create a safe filename from URL
        safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', url.split('//')[-1])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"hackathon_{timestamp}_{safe_filename[:50]}.html"
        
        # Ensure full path is valid
        file_path = os.path.join(PATHS['html_dir'], filename)
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"Source URL: {url}\n\n")
            f.write(content)
            
        print(f"Successfully saved HTML for {url}")
        return file_path
    except Exception as e:
        print(f"Error saving HTML for {url}: {str(e)}")
        return None

async def fetch_page_with_js(url: str, context: str) -> Dict:
    """Fetch page using Playwright to handle JavaScript-rendered content"""
    try:
        print(f"Fetching with JS: {url}")
        
        async with async_playwright() as p:
            # Launch browser in headless mode
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Set timeout and go to URL
            page.set_default_timeout(30000)
            await page.goto(url, wait_until='networkidle')
            
            # Wait for content to load
            await asyncio.sleep(2)  # Additional wait for dynamic content
            
            # Get the rendered HTML
            content = await page.content()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for hackathon terms
            text_content = soup.get_text().lower()
            hackathon_terms = ['hackathon', 'register', 'registration', 'prize', 
                             'deadline', 'submit', 'participate', 'team']
            
            if not any(term in text_content for term in hackathon_terms):
                print(f"No hackathon terms found in {url}")
                await browser.close()
                return None
            
            # Clean HTML content
            for tag in soup.find_all(['script', 'style']):
                tag.decompose()
            
            # Try to get main content
            main_content = (
                soup.find('main') or 
                soup.find('article') or 
                soup.find('div', {'class': ['content', 'main-content']}) or 
                soup.find('body')
            )
            
            if not main_content:
                print(f"No main content found in {url}")
                await browser.close()
                return None
            
            # Save HTML content
            file_path = await save_html_content(str(main_content), url)
            if not file_path:
                await browser.close()
                return None
            
            # Extract dates
            date_patterns = [
                r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
                r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
                r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'
            ]
            
            dates_found = []
            for pattern in date_patterns:
                dates_found.extend(re.findall(pattern, text_content))
            
            await browser.close()
            
            return {
                'url': url,
                'context': context,
                'file_path': file_path,
                'dates_found': dates_found,
                'crawled_at': datetime.now().isoformat(),
                'title': soup.title.string if soup.title else url,
                'js_rendered': True
            }
            
    except Exception as e:
        print(f"Error processing {url} with JS: {str(e)}")
        return None

def is_js_heavy_site(url: str) -> bool:
    """Check if site likely requires JavaScript"""
    domain = urlparse(url).netloc.lower()
    js_heavy_sites = [
        'unstop.com',
        'devfolio.co',
        'hackerearth.com',
        'devpost.com',
        'linkedin.com',
        'instagram.com',
        'facebook.com'
    ]
    return any(site in domain for site in js_heavy_sites)

async def fetch_page(session: aiohttp.ClientSession, url: str, context: str) -> Dict:
    """Fetch page with appropriate method based on site"""
    if is_js_heavy_site(url):
        return await fetch_page_with_js(url, context)
    else:
        try:
            print(f"Fetching: {url}")
            async with session.get(url, headers=HEADERS, timeout=30) as response:
                if response.status != 200:
                    print(f"Error {response.status} for {url}")
                    return None
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Check for hackathon terms
                text_content = soup.get_text().lower()
                hackathon_terms = ['hackathon', 'register', 'registration', 'prize', 
                                'deadline', 'submit', 'participate', 'team']
                
                if not any(term in text_content for term in hackathon_terms):
                    print(f"No hackathon terms found in {url}")
                    return None
                
                # Clean HTML content
                for tag in soup.find_all(['script', 'style']):
                    tag.decompose()
                
                # Try to get main content
                main_content = (
                    soup.find('main') or 
                    soup.find('article') or 
                    soup.find('div', {'class': ['content', 'main-content']}) or 
                    soup.find('body')
                )
                
                if not main_content:
                    print(f"No main content found in {url}")
                    return None
                
                # Save HTML content
                file_path = await save_html_content(str(main_content), url)
                if not file_path:
                    return None
                
                # Extract dates
                date_patterns = [
                    r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
                    r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
                    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'
                ]
                
                dates_found = []
                for pattern in date_patterns:
                    dates_found.extend(re.findall(pattern, text_content))
                
                return {
                    'url': url,
                    'context': context,
                    'file_path': file_path,
                    'dates_found': dates_found,
                    'crawled_at': datetime.now().isoformat(),
                    'title': soup.title.string if soup.title else url,
                    'js_rendered': False
                }
                
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return None

def save_results(pages: List[Dict]):
    """Save crawled pages to index"""
    try:
        existing = load_results()
        
        # Use URL as key to avoid duplicates
        url_to_page = {page['url']: page for page in existing}
        
        new_count = 0
        for page in pages:
            if page['url'] not in url_to_page:
                url_to_page[page['url']] = page
                new_count += 1
        
        # Save updated index
        with open(PATHS['index_file'], 'w') as f:
            json.dump(list(url_to_page.values()), f, indent=2)
        
        print(f"Saved {new_count} new pages")
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def load_results() -> List[Dict]:
    """Load saved results"""
    try:
        if os.path.exists(PATHS['index_file']):
            with open(PATHS['index_file'], 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading results: {str(e)}")
    return []

def get_search_queries() -> List[Dict[str, str]]:
    """
    Generate search queries for finding hackathon events
    
    Returns a list of dictionaries containing:
    - query: The search string to use
    - context: Category/type of the hackathon search
    
    Uses current date to filter for upcoming events
    """
    # Get current year and calculate next year
    current_year = datetime.now().year
    next_year = current_year + 1
    # Get current month name and date for filtering
    current_month = datetime.now().strftime("%B")  # Full month name
    current_date = datetime.now().strftime("%d")
    
    # Create date filter string for Google search
    date_filter = f"after:{current_month} {current_date}"
    
    # Return list of search queries with their contexts
    return [
        {
            'query': f"upcoming web3, ai, blockchain hackathon {current_year}, {next_year} registration open {date_filter}",
            'context': 'upcoming'
        },
        {
            'query': f"new hackathon announcement {current_year}, {next_year} prize {date_filter}",
            'context': 'new'
        },
        {
            'query': f"hackathon {current_year}, {next_year} registration open {date_filter}",
            'context': 'future'
        },
        {
            'query': f"student hackathon {current_year}, {next_year} registration {date_filter}",
            'context': 'student'
        },
        {
            'query': f"university hackathon competition {current_year}, {next_year} apply {date_filter}",
            'context': 'university'
        },
        {
            'query': f"international hackathon {current_year}, {next_year} web3, ai, blockchain {date_filter}",
            'context': 'international'
        },
        {
            'query': f"AI ML hackathon {current_year}, {next_year} registration {date_filter}",
            'context': 'ai_ml'
        },
        {
            'query': f"blockchain web3 hackathon {current_year}, {next_year} apply {date_filter}",
            'context': 'blockchain'
        }
    ]

async def search_hackathons(query: str, num_results: int = 8) -> List[str]:
    """
    Search for hackathon URLs using Google search
    
    Args:
        query: Search query string
        num_results: Maximum number of results to return
        
    Returns:
        List of filtered URLs that likely contain hackathon information
    """
    try:
        print(f"Searching: {query}")
        # Add negative terms to exclude irrelevant results
        search_query = f"{query} -github -youtube -past -winners -completed -ended"
        # Perform Google search
        results = list(search(search_query, num_results=num_results))
        
        # Filter out unwanted URLs that likely don't contain relevant info
        filtered_results = []
        unwanted_terms = ['github.com', 'youtube.com', 'past-hack', 'winners', 
                         'blog.', 'news.', 'article', 'about-us']
        
        # Only keep URLs that don't contain unwanted terms
        for url in results:
            if not any(term in url.lower() for term in unwanted_terms):
                filtered_results.append(url)
                
        print(f"Found {len(filtered_results)} relevant results")
        return filtered_results
    except Exception as e:
        print(f"Search error: {str(e)}")
        return []

async def crawl_hackathons() -> Dict:
    """
    Main function to discover and crawl hackathon pages
    
    Coordinates the entire crawling process:
    1. Gets search queries
    2. Searches for URLs
    3. Fetches and processes pages
    4. Saves results
    
    Returns:
        Dictionary with crawling statistics and results
    """
    try:
        print("Starting hackathon discovery")
        all_pages = []
        
        # Get list of search queries
        queries = get_search_queries()
        
        # Create async session and process queries
        async with aiohttp.ClientSession() as session:
            for query_info in queries:
                # Search for URLs
                urls = await search_hackathons(query_info['query'])
                if urls:
                    # Create tasks for fetching each URL
                    tasks = [fetch_page(session, url, query_info['context']) for url in urls]
                    # Run tasks concurrently
                    results = await asyncio.gather(*tasks)
                    # Add successful results to list
                    all_pages.extend([r for r in results if r])
                
                # Delay between queries to avoid rate limiting
                await asyncio.sleep(2)
        
        # Save results if any pages were found
        if all_pages:
            save_results(all_pages)
        
        # Prepare result summary
        result = {
            "status": "success",
            "pages_crawled": len(all_pages),
            "contexts": list(set(page['context'] for page in all_pages))
        }
        print(f"\nFinal result: {result}")
        return result
            
    except Exception as e:
        print(f"Error in crawl_hackathons: {str(e)}")
        return {"status": "error", "message": str(e)}
