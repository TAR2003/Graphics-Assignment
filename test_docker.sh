#!/bin/bash

echo "🧪 Testing Docker setup for Motion Blur Project"
echo "==============================================="

# Test if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found!"
    exit 1
fi

echo "✅ docker-compose found"

# Test if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon not running!"
    exit 1
fi

echo "✅ Docker daemon is running"

# Test building the project
echo ""
echo "🔨 Building the project..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful!"
else
    echo "❌ Docker build failed!"
    exit 1
fi

# Test running the project
echo ""
echo "🚀 Running the project..."
docker-compose up --remove-orphans

if [ $? -eq 0 ]; then
    echo "✅ Docker run successful!"
else
    echo "❌ Docker run failed!"
    exit 1
fi

echo ""
echo "🎯 All tests passed! Your Docker setup is working correctly."
