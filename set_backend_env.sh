#!/bin/bash

# Script to set environment variables for the backend Heroku app
# This script reads the backend/.env file and sets the variables on the backend app

APP_NAME="attestation-backend-api"
ENV_FILE="backend/.env"

echo "Setting environment variables for backend app: $APP_NAME"

# Check if backend/.env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ $ENV_FILE file not found!"
    echo "Please create a $ENV_FILE file with your environment variables first."
    echo "You can copy from backend/env.example"
    exit 1
fi

echo "✅ Found $ENV_FILE file"

# Read backend/.env file and set Heroku config variables for backend
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
        
        echo "Setting $key on backend..."
        heroku config:set --app $APP_NAME "$key=$value"
    fi
done < "$ENV_FILE"

echo "✅ All environment variables have been set on backend app: $APP_NAME"
echo "You can verify with: heroku config --app $APP_NAME"
