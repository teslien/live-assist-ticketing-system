# Deployment Guide

This Flask ticketing system with WebSocket support can be deployed on several platforms. Here are the recommended options:

## 🚀 **Recommended: Render.com (Best for Flask + WebSockets)**

### Steps:
1. **Create Render Account**: Sign up at [render.com](https://render.com)
2. **Connect GitHub**: Link your GitHub account
3. **Create Web Service**: 
   - Choose "Web Service"
   - Connect your repository
   - Render will auto-detect the `render.yaml` configuration
   - Or manually set:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:application`
     - **Environment**: `Python 3`
4. **Deploy**: Render will automatically deploy your app with production server

### Features:
- ✅ WebSocket support
- ✅ Persistent disk storage for SQLite
- ✅ HTTPS included
- ✅ Auto-deploys on git push

---

## 🚄 **Alternative: Railway.app**

### Steps:
1. **Create Railway Account**: Sign up at [railway.app](https://railway.app)
2. **Deploy from GitHub**:
   - Click "Deploy from GitHub"
   - Select your repository
   - Railway auto-detects Python and deploys
3. **Access**: Get your app URL from Railway dashboard

### Features:
- ✅ WebSocket support
- ✅ PostgreSQL option available
- ✅ Simple deployment
- ✅ Free tier available

---

## 🟣 **Alternative: Heroku**

### Steps:
1. **Install Heroku CLI**: Download from [heroku.com](https://heroku.com)
2. **Login**: `heroku login`
3. **Create App**: `heroku create your-ticketing-system`
4. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Features:
- ✅ WebSocket support (with upgrade)
- ⚠️ Ephemeral filesystem (database resets)
- ✅ Add-ons available (PostgreSQL)

---

## ⚡ **For Static Hosting (Netlify/Vercel) - Limited**

**Note**: These platforms don't support full Flask apps with WebSockets. You would need to:
1. Convert to serverless functions
2. Use external database
3. Replace WebSockets with polling
4. Significant code changes required

---

## 🔧 **Environment Variables**

Set these environment variables in your deployment platform:

| Variable | Value | Description |
|----------|-------|-------------|
| `PORT` | `5000` | Port number (auto-set by most platforms) |
| `FLASK_ENV` | `production` | Disables debug mode |

---

## 📦 **Pre-deployment Checklist**

- [x] `requirements.txt` includes all dependencies
- [x] `app.py` reads PORT from environment
- [x] Database initialization on startup
- [x] Static files properly configured
- [x] CORS settings for WebSockets
- [x] Secret key configured

---

## 🛠 **Database Considerations**

### SQLite (Current):
- ✅ Simple setup
- ✅ No external dependencies
- ⚠️ Single file database
- ⚠️ May not persist on some platforms

### PostgreSQL (Recommended for Production):
To upgrade to PostgreSQL, update `app.py`:

```python
import psycopg2
from urllib.parse import urlparse

# Replace SQLite connection with:
def get_db_connection():
    if os.environ.get('DATABASE_URL'):
        # Production PostgreSQL
        url = urlparse(os.environ.get('DATABASE_URL'))
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    else:
        # Development SQLite
        conn = sqlite3.connect('tickets.db')
    return conn
```

---

## 📱 **API Testing After Deployment**

Once deployed, test the API:

```bash
curl -X POST https://your-app-url.com/create_ticket \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "pdf_link": "https://example.com/guide.pdf",
    "product_id": "TEST-001"
  }'
```

---

## 🎯 **Quick Start: Render Deployment**

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Use default Python settings
6. Deploy!

Your ticketing system will be live with real-time WebSocket updates! 🎉
