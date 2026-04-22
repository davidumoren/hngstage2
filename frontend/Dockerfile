# Stage 1: builder
FROM node:20-slim AS builder

WORKDIR /build

COPY package.json package-lock.json* ./
RUN npm ci --omit=dev

# Stage 2: final
FROM node:20-slim

RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/sh --create-home appuser

WORKDIR /app

COPY --from=builder /build/node_modules ./node_modules
COPY app.js package.json ./
COPY views ./views

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1); }).on('error', () => process.exit(1));"

CMD ["node", "app.js"]