# HealthSystems Platform - Railway Deployment Guide

## Project Info
- **Project Name**: reasonable-intuition
- **Project ID**: 50cb4184-2fd9-4599-a0e4-4e2ebcbf483e

---

## Services Overview

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | `https://beautiful-perfection-production-5645.up.railway.app` | React SPA |
| Backend | `https://backend-production-b6c2.up.railway.app` | FastAPI REST API |
| PostgreSQL | Internal (`postgres.railway.internal`) | Database |
| Redis | Internal (`redis.railway.internal`) | Caching/Celery |

---

## Frontend Service

### Railway Dashboard Settings

| Setting | Value |
|---------|-------|
| **Root Directory** | `frontend` |
| **Dockerfile Path** | `Dockerfile` |
| **Builder** | Dockerfile |

### Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `REACT_APP_API_URL` | `https://backend-production-b6c2.up.railway.app` | **Critical**: Baked in at build time |
| `PORT` | Auto-set by Railway | Usually 3000 |

### Key Files

- `frontend/Dockerfile` - Multi-stage build with Node.js and serve
- `frontend/railway.json` - Railway build configuration
- `frontend/nixpacks.toml` - Alternative Nixpacks config (backup)

### Dockerfile Notes

```dockerfile
# Uses relative paths (build context is frontend/)
COPY package*.json ./
COPY . .

# ESLint disabled during build to prevent CI failures
RUN DISABLE_ESLINT_PLUGIN=true npm run build

# Serve with SPA fallback
CMD ["sh", "-c", "serve -s build --listen tcp://0.0.0.0:$PORT"]
```

### Deploy from CLI

```bash
cd frontend
railway up --service frontend --detach
```

---

## Backend Service

### Railway Dashboard Settings

| Setting | Value |
|---------|-------|
| **Root Directory** | *(empty)* |
| **Dockerfile Path** | `Dockerfile` |
| **Builder** | Dockerfile |

**Important**: When deploying from CLI inside `backend/` directory, Root Directory must be empty.

### Environment Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | `postgresql://...@postgres.railway.internal:5432/railway` | Auto-linked from PostgreSQL service |
| `REDIS_URL` | `redis://...@redis.railway.internal:6379` | Auto-linked from Redis service |
| `CORS_ORIGINS` | `https://beautiful-perfection-production-5645.up.railway.app,http://localhost:3000,http://localhost:5173` | **Required for frontend access** |
| `ANTHROPIC_API_KEY` | `sk-ant-...` | For LLM features |
| `SECRET_KEY` | Random string | For session security |
| `PORT` | `8002` | Railway assigns this |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

### Key Files

- `backend/Dockerfile` - Multi-stage Python build
- `backend/railway.json` - Railway deploy configuration
- `backend/start.sh` - Startup script (migrations + seeding + uvicorn)
- `backend/alembic/` - Database migrations
- `backend/scripts/seed_database.py` - Seeds nodes and mechanisms

### Dockerfile Notes

```dockerfile
# Uses relative paths (build context is backend/)
COPY requirements.txt ./
COPY . .

# Runs start.sh which handles:
# 1. Alembic migrations
# 2. Database seeding
# 3. Uvicorn startup
CMD ["./start.sh"]
```

### Deploy from CLI

```bash
cd backend
railway up --service backend --detach
```

---

## Data Sources (Copied into Docker)

### Nodes
- **Location**: `backend/Nodes/by_scale/`
- **Structure**: 7 scale folders (scale_1_structural through scale_7_crisis)
- **Format**: YAML files

### Mechanisms
- **Location**: `backend/mechanism-bank/mechanisms/`
- **Categories**: behavioral, biological, built_environment, economic, healthcare_access, political, social_environment
- **Format**: YAML files

---

## CORS Configuration

The backend must allow requests from the frontend domain. This is configured via the `CORS_ORIGINS` environment variable.

### Setting CORS via CLI

```bash
railway variables --set "CORS_ORIGINS=https://beautiful-perfection-production-5645.up.railway.app,http://localhost:3000,http://localhost:5173" --service backend
```

### After Setting CORS

Redeploy the backend to pick up the new environment variable:

```bash
cd backend
railway up --service backend --detach
```

Or trigger a redeploy:

```bash
railway redeploy --service backend --yes
```

---

## Common Issues & Solutions

### 1. Frontend calling localhost instead of production backend

**Cause**: `REACT_APP_API_URL` is baked in at build time. Old builds have localhost hardcoded.

**Fix**:
1. Set `REACT_APP_API_URL=https://backend-production-b6c2.up.railway.app` in Railway dashboard
2. Trigger a new build (redeploy or push)

### 2. CORS errors in browser console

**Cause**: Backend doesn't have frontend URL in `CORS_ORIGINS`.

**Fix**:
```bash
railway variables --set "CORS_ORIGINS=https://beautiful-perfection-production-5645.up.railway.app,http://localhost:3000" --service backend
railway redeploy --service backend --yes
```

### 3. Dockerfile not found error

**Cause**: Mismatch between Root Directory and Dockerfile Path settings.

**Fix for CLI deploys from subdirectory**:
- Root Directory: *(empty)*
- Dockerfile Path: `Dockerfile`

**Fix for git push deploys**:
- Root Directory: `backend` or `frontend`
- Dockerfile Path: `Dockerfile`

### 4. ESLint errors blocking frontend build

**Cause**: Create React App treats warnings as errors in CI mode.

**Fix**: Set `DISABLE_ESLINT_PLUGIN=true` before `npm run build` in Dockerfile.

### 5. Serve command failing with "Unknown --listen endpoint scheme"

**Cause**: Newer versions of `serve` package require different syntax.

**Fix**: Use `--listen tcp://0.0.0.0:$PORT` format:
```dockerfile
CMD ["sh", "-c", "serve -s build --listen tcp://0.0.0.0:$PORT"]
```

### 6. Deploy skipped / no changes detected

**Cause**: Railway sometimes skips deploys if it thinks nothing changed.

**Fix**: Deploy from CLI instead of relying on git push:
```bash
cd backend  # or frontend
railway up --service backend --detach
```

### 7. "Could not find root directory: /backend" error

**Cause**: Root Directory is set in dashboard but CLI deploy uses different context.

**Fix**: Clear Root Directory in Railway dashboard (leave empty) when deploying from CLI.

### 8. DuplicateTable error in migrations

**Cause**: Table already exists from previous migration.

**Fix**: Migrations are idempotent (check if table exists before creating).

### 9. DATABASE_URL not being read

**Cause**: Alembic config not reading from environment.

**Fix**: `alembic/env.py` overrides sqlalchemy.url with DATABASE_URL env var.

---

## Useful Railway CLI Commands

```bash
# List services
railway service list

# Check variables for a service
railway variables --service backend
railway variables --service frontend

# Set a variable
railway variables --set "KEY=value" --service backend

# View logs
railway logs --service backend
railway logs --service frontend

# Trigger redeploy
railway redeploy --service backend --yes

# Deploy from current directory
railway up --service backend --detach

# Check deployment status
railway status

# Get service domain
railway domain
```

---

## Environment Variable Reference

### Frontend (Build-time)

| Variable | Required | Description |
|----------|----------|-------------|
| `REACT_APP_API_URL` | Yes | Backend API URL (baked into JS bundle) |
| `DISABLE_ESLINT_PLUGIN` | No | Set to `true` to skip ESLint in build |

### Backend (Runtime)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REDIS_URL` | Yes | Redis connection string |
| `CORS_ORIGINS` | Yes | Comma-separated allowed origins |
| `ANTHROPIC_API_KEY` | Yes | For LLM mechanism discovery |
| `SECRET_KEY` | Yes | Application secret |
| `PORT` | Auto | Railway sets this |
| `LOG_LEVEL` | No | Default: INFO |

---

## Local Development vs Production

| Setting | Local | Production (Railway) |
|---------|-------|---------------------|
| Backend URL | http://localhost:8000 | https://backend-production-b6c2.up.railway.app |
| Database | SQLite (healthsystems.db) | PostgreSQL (Railway managed) |
| Frontend URL | http://localhost:3000 | https://beautiful-perfection-production-5645.up.railway.app |
| CORS | localhost origins | Railway origins |

---

## Deployment Checklist

- [ ] Frontend `REACT_APP_API_URL` points to production backend
- [ ] Backend `CORS_ORIGINS` includes frontend URL
- [ ] Backend `DATABASE_URL` is set (auto-linked from PostgreSQL)
- [ ] Backend `REDIS_URL` is set (auto-linked from Redis)
- [ ] Both services have correct Root Directory and Dockerfile Path settings
- [ ] Database migrations run successfully on deploy
- [ ] Health check endpoint (`/health`) is responding
