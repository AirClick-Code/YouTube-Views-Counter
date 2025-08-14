import requests
import re
import json
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import sys
import time
from pathlib import Path

def extract_video_id(url):
    """
    Extract video ID from various forms of YouTube URLs
    """
    parsed_url = urlparse(url)
    
    if parsed_url.netloc == 'youtu.be':
        return parsed_url.path[1:]
    
    if parsed_url.netloc in ('youtube.com', 'www.youtube.com'):
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            return query_params['v'][0]
    
    raise ValueError("Invalid YouTube URL")

def get_video_views(url, debug=False):
    """
    Get view count for a YouTube video without using the API
    """
    try:
        video_id = extract_video_id(url)
        if debug:
            print(f"Extracted video ID: {video_id}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'CONSENT=YES+; PREF=f4=4000000&tz=UTC',
        }
        
        response = requests.get(
            f'https://www.youtube.com/watch?v={video_id}',
            headers=headers,
            cookies={'CONSENT': 'YES+'}
        )
        response.raise_for_status()
        
        if debug:
            print(f"Response status code: {response.status_code}")

        # Try multiple patterns
        patterns = [
            r'"viewCount":\{"simpleText":"([\d,]+)\s+views"\}',
            r'\"viewCount\":\"([\d,]+)\"',
            r'"text":"([\d,]+)\s+views"',
            r'videoViewCountRenderer":\{"viewCount":\{"simpleText":"([\d,]+)',
            r'"viewCount":\{"text":\s*"([\d,]+)[^"]*"\}',
        ]

        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                views = match.group(1).replace(',', '')
                return int(views)

        # Try parsing with BeautifulSoup as fallback
        soup = BeautifulSoup(response.text, 'html.parser')
        
        view_elements = [
            soup.select_one('ytd-watch-info-text #info'),
            soup.select_one('meta[itemprop="interactionCount"]'),
            soup.select_one('.view-count'),
            soup.select_one('yt-formatted-string[id="info"]'),
        ]

        for element in view_elements:
            if element:
                view_text = element.get('content', element.text)
                views_match = re.search(r'([\d,]+)', view_text)
                if views_match:
                    views = views_match.group(1).replace(',', '')
                    return int(views)

        raise ValueError("Could not find view count in page")
            
    except requests.RequestException as e:
        raise Exception(f"Error fetching video: {str(e)}")
    except ValueError as e:
        raise Exception(f"Error processing video: {str(e)}")

def process_url_file(input_file, output_file=None, debug=False):
    """
    Process URLs from input file and optionally save results to output file
    """
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        return

    results = []
    total_views = 0
    successful_urls = 0
    failed_urls = 0
    total_urls = sum(1 for _ in open(input_file, 'r'))
    
    print(f"Processing {total_urls} URLs...")
    
    with open(input_file, 'r') as f:
        for i, line in enumerate(f, 1):
            url = line.strip()
            if not url:  # Skip empty lines
                continue
                
            print(f"\nProcessing URL {i}/{total_urls}: {url}")
            try:
                views = get_video_views(url, debug)
                result = f"{url},{views}"
                results.append(result)
                total_views += views
                successful_urls += 1
                print(f"Views: {views:,}")
            except Exception as e:
                error_msg = f"{url},Error: {str(e)}"
                results.append(error_msg)
                failed_urls += 1
                print(f"Error: {str(e)}")
            
            # Add delay to avoid rate limiting
            if i < total_urls:  # Don't sleep after the last URL
                time.sleep(2)

    # Save results
    if output_file:
        with open(output_file, 'w') as f:
            f.write("URL,Views\n")  # CSV header
            for result in results:
                f.write(f"{result}\n")
            # Add summary at the end
            f.write("\nSummary\n")
            f.write(f"Total Views,{total_views}\n")
            f.write(f"Successful URLs,{successful_urls}\n")
            f.write(f"Failed URLs,{failed_urls}\n")
        print(f"\nResults saved to {output_file}")
    
    # Print summary
    print("\nSummary:")
    print("=" * 40)
    print(f"Total Views: {total_views:,}")
    print(f"Successfully Processed URLs: {successful_urls}")
    print(f"Failed URLs: {failed_urls}")
    print("=" * 40)
    
    return results, total_views

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search.py input_file.txt [output_file.csv]")
        print("Example: python3 search.py urls.txt results.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    print("Make sure you have BeautifulSoup installed:")
    print("pip install beautifulsoup4")
    print("\nStarting URL processing...")
    
    results, total_views = process_url_file(input_file, output_file, debug=False)