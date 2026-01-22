# Deploying Council Bot to DigitalOcean

This guide explains how to deploy the Council News Bot to a DigitalOcean Droplet (or any Ubuntu VPS) using Docker.

## Prerequisites

1.  **DigitalOcean Account**: Create a Droplet (Basic, Regular Intel, $6/mo is sufficient).
2.  **SSH Access**: Ensure you can `ssh root@your-ip`.
3.  **Project Files**: You have this repository on your local machine.

## Quick Deploy (Script)

We have created a helper script to automate the deployment.

1.  Run the deployment script:
    ```bash
    ./scripts/deploy_to_vps.sh
    ```
2.  When prompted for a password, enter: `TOWING.takeshi7staples9vault`

## Manual Deployment Steps

If the script fails, follow these manual steps.

## Step 1: Prepare the VPS

1.  SSH into your new Droplet:
    ```bash
    ssh root@<your-droplet-ip>
    ```

2.  Run the setup script (copy-paste this or upload the script):
    ```bash
    # You can copy the content of scripts/setup_vps.sh and run it:
    nano setup.sh
    # Paste content...
    bash setup.sh
    ```

## Step 2: Upload Code

From your **local machine**, use `rsync` to copy the project files to the VPS.

```bash
# Run this from your project root folder on your Mac
rsync -avz --exclude 'venv' --exclude '.git' --exclude '__pycache__' \
    . root@<your-droplet-ip>:/opt/council-news-bot
```

## Step 3: Configure Environment

1.  SSH back into the VPS.
2.  Go to the project folder:
    ```bash
    cd /opt/council-news-bot
    ```
3.  Create/Edit the `.env` file:
    ```bash
    nano .env
    ```
4.  Paste your environment variables (BlueSky credentials, etc.):
    ```env
    # BlueSky Credentials
    BLUESKY_HANDLE_VIC=...
    BLUESKY_PASSWORD_VIC=...
    BLUESKY_HANDLE_NSW=...
    BLUESKY_PASSWORD_NSW=...
    BLUESKY_HANDLE_QLD=...
    BLUESKY_PASSWORD_QLD=...
    
    # Proxy (Optional)
    COUNCIL_BOT_PROXY=http://user:pass@host:port
    ```

## Step 4: Launch

Run the bot using Docker Compose:

```bash
docker compose up -d --build
```

## Step 5: Verify

Check if the bot is running:

```bash
docker compose ps
docker compose logs -f
```

## Maintenance

*   **Update Code**: Run the `rsync` command again, then `docker compose up -d --build`.
*   **View Logs**: `docker compose logs -f --tail=100`.
*   **Restart**: `docker compose restart`.
*   **Stop**: `docker compose down`.

## Data Persistence

*   The database is stored in `/opt/council-news-bot/data/bot.db`.
*   This file persists even if you destroy the container.
*   **Backup**: Periodically download this file to your local machine:
    ```bash
    scp root@<your-droplet-ip>:/opt/council-news-bot/data/bot.db ./backup_bot.db
    ```
