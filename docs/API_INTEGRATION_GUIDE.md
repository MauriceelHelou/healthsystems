# API Integration Guide for HealthSystems Platform

## Overview

This guide documents all external APIs integrated into the HealthSystems Platform for mechanism discovery, literature search, and data retrieval related to social determinants of health.

---

## Table of Contents

1. [Literature Search APIs](#literature-search-apis)
2. [Public Health Data APIs](#public-health-data-apis)
3. [Economic & Social Data APIs](#economic--social-data-apis)
4. [Environmental Data APIs](#environmental-data-apis)
5. [Healthcare System APIs](#healthcare-system-apis)
6. [API Key Management](#api-key-management)
7. [Rate Limiting & Best Practices](#rate-limiting--best-practices)

---

## Literature Search APIs

### 1. Semantic Scholar API

**Purpose**: Search academic literature for mechanism discovery

**Registration**: https://www.semanticscholar.org/product/api

**Rate Limits**:
- Without API key: 100 requests per 5 minutes
- With API key: Higher limits (contact Semantic Scholar)

**Base URL**: `https://api.semanticscholar.org/graph/v1`

**Key Endpoints**:
- `/paper/search` - Search for papers by query
- `/paper/{paperId}` - Get paper details
- `/paper/DOI:{doi}` - Look up paper by DOI

**Implementation**: See [backend/pipelines/literature_search.py](../backend/pipelines/literature_search.py)

**Configuration**:
```bash
SEMANTIC_SCHOLAR_API_KEY=your_key_here  # Optional
```

**Example Usage**:
```python
from backend.pipelines.literature_search import SemanticScholarSearch

client = SemanticScholarSearch(api_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY"))
papers = client.search_papers(
    query="housing quality respiratory health",
    limit=10,
    year_range=(2010, 2024),
    min_citations=10
)
```

---

### 2. PubMed E-utilities API

**Purpose**: Search biomedical and life sciences literature

**Registration**: No API key required (but recommended)
- Get API key: https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

**Rate Limits**:
- Without API key: 3 requests per second
- With API key: 10 requests per second

**Base URL**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils`

**Key Endpoints**:
- `/esearch.fcgi` - Search for PMIDs
- `/efetch.fcgi` - Fetch paper details
- `/esummary.fcgi` - Get paper summaries

**Implementation**: See [backend/pipelines/literature_search.py](../backend/pipelines/literature_search.py)

**Configuration**:
```bash
PUBMED_EMAIL=your_email@example.com  # Recommended
PUBMED_API_KEY=your_key_here         # Optional
```

**Example Usage**:
```python
from backend.pipelines.literature_search import PubMedSearch

client = PubMedSearch(
    email=os.getenv("PUBMED_EMAIL"),
    api_key=os.getenv("PUBMED_API_KEY")
)
papers = client.search_papers(
    query="social determinants cardiovascular disease",
    limit=20,
    min_date="2015/01/01"
)
```

---

## Public Health Data APIs

### 3. CDC WONDER API

**Purpose**: Access vital statistics, mortality, natality, and cancer data

**Registration**: No API key required

**Rate Limits**:
- **1 request per 2 minutes recommended** (per CDC documentation)
- Use sequential queries only (no parallel requests)

**Base URL**: `https://wonder.cdc.gov/controller/datarequest/{database_id}`

**Available Databases**:
- `D76` - Detailed Mortality 1999-2013
- `D77` - Detailed Mortality 2013+
- `D149` - Natality (births) data
- `D66` - Cancer incidence
- Additional databases listed at: https://wonder.cdc.gov/

**Request Format**: XML POST with `request_xml` parameter

**Key Limitations**:
- ⚠️ **Only national data available** via API
- Cannot filter or group by Region, Division, State, County, or Urbanization
- For geographic queries, use the web interface instead

**Implementation**: See [backend/pipelines/cdc_wonder_api.py](../backend/pipelines/cdc_wonder_api.py) (to be created)

**Configuration**:
```bash
CDC_WONDER_ENABLED=true
CDC_WONDER_RATE_LIMIT_SECONDS=120  # 2 minutes between requests
```

**XML Request Structure**:
```xml
<request-parameters>
    <accept_datause_restrictions>true</accept_datause_restrictions>
    <parameter>
        <name>B_1</name>  <!-- Group by variables -->
        <value>D76.V1-level1</value>  <!-- e.g., by year -->
    </parameter>
    <parameter>
        <name>M_1</name>  <!-- Measures -->
        <value>D76.M1</value>  <!-- e.g., deaths -->
    </parameter>
    <parameter>
        <name>F_D76.V1</name>  <!-- Filter parameters -->
        <value>2015 2016 2017</value>  <!-- e.g., year range -->
    </parameter>
    <parameter>
        <name>V_D76.V2</name>  <!-- ICD-10 codes -->
        <value>I00-I99</value>  <!-- e.g., cardiovascular diseases -->
    </parameter>
</request-parameters>
```

**Example Usage** (Python):
```python
import requests
import xml.etree.ElementTree as ET

xml_request = """
<request-parameters>
    <accept_datause_restrictions>true</accept_datause_restrictions>
    <!-- Add your parameters here -->
</request-parameters>
"""

response = requests.post(
    "https://wonder.cdc.gov/controller/datarequest/D76",
    data={"request_xml": xml_request}
)

root = ET.fromstring(response.content)
# Parse response XML
```

**Getting Parameter Codes**:
1. Use the CDC WONDER web interface to build your query
2. Click "API Options" button after viewing results
3. Download the XML request file to see correct parameter codes

**References**:
- Official Documentation: https://wonder.cdc.gov/wonder/help/wonder-api.html
- Python Examples: https://github.com/alipphardt/cdc-wonder-api

---

### 4. U.S. Census Bureau API

**Purpose**: Demographic, economic, housing, and social determinant data

**Registration**: https://api.census.gov/data/key_signup.html

**Rate Limits**: No strict published limits, but be respectful

**Base URL**: `https://api.census.gov/data`

**Key Datasets**:

#### American Community Survey (ACS) 5-Year
- **Endpoint**: `/data/{year}/acs/acs5`
- **Years Available**: 2009-2023
- **Geographic Levels**: Nation, state, county, tract, block group
- **Key Variables**:
  - `B19013_001E` - Median household income
  - `B17001_002E` - Population below poverty level
  - `B25003_001E` - Housing tenure (owner vs renter)
  - `B27001_001E` - Health insurance coverage
  - `B15003_001E` - Educational attainment
  - `B23025_005E` - Unemployment rate

#### Decennial Census
- **Endpoint**: `/data/{year}/dec/pl` (redistricting data)
- **Years Available**: 2020, 2010, 2000

#### Small Area Income and Poverty Estimates (SAIPE)
- **Endpoint**: `/data/{year}/saipe`
- **Provides**: Poverty and income estimates for school districts, counties, states

**Configuration**:
```bash
CENSUS_API_KEY=b65604fd7d0ed35af2b201eba907348c10c3f6d8
```

**Example Usage**:
```python
import requests

# Get poverty rate by county in Massachusetts
response = requests.get(
    "https://api.census.gov/data/2021/acs/acs5",
    params={
        "get": "NAME,B17001_002E,B17001_001E",  # Below poverty, total pop
        "for": "county:*",
        "in": "state:25",  # Massachusetts FIPS code
        "key": os.getenv("CENSUS_API_KEY")
    }
)

data = response.json()
```

**Variable Discovery**:
- Browse variables: https://api.census.gov/data/2021/acs/acs5/variables.html
- ACS Subject Tables: https://www.census.gov/programs-surveys/acs/data/data-tables.html

---

### 5. CDC Data API (PLACES, BRFSS, NHANES)

**Purpose**: Local health data, behavioral risk factors, nutrition data

**Registration**: https://data.cdc.gov/profile/edit/developer_settings

**Rate Limits**: No strict published limits

**Base URL**: `https://data.cdc.gov/resource/`

**Key Datasets**:

#### PLACES (Local Data for Better Health)
- **Dataset ID**: `cwsq-ngmh` (500 Cities) or updated PLACES datasets
- **Geographic Levels**: Census tract, county, state
- **Measures**: Prevalence of chronic diseases, preventive services, health behaviors
- **Example Endpoint**: `https://data.cdc.gov/resource/cwsq-ngmh.json`

#### BRFSS (Behavioral Risk Factor Surveillance System)
- **Dataset ID**: Varies by year
- **State-level health behavior data**

**Configuration**:
```bash
CDC_API_KEY=your_key_here
```

**Example Usage** (SODA API):
```python
import requests

response = requests.get(
    "https://data.cdc.gov/resource/cwsq-ngmh.json",
    params={
        "stateabbr": "MA",
        "measure": "Obesity",
        "$limit": 1000
    },
    headers={"X-App-Token": os.getenv("CDC_API_KEY")}
)

data = response.json()
```

---

## Economic & Social Data APIs

### 6. Bureau of Labor Statistics (BLS) API

**Purpose**: Employment, unemployment, wages, occupational data

**Registration**: https://data.bls.gov/registrationEngine/

**Rate Limits**:
- Version 1.0 (no key): 25 queries per day, 10 years per query
- Version 2.0 (with key): 500 queries per day, 20 years per query

**Base URL**: `https://api.bls.gov/publicAPI/v2/timeseries/data/`

**Key Series**:
- `LNS14000000` - Unemployment rate (national)
- `LAUCN{fips}000000003` - County unemployment rate
- `CUUR0000SA0` - Consumer Price Index (CPI)
- `CES0000000001` - Total nonfarm employment

**Configuration**:
```bash
BLS_API_KEY=your_key_here
```

**Example Usage**:
```python
import requests

response = requests.post(
    "https://api.bls.gov/publicAPI/v2/timeseries/data/",
    json={
        "seriesid": ["LNS14000000"],
        "startyear": "2015",
        "endyear": "2023",
        "registrationkey": os.getenv("BLS_API_KEY")
    }
)

data = response.json()
```

---

## Environmental Data APIs

### 7. EPA Air Quality System (AQS) API

**Purpose**: Air quality monitoring data, pollutant concentrations

**Registration**: https://aqs.epa.gov/aqsweb/documents/data_api.html

**Rate Limits**:
- 10 requests per minute
- 500 requests per hour

**Base URL**: `https://aqs.epa.gov/data/api`

**Key Endpoints**:
- `/dailyData/byCounty` - Daily air quality by county
- `/annualData/byState` - Annual summaries by state
- `/monitors/byCounty` - Monitor locations

**Configuration**:
```bash
EPA_AQS_EMAIL=your_email@example.com
EPA_AQS_KEY=your_key_here
```

**Example Usage**:
```python
import requests

response = requests.get(
    "https://aqs.epa.gov/data/api/dailyData/byCounty",
    params={
        "email": os.getenv("EPA_AQS_EMAIL"),
        "key": os.getenv("EPA_AQS_KEY"),
        "param": "44201",  # Ozone
        "bdate": "20230101",
        "edate": "20231231",
        "state": "25",  # Massachusetts
        "county": "025"  # Suffolk County
    }
)

data = response.json()
```

---

## Healthcare System APIs

### 8. CMS (Centers for Medicare & Medicaid Services) API

**Purpose**: Healthcare utilization, quality, cost data

**Base URL**: `https://data.cms.gov/data-api/v1/dataset`

**Key Datasets**:
- Hospital Compare data
- Medicare spending by geographic area
- Quality metrics (readmissions, mortality rates)
- Provider directories

**Configuration**:
```bash
CMS_API_KEY=your_key_here
```

**Example Usage**:
```python
import requests

response = requests.get(
    "https://data.cms.gov/data-api/v1/dataset/xubh-q36u/data",
    params={
        "filter[state]": "MA",
        "size": 100
    }
)

data = response.json()
```

---

### 9. HRSA Data Warehouse API

**Purpose**: Health workforce, HPSA designations, medically underserved areas

**Registration**: https://data.hrsa.gov/tools/apis

**Key Data**:
- Health Professional Shortage Areas (HPSA)
- Medically Underserved Areas/Populations (MUA/P)
- Health workforce supply
- Health center locations

**Configuration**:
```bash
HRSA_API_KEY=your_key_here
```

---

### 10. HUD (Housing and Urban Development) API

**Purpose**: Housing assistance, fair market rents, income limits

**Registration**: https://www.huduser.gov/portal/dataset/api-terms.html

**Key Datasets**:
- Fair Market Rents (FMR)
- Income Limits
- Comprehensive Housing Affordability Strategy (CHAS)

**Configuration**:
```bash
HUD_API_KEY=your_key_here
```

**Example Usage**:
```python
import requests

# Get Fair Market Rents for Boston metro area
response = requests.get(
    f"https://www.huduser.gov/hudapi/public/fmr/data/{zip_code}",
    params={"year": 2023},
    headers={"Authorization": f"Bearer {os.getenv('HUD_API_KEY')}"}
)

data = response.json()
```

---

## API Key Management

### Environment Variables

All API keys should be stored in environment variables, never committed to version control.

**Setup**:
1. Copy `.env.example` to `.env`
2. Fill in your API keys
3. Add `.env` to `.gitignore` (already done)

**Backend** (`.env`):
```bash
# Literature Search
SEMANTIC_SCHOLAR_API_KEY=your_key
PUBMED_API_KEY=your_key
PUBMED_EMAIL=your_email@example.com

# Public Health
CENSUS_API_KEY=b65604fd7d0ed35af2b201eba907348c10c3f6d8
CDC_API_KEY=your_key
CDC_WONDER_ENABLED=true

# Environmental
EPA_AQS_EMAIL=your_email
EPA_AQS_KEY=your_key

# Economic
BLS_API_KEY=your_key

# Healthcare
CMS_API_KEY=your_key
HRSA_API_KEY=your_key
HUD_API_KEY=your_key
```

### Loading in Python

```python
import os
from dotenv import load_dotenv

load_dotenv()

census_key = os.getenv("CENSUS_API_KEY")
```

---

## Rate Limiting & Best Practices

### Rate Limiting Strategy

Implement rate limiting for all external APIs to avoid being blocked:

```python
import time
from functools import wraps

def rate_limit(calls_per_minute: int):
    """Decorator to rate limit API calls"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed

            if left_to_wait > 0:
                time.sleep(left_to_wait)

            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret

        return wrapper
    return decorator

# Example usage
@rate_limit(calls_per_minute=30)  # CDC WONDER: 1 call per 2 min = 0.5 calls/min
def query_cdc_wonder(xml_request: str):
    # API call implementation
    pass
```

### API-Specific Rate Limits

| API | Rate Limit | Strategy |
|-----|------------|----------|
| Semantic Scholar | 100 req / 5 min | 1 second between requests |
| PubMed | 3-10 req/sec | 0.5 second delay (safe) |
| CDC WONDER | 1 req / 2 min | **120 second delay** |
| Census | No strict limit | 1 second between requests |
| BLS | 500 req/day | Track daily count |
| EPA AQS | 10 req/min | 6 second delay |

### Error Handling

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session_with_retries():
    """Create requests session with automatic retries"""
    session = requests.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=2,  # Wait 2, 4, 8 seconds
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session
```

### Caching Strategy

Cache API responses to minimize external calls:

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_api_response(ttl_seconds: int = 3600):
    """Cache API responses in Redis"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{json.dumps(args)}:{json.dumps(kwargs)}"

            # Check cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Call API
            result = func(*args, **kwargs)

            # Store in cache
            redis_client.setex(
                cache_key,
                ttl_seconds,
                json.dumps(result)
            )

            return result

        return wrapper
    return decorator
```

### Best Practices

1. **Use API keys when available** - Higher rate limits, better support
2. **Respect rate limits** - Implement delays and retries
3. **Cache aggressively** - Reduce load and improve performance
4. **Handle errors gracefully** - Retry with exponential backoff
5. **Monitor usage** - Track API calls and quotas
6. **Batch requests** - Use bulk endpoints when available
7. **Document your use** - Some APIs require citation/attribution

---

## Summary of APIs Used in Current Pipelines

### Literature Search Pipeline
- **Semantic Scholar**: Academic paper search
- **PubMed**: Biomedical literature search
- Status: ✅ Implemented in `backend/pipelines/literature_search.py`

### LLM Mechanism Discovery Pipeline
- **Anthropic Claude API**: Mechanism extraction from papers
- Status: ✅ Implemented in `backend/pipelines/llm_mechanism_discovery.py`

### Data Pipelines (To Be Implemented)
- **Census API**: Social determinant data retrieval
- **CDC WONDER**: Mortality and vital statistics
- **EPA AQS**: Environmental exposure data
- **BLS**: Economic indicators
- Status: 🔄 Integration modules to be created

---

## Next Steps

1. ✅ Update `.env.example` files with all API configurations
2. 🔄 Create CDC WONDER integration module (`backend/pipelines/cdc_wonder_api.py`)
3. 🔄 Create Census API integration module (`backend/pipelines/census_api.py`)
4. 🔄 Create EPA AQS integration module (`backend/pipelines/epa_aqs_api.py`)
5. 🔄 Create unified data retrieval pipeline combining all sources
6. 🔄 Add API usage monitoring and quota tracking
7. 🔄 Write integration tests for each API client

---

## References

- Semantic Scholar API: https://api.semanticscholar.org/
- PubMed E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- CDC WONDER API: https://wonder.cdc.gov/wonder/help/wonder-api.html
- Census API: https://www.census.gov/data/developers/guidance.html
- BLS API: https://www.bls.gov/developers/
- EPA AQS API: https://aqs.epa.gov/aqsweb/documents/data_api.html

---

**Last Updated**: 2025-01-22
