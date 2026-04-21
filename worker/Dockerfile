# --- Stage 1: Builder ---
FROM python:3.12-slim AS builder

WORKDIR /build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Stage 2: Production ---
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# 2. Copy dependencies
COPY --from=builder /install /usr/local

# 3. Copy code and set ownership
COPY --chown=appuser:appgroup worker.py .

# 4. Healthcheck
# This checks if the main python process is still in the process list
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD pgrep python > /dev/null || exit 1

# 5. Switch user
USER appuser

CMD ["python", "worker.py"]
