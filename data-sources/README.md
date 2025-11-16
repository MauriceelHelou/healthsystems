# Data Sources

ETL pipelines and API integrations for contextual data collection.

## Overview

The data-sources module provides automated collection of geographic, demographic, environmental, and economic data to contextualize mechanism weights. All scrapers respect rate limits and cache data to minimize API calls.

## Directory Structure

```
data-sources/
├── scrapers/          # Web scrapers for various data sources
│   ├── census/        # U.S. Census Bureau data
│   ├── cdc/           # CDC health outcome data
│   ├── epa/           # Environmental Protection Agency
│   ├── bls/           # Bureau of Labor Statistics
│   └── other/         # Additional data sources
├── apis/              # API client modules
├── configs/           # Data source configurations and metadata
├── cache/             # Cached data (gitignored)
├── tests/             # Tests for scrapers and APIs
└── utils/             # Shared utilities
```

## Data Sources

### 1. U.S. Census Bureau
- **Data**: Demographics, housing, income, education
- **API**: Census API (requires API key)
- **Geographies**: Nation, state, county, tract, block group
- **Update frequency**: Annual (ACS), Decennial (Census)

### 2. CDC PLACES
- **Data**: Health outcomes, risk factors, prevention measures
- **API**: CDC PLACES API
- **Geographies**: County, city, census tract
- **Update frequency**: Annual

### 3. EPA Environmental Data
- **Data**: Air quality, water quality, toxic releases
- **APIs**: AirNow API, EJSCREEN, TRI
- **Geographies**: County, zip code
- **Update frequency**: Real-time (air), annual (others)

### 4. Bureau of Labor Statistics
- **Data**: Employment, unemployment, wages, CPI
- **API**: BLS Public Data API
- **Geographies**: National, state, MSA, county
- **Update frequency**: Monthly

### 5. Additional Sources
- Housing and Urban Development (HUD)
- Department of Education
- USDA Food Access Research Atlas
- American Community Survey

## Usage

### Running Scrapers

```python
from data_sources.scrapers.census import CensusScraper

# Initialize scraper
scraper = CensusScraper(api_key="your-api-key")

# Get data for a geography
data = scraper.get_demographics(
    geography="county",
    state="MA",
    county="025"  # Suffolk County
)
```

### Using API Clients

```python
from data_sources.apis.cdc_places import CDCPlacesClient

# Initialize client
client = CDCPlacesClient()

# Get health outcomes for a location
outcomes = client.get_county_data(
    state="25",
    county="025"
)
```

### Batch Collection

```python
from data_sources.utils.batch_collector import BatchCollector

# Collect all data for a geography
collector = BatchCollector()
context_data = collector.collect_all(
    geography_type="county",
    geography_id="25025"  # FIPS code
)
```

## Configuration

Data source configurations are stored in `configs/` as YAML files:

```yaml
name: census_acs
source: U.S. Census Bureau
api_endpoint: https://api.census.gov/data
api_key_required: true
rate_limit: 500  # requests per day
variables:
  - name: poverty_rate
    code: S1701_C03_001E
    description: Percentage below poverty level
  - name: median_income
    code: S1901_C01_012E
    description: Median household income
```

## Caching

All scraped data is cached locally to minimize API calls:

- Cache location: `data-sources/cache/`
- Cache duration: Configurable per data source (default: 30 days)
- Cache format: JSON with metadata

```python
# Check cache before scraping
from data_sources.utils.cache import Cache

cache = Cache()
cached_data = cache.get(
    source="census",
    geography="25025",
    max_age_days=30
)
```

## Rate Limiting

Respect API rate limits:

- Census API: 500 requests/day
- CDC APIs: No official limit, but use reasonable delays
- EPA APIs: Varies by endpoint
- BLS API: 500 requests/day

All scrapers include automatic rate limiting and retry logic.

## Data Quality

Scrapers validate data quality:

- Check for missing values
- Verify data ranges
- Log warnings for anomalies
- Track data vintage/update dates

## Testing

```bash
# Run all scraper tests
pytest data-sources/tests/

# Test specific scraper
pytest data-sources/tests/test_census_scraper.py

# Integration tests (requires API keys)
pytest data-sources/tests/integration/ --api-keys
```

## Contributing

When adding new data sources:

1. Create scraper in appropriate subdirectory
2. Add configuration file to `configs/`
3. Implement caching and rate limiting
4. Add comprehensive tests
5. Update this README
6. Document data licensing and attribution

## Data Attribution

When using data from these sources, proper attribution is required:

- **Census**: "Data sourced from U.S. Census Bureau, American Community Survey [Year]"
- **CDC**: "Data from Centers for Disease Control and Prevention, PLACES [Year]"
- **EPA**: "Environmental data from U.S. Environmental Protection Agency"
- **BLS**: "Labor statistics from U.S. Bureau of Labor Statistics"

## API Keys

Store API keys in `.env` file (never commit!):

```bash
CENSUS_API_KEY=your-key-here
CDC_API_KEY=your-key-here
EPA_API_KEY=your-key-here
BLS_API_KEY=your-key-here
```

Apply for keys:
- Census: https://api.census.gov/data/key_signup.html
- CDC: Generally no key required
- EPA: Varies by service
- BLS: https://www.bls.gov/developers/
