import textwrap
import os

# Get max length from environment or use default
MAX_LENGTH = int(os.environ.get('MAX_LINKEDIN_LENGTH', 2500))


def format_for_linkedin(post):
    title = post['title']
    url = post['url']
    text = post['content']
    images = post.get('images', [])

    # Trim to LinkedIn character limit (title + body + footer)
    safe_body_len = MAX_LENGTH - len(title) - len(url) - 100
    trimmed_text = textwrap.shorten(text, width=safe_body_len, placeholder='...')

    # Build LinkedIn body
    formatted = f"🔹 {title}\n\n{trimmed_text}\n\n📖 Read more: {url}"

    if images:
        formatted += "\n\n📷 Images:\n"
        for i, img in enumerate(images, 1):
            formatted += f"- Image {i}: {img}\n"

    return formatted.strip(), images
