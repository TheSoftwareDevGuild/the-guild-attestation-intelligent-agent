#!/bin/bash

# Script to set Heroku environment variables from .env file
# This script reads your .env file and sets the variables on Heroku

echo "Reading environment variables from .env file..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your environment variables first."
    exit 1
fi

echo "✅ Found .env file"

# Read .env file and set Heroku config variables
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
        
        echo "Setting $key..."
        heroku config:set "$key=$value"
    fi
done < .env

echo "✅ All environment variables from .env have been set on Heroku!"
echo "You can verify with: heroku config"
