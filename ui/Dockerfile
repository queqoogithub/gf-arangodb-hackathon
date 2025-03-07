FROM node:23-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
# RUN npm ci
RUN npm install --legacy-peer-deps

# Copy the rest of the application
COPY . .

# Build the project (for Vite)
RUN npm run build
# RUN npm run preview

# Install 'serve' globally to serve the build
RUN npm install -g serve

# Expose the necessary port (Cloud Run automatically assigns a port)
EXPOSE 8080

# Set the production environment
ENV NODE_ENV=production
ENV PORT=8080
# EXPOSE 8080

CMD ["npm", "run", "dev", "--", "--port", "8080", "--host"]
 