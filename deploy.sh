#!/bin/bash

# 🚀 Monk-AI Heroku Deployment Script
# Run this script to deploy your backend to Heroku

set -e  # Exit on any error

echo "🧙‍♂️ Monk-AI Heroku Deployment"
echo "=============================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please log in to Heroku first:"
    heroku login
fi

# Get app name from user
read -p "Enter your Heroku app name (or press Enter for auto-generated): " APP_NAME

# Create Heroku app
if [ -z "$APP_NAME" ]; then
    echo "🏗️ Creating new Heroku app..."
    heroku create
else
    echo "🏗️ Creating Heroku app: $APP_NAME"
    heroku create "$APP_NAME"
fi

# Get the actual app name (in case it was auto-generated)
APP_NAME=$(heroku apps:info --json | grep -o '"name":"[^"]*' | cut -d'"' -f4)
echo "✅ App created: https://$APP_NAME.herokuapp.com"

# Set environment variables
echo "🔧 Setting environment variables..."

# Prompt for required API keys
read -p "Enter your OpenAI API Key: " OPENAI_KEY
heroku config:set OPENAI_API_KEY="$OPENAI_KEY"

read -p "Enter your Gemini API Key (optional, press Enter to skip): " GEMINI_KEY
if [ ! -z "$GEMINI_KEY" ]; then
    heroku config:set GEMINI_API_KEY="$GEMINI_KEY"
fi

read -p "Enter your frontend URL (e.g., https://yourapp.vercel.app): " FRONTEND_URL
heroku config:set FRONTEND_URL="$FRONTEND_URL"

# Set other configuration
heroku config:set LLM_PROVIDER="openai"
heroku config:set LLM_MODEL="gpt-4o"
heroku config:set ENVIRONMENT="production"
heroku config:set DEBUG="false"

# Generate secret keys
echo "🔑 Generating secret keys..."
heroku config:set SECRET_KEY="$(openssl rand -hex 32)"
heroku config:set JWT_SECRET_KEY="$(openssl rand -hex 32)"

# Add PostgreSQL database
echo "🗄️ Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini

# Commit changes if needed
if [[ `git status --porcelain` ]]; then
    echo "📝 Committing deployment files..."
    git add .
    git commit -m "Add Heroku deployment configuration"
fi

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git push heroku main

# Check deployment status
echo "📊 Checking deployment status..."
heroku ps

# Open the app
echo "🌐 Opening your deployed app..."
heroku open

echo ""
echo "✅ Deployment Complete!"
echo "======================================"
echo "🔗 Backend URL: https://$APP_NAME.herokuapp.com"
echo "📱 Frontend CORS: Configured for $FRONTEND_URL"
echo "📊 Monitor logs: heroku logs --tail"
echo "⚙️  Manage app: https://dashboard.heroku.com/apps/$APP_NAME"
echo ""
echo "🎯 Next Steps:"
echo "1. Update your Vercel frontend environment variables:"
echo "   NEXT_PUBLIC_API_URL=https://$APP_NAME.herokuapp.com"
echo "2. Test your API endpoints"
echo "3. Monitor application logs"
echo ""
echo "Happy coding! 🚀" 