# ================================
# Stage 1: Build Frontend
# ================================
FROM node:18-alpine AS frontend-builder

WORKDIR /frontend

# Copy frontend package files
COPY frontend/package.json frontend/package-lock.json* ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build frontend (output to /frontend/dist)
RUN npm run build

# ================================
# Stage 2: Python Backend + Serve Frontend
# ================================
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY attention_surgery/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn fastapi python-multipart

# Copy Backend Code
COPY attention_surgery/ ./attention_surgery/

# Copy built frontend from Stage 1
COPY --from=frontend-builder /frontend/dist ./frontend/dist

# Set Python Path
ENV PYTHONPATH=/app

# Create cache directory for Hugging Face models with correct permissions
RUN mkdir -p /app/cache && chmod 777 /app/cache
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HOME=/app/cache

# Expose port (Render uses PORT env variable)
EXPOSE 7860
ENV PORT=7860

# Run command - Use shell form to allow environment variable substitution
CMD uvicorn attention_surgery.api:app --host 0.0.0.0 --port ${PORT}
