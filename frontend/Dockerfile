# --- Stage 1: Build ---
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# --- Stage 2: Serve ---
FROM nginx:stable-alpine

# 1. Create a non-root user/group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 2. Set up permissions for Nginx to run as non-root
# We need to give the user access to cache, pids, and logs
RUN chown -R appuser:appgroup /usr/share/nginx/html && \
    chown -R appuser:appgroup /var/cache/nginx && \
    chown -R appuser:appgroup /var/log/nginx && \
    chown -R appuser:appgroup /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown -R appuser:appgroup /var/run/nginx.pid

# 3. Change Nginx to listen on a higher port (>1024)
RUN sed -i 's/listen       80;/listen       8080;/' /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html

# 4. Copy build files with correct ownership
COPY --from=build --chown=appuser:appgroup /app/dist .

# 5. Switch to non-root user
USER appuser

# 6. Expose the new port
EXPOSE 8080

# 7. Healthcheck (checks if the server is responding on 8080)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
