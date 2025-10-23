FROM python:3.12-slim

WORKDIR /app

# Enable bytecode compilation and Python optimization
ENV UV_COMPILE_BYTECODE=1
ENV PYTHONOPTIMIZE=1
ENV UV_LINK_MODE=copy

# Set Python path and memory optimization environment variables
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV MALLOC_TRIM_THRESHOLD_=131072
ENV MALLOC_MMAP_THRESHOLD_=131072
ENV WEB_CONCURRENCY=1

# Copy requirements first for better caching
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy source code
COPY src ./src/

# Pre-compile Python files to bytecode
RUN python -m compileall ./src

# Create non-root user
RUN addgroup --system app && \
    adduser --system --ingroup app app && \
    chown -R app:app /app

USER app

# Expose port (Heroku will set PORT env var)
EXPOSE $PORT

# Run with gunicorn using Heroku's PORT environment variable
CMD gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:$PORT --timeout 60 --graceful-timeout 30 --max-requests 100 --max-requests-jitter 10 --worker-tmp-dir /dev/shm src.app:app