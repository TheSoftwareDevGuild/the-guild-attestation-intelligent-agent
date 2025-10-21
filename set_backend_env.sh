#!/bin/bash

# Script to set environment variables for the backend Heroku app
# This script reads your .env file and sets the variables on the backend app

APP_NAME="attestation-backend-api"

echo "Setting environment variables for backend app: $APP_NAME"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your environment variables first."
    exit 1
fi

echo "✅ Found .env file"

# Read .env file and set Heroku config variables for backend
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
done < .env

echo "✅ All environment variables have been set on backend app: $APP_NAME"
echo "You can verify with: heroku config --app $APP_NAME"
