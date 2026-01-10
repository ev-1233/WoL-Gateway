# Use Python 3.13 slim image for smaller size
FROM python:3.13-slim

# Install system dependencies (wakeonlan)
RUN apt-get update && \
    apt-get install -y --no-install-recommends wakeonlan && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask

# Set working directory
WORKDIR /app

# Copy application files
COPY wol_gatway.py .
COPY WOL_Brige.config .

# Expose the port (will be configurable via config file)
EXPOSE 500

# Run as non-root user for security (but Docker will handle port mapping)
RUN useradd -m -u 1000 woluser && \
    chown -R woluser:woluser /app

USER woluser

# Start the application
CMD ["python3", "wol_gatway.py"]
