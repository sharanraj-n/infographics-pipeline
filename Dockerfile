# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY infographic_pipeline/ ./infographic_pipeline/
COPY requirements.txt ./
COPY run_pipeline.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Google API key
ENV GOOGLE_API_KEY=""

# Default command
CMD ["python", "run_pipeline.py"]
