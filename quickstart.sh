#!/bin/bash

# Quick Start Script for GitHub Commit Data Collector
# This script helps you get started quickly

set -e  # Exit on error

echo "=================================================="
echo "GitHub Commit Data Collector - Quick Start"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Error: Python is not installed"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"

# Check if requirements are installed
echo ""
echo "Checking dependencies..."
if $PYTHON_CMD -c "import requests" 2>/dev/null; then
    echo "✓ Dependencies already installed"
else
    echo "Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Check for .env file
echo ""
echo "Checking configuration..."
if [ ! -f .env ]; then
    echo "⚠ No .env file found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo "=================================================="
    echo "⚠ IMPORTANT: Configure your GitHub token!"
    echo "=================================================="
    echo "1. Get a GitHub token: https://github.com/settings/tokens"
    echo "2. Edit .env file and add your token:"
    echo "   GITHUB_TOKEN=your_token_here"
    echo "3. Run this script again"
    echo "=================================================="
    exit 1
else
    # Check if token is configured
    if grep -q "your_github_personal_access_token_here" .env; then
        echo "⚠ GitHub token not configured in .env"
        echo "Please edit .env and add your token"
        exit 1
    fi
    echo "✓ Configuration file found"
fi

# Create necessary directories
echo ""
echo "Setting up directories..."
mkdir -p output logs
echo "✓ Directories ready"

# Test connection
echo ""
echo "Testing GitHub API connection..."
if $PYTHON_CMD src/main.py --test-connection 2>&1 | grep -q "successful"; then
    echo "✓ Successfully connected to GitHub API"
else
    echo "❌ Connection test failed"
    echo "Please check your GitHub token in .env file"
    exit 1
fi

# Check if repositories are configured
echo ""
echo "Checking repository configuration..."
if [ -f config/repositories.yaml ]; then
    REPO_COUNT=$(grep -c "url:" config/repositories.yaml || echo "0")
    if [ "$REPO_COUNT" -gt 0 ]; then
        echo "✓ Found $REPO_COUNT configured repositories"
    else
        echo "⚠ No repositories configured"
        echo "Edit config/repositories.yaml to add repositories"
    fi
else
    echo "⚠ No repositories.yaml found"
    echo "Using default configuration"
fi

# Summary
echo ""
echo "=================================================="
echo "Setup Complete! 🎉"
echo "=================================================="
echo ""
echo "Quick start commands:"
echo ""
echo "1. Test with a public repository:"
echo "   $PYTHON_CMD src/main.py --repo https://github.com/octocat/Hello-World"
echo ""
echo "2. Collect from configured repositories:"
echo "   $PYTHON_CMD src/main.py"
echo ""
echo "3. Collect with date filter:"
echo "   $PYTHON_CMD src/main.py --date-from 2024-01-01 --date-to 2024-01-31"
echo ""
echo "4. Export as CSV:"
echo "   $PYTHON_CMD src/main.py --format csv --include-file-details"
echo ""
echo "For more options, run:"
echo "   $PYTHON_CMD src/main.py --help"
echo ""
echo "Documentation:"
echo "   README.md  - Full documentation"
echo "   SETUP.md   - Detailed setup guide"
echo "   output/SCHEMA.md - Output format reference"
echo ""
echo "=================================================="