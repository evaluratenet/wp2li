import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import os
import logging
import urllib.parse

logger = logging.getLogger(__name__)

def get_rss_url_with_params(base_url, posts_per_page=50):
    """Add parameters to RSS URL to get more posts"""
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
        
        # Try to get more posts by modifying the RSS URL
        rss_url = get_rss_url_with_params(base_rss_url, posts_per_page=posts_per_page)
        logger.info(f"Fetching posts from: {rss_url}")
        
        feed = feedparser.parse(rss_url)
        
        # Check for feed parsing errors
        if hasattr(feed, 'bozo') and feed.bozo:
            logger.error(f"RSS feed parsing error: {feed.bozo_exception}")
            # Try original URL as fallback
            logger.info("Trying original RSS URL as fallback")
            feed = feedparser.parse(base_rss_url)
            if hasattr(feed, 'bozo') and feed.bozo:
                logger.error(f"Fallback RSS feed also failed: {feed.bozo_exception}")
                return None
            
        if not feed.entries:
            logger.warning("No entries found in RSS feed")
            return []
            
        posts = []

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

                posts.append({
                    'title': title,
                    'url': url,
                    'published': published,
                    'content': text_content,
                    'images': image_urls,
                    'linkedin_date': ''
                })
                
            except Exception as e:
                logger.error(f"Error processing entry {entry.get('title', 'Unknown')}: {e}")
                continue

        logger.info(f"Successfully fetched {len(posts)} posts")
        return posts
        
    except Exception as e:
        logger.error(f"Error fetching RSS feed: {e}")
        return None
