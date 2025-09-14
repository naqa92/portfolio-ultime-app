
# Use a specific version and multi-stage build for better security
FROM python:3.13-slim AS builder

WORKDIR /app

# Copy requirements first for better layer caching
COPY app/requirements.txt ./

# Install dependencies in a temporary location
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl=8.14.1-2 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY app/app.py ./
COPY app/templates/ ./templates/

# Change ownership of the app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 5000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]