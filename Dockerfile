# Fast Motion Blur Project Dockerfile
FROM python:3.10-slim

# Avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC
ENV PYTHONUNBUFFERED=1

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-pictures \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3 as default (already available in python:3.10-slim)

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip

# Install minimal Python packages for motion blur demo
RUN pip install --no-cache-dir \
    numpy \
    opencv-python-headless \
    matplotlib \
    pillow

# Set working directory
WORKDIR /app

# Create output directory
RUN mkdir -p /app/output

# Copy project files
COPY . .

# Make the build script executable
RUN chmod +x build_and_run.sh

# Set the default command to run the build script
CMD ["./build_and_run.sh"]

# Expose volume for output
VOLUME ["/app/output"]
