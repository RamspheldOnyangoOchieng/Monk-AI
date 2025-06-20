#!/bin/bash

# 🔄 Setup Git Remotes for Fork and PR Creation
# Run this after creating your fork on GitHub

echo "🔄 Setting up Git remotes for fork and PR creation"
echo "================================================="

# Get user's GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo "🔧 Setting up remotes..."

# Add the original repository as upstream
git remote add upstream https://github.com/RamspheldOnyangoOchieng/Monk-AI.git

# Update origin to point to your fork
git remote set-url origin https://github.com/$GITHUB_USERNAME/Monk-AI.git

echo "✅ Remotes configured:"
git remote -v

echo ""
echo "🚀 Now you can:"
echo "1. Push to your fork: git push origin main"
echo "2. Create PR from your fork to upstream"
echo "3. Fetch upstream changes: git fetch upstream"
echo ""

# Try to push to your fork
read -p "Push changes to your fork now? (y/n): " PUSH_NOW

if [ "$PUSH_NOW" = "y" ] || [ "$PUSH_NOW" = "Y" ]; then
    echo "📤 Pushing to your fork..."
    git push origin main
    
    echo ""
    echo "✅ Changes pushed successfully!"
    echo "🎯 Create PR at: https://github.com/$GITHUB_USERNAME/Monk-AI/compare"
    echo ""
    echo "PR Title: Add Heroku Deployment Configuration"
    echo "PR Description:"
    echo "- Add Procfile for Heroku deployment"
    echo "- Add runtime.txt with Python 3.11"
    echo "- Add app.json for Heroku configuration"
    echo "- Add deployment script and documentation"
    echo "- Update CORS settings for production"
    echo "- Support Vercel frontend + Heroku backend architecture"
fi 