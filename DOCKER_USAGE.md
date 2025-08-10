# Docker Setup Guide

## Fixed Issues

✅ **Dockerfile cleaned up**: Removed embedded scripts and simplified structure
✅ **docker-compose.yml optimized**: Fixed volume mapping and environment variables  
✅ **Build script separated**: Created `build_and_run.sh` as standalone script
✅ **Dependencies optimized**: Used `opencv-python-headless` for server environments
✅ **Added .dockerignore**: Excludes unnecessary files for faster builds

## Quick Start

### Method 1: Using docker-compose (Recommended)
```bash
# Build and run in one command
docker-compose up --build

# Or build first, then run
docker-compose build
docker-compose up
```

### Method 2: Using Docker directly
```bash
# Build the image
docker build -t motion-blur .

# Run the container
docker run -v $(pwd)/output:/app/output motion-blur
```

## What the Container Does

1. **LaTeX Processing**: Compiles `main.tex` to PDF presentation
2. **Python Demo**: Runs the motion blur demonstration script
3. **Output Generation**: Saves all results to the `output/` directory

## Output Files

After running, check the `output/` directory for:
- `Motion_Blur_Presentation.pdf` - LaTeX presentation
- `motion_blur_comparison_*.png` - Comparison images
- `velocity_buffer_visualization.png` - Velocity buffer visualization

## Troubleshooting

### Common Issues:
1. **Build fails**: Ensure Docker daemon is running
2. **Permission errors**: Check if Docker has access to the project directory
3. **LaTeX errors**: Check `latex_build.log` for compilation issues
4. **Python errors**: Ensure all Python dependencies are properly installed

### Testing the Setup:
Run the test script to verify everything works:
```bash
# On Windows PowerShell
.\test_docker.ps1

# On Linux/Mac or Git Bash
./test_docker.sh
```

## Performance Tips

- First build may take 10-15 minutes due to LaTeX installation
- Subsequent builds are faster thanks to Docker layer caching
- Use `.dockerignore` to exclude unnecessary files
- Consider using multi-stage builds for production

## Environment Variables

- `PYTHONUNBUFFERED=1`: Ensures Python output is displayed in real-time
- `DEBIAN_FRONTEND=noninteractive`: Prevents interactive prompts during build
- `TZ=UTC`: Sets timezone to avoid timezone-related issues
