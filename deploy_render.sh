#!/bin/bash

# This script deploys to Render via Render's GitHub integration or CLI

echo "Deploying to Render..."

# Trigger the deployment by pushing to the Render-connected GitHub repository
# Since Render is integrated with GitHub, pushing to the main branch should trigger an automatic deployment
##
git push render main  # Push to Render (ensure your GitHub repository is connected to Render)
