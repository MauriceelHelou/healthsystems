# Railway Deployment Skill

**Purpose**: Comprehensive deployment review and 500 error prevention for Railway deployments of FastAPI + React applications.

## When to Use This Skill

Invoke this skill when:
- Reviewing Dockerfiles for production readiness
- Debugging 500 errors in Railway deployments
- Configuring CORS for FastAPI + React apps
- Setting up environment variables
- Preparing for deployment to Railway
- Troubleshooting deployment failures

---

## HealthSystems Platform Context

**Production URLs**:
- Frontend: `https://beautiful-perfection-production-5645.up.railway.app`
- Backend: `https://backend-production-b6c2.up.railway.app`

**Architecture**:
- Backend: FastAPI (Python 3.11) with PostgreSQL and Redis
- Frontend: React/TypeScript served by Node.js `serve`
- Database: Railway-managed PostgreSQL
- Cache: Railway-managed Redis

**Key Files**:
| File | Purpose |
|------|---------|
| `backend/api/main.py` | FastAPI app, CORS (line 61), health check (lines 97-109) |
| `backend/api/config.py` | Settings with `allowed_origins` (lines 31-38) |
| `backend/api/middleware/rate_limit.py` | Rate limiter (line 24) |
| `backend/Dockerfile` | Backend container configuration |
| `frontend/Dockerfile` | Frontend container configuration |
| `backend/start.sh` | Startup script (migrations, seeding, uvicorn) |
| `backend/railway.json` | Railway deploy configuration |
| `DEPLOYMENT.md` | Deployment documentation |

---

## Critical Issue Checklist

### 1. CORS Configuration

**Check**: Does `main.py` use environment-based origins instead of wildcards?

✗ **BROKEN Pattern** (security risk, credentials broken):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows ANY origin - security vulnerability
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

✓ **CORRECT Pattern** (environment-based):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # From config.py or CORS_ORIGINS env var
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

**Files to Check**:
- `backend/api/main.py:59-65` - Where CORS middleware is added
- `backend/api/config.py:31-38` - Where `allowed_origins` is defined

**Why This Matters**: Wildcard CORS with credentials can break browser security, and allows any malicious site to make authenticated requests to your API.

---

### 2. Health Check Depth

**Check**: Does the `/health` endpoint verify database connectivity?

✗ **BROKEN Pattern** (lies about health):
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}  # Returns healthy even if DB is down!
```

✓ **CORRECT Pattern** (verifies dependencies):
```python
from fastapi.responses import JSONResponse
from sqlalchemy import text

@app.get("/health")
async def health_check():
    health_status = {
        "status": "healthy",
        "version": "0.1.0",
        "checks": {}
    }

    # Database check
    try:
        from models.database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["checks"]["database"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = f"error: {str(e)}"

    # Redis check (if applicable)
    if settings.redis_url:
        try:
            import redis
            r = redis.from_url(settings.redis_url)
            r.ping()
            health_status["checks"]["redis"] = "connected"
        except Exception as e:
            health_status["checks"]["redis"] = f"error: {str(e)}"

    status_code = 200 if health_status["status"] == "healthy" else 503
    return JSONResponse(content=health_status, status_code=status_code)
```

**Files to Check**:
- `backend/api/main.py:97-109` - Health check endpoint

**Why This Matters**: Railway routes traffic based on health checks. A lying health check means traffic goes to broken instances, causing 500 errors.

---

### 3. Memory Leak Prevention

**Check**: Is rate limiting Redis-backed (not in-memory)?

✗ **BROKEN Pattern** (memory grows unbounded):
```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)  # MEMORY LEAK: grows forever
```

✓ **CORRECT Pattern** (Redis-backed with slowapi):
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Use Redis backend for production
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.redis_url  # Redis stores rate limit data
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/resource")
@limiter.limit("100/minute")
async def get_resource():
    ...
```

**Files to Check**:
- `backend/api/middleware/rate_limit.py:24` - In-memory storage

**Why This Matters**: In-memory rate limiters store per-IP request history indefinitely. In production with many IPs, memory grows until the container crashes with OOM errors.

---

### 4. Environment Variable Validation

**Check**: Are required environment variables validated at startup?

✗ **BROKEN Pattern** (cryptic runtime errors):
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # No validation - if DATABASE_URL is missing, you get a cryptic
    # SQLAlchemy error at first request, not at startup
    await init_db()
    yield
```

✓ **CORRECT Pattern** (fail fast with clear errors):
```python
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Validate required environment variables
    required_vars = {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "SECRET_KEY": os.getenv("SECRET_KEY"),
    }

    missing = [k for k, v in required_vars.items()
               if not v or v == "dev-secret-key-change-in-production"]

    if missing and settings.environment == "production":
        raise RuntimeError(
            f"Missing required environment variables: {missing}. "
            "Set these in Railway dashboard before deploying."
        )

    logger.info("Starting HealthSystems Platform API...")
    await init_db()
    logger.info("Database initialized")

    yield

    logger.info("Shutting down...")
    await close_db()
```

**Files to Check**:
- `backend/api/main.py:26-42` - Lifespan handler

**Why This Matters**: Without validation, missing env vars cause cryptic errors at runtime. With validation, you get a clear error at startup telling you exactly what's missing.

---

### 5. Dockerfile Best Practices

**Backend Dockerfile Checklist** (`backend/Dockerfile`):
- [ ] **Multi-stage build** (base → production) to reduce image size
- [ ] **Non-root user** (`USER appuser`) for security
- [ ] **Health check command** (`HEALTHCHECK`) for Railway monitoring
- [ ] **PORT env var support** (`${PORT:-8000}`) for Railway's dynamic ports
- [ ] **No secrets in image** (use environment variables)
- [ ] **Minimal dependencies** (production stage only has runtime deps)

✓ **Good Backend Dockerfile Example**:
```dockerfile
FROM python:3.11-slim as base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

FROM base as production
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x start.sh

# Security: non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check for Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

EXPOSE 8000
CMD ["./start.sh"]
```

**Frontend Dockerfile Checklist** (`frontend/Dockerfile`):
- [ ] **Build-time API URL** (`REACT_APP_API_URL` as ARG)
- [ ] **ESLint disabled for CI** (`DISABLE_ESLINT_PLUGIN=true`)
- [ ] **SPA fallback** (`serve -s build` with `-s` flag)
- [ ] **PORT binding** (`--listen tcp://0.0.0.0:$PORT`)

✓ **Good Frontend Dockerfile Example**:
```dockerfile
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --legacy-peer-deps
COPY . .
# Disable ESLint to prevent warnings from failing build
RUN DISABLE_ESLINT_PLUGIN=true npm run build

FROM node:20-alpine as production
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/build ./build
ENV PORT=3000
EXPOSE ${PORT}
# SPA fallback with -s flag, correct PORT syntax
CMD ["sh", "-c", "serve -s build --listen tcp://0.0.0.0:$PORT"]
```

---

### 6. Error Handling in Routes

**Check**: Do database routes have try/except blocks?

✗ **BROKEN Pattern** (crashes on DB errors):
```python
@router.get("/items/{id}")
async def get_item(id: str, db: Session = Depends(get_db)):
    # If database is unreachable, this crashes with 500 and cryptic error
    return db.query(Item).filter(Item.id == id).first()
```

✓ **CORRECT Pattern** (graceful error handling):
```python
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

@router.get("/items/{id}")
async def get_item(id: str, db: Session = Depends(get_db)):
    try:
        item = db.query(Item).filter(Item.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Item {id} not found")
        return item
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching item {id}: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")
```

**Alternative: Global Exception Handler**:
```python
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error on {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred"}
    )
```

**Files to Check**:
- `backend/api/routes/nodes.py` - Many routes lack error handling

**Why This Matters**: Unhandled exceptions return raw error messages which may expose internal details and provide poor user experience.

---

## Railway-Specific Configuration

### Required Environment Variables

| Variable | Required | Source | Notes |
|----------|----------|--------|-------|
| `DATABASE_URL` | Yes | Auto-linked | Railway PostgreSQL reference variable |
| `REDIS_URL` | Yes | Auto-linked | Railway Redis reference variable |
| `CORS_ORIGINS` | Yes | Manual | Comma-separated: `https://frontend.railway.app,http://localhost:3000` |
| `SECRET_KEY` | Yes | Manual | Random string, min 32 characters |
| `ANTHROPIC_API_KEY` | Yes | Manual | For LLM mechanism discovery |
| `PORT` | Auto | Railway | Railway sets this automatically |
| `LOG_LEVEL` | No | Manual | Default: `INFO` |

### Setting Environment Variables via CLI

```bash
# Set CORS origins
railway variables --set "CORS_ORIGINS=https://beautiful-perfection-production-5645.up.railway.app,http://localhost:3000" --service backend

# Set secret key
railway variables --set "SECRET_KEY=$(openssl rand -hex 32)" --service backend

# Verify variables
railway variables --service backend
```

### Common Railway Issues

1. **Root Directory mismatch**
   - **Symptom**: "Dockerfile not found" error
   - **Fix**: Clear Root Directory in Railway dashboard when deploying from CLI

2. **Build-time vs runtime variables**
   - **Issue**: `REACT_APP_*` variables are baked into JS bundle at build time
   - **Fix**: Trigger new build after changing `REACT_APP_API_URL`

3. **Serve command syntax**
   - **Symptom**: "Unknown --listen endpoint scheme" error
   - **Fix**: Use `--listen tcp://0.0.0.0:$PORT` format

4. **Health check path not configured**
   - **Symptom**: Service marked unhealthy despite working
   - **Fix**: Set `healthcheckPath: "/health"` in `railway.json`

5. **CORS errors in browser**
   - **Symptom**: "Access-Control-Allow-Origin" errors
   - **Fix**: Add frontend URL to `CORS_ORIGINS` env var and redeploy

6. **Deploy skipped / no changes detected**
   - **Symptom**: Railway says "no changes" but you need to redeploy
   - **Fix**: Deploy from CLI: `railway up --service backend --detach`

---

## Pre-Deployment Checklist

### Code Quality
- [ ] CORS uses `settings.allowed_origins` (not `["*"]`)
- [ ] Health check verifies database connectivity (returns 503 if unhealthy)
- [ ] Rate limiter is Redis-backed (not in-memory `defaultdict`)
- [ ] Required env vars validated at startup with clear error messages
- [ ] Routes have error handling (try/except or global handler)

### Docker Configuration
- [ ] Backend Dockerfile uses non-root user
- [ ] Backend Dockerfile has HEALTHCHECK command
- [ ] Frontend Dockerfile has ESLint disabled for CI
- [ ] Both Dockerfiles support `${PORT}` environment variable

### Railway Configuration
- [ ] `REACT_APP_API_URL` set to production backend URL
- [ ] `CORS_ORIGINS` includes production frontend URL
- [ ] `DATABASE_URL` linked from PostgreSQL service
- [ ] `REDIS_URL` linked from Redis service
- [ ] `SECRET_KEY` is not the default value
- [ ] Health check path configured in `railway.json`

### Post-Deployment Verification
- [ ] Health endpoint returns 200: `curl https://backend.railway.app/health`
- [ ] CORS preflight works: `curl -X OPTIONS -H "Origin: https://frontend.railway.app" https://backend.railway.app/api/nodes`
- [ ] Frontend can reach backend (no CORS errors in browser console)
- [ ] Logs show no errors: `railway logs --service backend`

---

## Useful Railway CLI Commands

```bash
# List services
railway service list

# Check environment variables
railway variables --service backend
railway variables --service frontend

# Set environment variable
railway variables --set "KEY=value" --service backend

# View logs
railway logs --service backend
railway logs --service frontend --limit 100

# Trigger redeploy
railway redeploy --service backend --yes

# Deploy from current directory
cd backend && railway up --service backend --detach

# Check deployment status
railway status

# Get service domain
railway domain
```

---

## Quick Fixes Reference

### Fix CORS (main.py:59-65)
```python
# Change this:
allow_origins=["*"]
# To this:
allow_origins=settings.allowed_origins
```

### Fix Health Check (main.py:97-109)
Add database connectivity check that returns 503 on failure.

### Fix Rate Limiter (rate_limit.py)
Replace `defaultdict(list)` with Redis-backed `slowapi.Limiter`.

### Fix Startup Validation (main.py lifespan)
Add `required_vars` check that raises `RuntimeError` for missing vars in production.
