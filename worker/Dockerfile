# --- Stage 1: Builder ---
FROM python:3.12-alpine AS builder

WORKDIR /build

# Install build dependencies for Alpine
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

COPY requirements.txt .
# Install to the user directory
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Stage 2: Production ---
FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# 1. Create non-root user (Alpine syntax)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 2. Copy only the installed packages from builder
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local

# 3. Copy code and set ownership
COPY --chown=appuser:appgroup worker.py .

# 4. Healthcheck
# pgrep is not in base Alpine, so we use 'ps' to check for the python process
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD ps aux | grep "[p]ython" || exit 1

# 5. Switch user
USER appuser

CMD ["python", "worker.py"]
