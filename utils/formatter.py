import textwrap
import os
import re

# Get max length from environment or use default
MAX_LENGTH = int(os.environ.get('MAX_LINKEDIN_LENGTH', 2500))

def clean_text_for_linkedin(text):
    """Clean and format text for LinkedIn while preserving important formatting"""
    if not text:
        return ""
    
    # Clean up excessive whitespace while preserving paragraph breaks
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Replace multiple line breaks with double
    text = re.sub(r' +', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'\n +', '\n', text)  # Remove leading spaces after line breaks
    
    return text.strip()

def format_for_linkedin(post):
    title = post['title']
    url = post['url']
    text = post['content']
    images = post.get('images', [])

    # Clean the text while preserving formatting
    cleaned_text = clean_text_for_linkedin(text)
    
    # Calculate available space for content
    title_length = len(title)
    url_length = len(url)
    footer_length = 50  # Space for emojis and formatting
    available_length = MAX_LENGTH - title_length - url_length - footer_length
    
    # Truncate text if needed while preserving paragraph breaks
    if len(cleaned_text) > available_length:
        # Try to break at paragraph boundaries
        paragraphs = cleaned_text.split('\n\n')
        truncated_text = ""
        
        for paragraph in paragraphs:
            if len(truncated_text + paragraph + '\n\n') <= available_length:
                truncated_text += paragraph + '\n\n'
            else:
                # If we can't fit the whole paragraph, truncate it
                remaining_length = available_length - len(truncated_text)
                if remaining_length > 10:  # Only add if we have meaningful space
                    truncated_text += textwrap.shorten(paragraph, width=remaining_length, placeholder='...')
                break
        
        cleaned_text = truncated_text.strip()

    # Build LinkedIn body with preserved formatting
    formatted = f"🔹 {title}\n\n{cleaned_text}\n\n📖 Read more: {url}"

    if images:
        formatted += "\n\n📷 Images:\n"
        for i, img in enumerate(images, 1):
            formatted += f"- Image {i}: {img}\n"

    return formatted.strip(), images
