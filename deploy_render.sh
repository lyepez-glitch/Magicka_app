#!/bin/bash
echo "Starting deployment to Render..."

# Ensure Daphne starts the ASGI application
daphne -b 0.0.0.0 -p 8000 your_project.asgi:application
