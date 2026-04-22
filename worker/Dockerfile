# Stage 1: builder
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: final
FROM python:3.11-slim

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/sh --create-home appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY worker.py .

RUN chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import redis, os; r = redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=int(os.getenv('REDIS_PORT',6379)), password=os.getenv('REDIS_PASSWORD',None)); r.ping()" || exit 1

CMD ["python", "worker.py"]