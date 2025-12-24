#!/bin/bash

# GitHub Repository Setup Script
# This script helps you set up the repository for first-time GitHub deployment

echo "=========================================="
echo "  GitHub Repository Setup"
echo "=========================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

echo "✓ Git found"
echo ""

# Initialize git repository if not already initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✓ Git repository initialized"
else
    echo "✓ Git repository already initialized"
fi
echo ""

# Check if .gitignore exists
if [ ! -f .gitignore ]; then
    echo "❌ .gitignore not found! This is critical for security."
    exit 1
fi

echo "✓ .gitignore found"
echo ""

# Check if .env exists (it should NOT be committed)
if [ -f .env ]; then
    echo "⚠️  WARNING: .env file found!"
    echo "    Make sure it's listed in .gitignore"
    echo "    This file contains sensitive API keys and should NEVER be committed"
    
    # Check if .env is in .gitignore
    if grep -q "^\.env$" .gitignore; then
        echo "✓ .env is in .gitignore (good!)"
    else
        echo "❌ .env is NOT in .gitignore!"
        echo "    Adding it now..."
        echo ".env" >> .gitignore
    fi
else
    echo "✓ No .env file (you'll create it from .env.example)"
fi
echo ""

# Check if .env.example exists
if [ ! -f .env.example ]; then
    echo "⚠️  .env.example not found (recommended to have one)"
else
    echo "✓ .env.example found"
fi
echo ""

# Create .env from .env.example if it doesn't exist
if [ ! -f .env ] && [ -f .env.example ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env created. Please edit it to add your API key."
    echo ""
    echo "⚠️  IMPORTANT: Open .env and add your Anthropic API key!"
    echo ""
fi

# Check what files would be committed
echo "📋 Checking files to be committed..."
git add .
git status --short

echo ""
echo "⚠️  VERIFY: Make sure these files are NOT listed above:"
echo "   - .env (contains API keys)"
echo "   - data/ (contains user data)"
echo "   - Any files with passwords or secrets"
echo ""

# Ask for confirmation
read -p "Do you want to proceed with the first commit? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "📝 Creating first commit..."
    git add .
    git commit -m "Initial commit: Equipment Quote Management System"
    echo "✓ First commit created"
    echo ""
    
    echo "Next steps:"
    echo "1. Create a new repository on GitHub"
    echo "2. Run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/quote-management-system.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. IMPORTANT: In GitHub repository settings, verify that .env is NOT visible"
    echo "4. Add secrets in Streamlit Cloud or your deployment platform"
    echo ""
else
    echo ""
    echo "❌ Commit cancelled. Review files and run this script again when ready."
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
