# PROMPT 7: Centralize Configuration

## Context
Configuration settings are **scattered across multiple files** with hardcoded values, making it difficult to manage environment-specific settings and API configurations.

## Current State

### Scattered Configuration

**API URLs (hardcoded 8+ times):**
```typescript
// frontend/src/hooks/usePathfinding.ts
const API_URL = 'http://localhost:8000';

// frontend/src/hooks/useCrisisSubgraph.ts
const BASE_URL = 'http://localhost:8000';

// frontend/src/utils/api.ts
const API_BASE = 'http://localhost:8000';

// ... 5 more instances
```

**LLM Settings (hardcoded in scripts):**
```python
# backend/scripts/run_alcohol_extraction.py
MODEL = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 16000
TEMPERATURE = 0.0
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# backend/scripts/batch_topic_extraction.py (duplicate)
MODEL = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 16000
TEMPERATURE = 0.0
```

**Database URLs (in multiple places):**
```python
# backend/models.py
DATABASE_URL = "sqlite:///./mechanisms.db"

# backend/api/main.py (duplicate)
DATABASE_URL = "sqlite:///./mechanisms.db"
```

**Feature Flags (nonexistent):**
- No way to toggle features
- No environment-specific settings
- No deployment configuration

## Target Architecture

```
# Frontend Configuration
frontend/
├── .env.example                    # Template with all vars
├── .env.local                      # Local overrides (gitignored)
├── .env.development                # Dev settings
├── .env.production                 # Production settings
│
└── src/
    └── config/
        ├── index.ts                # Main config export
        ├── api.ts                  # API configuration
        ├── features.ts             # Feature flags
        └── constants.ts            # App constants

# Backend Configuration
backend/
├── .env.example                    # Template
├── .env                            # Local (gitignored)
│
└── config/
    ├── __init__.py                 # Config exports
    ├── database.py                 # Database settings
    ├── llm.py                      # LLM configuration
    └── api.py                      # API settings
```

## Implementation Steps

### Step 1: Create Frontend Configuration

**File: `frontend/.env.example`**

```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_ENABLE_PATHFINDING=true
VITE_ENABLE_CRISIS_EXPLORER=true
VITE_ENABLE_PATHWAY_EXPLORER=false
VITE_ENABLE_ALCOHOLISM_VIEW=true

# Visualization Settings
VITE_GRAPH_MAX_NODES=1000
VITE_GRAPH_MAX_EDGES=2000

# Debug Settings
VITE_DEBUG=false
VITE_LOG_LEVEL=info
```

**File: `frontend/src/config/api.ts`**

```typescript
/**
 * API configuration settings.
 * Centralized API URL and timeout management.
 */

export const apiConfig = {
  // Base API URL
  baseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',

  // Request timeout (ms)
  timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000', 10),

  // Endpoints
  endpoints: {
    nodes: '/api/nodes',
    mechanisms: '/api/mechanisms',
    pathways: '/api/pathways',
  },

  // Retry configuration
  retry: {
    attempts: 3,
    delay: 1000,
    backoff: 2,
  },
} as const;

/**
 * Get full API URL for endpoint.
 */
export function getApiUrl(endpoint: string): string {
  return `${apiConfig.baseUrl}${endpoint}`;
}

/**
 * Check if API is in development mode.
 */
export function isDevelopment(): boolean {
  return apiConfig.baseUrl.includes('localhost') || apiConfig.baseUrl.includes('127.0.0.1');
}
```

**File: `frontend/src/config/features.ts`**

```typescript
/**
 * Feature flags configuration.
 * Controls which features are enabled in the application.
 */

export const features = {
  // Main features
  pathfinding: import.meta.env.VITE_ENABLE_PATHFINDING === 'true',
  crisisExplorer: import.meta.env.VITE_ENABLE_CRISIS_EXPLORER === 'true',
  pathwayExplorer: import.meta.env.VITE_ENABLE_PATHWAY_EXPLORER === 'true',
  alcoholismView: import.meta.env.VITE_ENABLE_ALCOHOLISM_VIEW === 'true',

  // Experimental features
  forceDirectedLayout: false,
  advancedFilters: true,
  batchOperations: false,
} as const;

/**
 * Check if a feature is enabled.
 */
export function isFeatureEnabled(feature: keyof typeof features): boolean {
  return features[feature] === true;
}

/**
 * Get list of enabled features.
 */
export function getEnabledFeatures(): string[] {
  return Object.entries(features)
    .filter(([, enabled]) => enabled)
    .map(([name]) => name);
}
```

**File: `frontend/src/config/constants.ts`**

```typescript
/**
 * Application constants.
 * Non-configurable application-wide values.
 */

// Visualization constants
export const VISUALIZATION = {
  maxNodes: parseInt(import.meta.env.VITE_GRAPH_MAX_NODES || '1000', 10),
  maxEdges: parseInt(import.meta.env.VITE_GRAPH_MAX_EDGES || '2000', 10),
  defaultWidth: 1200,
  defaultHeight: 800,
  minZoom: 0.1,
  maxZoom: 4,
} as const;

// Node scale definitions
export const NODE_SCALES = {
  1: 'Structural Determinants',
  2: 'Built Environment',
  3: 'Institutional Infrastructure',
  4: 'Individual/Household',
  5: 'Health Behaviors',
  6: 'Biological Processes',
  7: 'Health Outcomes',
} as const;

// Evidence quality grades
export const EVIDENCE_GRADES = {
  A: { label: 'Strong', color: 'green', weight: 1.0 },
  B: { label: 'Moderate', color: 'yellow', weight: 0.6 },
  C: { label: 'Limited', color: 'orange', weight: 0.3 },
} as const;

// Category definitions
export const CATEGORIES = [
  'economic',
  'social_environment',
  'built_environment',
  'healthcare_access',
  'political',
  'behavioral',
  'biological',
] as const;

export type Category = typeof CATEGORIES[number];
```

**File: `frontend/src/config/index.ts`**

```typescript
/**
 * Main configuration export.
 * Single import point for all config settings.
 */
export * from './api';
export * from './features';
export * from './constants';

// Debug configuration
export const debug = {
  enabled: import.meta.env.VITE_DEBUG === 'true',
  logLevel: import.meta.env.VITE_LOG_LEVEL || 'info',
};

/**
 * Log debug information if debug mode is enabled.
 */
export function debugLog(message: string, ...args: any[]) {
  if (debug.enabled) {
    console.log(`[DEBUG] ${message}`, ...args);
  }
}
```

### Step 2: Create Backend Configuration

**File: `backend/.env.example`**

```env
# Database Configuration
DATABASE_URL=sqlite:///./mechanisms.db
DATABASE_ECHO=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
API_CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# LLM Configuration
ANTHROPIC_API_KEY=your_api_key_here
LLM_MODEL=claude-3-5-sonnet-20241022
LLM_MAX_TOKENS=16000
LLM_TEMPERATURE=0.0
LLM_MAX_RETRIES=3

# Extraction Configuration
EXTRACTION_OUTPUT_DIR=mechanism-bank/mechanisms
EXTRACTION_BATCH_SIZE=10

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

**File: `backend/config/__init__.py`**

```python
"""
Configuration package.
Centralized settings management.
"""
from .database import database_config
from .llm import llm_config
from .api import api_config

__all__ = ['database_config', 'llm_config', 'api_config']
```

**File: `backend/config/database.py`**

```python
"""
Database configuration.
"""
import os
from pathlib import Path


class DatabaseConfig:
    """Database configuration settings."""

    def __init__(self):
        self.url = os.environ.get('DATABASE_URL', 'sqlite:///./mechanisms.db')
        self.echo = os.environ.get('DATABASE_ECHO', 'false').lower() == 'true'
        self.pool_size = int(os.environ.get('DATABASE_POOL_SIZE', '5'))
        self.max_overflow = int(os.environ.get('DATABASE_MAX_OVERFLOW', '10'))

    @property
    def is_sqlite(self) -> bool:
        return self.url.startswith('sqlite')

    @property
    def is_postgres(self) -> bool:
        return self.url.startswith('postgresql')

    def get_engine_kwargs(self) -> dict:
        """Get SQLAlchemy engine kwargs."""
        kwargs = {
            'echo': self.echo,
        }

        # Only add pooling for non-SQLite databases
        if not self.is_sqlite:
            kwargs.update({
                'pool_size': self.pool_size,
                'max_overflow': self.max_overflow,
                'pool_pre_ping': True,
            })

        return kwargs


# Global config instance
database_config = DatabaseConfig()
```

**File: `backend/config/llm.py`**

```python
"""
LLM configuration.
"""
import os


class LLMConfig:
    """LLM configuration settings."""

    def __init__(self):
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.model = os.environ.get('LLM_MODEL', 'claude-3-5-sonnet-20241022')
        self.max_tokens = int(os.environ.get('LLM_MAX_TOKENS', '16000'))
        self.temperature = float(os.environ.get('LLM_TEMPERATURE', '0.0'))
        self.max_retries = int(os.environ.get('LLM_MAX_RETRIES', '3'))

    def validate(self):
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set")

        if self.max_tokens < 1000 or self.max_tokens > 200000:
            raise ValueError("LLM_MAX_TOKENS must be between 1000 and 200000")

        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("LLM_TEMPERATURE must be between 0 and 1")

    def to_dict(self) -> dict:
        """Convert to dict for logging (excluding API key)."""
        return {
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'max_retries': self.max_retries,
        }


# Global config instance
llm_config = LLMConfig()
```

**File: `backend/config/api.py`**

```python
"""
API configuration.
"""
import os


class APIConfig:
    """API server configuration."""

    def __init__(self):
        self.host = os.environ.get('API_HOST', '0.0.0.0')
        self.port = int(os.environ.get('API_PORT', '8000'))
        self.reload = os.environ.get('API_RELOAD', 'true').lower() == 'true'
        self.cors_origins = self._parse_cors_origins()
        self.log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()

    def _parse_cors_origins(self) -> list:
        """Parse CORS origins from environment."""
        origins_str = os.environ.get('API_CORS_ORIGINS', '')
        if not origins_str:
            return ['http://localhost:5173', 'http://localhost:3000']

        return [origin.strip() for origin in origins_str.split(',')]

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.reload

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.reload


# Global config instance
api_config = APIConfig()
```

### Step 3: Update Frontend to Use Config

**File: `frontend/src/utils/api.ts` (updated)**

```typescript
import { apiConfig, getApiUrl } from '../config';

// Use config instead of hardcoded values
export const API_ENDPOINTS = {
  nodes: {
    list: '/api/nodes',
    pathfinding: '/api/nodes/pathfinding',
    // ...
  },
  // ...
} as const;

async function buildUrl(endpoint: string, params?: Record<string, any>): string {
  return getApiUrl(endpoint) + (params ? `?${new URLSearchParams(params)}` : '');
}

// Use config timeout
export const apiClient = {
  async get<T>(endpoint: string, options: ApiRequestOptions = {}): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), apiConfig.timeout);

    try {
      const response = await fetch(buildUrl(endpoint, options.params), {
        signal: controller.signal,
        // ...
      });
      return handleResponse<T>(response);
    } finally {
      clearTimeout(timeoutId);
    }
  },
  // ...
};
```

**File: `frontend/src/layouts/DashboardLayout.tsx` (updated)**

```typescript
import { features } from '../config';

// Conditionally render navigation based on feature flags
<nav>
  <Link to="/">Systems Map</Link>

  {features.pathfinding && (
    <Link to="/pathfinder">Pathfinder</Link>
  )}

  {features.crisisExplorer && (
    <Link to="/crisis-explorer">Crisis Explorer</Link>
  )}

  {features.pathwayExplorer && (
    <Link to="/pathways">Pathways</Link>
  )}

  {features.alcoholismView && (
    <Link to="/systems/alcoholism">Alcoholism System</Link>
  )}
</nav>
```

### Step 4: Update Backend to Use Config

**File: `backend/models.py` (updated)**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import database_config

# Use config instead of hardcoded values
engine = create_engine(
    database_config.url,
    **database_config.get_engine_kwargs()
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**File: `backend/api/main.py` (updated)**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import api_config
import logging

# Setup logging
logging.basicConfig(level=api_config.log_level)
logger = logging.getLogger(__name__)

app = FastAPI(title="HealthSystems API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=api_config.host,
        port=api_config.port,
        reload=api_config.reload,
        log_level=api_config.log_level.lower()
    )
```

**File: `backend/extraction/llm_client.py` (updated)**

```python
from anthropic import Anthropic
from config import llm_config

class LLMClient:
    def __init__(self):
        # Validate config on init
        llm_config.validate()

        self.client = Anthropic(api_key=llm_config.api_key)
        self.model = llm_config.model
        self.max_tokens = llm_config.max_tokens
        self.temperature = llm_config.temperature
        self.max_retries = llm_config.max_retries

    def call(self, prompt: str) -> str:
        for attempt in range(self.max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                # Retry
                continue
```

### Step 5: Update .gitignore

```gitignore
# Environment files
.env
.env.local
.env.*.local

# Keep templates
!.env.example
```

## Migration Checklist

### Phase 1: Create Config Files (2 hours)
- [ ] Create all frontend config files
- [ ] Create all backend config files
- [ ] Create .env.example templates
- [ ] Test config loading

### Phase 2: Update Frontend (2 hours)
- [ ] Update all hardcoded API URLs
- [ ] Add feature flag checks
- [ ] Update navigation based on flags
- [ ] Test with different .env values

### Phase 3: Update Backend (2 hours)
- [ ] Update database initialization
- [ ] Update API startup
- [ ] Update LLM client
- [ ] Update all scripts

### Phase 4: Documentation (1 hour)
- [ ] Document environment variables
- [ ] Create setup guide
- [ ] Document feature flags
- [ ] Commit: "refactor: centralize configuration"

## Testing Requirements

**Test environment variable loading:**

```bash
# Frontend
cd frontend
echo "VITE_API_URL=http://test:8000" > .env.test
npm run build
# Check that build uses test URL

# Backend
cd backend
export DATABASE_URL="sqlite:///./test.db"
python -c "from config import database_config; print(database_config.url)"
# Should print: sqlite:///./test.db
```

**Test feature flags:**

```bash
# Disable pathfinder
echo "VITE_ENABLE_PATHFINDING=false" >> frontend/.env.local
npm run dev
# Navigate to app - pathfinder link should be hidden
```

## Success Criteria

- ✅ All config in centralized files
- ✅ No hardcoded URLs/settings in code
- ✅ Feature flags working
- ✅ Environment-specific configs working
- ✅ .env.example documented
- ✅ All tests passing
- ✅ Documentation complete

## Estimated Effort
**1.5 days** (1 day implementation, 0.5 day testing/docs)
