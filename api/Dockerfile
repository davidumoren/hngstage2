# ---------- Stage 1: Builder ----------
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install build dependencies for Alpine
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# 1. Create a non-root user (Alpine syntax)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 2. Copy only the installed packages from builder
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local

# 3. Copy application code
COPY --chown=appuser:appgroup . .

# 4. Healthcheck (Alpine uses wget)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8000/health || exit 1

# 5. Security & Execution
USER appuser
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
