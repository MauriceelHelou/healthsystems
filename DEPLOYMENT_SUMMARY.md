# Railway Deployment - Setup Complete

## What Was Done

### 1. Database Migration for Scale Column
- **File**: [backend/alembic/versions/5cf6a1974760_add_scale_column_to_nodes.py](backend/alembic/versions/5cf6a1974760_add_scale_column_to_nodes.py)
- **Purpose**: Adds `scale` column (1-7 taxonomy) to nodes table
- **Features**:
  - Safely adds column with default value
  - Backfills existing rows with scale=4
  - Adds check constraint (scale >= 1 AND scale <= 7)
  - Creates index for performance

### 2. Database Seeding Script
- **File**: [backend/scripts/seed_database.py](backend/scripts/seed_database.py)
- **Purpose**: Automatically loads mechanism-bank YAML files into Railway database
- **Features**:
  - Loads all YAML files from `mechanism-bank/mechanisms/`
  - Extracts nodes from mechanism IDs
  - Infers scale levels automatically using keyword matching
  - Idempotent - safe to run multiple times
  - Skips invalid YAML files with warnings
  - Comprehensive logging

### 3. Railway Startup Script
- **File**: [backend/start.sh](backend/start.sh)
- **Purpose**: Orchestrates Railway deployment startup
- **Steps**:
  1. Waits for PostgreSQL to be ready (30 retries)
  2. Runs database migrations (`alembic upgrade head`)
  3. Seeds database with mechanism data
  4. Starts FastAPI server with dynamic port

### 4. Updated Docker Configuration
- **File**: [backend/Dockerfile](backend/Dockerfile)
- **Changes**: Now uses `start.sh` as entry point for production
- **Benefits**: Automatic migrations and seeding on every deploy

### 5. Railway Configuration
- **File**: [railway.toml](railway.toml)
- **Updated**: Points to `backend/Dockerfile`
- **Includes**: Documentation of required environment variables

### 6. Comprehensive Documentation
- **File**: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- **Covers**:
  - Step-by-step deployment guide
  - Database architecture explanation
  - Environment variable configuration
  - Troubleshooting common issues
  - Rollback procedures
  - Security best practices

### 7. Deployment Readiness Checker
- **File**: [backend/scripts/check_deployment_ready.py](backend/scripts/check_deployment_ready.py)
- **Purpose**: Pre-deployment validation
- **Checks**:
  - Migration files exist
  - Mechanism YAML files are valid
  - Environment config files exist
  - Docker configuration is correct
  - No hardcoded secrets
  - Railway config is present

## Key Concepts Explained

### Local vs Railway Database

```
┌─────────────────────┐         ┌──────────────────────┐
│   Local Database    │         │   Railway Database   │
│                     │         │                      │
│  SQLite or          │   ✗     │  PostgreSQL          │
│  Local PostgreSQL   │  NO     │  (Managed, Cloud)    │
│                     │  SYNC   │                      │
│  Development data   │         │  Production data     │
└─────────────────────┘         └──────────────────────┘
```

**Important**: Changes to local database do NOT automatically sync to Railway.

### Deployment Flow

```
1. Push to GitHub
   ↓
2. Railway detects push
   ↓
3. Builds Docker image (backend/Dockerfile)
   ↓
4. Runs start.sh
   ├── Waits for PostgreSQL
   ├── Runs migrations (alembic upgrade head)
   ├── Seeds data (scripts/seed_database.py)
   └── Starts server (uvicorn)
   ↓
5. Health checks pass
   ↓
6. Deployment complete!
```

### Data Seeding Process

```
mechanism-bank/mechanisms/*.yml
          ↓
   [seed_database.py]
          ↓
    Parse YAML files
          ↓
   Extract nodes from mechanism IDs
   (e.g., "housing_quality_to_respiratory_health")
          ↓
   Infer scale levels (1-7 taxonomy)
          ↓
   Create Node records
          ↓
   Create Mechanism records
          ↓
   Railway PostgreSQL Database
```

## Quick Start: Deploy to Railway

### 1. Prepare Your Code

```bash
# Run deployment readiness check
cd backend
python scripts/check_deployment_ready.py

# If checks pass, commit changes
git add .
git commit -m "Configure Railway deployment with auto-migrations and seeding"
git push origin main
```

### 2. Set Up Railway Project

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Add PostgreSQL database service
4. Railway automatically sets `DATABASE_URL`

### 3. Configure Environment Variables

In Railway dashboard → Variables:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend.up.railway.app
```

### 4. Deploy

Railway deploys automatically when you push to GitHub.

Monitor logs:
```bash
railway logs
```

### 5. Verify

```bash
# Check health
curl https://your-app.up.railway.app/health

# Check mechanisms loaded
curl https://your-app.up.railway.app/api/mechanisms

# Check nodes loaded
curl https://your-app.up.railway.app/api/nodes
```

## What Happens on Each Deploy

1. **Container starts** - Railway spins up Docker container
2. **Database waits** - Startup script waits for PostgreSQL (max 60s)
3. **Migrations run** - `alembic upgrade head` creates/updates tables
4. **Data seeds** - Loads mechanism YAML files (skips if already loaded)
5. **Server starts** - FastAPI application launches on dynamic port
6. **Health checks** - Railway monitors `/health` endpoint

## Expected Database State After First Deploy

### Tables Created

- **nodes** (~150 nodes from all mechanisms)
- **mechanisms** (~80 mechanisms from YAML files)
- **geographic_contexts** (empty initially)

### Sample Data

```sql
-- Check node count
SELECT COUNT(*) FROM nodes;
-- Expected: 150+

-- Check mechanism count
SELECT COUNT(*) FROM mechanisms;
-- Expected: 80+

-- Check scale distribution
SELECT scale, COUNT(*) FROM nodes GROUP BY scale ORDER BY scale;
-- Expected distribution across scales 1-7
```

## Maintenance Tasks

### Adding New Mechanisms

1. Add YAML file to `mechanism-bank/mechanisms/`
2. Commit and push
3. Railway redeploys and auto-loads new mechanism

### Updating Existing Mechanisms

1. Edit YAML file
2. Commit and push
3. Either:
   - Update via SQL directly in Railway database
   - Or reset database and redeploy (loses all data!)

### Creating New Migrations

```bash
# Locally, modify backend/models/*.py
cd backend
python -m alembic revision --autogenerate -m "description"

# Review and edit migration file
# Test locally
python -m alembic upgrade head

# Commit and push
git add alembic/versions/*.py
git commit -m "Add migration: description"
git push
```

## Troubleshooting

### Deployment Fails

Check Railway logs for:
```
Database is ready!
Running database migrations...
Seeding database with mechanism data...
```

Common issues:
- PostgreSQL service not provisioned
- `DATABASE_URL` not set (should be automatic)
- Migration syntax error
- YAML parsing errors (check logs for specific files)

### Database is Empty

1. Check seeding logs: `railway logs | grep "Seeding"`
2. Run manually: `railway run python scripts/seed_database.py`
3. Verify mechanism files: Check if YAML files are in git repo

### Migrations Don't Run

1. Check `start.sh` is executable: `chmod +x backend/start.sh`
2. Verify Dockerfile uses `start.sh`
3. Check alembic.ini configuration
4. Review Railway deployment logs

## Files Created/Modified

### New Files
- ✅ [backend/scripts/seed_database.py](backend/scripts/seed_database.py)
- ✅ [backend/scripts/check_deployment_ready.py](backend/scripts/check_deployment_ready.py)
- ✅ [backend/start.sh](backend/start.sh)
- ✅ [backend/alembic/versions/5cf6a1974760_add_scale_column_to_nodes.py](backend/alembic/versions/5cf6a1974760_add_scale_column_to_nodes.py)
- ✅ [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- ✅ [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) (this file)

### Modified Files
- ✅ [backend/Dockerfile](backend/Dockerfile) - Updated CMD to use start.sh
- ✅ [railway.toml](railway.toml) - Updated Dockerfile path and added comments
- ✅ [backend/models/mechanism.py](backend/models/mechanism.py) - Added scale column (already done)

## Next Steps

1. **Test locally** (optional):
   ```bash
   cd backend
   python -m alembic upgrade head
   python scripts/seed_database.py
   ```

2. **Run pre-deployment check**:
   ```bash
   cd backend
   python scripts/check_deployment_ready.py
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Add Railway deployment automation"
   git push origin main
   ```

4. **Set up Railway**:
   - Create project from GitHub
   - Add PostgreSQL service
   - Set environment variables

5. **Monitor first deployment**:
   ```bash
   railway logs -f
   ```

6. **Verify deployment**:
   - Check `/health` endpoint
   - Check `/api/mechanisms` returns data
   - Check `/api/nodes` returns data

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Deployment Guide**: See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

## Summary

Your HealthSystems Platform is now fully configured for Railway deployment with:

✅ Automatic database migrations
✅ Automatic data seeding from mechanism-bank
✅ Idempotent deployment (safe to redeploy)
✅ Comprehensive error handling
✅ Production-ready Docker configuration
✅ Complete documentation

**You're ready to deploy!** 🚀
