import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

# Configurable RSS feed URL
RSS_FEED_URL = os.environ.get('RSS_FEED_URL', 'https://blog.mmlogistix.com/feed/')

def fetch_blog_posts():
    try:
        logger.info(f"Fetching posts from: {RSS_FEED_URL}")
        feed = feedparser.parse(RSS_FEED_URL)
        
        # Check for feed parsing errors
        if hasattr(feed, 'bozo') and feed.bozo:
            logger.error(f"RSS feed parsing error: {feed.bozo_exception}")
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
