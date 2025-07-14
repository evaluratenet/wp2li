import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import os
import logging
import urllib.parse

logger = logging.getLogger(__name__)

def get_rss_url_with_params(base_url, posts_per_page=50):
    """Add parameters to RSS URL to get more posts from WordPress"""
    parsed = urllib.parse.urlparse(base_url)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    # Add WordPress RSS parameters for more posts
    query_params['posts_per_rss'] = [str(posts_per_page)]
    query_params['orderby'] = ['date']
    query_params['order'] = ['DESC']
    
    # Rebuild URL with parameters
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    return urllib.parse.urlunparse((
        parsed.scheme, parsed.netloc, parsed.path,
        parsed.params, new_query, parsed.fragment
    ))

def fetch_blog_posts():
    try:
        # Get configuration
        from config import config
        app_config = config['default']()
        base_rss_url = app_config.RSS_FEED_URL
        posts_per_page = app_config.RSS_POSTS_PER_PAGE
        rss_debug = app_config.RSS_DEBUG
        
        if rss_debug:
            logger.info(f"RSS Debug enabled. Base URL: {base_rss_url}, Posts per page: {posts_per_page}")
        
        # Try multiple approaches to get more posts
        urls_to_try = [
            # Method 1: With parameters
            get_rss_url_with_params(base_rss_url, posts_per_page=posts_per_page),
            # Method 2: Direct with parameters
            f"{base_rss_url}?posts_per_rss={posts_per_page}",
            # Method 3: Try different post limits
            f"{base_rss_url}?posts_per_rss=100",
            f"{base_rss_url}?posts_per_rss=200",
            # Method 4: Try RSS2 format
            base_rss_url.replace('/feed/', '/feed/rss2/'),
            # Method 5: Try RSS2 with parameters
            f"{base_rss_url.replace('/feed/', '/feed/rss2/')}?posts_per_rss={posts_per_page}",
            # Method 6: Original URL as last resort
            base_rss_url
        ]
        
        posts = []
        
        for i, rss_url in enumerate(urls_to_try):
            if rss_debug:
                logger.info(f"Trying RSS URL method {i+1}: {rss_url}")
            
            try:
                feed = feedparser.parse(rss_url)
                
                # Check for feed parsing errors
                if hasattr(feed, 'bozo') and feed.bozo:
                    logger.error(f"RSS feed parsing error: {feed.bozo_exception}")
                    continue
                    
                if not feed.entries:
                    if rss_debug:
                        logger.warning(f"No entries found in RSS feed method {i+1}")
                    continue
                
                if rss_debug:
                    logger.info(f"Method {i+1} found {len(feed.entries)} posts")
                
                # Process entries
                for entry in feed.entries:
                    try:
                        title = entry.title or "Untitled"
                        url = entry.link or ""
                        published = entry.published or ""
                        content_html = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")

                        # Parse content to extract images
                        soup = BeautifulSoup(content_html, 'html.parser')
                        text_content = soup.get_text("\n", strip=True)
                        image_urls = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

                        post_data = {
                            'title': title,
                            'url': url,
                            'published': published,
                            'content': text_content,
                            'images': image_urls,
                            'linkedin_date': ''
                        }
                        
                        # Only add if not already present (avoid duplicates)
                        if not any(p['url'] == url for p in posts):
                            posts.append(post_data)
                            if rss_debug:
                                logger.info(f"Added post: {title}")
                        
                    except Exception as e:
                        logger.error(f"Error processing entry {entry.get('title', 'Unknown')}: {e}")
                        continue
                
                # If we got posts, break (don't try other methods)
                if posts:
                    logger.info(f"Successfully fetched {len(posts)} unique posts using method {i+1}")
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching from URL {rss_url}: {e}")
                continue

        if not posts:
            logger.warning("No posts found from any RSS method")
            return []
            
        logger.info(f"Final result: {len(posts)} unique posts fetched")
        return posts
        
    except Exception as e:
        logger.error(f"Error fetching RSS feed: {e}")
        return None
