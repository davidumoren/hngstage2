# ---------- Stage 1: Builder ----------
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install dependencies into a prefix for clean copying
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------- Stage 2: Runtime ----------
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Create a non-root user and group for security
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# 2. Copy dependencies from builder
COPY --from=builder /install /usr/local

# 3. Copy application code and set ownership to appuser
# Use --chown to avoid needing a separate RUN chown command (saves a layer)
COPY --chown=appuser:appgroup . .

# 4. Expose FastAPI port
EXPOSE 8000

# 5. Add a HEALTHCHECK instruction
# Note: --interval=30s is standard; wget is used for slim images
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 6. Switch to the non-root user
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
