# Water Reminder Bot 💧

A lightweight Python script that sends random water drinking reminders to a Discord channel via Webhooks.

## Features

- **Randomized Intervals**: Sends a reminder every 30 to 90 minutes.
- **Sleep Time Aware**: Automatically pauses reminders between 11:00 PM (23:00) and 09:00 AM.
- **Rich Embeds**: Sends aesthetically pleasing Discord embed messages instead of plain text.
- **Fast Package Management**: Built with [`uv`](https://github.com/astral-sh/uv) and Python 3.13 for blazing fast dependency management.
- **Containerized**: Fully compatible with Docker for easy background deployment.

## Prerequisites

- Python 3.13 / `uv`
- Docker (optional, if you want to run it containerized)
- A Discord Webhook URL

## Setup

1. **Clone or Navigate to the Directory**:
   ```bash
   cd water-reminder
   ```

2. **Configure Environment Variables**:
   Copy the sample environment file to `.env`:
   ```bash
   cp .env.sample .env
   # Depending on OS, use `copy .env.sample .env` on Windows CMD
   ```
   Open `.env` and fill in your Discord Webhook:
   ```env
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
   ```

## Running Locally

Run the bot directly using `uv`:

```bash
uv run src/water_reminder.py
```

## Running with Docker

```bash
docker compose up -d
```