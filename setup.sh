#!/bin/bash

set -e

echo "🚀 Setting up AWS Automation Platform..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Start development services
echo "🐳 Starting development services (PostgreSQL, Redis)..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Run database migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run 'make run-server' to start the API server"
echo "3. Run 'make run-worker' in another terminal for Celery worker"
echo "4. Run 'make run-beat' in another terminal for Celery scheduler"
echo "5. In frontend directory: 'npm install && npm run dev'"
