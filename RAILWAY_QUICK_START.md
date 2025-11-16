# Railway Deployment - Quick Start Guide

## Fixed Issues ✅

All deployment blockers have been resolved:
- ✅ Backend now reads PORT from environment variable
- ✅ Frontend has preview script with serve package
- ✅ Dockerfiles use dynamic $PORT variable
- ✅ Removed conflicting railway.json
- ✅ Added .dockerignore files for faster builds

---

## Step-by-Step Deployment Instructions

### Prerequisites

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Railway Account** - Sign up free at [railway.app](https://railway.app)
3. **Anthropic API Key** - Get from [console.anthropic.com](https://console.anthropic.com)

---

## PART 1: Set Up Railway Project (5 minutes)

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Click **"Login"** → **"Login with GitHub"**
3. Authorize Railway to access your GitHub account

### Step 2: Create New Project

1. Click **"New Project"** button (top right)
2. Select **"Deploy from GitHub repo"**
3. Choose your **healthsystems** repository
4. Railway will create an empty project (don't worry, we'll configure it next)

---

## PART 2: Add Databases (3 minutes)

### Step 3: Add PostgreSQL

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"**
3. Click **"Add PostgreSQL"**
4. Railway provisions the database automatically
5. **Important**: Note the service name (usually "Postgres")

### Step 4: Add Redis

1. Click **"+ New"** again
2. Select **"Database"**
3. Click **"Add Redis"**
4. Railway provisions Redis automatically
5. **Important**: Note the service name (usually "Redis")

**You now have 2 services:**
- ✅ PostgreSQL
- ✅ Redis

---

## PART 3: Deploy Backend Service (10 minutes)

### Step 5: Add Backend Service

1. Click **"+ New"** in your Railway project
2. Select **"GitHub Repo"** → Choose **healthsystems** repository
3. Railway will ask what to deploy - we need to configure it manually

### Step 6: Configure Backend Service

1. Click on the new service (it might say "healthsystems" or be unnamed)
2. Go to **"Settings"** tab
3. Configure the following:

**Service Name:**
```
backend
```

**Root Directory:**
```
backend
```

**Build Configuration:**
- Railway auto-detects the Dockerfile ✓
- No changes needed

**Start Command:** (leave empty - Dockerfile CMD will be used)

**Deploy Branch:**
```
main
```

### Step 7: Add Backend Environment Variables

Click on **"Variables"** tab and add these variables:

**Critical Variables (MUST SET):**
```bash
PORT=${{RAILWAY_PORT}}
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=your-super-secret-key-at-least-32-characters-long
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
ALLOWED_ORIGINS=http://localhost:3000
```

**Optional but Recommended:**
```bash
ENVIRONMENT=production
API_V1_PREFIX=/api/v1
PROJECT_NAME=HealthSystems Platform
LOG_LEVEL=INFO
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
```

**How to use Railway Variables:**
- `${{RAILWAY_PORT}}` - Railway's dynamic port assignment
- `${{Postgres.DATABASE_URL}}` - References PostgreSQL service
- `${{Redis.REDIS_URL}}` - References Redis service

### Step 8: Deploy Backend

1. Click **"Deploy"** button (or it may auto-deploy)
2. Watch the build logs (click "View Logs")
3. Wait for **"Success"** message (2-5 minutes)

**Expected logs:**
```
Installing dependencies...
Building Docker image...
Starting uvicorn...
Application startup complete.
```

### Step 9: Get Backend URL

1. Go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. Copy the URL (e.g., `backend-production-abc123.up.railway.app`)

**Test it:**
```
https://backend-production-abc123.up.railway.app/health
```

Should return:
```json
{"status": "healthy"}
```

**You now have 3 services:**
- ✅ PostgreSQL
- ✅ Redis
- ✅ Backend API

---

## PART 4: Deploy Frontend Service (10 minutes)

### Step 10: Add Frontend Service

1. Click **"+ New"** in your Railway project
2. Select **"GitHub Repo"** → Choose **healthsystems** repository again
3. Railway creates another service from the same repo

### Step 11: Configure Frontend Service

Click on the new service → **"Settings"** tab:

**Service Name:**
```
frontend
```

**Root Directory:**
```
frontend
```

**Build Configuration:**
- Railway auto-detects Dockerfile ✓

**Start Command:** (leave empty - uses package.json script)

### Step 12: Add Frontend Environment Variables

Click **"Variables"** tab:

**Critical Variables:**
```bash
PORT=${{RAILWAY_PORT}}
REACT_APP_API_URL=https://backend-production-abc123.up.railway.app
```

**Replace** `backend-production-abc123.up.railway.app` with YOUR backend URL from Step 9!

### Step 13: Update Backend CORS

Now that we know the frontend URL, we need to update the backend:

1. Go back to **backend** service
2. Click **"Variables"** tab
3. Update `ALLOWED_ORIGINS`:

**BEFORE:**
```
ALLOWED_ORIGINS=http://localhost:3000
```

**AFTER:**
```
ALLOWED_ORIGINS=https://frontend-production-xyz789.up.railway.app,http://localhost:3000
```

(Replace with YOUR frontend Railway URL)

4. Backend will auto-redeploy with new CORS settings

### Step 14: Deploy Frontend

1. Frontend should auto-deploy
2. Watch build logs (click "View Logs")
3. Wait for **"Success"** (3-7 minutes - npm install takes time)

**Expected logs:**
```
Installing dependencies...
npm install
Building React app...
npm run build
Creating optimized production build...
Serving on port $PORT
```

### Step 15: Test Frontend

1. Go to **"Settings"** → **"Domains"**
2. Click **"Generate Domain"**
3. Visit the URL

You should see the HealthSystems Platform React app!

**You now have 4 services:**
- ✅ PostgreSQL
- ✅ Redis
- ✅ Backend API
- ✅ Frontend

---

## PART 5: Deploy Celery Worker (Optional - 5 minutes)

Skip this if you don't need background jobs yet.

### Step 16: Add Celery Worker Service

1. Click **"+ New"** → **"GitHub Repo"** → **healthsystems**
2. Configure in **"Settings"**:

**Service Name:**
```
celery-worker
```

**Root Directory:**
```
backend
```

**Start Command:**
```
celery -A api.tasks worker --loglevel=info --concurrency=4
```

### Step 17: Add Celery Environment Variables

Same as backend:
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
ANTHROPIC_API_KEY=sk-ant-your-key-here
ENVIRONMENT=production
```

### Step 18: Deploy Celery Worker

Click **"Deploy"** and wait for success.

**You now have 5 services:**
- ✅ PostgreSQL
- ✅ Redis
- ✅ Backend API
- ✅ Frontend
- ✅ Celery Worker

---

## PART 6: Verify Deployment (5 minutes)

### Health Checks

**Backend Health:**
```
https://your-backend.up.railway.app/health
```
Expected: `{"status": "healthy"}`

**Backend API Docs:**
```
https://your-backend.up.railway.app/docs
```
Expected: FastAPI Swagger UI

**Frontend:**
```
https://your-frontend.up.railway.app
```
Expected: React app loads

### Check Logs

For each service:
1. Click on service
2. Click **"View Logs"** tab
3. Look for errors

**Good backend logs:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:PORT
```

**Good frontend logs:**
```
Serving build on port PORT
Server listening at http://0.0.0.0:PORT
```

---

## Troubleshooting Common Issues

### Issue 1: Backend Won't Start

**Error:** `Port 8000 is already in use`

**Fix:**
- Check environment variables
- Ensure `PORT=${{RAILWAY_PORT}}` is set
- Redeploy backend service

### Issue 2: Frontend Can't Connect to Backend

**Error:** CORS error or network error in browser console

**Fix:**
1. Check backend `ALLOWED_ORIGINS` includes frontend URL
2. Check frontend `REACT_APP_API_URL` points to correct backend URL
3. Make sure both URLs use `https://` not `http://`

### Issue 3: Database Connection Failed

**Error:** `could not connect to server`

**Fix:**
- Check `DATABASE_URL=${{Postgres.DATABASE_URL}}` is set correctly
- Make sure PostgreSQL service is running
- Try restarting backend service

### Issue 4: Build Failed - Out of Memory

**Error:** `JavaScript heap out of memory`

**Fix:**
1. Go to service **"Settings"**
2. Scroll to **"Resources"**
3. Increase memory to 2GB
4. Redeploy

### Issue 5: Frontend Shows Blank Page

**Fix:**
1. Check browser console for errors
2. Verify `REACT_APP_API_URL` is set correctly
3. Check frontend build logs for errors
4. Try clearing browser cache

---

## Cost Monitoring

### View Usage

1. Click your profile (top right)
2. Go to **"Usage"**
3. See current month's cost

### Set Budget Alert

1. Go to **"Project Settings"**
2. Click **"Usage & Billing"**
3. Set monthly budget limit (e.g., $150)
4. Railway emails you when approaching limit

**Expected costs:**
- Month 1: $60-120
- With light traffic: $80-150/month
- With moderate traffic: $150-250/month

---

## Next Steps After Deployment

### 1. Initialize Database

Run migrations to set up database schema:

**Via Railway CLI:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to backend service
railway link

# Run migration
railway run alembic upgrade head
```

**Or via backend service:**
Add this to backend startup in `api/main.py` (if not already there):
```python
@app.on_event("startup")
async def startup_event():
    # Run migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
```

### 2. Load Initial Data

Load mechanism bank data:
```bash
railway run python scripts/load_mechanisms.py
```

### 3. Set Up Custom Domain (Optional)

**For Frontend:**
1. Go to frontend service → **"Settings"** → **"Domains"**
2. Click **"+ Custom Domain"**
3. Enter your domain: `app.yourdomain.com`
4. Add CNAME record to your DNS:
   ```
   Type: CNAME
   Name: app
   Value: frontend-production-xyz.up.railway.app
   ```

**For Backend:**
1. Same process for backend
2. Use subdomain: `api.yourdomain.com`

**Update Environment Variables:**
```bash
# Backend
ALLOWED_ORIGINS=https://app.yourdomain.com

# Frontend
REACT_APP_API_URL=https://api.yourdomain.com
```

### 4. Set Up Monitoring

Add Sentry for error tracking:

1. Create free account at [sentry.io](https://sentry.io)
2. Create project for backend and frontend
3. Add to Railway environment variables:
   ```bash
   SENTRY_DSN=https://your-dsn@sentry.io/project-id
   SENTRY_ENVIRONMENT=production
   ```

### 5. Enable Automatic Backups

Railway backs up PostgreSQL automatically, but verify:

1. Go to PostgreSQL service
2. Click **"Settings"**
3. Scroll to **"Backups"**
4. Enable daily backups (should be on by default)

---

## Deployment Checklist

Before going live, verify:

- [ ] Backend health endpoint returns 200
- [ ] Frontend loads without errors
- [ ] Backend CORS allows frontend origin
- [ ] Database connection successful
- [ ] Redis cache working
- [ ] API documentation accessible
- [ ] Environment variables set correctly
- [ ] Custom domain configured (if using)
- [ ] Monitoring/logging set up
- [ ] Budget alerts configured
- [ ] Database migrations run
- [ ] Initial data loaded
- [ ] Test user authentication (if enabled)
- [ ] Test end-to-end scenario execution

---

## Quick Reference

### Railway CLI Commands

```bash
# Install
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# View logs
railway logs

# Run command in service
railway run <command>

# Connect to database
railway connect postgres

# Set environment variable
railway variables set KEY=value

# Deploy
railway up
```

### Service URLs Pattern

```
Backend:  https://backend-production-[hash].up.railway.app
Frontend: https://frontend-production-[hash].up.railway.app
```

### Important Environment Variables

**Backend:**
- `PORT=${{RAILWAY_PORT}}`
- `DATABASE_URL=${{Postgres.DATABASE_URL}}`
- `REDIS_URL=${{Redis.REDIS_URL}}`
- `SECRET_KEY=<secret>`
- `ANTHROPIC_API_KEY=<api-key>`
- `ALLOWED_ORIGINS=<frontend-url>`

**Frontend:**
- `PORT=${{RAILWAY_PORT}}`
- `REACT_APP_API_URL=<backend-url>`

---

## Getting Help

**Railway Issues:**
- [Railway Docs](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Railway Status](https://status.railway.app)

**Application Issues:**
- Check service logs in Railway dashboard
- Review [docs/Deployment/RAILWAY_DEPLOYMENT.md](docs/Deployment/RAILWAY_DEPLOYMENT.md) for detailed troubleshooting
- Check browser console for frontend errors
- Verify environment variables are set correctly

---

## Summary

You should now have:
- ✅ PostgreSQL database running
- ✅ Redis cache running
- ✅ Backend API deployed and healthy
- ✅ Frontend deployed and accessible
- ✅ (Optional) Celery worker for background jobs

**Total setup time:** 30-40 minutes

**Monthly cost:** $60-150 initially

**Next:** Load your mechanism bank data and start building scenarios!

---

## Migration Path

When you outgrow Railway (500+ users, $500+/month cost):

1. Export PostgreSQL database
2. Deploy same Docker containers to AWS ECS/Fargate
3. Import data to AWS RDS
4. Update DNS to point to AWS
5. Zero downtime migration possible

Your Docker containers are cloud-agnostic - they'll run anywhere!
