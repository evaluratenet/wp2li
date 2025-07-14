import os

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # RSS Feed settings
    RSS_FEED_URL = os.environ.get('RSS_FEED_URL', 'https://blog.mmlogistix.com/feed/')
    RSS_POSTS_PER_PAGE = int(os.environ.get('RSS_POSTS_PER_PAGE', 50))  # Number of posts to fetch from RSS
    
    # Alternative RSS URLs to try if main feed is limited (different post limits)
    RSS_ALTERNATIVE_URLS = [
        'https://blog.mmlogistix.com/feed/?posts_per_rss=50',
        'https://blog.mmlogistix.com/feed/?posts_per_rss=100',
        'https://blog.mmlogistix.com/feed/?posts_per_rss=200'
    ]
    
    # File paths
    POSTS_FILE = 'data/posts.json'
    
    # LinkedIn formatting
    MAX_LINKEDIN_LENGTH = 2500
    
    # Development settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """Initialize app with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig  # Default to production for Render
} 