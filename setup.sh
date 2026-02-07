#!/bin/bash
# Setup script for Listen app

echo "🎤 Setting up Listen..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not found"
    echo "Install from: https://www.python.org/downloads/"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create config directory
mkdir -p ~/.listen

# Prompt for API key
echo ""
echo "Enter your OpenAI API key:"
read -s OPENAI_KEY
echo '{"openai_api_key": "'$OPENAI_KEY'"}' > ~/.listen/config.json

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run Listen:"
echo "  cd $(pwd)"
echo "  source venv/bin/activate"
echo "  python3 listen.py"
echo ""
echo "To run at startup, add to Login Items in System Preferences"
