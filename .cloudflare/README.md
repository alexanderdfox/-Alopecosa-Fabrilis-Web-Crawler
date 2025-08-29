# Cloudflare Deployment Guide

This guide explains how to deploy the Alopecosa Fabrilis Web Crawler to Cloudflare.

## Prerequisites

1. **Cloudflare Account**: Sign up at [cloudflare.com](https://cloudflare.com)
2. **Wrangler CLI**: Install Cloudflare's command-line tool
3. **Python 3.11+**: Ensure you have Python 3.11 or higher installed

## Installation Steps

### 1. Install Wrangler CLI

```bash
npm install -g wrangler
```

### 2. Login to Cloudflare

```bash
wrangler login
```

### 3. Configure Your Project

Edit `wrangler.toml` to set your project name and settings.

### 4. Deploy to Cloudflare

```bash
# Deploy to staging
npm run deploy:staging

# Deploy to production
npm run deploy:production
```

## Alternative: Cloudflare Pages

If you prefer Cloudflare Pages (easier for static sites):

1. Connect your GitHub repository to Cloudflare Pages
2. Set build command: `pip install -r requirements.txt`
3. Set build output directory: `src/`
4. Deploy automatically on git push

## Environment Variables

Set these in your Cloudflare dashboard:

- `DATABASE_URL`: Your database connection string
- `SECRET_KEY`: Flask secret key
- `CRAWLER_MAX_WORKERS`: Maximum concurrent crawlers

## Database Considerations

- **SQLite**: Not recommended for production on Cloudflare
- **PostgreSQL**: Use Cloudflare D1 or external provider
- **MySQL**: Use external provider like PlanetScale

## Monitoring

- Use Cloudflare Analytics to monitor traffic
- Set up alerts for errors and performance issues
- Monitor crawler performance and database usage

## Troubleshooting

- Check Cloudflare Workers logs in dashboard
- Verify Python compatibility
- Ensure all dependencies are in requirements.txt
