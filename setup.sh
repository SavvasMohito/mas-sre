#!/bin/bash
#
# Setup script for Security Requirements System
#

set -e

echo "=================================================="
echo "Security Requirements System - Setup"
echo "=================================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp env.template .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo ""
    read -p "Press Enter to continue after editing .env, or Ctrl+C to exit..."
else
    echo "✅ .env file exists"
fi

# Check for OPENAI_API_KEY
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Warning: OPENAI_API_KEY may not be set in .env"
fi

echo ""
echo "Step 1: Installing dependencies..."
if command -v pnpm &> /dev/null; then
    echo "Using pnpm..."
    pnpm install
elif command -v crewai &> /dev/null; then
    echo "Using CrewAI CLI..."
    crewai install
else
    echo "Using pip..."
    pip install -e .
fi

echo ""
echo "Step 2: Starting Weaviate database..."
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

docker-compose up -d

echo "Waiting for Weaviate to initialize (30 seconds)..."
sleep 30

echo ""
echo "Step 3: Preparing security standards data..."
python -m security_requirements_system.data.prepare_owasp_asvs
python -m security_requirements_system.data.prepare_nist
python -m security_requirements_system.data.prepare_iso27001

echo ""
echo "Step 4: Ingesting data into Weaviate..."
python -m security_requirements_system.tools.weaviate_setup

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Review sample inputs in inputs/ directory"
echo "  2. Run the system:"
echo "     crewai run"
echo "     or"
echo "     INPUT_FILE=inputs/sample_ecommerce.txt crewai run"
echo ""
echo "  3. Check outputs in outputs/ directory"
echo ""
echo "For more information, see README.md"
echo ""

