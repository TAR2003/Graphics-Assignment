# Test Docker setup for Motion Blur Project

Write-Host "🧪 Testing Docker setup for Motion Blur Project" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Test if docker-compose is available
try {
    docker-compose --version | Out-Null
    Write-Host "✅ docker-compose found" -ForegroundColor Green
} catch {
    Write-Host "❌ docker-compose not found!" -ForegroundColor Red
    exit 1
}

# Test if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker daemon not running!" -ForegroundColor Red
    exit 1
}

# Test building the project
Write-Host ""
Write-Host "🔨 Building the project..." -ForegroundColor Yellow
try {
    docker-compose build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker build successful!" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker build failed!" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Docker build failed with exception!" -ForegroundColor Red
    exit 1
}

# Test running the project
Write-Host ""
Write-Host "🚀 Running the project..." -ForegroundColor Yellow
try {
    docker-compose up --remove-orphans
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker run successful!" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker run failed!" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Docker run failed with exception!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 All tests passed! Your Docker setup is working correctly." -ForegroundColor Green
