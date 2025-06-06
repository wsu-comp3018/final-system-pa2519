# Build Stage
FROM node:20 as build-stage

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

# Generate static site
RUN npm run generate

# Production Stage - use nginx to serve static files
FROM nginx:alpine

# Remove default nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy generated static site to nginx public folder
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]