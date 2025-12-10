# HealthSystems Platform - Deployment Configuration

## Railway.app Deployment

### Project Info
- **Project Name**: reasonable-intuition
- **Project ID**: 50cb4184-2fd9-4599-a0e4-4e2ebcbf483e

---

## Services

### 1. Backend (FastAPI)
- **Service Name**: backend
- **URL**: https://backend-production-b6c2.up.railway.app
- **Build Method**: Dockerfile (`backend/Dockerfile`)
- **Root Directory**: `backend/`

#### Environment Variables (Railway Dashboard)
```
DATABASE_URL=postgresql://... (auto-injected from PostgreSQL service)
PORT=8000 (auto-set by Railway)
ANTHROPIC_API_KEY=sk-ant-... (if needed for LLM features)
```

#### Key Files
- `backend/Dockerfile` - Docker build configuration
- `backend/start.sh` - Startup script (migrations + seeding + uvicorn)
- `backend/alembic/` - Database migrations
- `backend/scripts/seed_database.py` - Seeds nodes and mechanisms

---

### 2. PostgreSQL Database
- **Service Name**: PostgreSQL (Railway managed)
- **Connection**: Auto-injected as `DATABASE_URL` to backend

---

### 3. Frontend (React)
- **Service Name**: frontend (TO BE CREATED)
- **URL**: TBD
- **Build Method**: Dockerfile (`frontend/Dockerfile`)
- **Root Directory**: `frontend/`
- **Server**: Node.js `serve` package (SPA mode with `-s` flag)

#### Environment Variables (Set in Railway Dashboard)
```
REACT_APP_API_URL=https://backend-production-b6c2.up.railway.app (build-time ARG)
PORT=3000 (runtime, auto-set by Railway)
```

#### Key Files
- `frontend/Dockerfile` - Multi-stage Docker build (node:20-alpine + serve)
- `frontend/.env.production` - Production environment variables (backup)

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

## Deployment Commands

### Deploy Backend
```bash
cd backend
railway up --detach
```

### Deploy Frontend
```bash
cd frontend
railway up --detach
```

### Check Logs
```bash
railway logs --service backend
railway logs --service frontend
```

### Get Service URLs
```bash
railway domain
```

---

## CORS Configuration

Backend allows origins (in `backend/api/config.py`):
- http://localhost:3000
- http://localhost:3002
- http://localhost:8000
- http://localhost:8002
- https://beautiful-perfection-production-5645.up.railway.app
- https://backend-production-b6c2.up.railway.app

**Note**: Add frontend Railway URL once deployed.

---

## Troubleshooting

### Backend Issues

1. **DuplicateTable error in migrations**
   - Solution: Migrations are idempotent (check if table exists before creating)
   - File: `backend/alembic/versions/516074b986c0_initial_migration_nodes_mechanisms_.py`

2. **DATABASE_URL not being read**
   - Solution: `alembic/env.py` overrides sqlalchemy.url with DATABASE_URL env var
   - Check Railway dashboard for DATABASE_URL variable

3. **Mechanism bank not found**
   - Solution: `mechanism-bank/` folder copied INTO `backend/` directory
   - Docker build context is `backend/` so can't access parent directories

### Frontend Issues

1. **API calls going to localhost**
   - Solution: Set `REACT_APP_API_URL` environment variable in Railway
   - Or use `.env.production` file

---

## Local Development vs Production

| Setting | Local | Production (Railway) |
|---------|-------|---------------------|
| Backend URL | http://localhost:8000 | https://backend-production-b6c2.up.railway.app |
| Database | SQLite (healthsystems.db) | PostgreSQL (Railway managed) |
| Frontend URL | http://localhost:3000 | TBD |
| CORS | localhost origins | Railway origins |
