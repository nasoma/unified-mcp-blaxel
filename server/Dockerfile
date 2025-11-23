# Start from a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /blaxel

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml uv.lock /blaxel/

# Install uv and dependencies
RUN pip install uv && uv sync --refresh

# Copy application code
COPY . .

# Set env variable to use the virtual environment
ENV PATH="/blaxel/.venv/bin:$PATH"

# Command to run when container starts
# Using the entrypoint defined in blaxel.toml
ENTRYPOINT [".venv/bin/python3", "src/server.py"]
