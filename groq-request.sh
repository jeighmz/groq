#!/bin/bash

# Make sure GROQ_API_KEY is set as an environment variable
if [ -z "$GROQ_API_KEY" ]; then
  echo "Error: GROQ_API_KEY environment variable is not set."
  exit 1
fi

# Perform the GET request using curl
curl -X GET "https://api.groq.com/openai/v1/models" \
     -H "Authorization: Bearer $GROQ_API_KEY" \
     -H "Content-Type: application/json"