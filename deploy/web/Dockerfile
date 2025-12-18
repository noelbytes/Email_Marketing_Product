FROM node:22 AS build

WORKDIR /app/frontend

COPY frontend/package*.json ./
COPY frontend/tsconfig*.json ./
COPY frontend/vite.config.ts ./
COPY frontend/postcss.config.cjs ./
COPY frontend/tailwind.config.cjs ./
COPY frontend/src ./src
COPY frontend/public ./public

RUN npm ci && npm run build-only

FROM nginx:1.27-alpine
COPY --from=build /app/frontend/dist /usr/share/nginx/html
COPY deploy/nginx/nginx.conf /etc/nginx/conf.d/default.conf

