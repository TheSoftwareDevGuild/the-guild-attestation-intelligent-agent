#!/bin/bash

# Script to set environment variables for the frontend Heroku app
# This script reads your .env file and sets the variables on the frontend app

APP_NAME="attestation-frontend-ui"
BACKEND_URL="https://attestation-backend-api-96a737e9a34c.herokuapp.com"

echo "Setting environment variables for frontend app: $APP_NAME"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your environment variables first."
    exit 1
fi

echo "✅ Found .env file"

# Set the backend URL for the frontend
echo "Setting API_URL to backend URL..."
heroku config:set --app $APP_NAME "API_URL=$BACKEND_URL"

# Read .env file and set relevant variables for frontend
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
        if [[ "$key" == "OPENAI_API_KEY" || "$key" == "GROQ_API_KEY" || "$key" == "GOOGLE_API_KEY" ]]; then
            echo "Setting $key on frontend..."
            heroku config:set --app $APP_NAME "$key=$value"
        else
            echo "⏭️  Skipping $key (not needed for frontend)"
        fi
    fi
done < .env

echo "✅ All environment variables have been set on frontend app: $APP_NAME"
echo "You can verify with: heroku config --app $APP_NAME"
