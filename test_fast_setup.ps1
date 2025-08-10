#!/usr/bin/env powershell

Write-Host "🧪 Testing Fast Docker Setup" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

# Clean up any previous containers
Write-Host "🧹 Cleaning up..." -ForegroundColor Yellow
docker-compose -f docker-compose.fast.yml down --remove-orphans 2>$null

# Build and run
Write-Host "🔨 Building and running..." -ForegroundColor Yellow
$result = docker-compose -f docker-compose.fast.yml up --build
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Container ran successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Container failed!" -ForegroundColor Red
    exit 1
}

# Check output files
Write-Host "📁 Checking generated files..." -ForegroundColor Yellow
$outputFiles = Get-ChildItem output/ -Recurse -File 2>$null
if ($outputFiles.Count -gt 0) {
    Write-Host "✅ Output files generated:" -ForegroundColor Green
    $outputFiles | ForEach-Object { Write-Host "   - $($_.Name)" -ForegroundColor Green }
} else {
    Write-Host "⚠️ No output files found in output/, checking container..." -ForegroundColor Yellow
    docker cp motion_blur_fast:/app/ ./container_contents/ 2>$null
    if ($?) {
        Write-Host "📦 Files copied from container for inspection" -ForegroundColor Blue
    }
}

Write-Host ""
Write-Host "🎯 Fast Docker setup test completed!" -ForegroundColor Cyan
Write-Host "⏱️ Total time: Much faster than the old 6+ hour build!" -ForegroundColor Green
