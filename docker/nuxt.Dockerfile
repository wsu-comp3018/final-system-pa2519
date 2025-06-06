FROM node:20 as build-stage

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

RUN npm run build

# Production image
FROM node:20-slim

WORKDIR /app

COPY --from=build-stage /app/.output .output
COPY --from=build-stage /app/package.json package.json
RUN npm install --only=production

EXPOSE 3000

# Start the production Nuxt app
CMD ["node", ".output/server/index.mjs"]