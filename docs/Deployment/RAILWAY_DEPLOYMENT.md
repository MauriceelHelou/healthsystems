# Railway.app Deployment Guide

This guide walks you through deploying the HealthSystems Platform on Railway.app for a simple, cost-effective initial deployment.

## Why Railway?

- **Simple**: Docker-native deployment (no infrastructure code needed)
- **Cheap**: ~$50-150/month for initial MVP (vs $500-1000/month on AWS)
- **Fast**: Deploy in under 1 hour from start to finish
- **Managed**: PostgreSQL + Redis included and maintained
- **Scalable**: Easy migration to AWS when you outgrow Railway

---

## Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Railway Account**: Sign up at [railway.app](https://railway.app)
3. **Anthropic API Key**: For Claude API (literature synthesis)
4. **Domain Name** (optional): For custom domain instead of `*.railway.app`

---

## Cost Estimate

Railway uses pay-per-use pricing. Expected monthly costs for MVP:

| Service | Resource | Estimated Cost |
|---------|----------|----------------|
| Backend API | 1 GB RAM, 2 vCPU | $20-40 |
| Celery Worker | 2 GB RAM, 2 vCPU | $20-40 |
| Frontend | 512 MB RAM, 1 vCPU | $5-10 |
| PostgreSQL | 1 GB storage, backups | $10-20 |
| Redis | 256 MB RAM | $5-10 |
| **Total** | | **$60-120/month** |

> **Note**: Railway offers $5 in free credits monthly. First month may be partially free.

---

## Deployment Steps

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select your `healthsystems` repository

### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database" → "PostgreSQL"**
3. Railway will provision a managed PostgreSQL instance
4. Note: Connection details are automatically added as environment variables

### Step 3: Add Redis Cache

1. Click **"+ New"** again
2. Select **"Database" → "Redis"**
3. Railway will provision a managed Redis instance
4. Connection details auto-populate to environment variables

### Step 4: Deploy Backend Service

1. Click **"+ New" → "GitHub Repo"** (if not already added)
2. Select **"Add Service"**
3. Configure the backend service:
   - **Name**: `backend`
   - **Root Directory**: `/backend`
   - **Build Command**: (uses Dockerfile automatically)
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 4`

4. Add environment variables (see [Environment Variables](#environment-variables) section below)

5. Click **"Deploy"**

### Step 5: Deploy Celery Worker Service

1. Click **"+ New" → "GitHub Repo"**
2. Add another service from the same repository:
   - **Name**: `celery-worker`
   - **Root Directory**: `/backend`
   - **Start Command**: `celery -A api.tasks worker --loglevel=info --concurrency=4`

3. Add same environment variables as backend (Railway can share variables across services)

4. Click **"Deploy"**

### Step 6: Deploy Frontend Service

1. Click **"+ New" → "GitHub Repo"**
2. Add frontend service:
   - **Name**: `frontend`
   - **Root Directory**: `/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run preview -- --host 0.0.0.0 --port $PORT`

3. Add environment variables:
   ```
   VITE_API_BASE_URL=https://backend.railway.app/api/v1
   VITE_APP_NAME=HealthSystems Platform
   ```

4. Click **"Deploy"**

---

## Environment Variables

Railway automatically provides some variables (like `DATABASE_URL`, `REDIS_URL`). You need to add these manually:

### Required Variables (All Services)

```bash
# Security
SECRET_KEY=your-super-secret-key-min-32-chars-long-change-this

# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
CLAUDE_MODEL=claude-3-sonnet-20240229

# Environment
ENVIRONMENT=production
```

### Backend-Specific Variables

```bash
# CORS (use your frontend Railway URL)
ALLOWED_ORIGINS=https://frontend-production-xxxx.up.railway.app,http://localhost:3000

# API Configuration
API_V1_PREFIX=/api/v1
PROJECT_NAME=HealthSystems Platform

# Database (auto-provided by Railway, but can override)
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}

# Celery
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}

# External APIs (optional)
CENSUS_API_KEY=your-census-api-key-here

# Monitoring (optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Frontend-Specific Variables

```bash
# API URL (use your backend Railway URL)
VITE_API_BASE_URL=https://backend-production-xxxx.up.railway.app/api/v1
VITE_APP_NAME=HealthSystems Platform
```

---

## Configuring Environment Variables in Railway

### Option 1: Via Dashboard (Recommended for first deployment)

1. Select a service (e.g., `backend`)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add each variable from the list above
5. Click **"Deploy"** to restart with new variables

### Option 2: Via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Add variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set ANTHROPIC_API_KEY="sk-ant-your-key"

# Deploy
railway up
```

### Option 3: Shared Variables (for multiple services)

Railway allows sharing variables across services:

1. Go to project settings
2. Navigate to **"Shared Variables"**
3. Add common variables (like `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`)
4. Services automatically inherit these

---

## Database Initialization

After deploying PostgreSQL, you need to initialize the schema:

### Method 1: Via Railway CLI

```bash
# Connect to Railway PostgreSQL
railway connect postgres

# Run migration script (if using Alembic)
railway run alembic upgrade head
```

### Method 2: Via Backend Service

The backend should auto-migrate on startup if configured. Check backend logs:

```bash
railway logs backend
```

Look for migration messages.

---

## Verifying Deployment

### Check Service Health

1. **Backend**: Visit `https://backend-production-xxxx.up.railway.app/health`
   - Should return: `{"status": "healthy"}`

2. **Frontend**: Visit `https://frontend-production-xxxx.up.railway.app`
   - Should load the React application

3. **API Docs**: Visit `https://backend-production-xxxx.up.railway.app/docs`
   - Should show FastAPI Swagger documentation

### Check Logs

```bash
# Via CLI
railway logs backend
railway logs celery-worker
railway logs frontend

# Via Dashboard
# Select service → "Logs" tab
```

### Test Database Connection

```bash
# Connect to PostgreSQL
railway connect postgres

# Check tables
\dt

# Verify mechanism bank data
SELECT COUNT(*) FROM mechanisms;
```

---

## Custom Domain Setup

### Add Domain to Frontend

1. Go to frontend service settings
2. Click **"Settings" → "Domains"**
3. Click **"+ Add Domain"**
4. Enter your domain (e.g., `app.healthsystems.org`)
5. Add DNS records to your domain provider:
   ```
   Type: CNAME
   Name: app
   Value: frontend-production-xxxx.up.railway.app
   ```

### Add Domain to Backend

1. Go to backend service settings
2. Add domain (e.g., `api.healthsystems.org`)
3. Add DNS CNAME record pointing to backend Railway URL

### Update Environment Variables

After adding custom domains, update CORS and API URLs:

```bash
# Backend
ALLOWED_ORIGINS=https://app.healthsystems.org,http://localhost:3000

# Frontend
VITE_API_BASE_URL=https://api.healthsystems.org/api/v1
```

---

## Scaling & Performance

### Vertical Scaling (Increase Resources)

1. Select service
2. Go to **"Settings" → "Resources"**
3. Adjust:
   - **Memory**: 512 MB → 2 GB (for heavy MCMC jobs)
   - **CPU**: Shared → Dedicated
   - **Replicas**: 1 → 2+ (horizontal scaling)

### Horizontal Scaling (Multiple Instances)

Railway supports auto-scaling:

1. Go to service settings
2. Enable **"Horizontal Scaling"**
3. Set min/max replicas
4. Railway auto-scales based on CPU/memory usage

### Database Scaling

For PostgreSQL:

1. Go to PostgreSQL service
2. **"Settings" → "Resources"**
3. Increase storage: 1 GB → 10 GB → 100 GB
4. Enable **"High Availability"** for production

---

## Monitoring & Logging

### Built-in Railway Monitoring

Railway provides:
- CPU usage graphs
- Memory usage graphs
- Network traffic
- Request logs

Access via service dashboard → **"Metrics"** tab

### External Monitoring (Optional)

#### Add Sentry for Error Tracking

1. Create account at [sentry.io](https://sentry.io)
2. Create new project for backend/frontend
3. Add Sentry DSN to Railway environment variables:
   ```bash
   SENTRY_DSN=https://your-dsn@sentry.io/project-id
   SENTRY_ENVIRONMENT=production
   ```

#### Add Datadog/New Relic (Optional)

For advanced APM, add agent to Docker container and configure API keys.

---

## Backup & Disaster Recovery

### Database Backups

Railway automatically backs up PostgreSQL:
- **Frequency**: Daily
- **Retention**: 7 days (configurable)
- **Restore**: Via Railway dashboard or CLI

#### Manual Backup

```bash
# Via Railway CLI
railway run pg_dump $DATABASE_URL > backup.sql

# Restore
railway run psql $DATABASE_URL < backup.sql
```

### Code Backups

Your code is in GitHub - Railway deploys from main branch.

### Mechanism Bank Backups

The mechanism bank is git-tracked, so it's automatically backed up in GitHub.

---

## CI/CD Integration

Railway auto-deploys on every push to main branch.

### Customize Deployment Triggers

1. Go to service settings
2. **"Settings" → "Source"**
3. Configure:
   - **Branch**: `main` (or `production`)
   - **Auto-deploy**: Enable/disable
   - **Build command**: Custom build script
   - **Watch paths**: Only deploy when specific files change

### GitHub Actions Integration

You can add additional CI/CD steps before Railway deployment:

```yaml
# .github/workflows/railway-deploy.yml
name: Railway Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: backend
```

---

## Cost Optimization Tips

1. **Use Shared Variables**: Reduce duplication
2. **Sleep Inactive Services**: Railway can auto-sleep low-traffic services
3. **Optimize Docker Images**: Use multi-stage builds (already in place)
4. **Use Redis Caching**: Reduce database queries (already configured)
5. **Monitor Usage**: Set budget alerts in Railway dashboard
6. **Use Spot Instances**: For Celery workers (available in Railway Pro)

### Set Budget Alerts

1. Go to **"Project Settings"**
2. Click **"Usage"**
3. Set monthly budget limit (e.g., $150)
4. Railway will email you when approaching limit

---

## Troubleshooting

### Backend Won't Start

**Check logs:**
```bash
railway logs backend
```

**Common issues:**
- Missing environment variables (DATABASE_URL, SECRET_KEY)
- Database migration failed
- Port binding issue (ensure using `$PORT` variable)

**Fix:**
1. Verify all required environment variables are set
2. Run migrations manually: `railway run alembic upgrade head`
3. Check Dockerfile uses `CMD uvicorn --port $PORT`

### Frontend Can't Connect to Backend

**Check:**
1. `VITE_API_BASE_URL` points to correct backend URL
2. Backend CORS allows frontend origin
3. Backend is actually running (check logs)

**Fix:**
```bash
# Backend variable
ALLOWED_ORIGINS=https://frontend-production-xxxx.up.railway.app

# Frontend variable
VITE_API_BASE_URL=https://backend-production-xxxx.up.railway.app/api/v1
```

### Database Connection Errors

**Check:**
1. PostgreSQL service is running
2. `DATABASE_URL` is correctly set
3. Connection pool not exhausted

**Fix:**
```bash
# Restart PostgreSQL service
railway restart postgres

# Check connection string
railway variables get DATABASE_URL
```

### Out of Memory Errors (Celery)

**Symptoms:** MCMC tasks fail with OOM errors

**Fix:**
1. Increase Celery worker memory: Settings → Resources → 4 GB RAM
2. Reduce MCMC samples in environment variables:
   ```bash
   MCMC_SAMPLES=1000  # Instead of 2000
   MCMC_CHAINS=2      # Instead of 4
   ```

### High Costs

**Check:**
1. Railway usage dashboard
2. Identify high-usage services
3. Check for runaway processes

**Fix:**
1. Scale down unused services
2. Enable auto-sleep for low-traffic services
3. Optimize database queries (use indexes)
4. Increase Redis cache TTL to reduce DB hits

---

## Migration to AWS (When You Outgrow Railway)

### When to Migrate

Migrate when you hit:
- 500+ concurrent users
- $500+ monthly Railway costs
- Need for multi-region deployment
- Advanced features (auto-scaling, load balancing, CDN)
- Compliance requirements (HIPAA, SOC2)

### Migration Path

Your Docker setup makes migration easy:

1. **Export Database**
   ```bash
   railway run pg_dump $DATABASE_URL > production_data.sql
   ```

2. **Set Up AWS Infrastructure**
   - ECS Fargate for containers (drop-in Docker compatibility)
   - RDS PostgreSQL (import dump)
   - ElastiCache Redis
   - ALB for load balancing
   - CloudFront for CDN

3. **Deploy Same Docker Images**
   - Push to AWS ECR (Elastic Container Registry)
   - Deploy to ECS with same environment variables

4. **Update DNS**
   - Point domain to AWS ALB
   - Zero downtime cutover

---

## Support & Resources

### Railway Documentation
- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)

### HealthSystems Platform
- Internal documentation: [docs/](../README.md)
- Architecture overview: [SYSTEM_ARCHITECTURE_OVERVIEW.md](../Foundational%20Principles/03_SYSTEM_ARCHITECTURE_OVERVIEW.md)

### Getting Help

1. **Check Railway logs** first
2. **Review environment variables**
3. **Test locally** with `docker-compose.railway.yml`
4. **Contact Railway support** via dashboard

---

## Quick Reference Commands

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up

# View logs
railway logs backend
railway logs celery-worker
railway logs frontend

# Connect to database
railway connect postgres
railway connect redis

# Run commands in service
railway run alembic upgrade head
railway run python manage.py createsuperuser

# Environment variables
railway variables set KEY="value"
railway variables get KEY
railway variables list

# Restart service
railway restart backend

# Open in browser
railway open
```

---

## Next Steps After Deployment

1. ✅ Verify all services are healthy
2. ✅ Run database migrations
3. ✅ Load initial mechanism bank data
4. ✅ Test end-to-end scenario execution
5. ✅ Set up monitoring (Sentry)
6. ✅ Configure custom domain
7. ✅ Set budget alerts
8. ✅ Create runbook for common issues
9. ✅ Schedule database backups
10. ✅ Test disaster recovery process

---

**Estimated Time to Deploy**: 1-2 hours for first deployment

**Ongoing Maintenance**: <1 hour/week (mostly monitoring)

**Cost**: $60-120/month initially, scales with usage
