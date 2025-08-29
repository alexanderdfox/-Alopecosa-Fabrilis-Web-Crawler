# 🚀 Cloudflare Deployment Guide

This guide will walk you through deploying your Alopecosa Fabrilis Web Crawler to Cloudflare Workers.

## 🎯 Overview

Your web crawler will be deployed as a Cloudflare Worker, providing:
- **Global CDN**: Fast access from anywhere in the world
- **Serverless**: No server management required
- **Scalability**: Automatically handles traffic spikes
- **Cost-effective**: Pay only for what you use

## 📋 Prerequisites

1. **Cloudflare Account**: [Sign up here](https://cloudflare.com)
2. **Node.js**: Version 18 or higher
3. **Git**: For version control
4. **Python 3.11+**: For local development

## 🛠️ Installation Steps

### Step 1: Install Wrangler CLI

```bash
npm install -g wrangler
```

### Step 2: Login to Cloudflare

```bash
wrangler login
```

This will open your browser to authenticate with Cloudflare.

### Step 3: Verify Installation

```bash
wrangler whoami
```

You should see your Cloudflare account information.

## 🚀 Quick Deployment

### Option A: Use the Deployment Script (Recommended)

```bash
# Deploy to default environment
./deploy_to_cloudflare.sh

# Deploy to staging
./deploy_to_cloudflare.sh staging

# Deploy to production
./deploy_to_cloudflare.sh production
```

### Option B: Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Deploy to Cloudflare
wrangler deploy

# Deploy to specific environment
wrangler deploy --env production
wrangler deploy --env staging
```

## ⚙️ Configuration

### Environment Variables

Set these in your Cloudflare dashboard or `wrangler.toml`:

```toml
[env.production.vars]
ENVIRONMENT = "production"
DATABASE_URL = "your-database-url"
SECRET_KEY = "your-secret-key"

[env.staging.vars]
ENVIRONMENT = "staging"
DATABASE_URL = "your-staging-database-url"
SECRET_KEY = "your-staging-secret-key"
```

### Custom Domains

1. Go to your Cloudflare dashboard
2. Navigate to Workers & Pages
3. Select your worker
4. Go to Settings > Triggers
5. Add your custom domain

## 🌐 Accessing Your Deployed App

After deployment, your crawler will be available at:

- **Default**: `https://alopecosa-crawler.your-subdomain.workers.dev`
- **Staging**: `https://alopecosa-crawler-staging.your-subdomain.workers.dev`
- **Production**: `https://alopecosa-crawler-prod.your-subdomain.workers.dev`

## 🔧 Local Development

### Test Locally

```bash
# Start local development server
wrangler dev

# Test with specific environment
wrangler dev --env staging
```

### Environment Variables for Local Development

Create a `.dev.vars` file:

```bash
# .dev.vars
ENVIRONMENT=development
DATABASE_URL=sqlite:///data/crawler_database.db
SECRET_KEY=local-development-key
```

## 📊 Monitoring & Analytics

### Cloudflare Analytics

1. **Workers Analytics**: Monitor request counts, errors, and performance
2. **Real User Monitoring**: Track actual user experience
3. **Web Analytics**: Comprehensive website analytics

### Logs

```bash
# View real-time logs
wrangler tail

# View logs for specific environment
wrangler tail --env production
```

## 🗄️ Database Considerations

### Current Setup (SQLite)

Your current SQLite database won't work on Cloudflare Workers. Consider:

1. **Cloudflare D1** (SQLite-compatible)
2. **PostgreSQL** (PlanetScale, Supabase)
3. **MongoDB Atlas**

### Migration to Cloudflare D1

```bash
# Create D1 database
wrangler d1 create alopecosa-crawler-db

# Run migrations
wrangler d1 execute alopecosa-crawler-db --file=./migrations/001_initial.sql
```

## 🔒 Security & Performance

### Security Headers

Your worker automatically includes:
- CORS headers
- Content-Type validation
- Input sanitization

### Performance Optimization

- **Edge Caching**: Automatic caching at Cloudflare's edge
- **Minification**: Automatic JavaScript/CSS optimization
- **Image Optimization**: Automatic image compression

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are in `requirements.txt`
2. **Database Connection**: Check database URL and credentials
3. **CORS Issues**: Verify CORS configuration in your worker
4. **Environment Variables**: Ensure all required vars are set

### Debug Commands

```bash
# Check worker status
wrangler whoami

# View worker details
wrangler secret list

# Test worker locally
wrangler dev

# View deployment logs
wrangler tail
```

### Getting Help

- **Cloudflare Docs**: [workers.cloudflare.com](https://workers.cloudflare.com)
- **Community**: [community.cloudflare.com](https://community.cloudflare.com)
- **GitHub Issues**: Report bugs in your repository

## 📈 Scaling & Optimization

### Auto-scaling

Cloudflare Workers automatically scale based on demand.

### Performance Tips

1. **Minimize Dependencies**: Only include necessary packages
2. **Optimize Code**: Use efficient algorithms and data structures
3. **Cache Strategically**: Implement appropriate caching strategies
4. **Monitor Metrics**: Use Cloudflare Analytics to identify bottlenecks

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloudflare
on:
  push:
    branches: [main, staging]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          environment: ${{ github.ref_name == 'main' && 'production' || 'staging' }}
```

## 🎉 Success!

Your Alopecosa Fabrilis Web Crawler is now running on Cloudflare's global network!

### Next Steps

1. **Test Your Deployment**: Visit your worker URL
2. **Configure Custom Domain**: Set up your preferred domain
3. **Monitor Performance**: Check Cloudflare Analytics
4. **Set Up Alerts**: Configure error notifications
5. **Optimize**: Monitor and improve performance

### Support

If you need help:
- Check the troubleshooting section above
- Review Cloudflare documentation
- Ask in the Cloudflare community
- Create an issue in your repository

---

**🕷️ Happy crawling with your Cloudflare-powered spider!** ✨
