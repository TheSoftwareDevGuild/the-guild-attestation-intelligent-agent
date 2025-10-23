#!/bin/bash

# Deploy frontend to Heroku
echo "🚀 Deploying frontend to Heroku..."

# Build and push from inside frontend so Dockerfile/context are picked up
(
  cd frontend && \
  heroku container:push web --app attestation-frontend-ui && \
  heroku container:release web --app attestation-frontend-ui
)

echo "✅ Frontend deployed successfully!"
echo "🌐 Frontend URL: https://attestation-frontend-ui-b7cce92d51fd.herokuapp.com"
