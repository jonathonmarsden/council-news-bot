#!/bin/bash

# Deployment Script for DigitalOcean Droplet
# Usage: ./scripts/deploy_to_vps.sh

HOST="vps.example.com"
USER="root"
TARGET_DIR="/opt/council-news-bot"

echo "=== Deploying to $USER@$HOST ==="
echo "You will be prompted for the password: TOWING.takeshi7staples9vault"

# 0. Ensure known_hosts
mkdir -p ~/.ssh
ssh-keyscan -H $HOST >> ~/.ssh/known_hosts 2>/dev/null

# 1. Create remote directory
echo "Creating remote directory..."
ssh $USER@$HOST "mkdir -p $TARGET_DIR"

# 2. Upload Files (including .env)
echo "Uploading project files..."
rsync -avz --progress \
    --exclude 'venv' \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.DS_Store' \
    --exclude 'data' \
    --exclude 'scheduler.log' \
    . $USER@$HOST:$TARGET_DIR

# 3. Execute Setup and Start
echo "Running remote setup and starting Docker..."
ssh $USER@$HOST "cd $TARGET_DIR && bash scripts/setup_vps.sh && docker compose down && docker compose up -d --build"

echo "=== Deployment Complete ==="
echo "Check status with: ssh $USER@$HOST 'cd $TARGET_DIR && docker compose logs -f --tail=50'"
