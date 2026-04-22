FROM python:3.12-alpine AS builder

WORKDIR /build

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

ENV PATH="/home/appuser/.local/bin:$PATH"

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD ps aux | grep "[p]ython" || exit 1

CMD ["python", "worker.py"]