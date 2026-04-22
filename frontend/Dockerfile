# ---------- Build ----------
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# ---------- Production ----------
FROM nginx:stable-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=build /app/dist /usr/share/nginx/html

# HEALTHCHECK
HEALTHCHECK CMD wget -qO- http://localhost || exit 1

USER appuser

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]