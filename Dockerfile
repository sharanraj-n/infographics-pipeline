# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for matplotlib, pdfkit, and other tools
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY infographic_pipeline/ ./infographic_pipeline/
COPY static/ ./static/
COPY .env ./

# Create output directory for generated files
RUN mkdir -p generated

# Expose FastAPI port
EXPOSE 8000

# Set environment variables (can be overridden at runtime)
ENV GOOGLE_GENAI_API_KEY=""
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000')"

# Run FastAPI with uvicorn
CMD ["uvicorn", "infographic_pipeline.webapi:app", "--host", "0.0.0.0", "--port", "8000"]
