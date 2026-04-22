# --- Stage 1: Build ---
FROM node:20-alpine AS build
WORKDIR /app
# Only copy dependency files first to leverage caching
COPY package*.json ./
RUN npm ci
# Copy source and build
COPY . .
RUN npm run build

# --- Stage 2: Serve ---
FROM nginx:stable-alpine

# 1. Create a non-root user/group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 2. Permissions setup (cleaner approach)
RUN touch /var/run/nginx.pid && \
    chown -R appuser:appgroup /var/run/nginx.pid /var/cache/nginx /var/log/nginx /etc/nginx/conf.d

# 3. Change Nginx to listen on 8080 (non-root requirement)
RUN sed -i 's/listen       80;/listen       8080;/' /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html

# 4. Copy ONLY the production build assets
# This ensures a clean multi-stage separation
COPY --from=build --chown=appuser:appgroup /app/dist .

# 5. Security & Execution
USER appuser
EXPOSE 8080

# 6. Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
