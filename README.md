# Playwright Scraper API

A lightweight REST API built with **FastAPI** and **Playwright** to render JavaScript-heavy websites and return their full HTML content. Designed to run on a VPS via Docker and integrate with automation workflows (n8n, Make, etc.).

## Why this exists

Standard HTTP requests only fetch the raw HTML — they don't execute JavaScript. Many modern websites render their content dynamically, making simple scrapers useless. This server spins up a real Chromium browser headlessly, waits for the page to fully load, and returns the rendered HTML.

## Stack

- **Python** + **FastAPI** — async REST API
- **Playwright** — headless Chromium browser
- **Docker** — containerized deployment
- **VPS (Hostinger)** — self-hosted, no timeout limits

## Architecture

```
n8n Workflow
    │
    │  POST /scrape  {"url": "https://example.com"}
    ▼
Playwright Scraper API  (port 8080)
    │
    │  Opens Chromium headlessly
    │  Loads the full page (JS rendered)
    │  Returns HTML
    ▼
n8n Code Node  →  Email extraction  →  Google Sheets
```

## Endpoint

### `POST /scrape`

**Request body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "html": "<!DOCTYPE html>..."
}
```

## Running locally

```bash
# Clone the repo
git clone https://github.com/henriquealencarr/playwright-scraper
cd playwright-scraper

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Deploying with Docker (VPS)

```bash
# Build the image
docker build -t playwright-scraper .

# Run the container
docker run -d \
  --network host \
  --restart always \
  --name playwright \
  playwright-scraper
```

The `--network host` flag is required so other Docker containers (e.g., n8n) can reach the API via the host gateway IP.

## Use case: Lead Generation Agent

This API is part of a larger **AI Lead Generation Agent** built with n8n:

1. **Google Maps Scraper** (Apify) — finds businesses by niche and location
2. **Supabase** — controls async polling state
3. **Playwright Scraper API** (this repo) — extracts emails from business websites
4. **Google Sheets** — stores enriched leads

The Playwright layer increased email extraction rate from ~3% (plain HTTP) to ~25% compared to simple fetch requests.

## Why self-hosted over managed services?

Services like Railway impose ~30s connection timeouts, which kills Playwright sessions mid-render. Running on a VPS removes that constraint entirely.

---

Built by [Henrique Alencar](https://github.com/henriquealencarr) — AI Automation Engineer
