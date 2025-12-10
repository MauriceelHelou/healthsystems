# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files (when rootDirectory is 'frontend', paths are relative to frontend/)
COPY package*.json ./

# Install dependencies (--legacy-peer-deps needed for react-scripts 5.0.1 + TypeScript 5 compatibility)
RUN npm ci --legacy-peer-deps

# Copy source code
COPY . .

# Build argument for API URL (can be overridden at build time)
ARG REACT_APP_API_URL=https://backend-production-b6c2.up.railway.app
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Build the app (DISABLE_ESLINT_PLUGIN disables ESLint during build)
RUN DISABLE_ESLINT_PLUGIN=true npm run build

# Production stage - serve with Node.js 'serve' package
FROM node:20-alpine

WORKDIR /app

# Install serve globally
RUN npm install -g serve

# Copy built assets from build stage
COPY --from=build /app/build ./build

# Railway requires listening on PORT env var (default 3000)
ENV PORT=3000

# Expose port
EXPOSE ${PORT}

# Serve the build folder with SPA fallback (-s flag)
# Use -p for port (newer serve syntax)
CMD ["sh", "-c", "serve -s build -p $PORT"]
