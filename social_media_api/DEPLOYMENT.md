# Deployment Guide - Social Media API

## Overview
This guide covers deploying the Django REST API to production using Railway (or similar hosting services).

## Prerequisites
- GitHub repository with your code
- Railway account (or Heroku/DigitalOcean)
- Environment variables configured

## Production Configuration

### 1. Settings Configuration
The `settings.py` has been configured for production with:
- Environment variable support for `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`
- Database configuration using `dj-database-url`
- Static files handling with WhiteNoise
- Security settings for HTTPS

### 2. Required Files
- `requirements.txt` - Python dependencies
- `Procfile` - Process configuration for deployment
- `runtime.txt` - Python version specification
- `gunicorn.conf.py` - Gunicorn server configuration
- `.env.example` - Environment variables template

## Deployment Steps

### Option 1: Railway Deployment

1. **Connect Repository**
   ```bash
   # Push your code to GitHub
   git add .
   git commit -m "Configure for production deployment"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up/login with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `Alx_DjangoLearnLab` repository
   - Choose the `social_media_api` directory

3. **Configure Environment Variables**
   Set these in Railway dashboard:
   ```
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   DATABASE_URL=postgresql://... (Railway provides this)
   ```

4. **Generate Secret Key**
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

### Option 2: Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Login to Heroku
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   cd social_media_api
   heroku create your-app-name
   ```

3. **Configure Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

## Post-Deployment

### 1. Run Migrations
```bash
# Railway: Automatic via Procfile
# Heroku: 
heroku run python manage.py migrate
```

### 2. Create Superuser
```bash
# Railway: Use Railway CLI or web console
# Heroku:
heroku run python manage.py createsuperuser
```

### 3. Collect Static Files
```bash
# Automatic via WhiteNoise during deployment
```

## API Endpoints

Once deployed, your API will be available at:
- Base URL: `https://your-app-name.railway.app/api/`
- Admin: `https://your-app-name.railway.app/admin/`

### Key Endpoints:
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `GET /api/posts/` - List posts
- `GET /api/posts/feed/` - User feed
- `POST /api/posts/{id}/like/` - Like post
- `GET /api/notifications/` - User notifications

## Security Features

### Production Security Settings
- `DEBUG = False`
- HTTPS enforcement
- Secure cookies
- XSS protection
- Content type sniffing protection
- HSTS headers

### Environment Variables
All sensitive data is stored in environment variables:
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string
- `ALLOWED_HOSTS` - Allowed hostnames

## Monitoring and Maintenance

### 1. Logging
- Check application logs in hosting service dashboard
- Monitor for errors and performance issues

### 2. Database Backups
- Railway/Heroku provide automatic database backups
- Schedule regular backups for production data

### 3. Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

## Troubleshooting

### Common Issues:
1. **Static files not loading**: Ensure WhiteNoise is configured
2. **Database errors**: Check DATABASE_URL environment variable
3. **ALLOWED_HOSTS error**: Add your domain to ALLOWED_HOSTS
4. **Secret key error**: Set SECRET_KEY environment variable

### Debug Commands:
```bash
# Check environment variables
heroku config  # or Railway dashboard

# View logs
heroku logs --tail  # or Railway logs

# Run Django shell
heroku run python manage.py shell
```

## Live Application

After successful deployment, your Social Media API will be accessible at:
`https://your-app-name.railway.app/`

The API includes:
- User authentication and profiles
- Post creation and management
- User following system
- Personalized feeds
- Like and notification system
- Complete REST API documentation
