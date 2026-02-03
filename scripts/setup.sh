#!/bin/bash

# RetailSync Pro - Quick Setup Script
# This script sets up your local development environment

set -e  # Exit on any error

echo "🚀 RetailSync Pro - Development Environment Setup"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed. Please install Node.js 18+${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js $NODE_VERSION found${NC}"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}⚠️  PostgreSQL not found. Install it or use Docker.${NC}"
    read -p "Do you want to use Docker instead? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        USE_DOCKER=true
    else
        echo -e "${RED}Please install PostgreSQL and run this script again.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ PostgreSQL found${NC}"
    USE_DOCKER=false
fi

echo ""
echo "📦 Setting up Backend..."
echo "========================"

# Create Python virtual environment
if [ ! -d "backend/venv" ]; then
    echo "Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
    cd backend
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip --quiet

# Install requirements (will create when we build backend)
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found (will be created in Phase 1)${NC}"
fi

cd ..

echo ""
echo "🎨 Setting up Frontend..."
echo "========================="

if [ -d "frontend" ]; then
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing Node.js dependencies..."
        npm install --quiet
        echo -e "${GREEN}✅ Node.js dependencies installed${NC}"
    else
        echo -e "${YELLOW}node_modules already exists${NC}"
    fi
    
    cd ..
else
    echo -e "${YELLOW}⚠️  Frontend directory not found (will be created in Phase 1)${NC}"
fi

echo ""
echo "🗄️  Setting up Database..."
echo "=========================="

if [ "$USE_DOCKER" = true ]; then
    echo "Starting PostgreSQL with Docker..."
    docker-compose up -d db
    echo -e "${GREEN}✅ PostgreSQL running in Docker${NC}"
else
    # Check if database exists
    if psql -lqt | cut -d \| -f 1 | grep -qw retailsync_dev; then
        echo -e "${YELLOW}Database 'retailsync_dev' already exists${NC}"
    else
        echo "Creating database..."
        createdb retailsync_dev
        echo -e "${GREEN}✅ Database 'retailsync_dev' created${NC}"
    fi
fi

echo ""
echo "📝 Setting up Environment Variables..."
echo "======================================="

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ .env file created from .env.example${NC}"
        echo -e "${YELLOW}⚠️  Please update .env with your actual values${NC}"
    else
        echo -e "${YELLOW}⚠️  .env.example not found (will be created in Phase 1)${NC}"
    fi
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi

echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "Next steps:"
echo "1. Review your .env file and update any necessary values"
echo "2. Start the backend:"
echo -e "   ${GREEN}cd backend${NC}"
echo -e "   ${GREEN}source venv/bin/activate${NC}"
echo -e "   ${GREEN}python manage.py migrate${NC}"
echo -e "   ${GREEN}python manage.py createsuperuser${NC}"
echo -e "   ${GREEN}python manage.py runserver${NC}"
echo ""
echo "3. In a new terminal, start the frontend:"
echo -e "   ${GREEN}cd frontend${NC}"
echo -e "   ${GREEN}npm start${NC}"
echo ""
echo "4. Access the application:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000/api"
echo "   - Django Admin: http://localhost:8000/admin"
echo ""
echo "📚 For more help, see:"
echo "   - README.md"
echo "   - docs/architecture/phase-1-roadmap.md"
echo "   - docs/deployment/local-setup.md"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
