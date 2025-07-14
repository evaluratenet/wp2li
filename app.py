from flask import Flask, render_template, request, redirect, url_for, flash
from utils.fetch_posts import fetch_blog_posts
from utils.formatter import format_for_linkedin
from config import config
import json
import os
from datetime import datetime
import logging

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Ensure folders exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    # Load or initialize posts data
    def load_posts():
        try:
            if os.path.exists(app.config['POSTS_FILE']):
                with open(app.config['POSTS_FILE'], 'r') as f:
                    return json.load(f)
            return []
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading posts: {e}")
            return []

    def save_posts(posts):
        try:
            with open(app.config['POSTS_FILE'], 'w') as f:
                json.dump(posts, f, indent=2)
        except IOError as e:
            logger.error(f"Error saving posts: {e}")
            flash("Error saving posts data", "error")

    def validate_date(date_string):
        """Validate date input format"""
        if not date_string:
            return True  # Empty dates are allowed
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @app.route('/')
    def index():
        posts = load_posts()
        return render_template('index.html', posts=posts)

    @app.route('/fetch', methods=['POST'])
    def fetch():
        try:
            current_posts = load_posts()
            new_posts = fetch_blog_posts()
            
            if new_posts is None:
                flash("Failed to fetch posts from RSS feed. Please check the feed URL.", "error")
                return redirect(url_for('index'))
            
            existing_urls = {p['url'] for p in current_posts}
            added_count = 0

            for post in new_posts:
                if post['url'] not in existing_urls:
                    current_posts.append(post)
                    added_count += 1

            save_posts(current_posts)
            
            if added_count > 0:
                flash(f"Successfully fetched {added_count} new posts!", "success")
            else:
                flash("No new posts found.", "info")
                
        except Exception as e:
            logger.error(f"Error fetching posts: {e}")
            flash("Error fetching posts. Please try again.", "error")
        
        return redirect(url_for('index'))

    @app.route('/update_date', methods=['POST'])
    def update_date():
        post_url = request.form.get('url')
        new_date = request.form.get('linkedin_date', '')
        
        if not post_url:
            flash("Invalid post URL", "error")
            return redirect(url_for('index'))
        
        if not validate_date(new_date):
            flash("Invalid date format. Please use YYYY-MM-DD format.", "error")
            return redirect(url_for('index'))
        
        try:
            posts = load_posts()
            updated = False
            
            for post in posts:
                if post['url'] == post_url:
                    post['linkedin_date'] = new_date
                    updated = True
                    break
            
            if updated:
                save_posts(posts)
                flash("Date updated successfully!", "success")
            else:
                flash("Post not found", "error")
                
        except Exception as e:
            logger.error(f"Error updating date: {e}")
            flash("Error updating date", "error")
        
        return redirect(url_for('index'))

    @app.route('/preview/<int:post_id>')
    def preview(post_id):
        try:
            posts = load_posts()
            if post_id >= len(posts):
                flash("Post not found", "error")
                return redirect(url_for('index'))
                
            post = posts[post_id]
            linkedin_text, image_urls = format_for_linkedin(post)
            return render_template('preview.html', post=post, linkedin_text=linkedin_text, images=image_urls)
            
        except Exception as e:
            logger.error(f"Error previewing post: {e}")
            flash("Error loading post preview", "error")
            return redirect(url_for('index'))

    return app

app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (for Render) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Bind to 0.0.0.0 for production deployment
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])