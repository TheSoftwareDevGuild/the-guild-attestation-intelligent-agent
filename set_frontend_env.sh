#!/bin/bash

# Script to set environment variables for the frontend Heroku app
# This script reads the frontend/.env file and sets the variables on the frontend app

APP_NAME="attestation-frontend-ui"
ENV_FILE="frontend/.env"
BACKEND_URL="https://attestation-backend-api-96a737e9a34c.herokuapp.com"

echo "Setting environment variables for frontend app: $APP_NAME"

# Check if frontend/.env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ $ENV_FILE file not found!"
    echo "Please create a $ENV_FILE file with your environment variables first."
    echo "You can copy from frontend/env.example"
    exit 1
fi

echo "✅ Found $ENV_FILE file"

# Set the backend URL for the frontend
echo "Setting API_URL to backend URL..."
heroku config:set --app $APP_NAME "API_URL=$BACKEND_URL"

# Read frontend/.env file and set relevant variables for frontend
while IFS= read -r line || [ -n "$line" ]; do
    # Skip empty lines and comments
    if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then
        continue
    fi
    
    # Extract key and value
    if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]}"
        
        # Remove quotes if present
        value=$(echo "$value" | sed 's/^"//;s/"$//')
        
        # Skip if value is empty
        if [ -z "$value" ]; then
            echo "⚠️  Skipping $key (empty value)"
            continue
        fi
        
        # Only set frontend-relevant variables
        if [[ "$key" == "API_URL" ]]; then
            echo "Setting $key on frontend..."
            heroku config:set --app $APP_NAME "$key=$value"
        else
            echo "⏭️  Skipping $key (not needed for frontend)"
        fi
    fi
done < "$ENV_FILE"

echo "✅ All environment variables have been set on frontend app: $APP_NAME"
echo "You can verify with: heroku config --app $APP_NAME"
