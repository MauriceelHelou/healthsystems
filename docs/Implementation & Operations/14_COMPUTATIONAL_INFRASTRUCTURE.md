# 14: Computational Infrastructure
**Cloud Deployment, Network Architecture, and Scalability**

---

## 1. Overview

This document specifies the **computational infrastructure** supporting the platform: cloud architecture, network design, data storage, API structure, security, and performance optimization strategies. The infrastructure must support **real-time user interactions**, **large-scale Monte Carlo simulations**, and **concurrent multi-user access** while maintaining <3 second response times for typical queries.

**Design Principles**: Serverless-first for cost efficiency, horizontally scalable for load management, geographically distributed for low latency, and security-hardened for sensitive health data handling.

---

## 2. Architecture Overview

### 2.1 Three-Layer System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Web App    │  │  Mobile App  │  │   API Docs   │     │
│  │  (React/TS)  │  │  (React      │  │  (OpenAPI)   │     │
│  │              │  │   Native)    │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/TLS 1.3
┌────────────────────────▼────────────────────────────────────┐
│                  APPLICATION LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           API Gateway (AWS API Gateway)              │  │
│  │  - Authentication (Cognito)                          │  │
│  │  - Rate limiting (1000 req/min per user)            │  │
│  │  - Request routing                                   │  │
│  └─────────────┬────────────────────────────────────────┘  │
│                │                                             │
│  ┌─────────────▼───────────┐  ┌─────────────────────────┐ │
│  │  Core Services (Lambda)  │  │  Background Jobs (SQS) │ │
│  │  - Scenario analysis     │  │  - Monte Carlo sims    │ │
│  │  - Geography context     │  │  - Calibration         │ │
│  │  - Mechanism retrieval   │  │  - Report generation   │ │
│  └─────────────┬────────────┘  └────────────┬────────────┘ │
└────────────────┼──────────────────────────────┼─────────────┘
                 │                              │
┌────────────────▼──────────────────────────────▼─────────────┐
│                   DATA LAYER                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │   S3 Storage │  │  ElastiCache │     │
│  │  (Aurora)    │  │  (mechanism  │  │  (Redis)     │     │
│  │  - User data │  │   bank, pdfs)│  │  - Session   │     │
│  │  - Results   │  │              │  │  - Cache     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

| Component | Technology Choice | Rationale |
|-----------|-------------------|-----------|
| **Frontend** | React 18 + TypeScript | Component reusability, type safety |
| **API Layer** | AWS API Gateway + Lambda | Serverless cost efficiency, auto-scaling |
| **Backend Services** | Python 3.11 (FastAPI) | Async support, scientific libraries (NumPy, SciPy) |
| **Database** | PostgreSQL 15 (Aurora) | ACID compliance, JSON support, geographic queries |
| **File Storage** | AWS S3 | Cost-effective object storage, versioning |
| **Cache** | Redis (ElastiCache) | Sub-millisecond latency, session management |
| **Message Queue** | AWS SQS | Decouple long-running jobs, guaranteed delivery |
| **CDN** | CloudFront | Global edge caching, DDoS protection |
| **Monitoring** | Datadog | Real-time metrics, log aggregation, alerting |
| **CI/CD** | GitHub Actions | Automated testing, deployment pipelines |

---

## 3. Cloud Deployment Architecture

### 3.1 AWS Multi-Region Deployment

**Primary Region**: `us-east-1` (Northern Virginia)  
**Secondary Region**: `us-west-2` (Oregon)  
**Rationale**: 99.99% uptime SLA via multi-region failover

```
┌───────────────────────────────────────────────────────────────┐
│                    us-east-1 (Primary)                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  VPC: 10.0.0.0/16                                     │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │    │
│  │  │ Public     │  │ Private    │  │ Data       │     │    │
│  │  │ Subnet     │  │ Subnet     │  │ Subnet     │     │    │
│  │  │ (API GW)   │  │ (Lambda)   │  │ (Aurora)   │     │    │
│  │  └────────────┘  └────────────┘  └────────────┘     │    │
│  │  AZ: us-east-1a     us-east-1b      us-east-1c      │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                               │
│  Cross-Region Replication ──────────────────────────┐       │
└───────────────────────────────────────────────────┼─────────┘
                                                     │
┌────────────────────────────────────────────────────▼─────────┐
│                   us-west-2 (Secondary)                       │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  VPC: 10.1.0.0/16                                     │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │    │
│  │  │ Public     │  │ Private    │  │ Data       │     │    │
│  │  │ Subnet     │  │ Subnet     │  │ Subnet     │     │    │
│  │  │ (Standby)  │  │ (Standby)  │  │ (Read      │     │    │
│  │  │            │  │            │  │  Replica)  │     │    │
│  │  └────────────┘  └────────────┘  └────────────┘     │    │
│  └──────────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────────┘
```

### 3.2 Serverless Lambda Configuration

```python
# lambda_config.yaml
functions:
  analyze_scenario:
    runtime: python3.11
    memory: 3008  # MB (max for Lambda)
    timeout: 300  # seconds (5 minutes)
    environment:
      MECHANISM_BANK_VERSION: "1.0"
      DATABASE_URL: "${ssm:/prod/database_url}"
      CACHE_ENDPOINT: "${ssm:/prod/redis_endpoint}"
    layers:
      - numpy-scipy-layer  # Pre-built scientific Python libraries
      - custom-models-layer
    concurrency:
      reserved: 50  # Guarantee capacity for critical functions
      provisioned: 10  # Keep warm instances
  
  monte_carlo_simulation:
    runtime: python3.11
    memory: 10240  # Use container (Lambda can't exceed 10GB)
    timeout: 900  # 15 minutes
    container_image: ${ECR_REPO}/monte-carlo:latest
    architecture: arm64  # Graviton2 for cost savings
  
  geographic_context:
    runtime: python3.11
    memory: 1024
    timeout: 60
    cache_ttl: 3600  # Cache results for 1 hour
```

### 3.3 Auto-Scaling Configuration

```yaml
# auto_scaling.yaml
api_gateway:
  throttle_settings:
    rate_limit: 10000  # requests per second
    burst_limit: 5000
  
lambda_concurrency:
  analyze_scenario:
    target_utilization: 0.70  # Scale at 70% capacity
    min_instances: 5
    max_instances: 100
  
  monte_carlo_simulation:
    target_utilization: 0.80
    min_instances: 0  # Cold start acceptable for background job
    max_instances: 50
  
aurora_auto_scaling:
  min_capacity: 2  # ACUs (Aurora Capacity Units)
  max_capacity: 64
  target_cpu: 70  # Scale when CPU > 70%
  target_connections: 90  # Scale when connections > 90% max
```

---

## 4. Network Architecture

### 4.1 API Design

**RESTful API Endpoints**:

```
POST   /api/v1/scenarios
  → Create new intervention scenario
  Request: {geography, population, intervention, time_horizon}
  Response: {scenario_id, status: "processing"}

GET    /api/v1/scenarios/{scenario_id}
  → Retrieve scenario results
  Response: {scenario_id, status: "complete", results: {...}}

GET    /api/v1/mechanisms
  → List available mechanisms
  Query params: ?geography=boston&limit=100
  Response: {mechanisms: [...], total: 2000}

POST   /api/v1/calibration
  → Trigger geography calibration
  Request: {geography, observed_endpoints}
  Response: {calibration_id, status: "processing"}

GET    /api/v1/comparisons
  → Compare multiple scenarios
  Query params: ?scenario_ids=123,456,789
  Response: {comparison: {...}}

WebSocket: /ws/simulations/{scenario_id}
  → Real-time progress updates for long-running simulations
```

**API Response Format**:
```json
{
  "status": "success" | "processing" | "error",
  "data": {...},
  "metadata": {
    "request_id": "uuid",
    "timestamp": "2026-01-15T10:30:00Z",
    "version": "1.0",
    "computation_time_ms": 1250
  },
  "links": {
    "self": "/api/v1/scenarios/123",
    "results": "/api/v1/scenarios/123/results",
    "sensitivity": "/api/v1/scenarios/123/sensitivity"
  }
}
```

### 4.2 Authentication & Authorization

```python
# AWS Cognito User Pools
authentication:
  provider: AWS Cognito
  user_pools:
    - name: public-users
      mfa_required: false
      password_policy:
        min_length: 12
        require_uppercase: true
        require_numbers: true
        require_symbols: true
    
    - name: organizational-users
      mfa_required: true  # SMS or TOTP
      federation: SAML  # Enterprise SSO integration
  
  jwt_validation:
    issuer: https://cognito-idp.us-east-1.amazonaws.com/{UserPoolId}
    audience: client_id
    algorithm: RS256

authorization:
  model: RBAC  # Role-Based Access Control
  roles:
    - free_tier:
        rate_limit: 100/day
        concurrent_scenarios: 1
        features: [basic_analysis, limited_geography]
    
    - pro_tier:
        rate_limit: 1000/day
        concurrent_scenarios: 5
        features: [full_analysis, all_geographies, sensitivity_analysis]
    
    - enterprise:
        rate_limit: unlimited
        concurrent_scenarios: 50
        features: [all, api_access, custom_mechanisms]
```

### 4.3 Rate Limiting

```python
# Redis-based rate limiting
from redis import Redis
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
    
    def check_rate_limit(self, user_id: str, tier: str) -> bool:
        """
        Token bucket algorithm for rate limiting
        """
        limits = {
            "free_tier": {"requests": 100, "window": 86400},  # 100/day
            "pro_tier": {"requests": 1000, "window": 86400},
            "enterprise": {"requests": 100000, "window": 86400}
        }
        
        limit_config = limits[tier]
        key = f"rate_limit:{user_id}:{datetime.now().date()}"
        
        # Increment request counter
        current_count = self.redis.incr(key)
        
        # Set expiration on first request
        if current_count == 1:
            self.redis.expire(key, limit_config["window"])
        
        # Check if limit exceeded
        if current_count > limit_config["requests"]:
            return False
        
        return True
```

### 4.4 Security Measures

```yaml
security:
  encryption:
    in_transit: TLS 1.3
    at_rest:
      database: AES-256 (AWS KMS)
      s3_storage: AES-256 (SSE-S3)
      secrets: AWS Secrets Manager
  
  network:
    vpc_isolation: Private subnets for compute and data layers
    security_groups:
      - lambda_sg:
          egress: database_sg, redis_sg, internet (HTTPS only)
          ingress: api_gateway only
      
      - database_sg:
          egress: none
          ingress: lambda_sg only
    
    ddos_protection: AWS Shield Standard + WAF rules
  
  compliance:
    hipaa_eligible: true  # Aurora, S3, Lambda all HIPAA-eligible
    data_residency: US-only (no cross-border data transfer)
    audit_logging: CloudTrail + CloudWatch Logs
  
  vulnerability_management:
    dependency_scanning: Snyk (weekly)
    container_scanning: AWS ECR scanning
    penetration_testing: Annual third-party audit
```

---

## 5. Data Storage Architecture

### 5.1 PostgreSQL Schema Design

```sql
-- Users and organizations
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    tier VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE organizations (
    org_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(50),
    user_limit INTEGER
);

-- Mechanism bank (versioned)
CREATE TABLE mechanism_bank_versions (
    version VARCHAR(20) PRIMARY KEY,
    release_date DATE,
    total_mechanisms INTEGER,
    changelog TEXT
);

CREATE TABLE mechanisms (
    mechanism_id VARCHAR(100) PRIMARY KEY,
    version VARCHAR(20) REFERENCES mechanism_bank_versions(version),
    source_node VARCHAR(100),
    target_node VARCHAR(100),
    effect_quantification JSONB,  -- Store complex nested data
    moderators JSONB,
    supporting_studies JSONB,
    created_at TIMESTAMP
);

-- Scenarios and results
CREATE TABLE scenarios (
    scenario_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    geography JSONB,
    population JSONB,
    intervention JSONB,
    status VARCHAR(50),
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE scenario_results (
    result_id UUID PRIMARY KEY,
    scenario_id UUID REFERENCES scenarios(scenario_id),
    results JSONB,  -- Full result object
    computation_time_ms INTEGER,
    created_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_scenarios_user ON scenarios(user_id);
CREATE INDEX idx_mechanisms_version ON mechanisms(version);
CREATE INDEX idx_mechanisms_nodes ON mechanisms USING GIN (source_node, target_node);
CREATE INDEX idx_results_scenario ON scenario_results(scenario_id);
```

### 5.2 S3 Storage Structure

```
s3://health-systems-platform-prod/
├── mechanism-bank/
│   ├── versions/
│   │   ├── 1.0/
│   │   │   ├── mechanisms.json
│   │   │   ├── nodes.json
│   │   │   └── metadata.json
│   │   └── 1.1/
│   └── literature/
│       ├── pdfs/
│       │   ├── smith_2022.pdf
│       │   └── jones_2020.pdf
│       └── embeddings/
│           └── corpus_v1.pkl
├── user-data/
│   ├── {user_id}/
│   │   ├── scenarios/
│   │   │   └── {scenario_id}.json
│   │   └── reports/
│   │       └── {report_id}.pdf
└── logs/
    └── {date}/
        └── api_logs.json.gz
```

### 5.3 Caching Strategy

```python
# Redis caching layers
from redis import Redis
import json
import hashlib

class CacheManager:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
    
    def cache_mechanism_bank(self, version: str, mechanisms: list):
        """
        Cache entire mechanism bank for version (TTL: 1 week)
        """
        key = f"mechanism_bank:{version}"
        self.redis.setex(
            key,
            604800,  # 1 week in seconds
            json.dumps(mechanisms)
        )
    
    def cache_geography_context(self, geography: dict, context: dict):
        """
        Cache geographic context (TTL: 1 day, refreshes daily)
        """
        geo_hash = hashlib.md5(json.dumps(geography, sort_keys=True).encode()).hexdigest()
        key = f"geo_context:{geo_hash}"
        self.redis.setex(key, 86400, json.dumps(context))
    
    def cache_scenario_result(self, scenario_id: str, result: dict):
        """
        Cache completed scenario results (TTL: 30 days)
        """
        key = f"scenario_result:{scenario_id}"
        self.redis.setex(key, 2592000, json.dumps(result))
    
    def get_cached(self, key: str):
        """
        Retrieve cached value
        """
        value = self.redis.get(key)
        return json.loads(value) if value else None
```

---

## 6. Performance Optimization

### 6.1 Computation Optimization

**Mechanism Caching**:
```python
# Pre-compute mechanism flows for common stock values
def build_mechanism_lookup_table(mechanism):
    """
    Cache flow values for sigmoid/logarithmic functions
    """
    if mechanism['functional_form'] == 'sigmoid':
        lookup = {}
        for s_i in np.arange(0, 1.01, 0.01):  # 0 to 1 in 0.01 increments
            lookup[round(s_i, 2)] = calculate_sigmoid_flow(s_i, mechanism['parameters'])
        
        return lookup
    
    # Linear mechanisms: no caching needed (direct calculation faster)
    return None
```

**Sparse Network Representation**:
```python
# Only activate mechanisms where stock changes occur
class SparseNetwork:
    def __init__(self, mechanisms):
        self.mechanisms = mechanisms
        self.active_mechanisms = set()
    
    def update_active_mechanisms(self, changed_stocks):
        """
        Only process mechanisms connected to changed stocks
        """
        self.active_mechanisms.clear()
        
        for stock in changed_stocks:
            # Find mechanisms where this stock is source
            outgoing = [m for m in self.mechanisms if m['source_node'] == stock]
            self.active_mechanisms.update(outgoing)
    
    def calculate_flows(self, stocks):
        """
        Only calculate flows for active mechanisms
        """
        flows = {}
        for mechanism in self.active_mechanisms:
            flows[mechanism['mechanism_id']] = calculate_flow(stocks, mechanism)
        
        return flows
```

**Parallel Monte Carlo**:
```python
from multiprocessing import Pool
import numpy as np

def run_monte_carlo_parallel(scenario, n_simulations=1000, n_workers=8):
    """
    Distribute Monte Carlo simulations across workers
    """
    # Split simulations across workers
    sims_per_worker = n_simulations // n_workers
    
    # Create parameter sets for each simulation
    param_sets = [
        {
            'scenario': scenario,
            'seed': seed,
            'n_sims': sims_per_worker
        }
        for seed in range(n_workers)
    ]
    
    # Execute in parallel
    with Pool(processes=n_workers) as pool:
        results = pool.map(run_simulation_batch, param_sets)
    
    # Aggregate results
    all_outcomes = np.concatenate([r['outcomes'] for r in results])
    
    return {
        'median': np.median(all_outcomes, axis=0),
        'ci_95': [
            np.percentile(all_outcomes, 2.5, axis=0),
            np.percentile(all_outcomes, 97.5, axis=0)
        ]
    }
```

### 6.2 Database Query Optimization

```sql
-- Use materialized views for expensive aggregations
CREATE MATERIALIZED VIEW scenario_summary AS
SELECT 
    user_id,
    DATE(created_at) as date,
    COUNT(*) as scenarios_created,
    AVG(computation_time_ms) as avg_computation_time
FROM scenarios
GROUP BY user_id, DATE(created_at);

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY scenario_summary;

-- Partition large tables by date
CREATE TABLE scenario_results_2026 PARTITION OF scenario_results
FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
```

### 6.3 CDN & Edge Caching

```yaml
cloudfront_config:
  distribution:
    price_class: PriceClass_100  # US, Canada, Europe
    default_ttl: 86400  # 1 day
    min_ttl: 0
    max_ttl: 31536000  # 1 year
  
  cache_behaviors:
    - path: /api/v1/mechanisms
      ttl: 3600  # Cache mechanism lists for 1 hour
      compress: true
    
    - path: /api/v1/scenarios/*
      ttl: 0  # Don't cache user-specific scenarios
    
    - path: /static/*
      ttl: 604800  # Cache static assets for 1 week
```

---

## 7. Monitoring & Observability

### 7.1 Metrics Collection

```python
# CloudWatch custom metrics
from datadog import statsd

class MetricsCollector:
    @staticmethod
    def record_api_latency(endpoint: str, duration_ms: float):
        statsd.histogram('api.latency', duration_ms, tags=[f'endpoint:{endpoint}'])
    
    @staticmethod
    def record_simulation_success(scenario_type: str):
        statsd.increment('simulation.success', tags=[f'type:{scenario_type}'])
    
    @staticmethod
    def record_cache_hit(cache_type: str):
        statsd.increment('cache.hit', tags=[f'type:{cache_type}'])
    
    @staticmethod
    def record_error(error_type: str, severity: str):
        statsd.increment('errors', tags=[f'type:{error_type}', f'severity:{severity}'])
```

### 7.2 Alerting Rules

```yaml
alerts:
  - name: high_error_rate
    condition: error_rate > 5%
    window: 5 minutes
    severity: critical
    action: page_on_call_engineer
  
  - name: slow_api_response
    condition: p95_latency > 3000ms
    window: 10 minutes
    severity: warning
    action: notify_slack
  
  - name: database_connections_high
    condition: connection_count > 90% max
    window: 5 minutes
    severity: warning
    action: auto_scale_aurora
  
  - name: lambda_throttling
    condition: throttle_rate > 1%
    window: 5 minutes
    severity: warning
    action: increase_reserved_concurrency
```

### 7.3 Logging Strategy

```python
import structlog
import json

# Structured logging for machine-readable logs
logger = structlog.get_logger()

def log_scenario_creation(user_id, scenario_id, geography):
    logger.info(
        "scenario_created",
        user_id=user_id,
        scenario_id=scenario_id,
        geography=geography,
        timestamp=datetime.now().isoformat()
    )

def log_computation_time(scenario_id, duration_ms, success):
    logger.info(
        "computation_completed",
        scenario_id=scenario_id,
        duration_ms=duration_ms,
        success=success
    )

# Logs shipped to CloudWatch → Datadog for analysis
```

---

## 8. Disaster Recovery & Backup

### 8.1 Backup Strategy

```yaml
backups:
  database:
    type: automated_snapshots
    frequency: daily
    retention: 30 days
    point_in_time_recovery: enabled  # 5-minute RPO
  
  s3_data:
    type: versioning + replication
    destination: us-west-2  # Cross-region replication
    lifecycle:
      - transition_to_glacier: 90 days
      - expire_non_current: 365 days
  
  mechanism_bank:
    type: git_repository + s3_backup
    frequency: on_every_update
    retention: all_versions (permanent)
```

### 8.2 Failover Procedures

```
Primary Region Failure (us-east-1):
  1. Route53 health check detects failure
  2. DNS automatically fails over to us-west-2 (30-60 seconds)
  3. Aurora read replica promoted to primary (2-5 minutes)
  4. Lambda functions cold-start in secondary region (~30 seconds)
  5. Total downtime: ~3-6 minutes
  
Database Failure:
  1. Aurora automatic failover to standby (~30 seconds)
  2. Application retries connection with exponential backoff
  3. If failover fails, promote read replica (manual, ~5 minutes)
```

---

## 9. Cost Optimization

### 9.1 Estimated Monthly Costs (1000 Active Users)

```
AWS Lambda (compute):
  - API requests: 5M invocations × $0.20/1M = $1.00
  - Compute time: 100k GB-seconds × $0.0000166667 = $1.67
  Subtotal: $2.67

Aurora PostgreSQL:
  - 2 ACUs average × $0.12/ACU-hour × 730 hours = $175.20
  - Storage: 100 GB × $0.10/GB = $10.00
  Subtotal: $185.20

ElastiCache Redis:
  - cache.t3.medium (1 node) × $0.068/hour × 730 hours = $49.64

S3 Storage:
  - 500 GB × $0.023/GB = $11.50
  - GET requests: 10M × $0.0004/1000 = $4.00
  Subtotal: $15.50

API Gateway:
  - 5M requests × $3.50/1M = $17.50

CloudFront:
  - Data transfer: 1 TB × $0.085/GB = $85.00

Monitoring (Datadog):
  - 10 hosts × $15/host = $150.00

TOTAL: ~$505/month for 1000 active users
       ~$0.50 per user per month
```

### 9.2 Cost Reduction Strategies

```python
# 1. Lambda reserved concurrency (save 40% on predictable load)
reserve_lambda_capacity(
    function='analyze_scenario',
    instances=10,
    discount='40%'
)

# 2. Aurora Serverless v2 (pay only for usage)
configure_aurora_scaling(
    min_capacity=0.5,  # Scale down to 0.5 ACU when idle
    max_capacity=64,
    auto_pause=True    # Pause after 5 minutes inactivity
)

# 3. S3 Intelligent-Tiering (auto-move cold data to cheaper tiers)
enable_s3_intelligent_tiering(
    bucket='mechanism-bank-prod',
    access_tiers=['frequent', 'infrequent', 'archive']
)

# 4. Spot instances for batch jobs (save 70%)
use_spot_instances(
    job_type='monte_carlo_simulation',
    max_price='$0.10/hour',
    fallback_to_on_demand=True
)
```

---

## 10. MVP Implementation Priorities

**Phase 1 (MVP)**:
- Single-region deployment (us-east-1)
- Serverless architecture (Lambda + Aurora Serverless)
- PostgreSQL for relational data, S3 for files
- Redis caching for mechanism bank and geography context
- Basic monitoring (CloudWatch)
- API rate limiting (100 requests/day free tier)
- HTTPS/TLS encryption

**Phase 2 Enhancements**:
- Multi-region deployment with automatic failover
- Advanced caching strategies (edge locations)
- Horizontal scaling for high concurrency (1000+ simultaneous users)
- Real-time WebSocket connections for simulation progress
- GraphQL API (alongside REST)
- Advanced monitoring (Datadog, custom dashboards)
- HIPAA compliance certification

---

## 11. Integration with System Components

**Provides Infrastructure For**:
- `15_USER_INTERFACE_WORKFLOWS.md`: Frontend hosting, API endpoints
- `07_TIME_SIMULATION_FRAMEWORK.md`: Compute resources for Monte Carlo
- `09-11_LLM_*`: Storage for mechanism bank, literature corpus
- `13_INITIAL_STATE_CALIBRATION.md`: Database for calibration results

**Dependencies On**:
- All technical documents (provides compute/storage for their specifications)

---

**Document Version**: 1.0  
**Cross-References**: All technical documents (provides infrastructure)  
**Status**: Technical specification for MVP implementation
