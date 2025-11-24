# Railway Deployment Guide

## Overview

This guide explains how to deploy the HealthSystems Platform to Railway, including database setup, migrations, and automatic data seeding.

## Architecture

### Local vs Railway Database

**Important:** Your local development database and Railway database are **completely separate**:

- **Local**: SQLite or PostgreSQL running on your machine
- **Railway**: Managed PostgreSQL instance in the cloud
- **Data does NOT sync** between local and Railway automatically

### Automatic Database Setup

When you deploy to Railway, the following happens automatically:

1. **Tables Created**: Alembic migrations run to create schema
2. **Data Seeded**: Mechanism-bank YAML files are loaded into database
3. **Idempotent**: Can redeploy without duplicating data

## Prerequisites

1. Railway account (sign up at [railway.app](https://railway.app))
2. Railway CLI (optional but recommended)
3. GitHub repository connected to Railway

## Step 1: Create Railway Project

### Option A: Using Railway Dashboard

1. Go to [railway.app](https://railway.app) and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `healthsystems` repository
5. Railway will automatically detect the Dockerfile

### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to your repo
railway link
```

## Step 2: Add PostgreSQL Database

### In Railway Dashboard:

1. Open your project
2. Click "New" → "Database" → "Add PostgreSQL"
3. Railway automatically:
   - Creates PostgreSQL instance
   - Sets `DATABASE_URL` environment variable
   - Makes database accessible to your app

**Note:** Railway's PostgreSQL is managed - backups, scaling, and maintenance are handled automatically.

## Step 3: Configure Environment Variables

### Required Variables (Set in Railway Dashboard)

Go to your service → Variables tab and add:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
ENVIRONMENT=production

# Optional but recommended
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
ANTHROPIC_MAX_TOKENS=8192
LOG_LEVEL=INFO

# Census API (if using data pipelines)
CENSUS_API_KEY=your-census-api-key

# CORS (update with your frontend URL)
CORS_ORIGINS=https://your-frontend.up.railway.app,https://yourdomain.com
ALLOWED_ORIGINS=https://your-frontend.up.railway.app,https://yourdomain.com
```

### Automatically Set by Railway

These are set automatically - **DO NOT override**:

- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Dynamic port assignment
- `RAILWAY_ENVIRONMENT` - Environment name

## Step 4: Deploy

### Automatic Deployment (Recommended)

Railway automatically deploys when you push to your main branch:

```bash
git add .
git commit -m "Configure Railway deployment"
git push origin main
```

Railway will:
1. Build Docker image from `backend/Dockerfile`
2. Run `start.sh` script which:
   - Waits for database to be ready
   - Runs Alembic migrations (`alembic upgrade head`)
   - Seeds database with mechanism data
   - Starts FastAPI server

### Manual Deployment

```bash
railway up
```

## Step 5: Verify Deployment

### Check Deployment Status

1. In Railway dashboard, go to your service
2. Click "Deployments" tab
3. View logs to confirm:
   ```
   ✓ Database is ready!
   ✓ Running database migrations...
   ✓ Seeding database with mechanism data...
   ✓ Starting FastAPI application...
   ```

### Test Health Endpoint

```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "production"
}
```

### Test API Endpoints

```bash
# List mechanisms
curl https://your-app.up.railway.app/api/mechanisms

# Get nodes
curl https://your-app.up.railway.app/api/nodes
```

## Database Schema Management

### Current Migrations

Your database has these migrations:

1. **516074b986c0** - Initial migration (nodes, mechanisms, geographic_contexts)
2. **5cf6a1974760** - Add scale column to nodes table

### Creating New Migrations

When you modify database models locally:

```bash
cd backend

# Generate migration
python -m alembic revision --autogenerate -m "description_of_changes"

# Review the generated migration file
# Edit if needed

# Test locally
python -m alembic upgrade head

# Commit and push
git add alembic/versions/*.py
git commit -m "Add database migration: description"
git push
```

Railway will automatically run the new migration on next deploy.

### Viewing Database

#### Using Railway Dashboard

1. Go to PostgreSQL service
2. Click "Data" tab
3. Browse tables directly

#### Using PostgreSQL Client

Get connection details from Railway dashboard:

```bash
# From Railway dashboard, copy DATABASE_URL
psql $DATABASE_URL

# Or use individual connection params
psql -h host -U user -d database
```

## Data Management

### Initial Seed Data

On first deployment, the database is automatically seeded with:

- **Nodes**: Extracted from mechanism YAML files (~150+ nodes)
- **Mechanisms**: All YAML files in `mechanism-bank/mechanisms/` (~80+ mechanisms)

### Updating Mechanism Data

To update mechanisms in production:

1. **Option A - Redeploy** (Simple, but recreates containers):
   ```bash
   # Modify YAML files locally
   git add mechanism-bank/
   git commit -m "Update mechanism definitions"
   git push
   ```
   The seeding script is idempotent - it won't duplicate existing data.

2. **Option B - Manual Update** (For single mechanism):
   - Use Railway's database interface
   - Connect with psql
   - Update specific records

### Resetting Database

**Warning:** This deletes all data!

```bash
# In Railway dashboard → PostgreSQL service
# Settings → Danger Zone → Reset Database

# OR via CLI
railway run python scripts/reset_database.py
```

After reset, redeploy to re-seed data.

## Monitoring and Logging

### View Logs

```bash
# Railway CLI
railway logs

# Or in dashboard → Deployments → Click deployment → View logs
```

### Key Log Sections

Look for these during deployment:

```
Database is ready!
Running database migrations...
  Upgrading 516074b986c0 -> 5cf6a1974760
Seeding database with mechanism data...
  Found 80 mechanism files
  Processed 80/80 files...
  Total nodes in database: 152
  Total mechanisms in database: 80
Starting FastAPI application...
```

### Health Checks

Railway automatically monitors `/health` endpoint every 30 seconds.

If health check fails 3 times, Railway:
1. Marks deployment as unhealthy
2. Attempts restart
3. Rolls back if restart fails

## Troubleshooting

### Migration Fails

**Symptom:** Deployment fails with Alembic error

**Solutions:**
```bash
# Check migration files for syntax errors
cat backend/alembic/versions/*.py

# Test migration locally
cd backend
python -m alembic upgrade head

# If migration is broken, create a fix
python -m alembic revision -m "fix_migration_issue"
```

### Database Connection Timeout

**Symptom:** "Failed to connect to database after 30 attempts"

**Solutions:**
1. Check PostgreSQL service is running in Railway
2. Verify `DATABASE_URL` is set correctly
3. Check Railway PostgreSQL service logs
4. Increase timeout in `start.sh` (max_retries=30)

### Seeding Script Fails

**Symptom:** "Error processing mechanism file"

**Solutions:**
```bash
# Test seeding locally
cd backend
python scripts/seed_database.py

# Check YAML syntax
yamllint mechanism-bank/mechanisms/**/*.yml

# Check logs for specific file causing issue
railway logs | grep "Error processing"
```

### Port Binding Error

**Symptom:** "Address already in use"

**Solutions:**
- Railway sets `PORT` dynamically
- Ensure Dockerfile uses `${PORT:-8000}`
- Don't hardcode port 8000 in production

### Out of Memory

**Symptom:** Container crashes, "Killed" in logs

**Solutions:**
1. Upgrade Railway plan for more memory
2. Reduce `WORKERS` env var (default=4)
3. Optimize database queries
4. Add pagination to API endpoints

## Environment Comparison

### Development (Local)

```bash
DATABASE_URL=sqlite:///healthsystems.db
ENVIRONMENT=development
API_RELOAD=true
WORKERS=1
```

### Production (Railway)

```bash
DATABASE_URL=postgresql://user:pass@host:port/db  # Auto-set by Railway
ENVIRONMENT=production
API_RELOAD=false
WORKERS=4
```

## Cost Optimization

### Hobby Plan (Free)

- 500 hours/month execution time
- Shared resources
- Suitable for development/testing

### Pro Plan ($20/month)

- Unlimited execution time
- Dedicated resources
- Recommended for production

### Database Costs

- Starter: 1GB storage (included in Hobby)
- Pro: 8GB+ storage
- Backups included

## Security Best Practices

1. **Never commit secrets**:
   ```bash
   # Ensure .env is in .gitignore
   echo ".env" >> .gitignore
   echo ".env.local" >> .gitignore
   ```

2. **Use Railway's secret management**:
   - Set sensitive vars in Railway dashboard
   - Use Railway's built-in encryption

3. **Enable CORS properly**:
   ```bash
   # In Railway variables
   CORS_ORIGINS=https://yourdomain.com
   ```

4. **Rotate API keys regularly**:
   - Update ANTHROPIC_API_KEY every 90 days
   - Rotate DATABASE_URL if compromised

## Rollback Procedure

### Via Railway Dashboard

1. Go to Deployments
2. Find last working deployment
3. Click "Redeploy"

### Via Git

```bash
# Find last working commit
git log --oneline

# Revert to that commit
git revert <commit-hash>
git push
```

## Multiple Environments

### Staging Environment

1. Create new Railway project: "healthsystems-staging"
2. Connect same GitHub repo
3. Set branch to `staging` or `develop`
4. Use separate PostgreSQL instance
5. Set `ENVIRONMENT=staging`

### Frontend + Backend

Deploy separately:

**Backend Service:**
- Service 1: Backend API (this guide)
- Uses `backend/Dockerfile`

**Frontend Service:**
- Service 2: React/Vite frontend
- Uses `frontend/Dockerfile`
- Set `VITE_API_BASE_URL` to backend URL

## Advanced: Custom Domains

1. Railway dashboard → Service → Settings
2. Add custom domain: `api.yourdomain.com`
3. Update DNS records as instructed
4. Update CORS_ORIGINS to include custom domain

## Support and Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [HealthSystems Platform Issues](https://github.com/yourusername/healthsystems/issues)

## Checklist: First Deployment

- [ ] Created Railway project
- [ ] Added PostgreSQL database service
- [ ] Set ANTHROPIC_API_KEY in Railway variables
- [ ] Set ENVIRONMENT=production
- [ ] Pushed code to GitHub
- [ ] Verified deployment succeeded in Railway logs
- [ ] Tested /health endpoint
- [ ] Verified mechanisms loaded: `curl /api/mechanisms`
- [ ] Verified nodes loaded: `curl /api/nodes`
- [ ] Updated frontend API URL (if deploying frontend)
- [ ] Configured custom domain (optional)

## Next Steps

After successful deployment:

1. Set up monitoring/alerts in Railway
2. Configure automatic backups
3. Deploy frontend to Railway or Vercel
4. Set up CI/CD for automated testing
5. Configure staging environment
6. Add error tracking (Sentry)
