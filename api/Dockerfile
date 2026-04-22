# ---------- Stage 1: Builder ----------
FROM python:3.12-alpine AS builder

WORKDIR /build

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---------- Stage 2: Runtime ----------
FROM python:3.12-alpine

WORKDIR /app

# Create non-root user (REQUIRED)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

ENV PATH="/home/appuser/.local/bin:$PATH"

# Copy dependencies
COPY --from=builder /root/.local /home/appuser/.local

# Copy app
COPY . .

# Change ownership
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

# HEALTHCHECK (REQUIRED)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]