# Stage 1: Build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Final Production Image
FROM nginx:stable-alpine
WORKDIR /usr/share/nginx/html

# 1. Install curl for the HEALTHCHECK (Required for fe_healthcheck)
RUN apk add --no-cache curl

# 2. Support non-root on port 8080 
# (Required for fe_named_nonroot_user and fe_user_creation_cmd)
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /etc/nginx/conf.d

# 3. Update Nginx to listen on 8080 instead of 80 (since 80 is root-only)
RUN sed -i 's/listen\(.*\)80;/listen 8080;/' /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist .

# 4. Use the built-in 'nginx' user
USER nginx

# 5. Updated Healthcheck to use port 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ || exit 1

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]