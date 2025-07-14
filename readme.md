# WordPress to LinkedIn Repost Scheduler

This is a lightweight Flask app that fetches blog posts from your WordPress RSS feed, lets you assign repost dates, and formats each post for LinkedIn with embedded images.

## 🌐 Features

- Manual fetch from WordPress RSS feed
- View and assign LinkedIn repost dates
- Format posts into LinkedIn-friendly text (2,500 char limit)
- Display blog images for preview and manual download
- Copy or download LinkedIn post text
- **NEW**: Error handling and user feedback
- **NEW**: Copy to clipboard functionality
- **NEW**: Configurable RSS feed URL via environment variables
- **NEW**: Improved UI with better styling and responsiveness

## 📁 Project Structure

```
├── app.py                  # Flask server
├── config.py               # Configuration management
├── utils/
│   ├── fetch_posts.py      # Pull blog posts via RSS
│   └── formatter.py        # Reformat for LinkedIn
├── templates/
│   ├── base.html
│   ├── index.html
│   └── preview.html
├── static/
│   └── style.css           # Custom styling
├── data/posts.json         # Stores blog post metadata
├── output/                 # (Future: saved formatted files)
├── requirements.txt
├── render.yaml
├── env.example             # Environment variables example
└── README.md
```

## 🚀 Deployment (Render)

1. Fork or upload this repo to your GitHub account
2. Go to [https://render.com](https://render.com)
3. Click **"New +" → "Web Service"**
4. Connect your repo and use these settings:

   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

5. **Optional**: Add environment variables in Render dashboard:
   - `RSS_FEED_URL`: Your WordPress RSS feed URL
   - `SECRET_KEY`: A secure secret key for Flask
   - `MAX_LINKEDIN_LENGTH`: Character limit (default: 2500)

6. Deploy! Open the URL and use the UI to fetch and schedule posts

## 📝 Usage Instructions

1. Click **"Fetch/Update Posts"** to pull blog entries
2. For each post, enter a **LinkedIn repost date** and click **Save**
3. Click **Preview** to view formatted LinkedIn post
4. Use the **"Copy to Clipboard"** button to copy the formatted text
5. Manually post to LinkedIn, uploading images as needed

## ⚙️ Configuration

The app can be configured using environment variables:

- `RSS_FEED_URL`: Your WordPress RSS feed URL (default: https://blog.mmlogistix.com/feed/)
- `SECRET_KEY`: Flask secret key for sessions
- `MAX_LINKEDIN_LENGTH`: LinkedIn character limit (default: 2500)
- `FLASK_DEBUG`: Set to 'True' for development, 'False' for production

## 🔧 Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `env.example` to `.env` and configure variables
4. Run: `python app.py`
5. Open http://localhost:5000

## 📌 Notes

- Supports basic formatting, trimming, and image inclusion
- Images are shown as previews and must be uploaded manually to LinkedIn
- Content is not auto-posted (manual copy-paste as requested)
- **NEW**: Improved error handling for RSS feed failures
- **NEW**: Date validation and user feedback
- **NEW**: Responsive design with better UX

---

Built for personal use to simplify reposting blog content on LinkedIn with style.
