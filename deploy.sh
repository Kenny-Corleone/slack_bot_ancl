#!/bin/bash

# Slack Task Assignment Bot Deployment Script
echo "🚀 Deploying Slack Task Assignment Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version+ is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp env.example .env
    echo "✅ .env file created. Please edit it with your Slack credentials."
else
    echo "✅ .env file already exists"
fi

# Create data directory
mkdir -p data

# Run the application
echo "🚀 Starting the Slack bot..."
echo "📍 The bot will be available at: http://localhost:5000"
echo "🔍 Health check: http://localhost:5000/health"
echo ""
echo "Press Ctrl+C to stop the bot"
echo ""

python app.py 