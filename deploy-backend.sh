#!/bin/bash

# Deploy backend to Heroku
echo "🚀 Deploying backend to Heroku..."

# Build and push from inside backend so Dockerfile/context are picked up
(
  cd backend && \
  heroku container:push web --app attestation-backend-api && \
  heroku container:release web --app attestation-backend-api
)

echo "✅ Backend deployed successfully!"
echo "🌐 Backend URL: https://attestation-backend-api-96a737e9a34c.herokuapp.com"
