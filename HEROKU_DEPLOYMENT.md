# 🚀 Heroku Deployment Guide for Monk-AI Backend

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your project is in a Git repository

## 📁 Files Created for Deployment

The following files have been created for Heroku deployment:
- `Procfile` - Tells Heroku how to run your app
- `runtime.txt` - Specifies Python version
- `app.json` - Heroku app configuration
- `requirements.txt` - Python dependencies (already exists)

## 🚀 Deployment Steps

### 1. **Login to Heroku**
```bash
heroku login
```

### 2. **Create Heroku App**
```bash
# Replace 'your-app-name' with your desired app name
heroku create your-monk-ai-backend

# Or let Heroku generate a random name
heroku create
```

### 3. **Set Environment Variables**
```bash
# Required API Keys
heroku config:set OPENAI_API_KEY="your_openai_api_key_here"
heroku config:set GEMINI_API_KEY="your_gemini_api_key_here"

# LLM Configuration
heroku config:set LLM_PROVIDER="openai"
heroku config:set LLM_MODEL="gpt-4o"

# Environment Settings
heroku config:set ENVIRONMENT="production"
heroku config:set DEBUG="false"

# Secret Keys
heroku config:set SECRET_KEY="$(openssl rand -hex 32)"
heroku config:set JWT_SECRET_KEY="$(openssl rand -hex 32)"

# Frontend URL (replace with your Vercel domain)
heroku config:set FRONTEND_URL="https://your-app.vercel.app"
```

### 4. **Add PostgreSQL Database** (Optional but recommended)
```bash
heroku addons:create heroku-postgresql:mini
```

### 5. **Deploy Your Application**
```bash
# Commit all changes
git add .
git commit -m "Add Heroku deployment configuration"

# Deploy to Heroku
git push heroku main

# Or if you're on a different branch:
git push heroku your-branch:main
```

### 6. **Check Your Deployment**
```bash
# Open your app in browser
heroku open

# Check logs
heroku logs --tail

# Check app status
heroku ps
```

## 🌐 Frontend + Backend Integration

### **Vercel Frontend Configuration**

Your Vercel frontend needs to know about your Heroku backend URL:

1. **Create/Update Environment Variables in Vercel:**
   ```
   NEXT_PUBLIC_API_URL=https://your-monk-ai-backend.herokuapp.com
   ```

2. **Update Frontend API Calls:**
   ```typescript
   // In your React components or API service
   const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
   
   // Example API call
   const response = await fetch(`${API_BASE_URL}/api/generate-project-scope`, {
     method: 'POST',
     headers: {
       'Content-Type': 'application/json',
     },
     body: JSON.stringify(requestData),
   });
   ```

3. **Update CORS Settings:**
   After deploying, update the `FRONTEND_URL` environment variable:
   ```bash
   heroku config:set FRONTEND_URL="https://your-actual-vercel-domain.vercel.app"
   ```

Your Vercel frontend and Heroku backend will work perfectly together! 🚀 