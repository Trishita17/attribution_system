#!/bin/bash

# Attribution System Setup Script
echo "🚀 Setting up Attribution System..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Copy environment template
if [ ! -f "attribution_agents/.env" ]; then
    echo "📝 Creating environment configuration..."
    cp attribution_agents/.env.example attribution_agents/.env
    echo "⚠️  Please edit attribution_agents/.env with your credentials before running the system"
else
    echo "✅ Environment file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit attribution_agents/.env with your Snowflake and Anthropic credentials"
echo "2. Run: source venv/bin/activate"
echo "3. Start server: python start_server.py"
echo "4. Test system: python test_api_simple.py"
echo ""
echo "📖 See README.md for detailed instructions"