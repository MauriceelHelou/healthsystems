# Full-Text Paper Access API Integration

This document describes the multi-source full-text paper retrieval system integrated into the HealthSystems mechanism discovery pipeline.

## Overview

The `FullTextFetcher` module provides unified access to academic paper full-text through a waterfall approach, trying multiple sources in priority order until one succeeds.

## Supported APIs

### 1. Unpaywall (Primary - Open Access)
- **Coverage**: 50,000+ publishers, finds legal OA versions of paywalled papers
- **Rate Limit**: 100,000 requests/day
- **Full-Text**: Links to OA PDFs hosted elsewhere
- **Authentication**: Email only (no API key)
- **Documentation**: https://unpaywall.org/products/api

```python
# Example response
{
    "is_oa": true,
    "best_oa_location": {
        "url_for_pdf": "https://...",
        "license": "cc-by",
        "host_type": "repository"
    }
}
```

### 2. PubMed Central (PMC)
- **Coverage**: 6M+ full-text articles (NIH-funded research)
- **Rate Limit**: 3 req/sec (10 req/sec with API key)
- **Full-Text**: Direct PDF and XML downloads
- **Authentication**: Email required, API key optional
- **Documentation**: https://www.ncbi.nlm.nih.gov/pmc/tools/oa-service/

### 3. Europe PMC
- **Coverage**: 9M+ full-text articles (European research)
- **Rate Limit**: Generous (unspecified)
- **Full-Text**: PDF and XML via REST API
- **Authentication**: None required
- **Documentation**: https://europepmc.org/developers

### 4. CORE
- **Coverage**: 200M+ open access papers from repositories worldwide
- **Rate Limit**: 10 req/10sec (single articles)
- **Full-Text**: Direct PDF download endpoint
- **Authentication**: API key optional (higher limits)
- **Documentation**: https://core.ac.uk/documentation/api

### 5. OpenAlex
- **Coverage**: 225M+ works with OA links when available
- **Rate Limit**: 1 req/sec (10 req/sec with email)
- **Full-Text**: Links to PDFs, not direct hosting
- **Authentication**: Email recommended (polite pool)
- **Documentation**: https://docs.openalex.org/

### 6. Elsevier ScienceDirect
- **Coverage**: Elsevier journals (DOIs starting with 10.1016/)
- **Rate Limit**: Varies by license
- **Full-Text**: Direct PDF content with institutional access
- **Authentication**: API key required, institutional token for full access
- **Documentation**: https://dev.elsevier.com/

```python
# Headers required
headers = {
    "X-ELS-APIKey": "your-api-key",
    "X-ELS-Insttoken": "your-institutional-token",  # Optional
    "Accept": "application/pdf"
}
```

### 7. Wiley TDM
- **Coverage**: Wiley journals (DOIs starting with 10.1002/, 10.1111/)
- **Rate Limit**: 3 requests/second
- **Full-Text**: Direct PDF content with subscription
- **Authentication**: TDM token required
- **Documentation**: https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining

```python
# Headers required
headers = {
    "Wiley-TDM-Client-Token": "your-tdm-token",
    "Accept": "application/pdf"
}
```

### 8. Semantic Scholar
- **Coverage**: 200M+ papers, OA PDFs when available
- **Rate Limit**: 100 req/5min (higher with API key)
- **Full-Text**: Links to OA PDFs
- **Authentication**: API key optional
- **Documentation**: https://www.semanticscholar.org/product/api

### 9. Harvard Library Proxy (Fallback)
- **Coverage**: All Harvard-subscribed content
- **Rate Limit**: N/A (generates URLs only)
- **Full-Text**: Generates authenticated proxy URLs for browser access
- **Authentication**: Requires Harvard login in browser

```python
# Generated URL format
"https://ezp-prod1.hul.harvard.edu/login?url=https://doi.org/10.1234/example"
```

## Configuration

### Environment Variables

Add these to `backend/.env`:

```bash
# Required for basic functionality
UNPAYWALL_EMAIL=your_email@harvard.edu
PUBMED_EMAIL=your_email@harvard.edu

# Optional - for higher rate limits
PUBMED_API_KEY=your_ncbi_api_key
SEMANTIC_SCHOLAR_API_KEY=your_s2_key
CORE_API_KEY=your_core_key

# Publisher APIs (institutional access)
ELSEVIER_API_KEY=your_elsevier_key
ELSEVIER_INST_TOKEN=your_institutional_token  # Contact datasupport@elsevier.com
WILEY_TDM_TOKEN=your_wiley_tdm_token

# OpenAlex uses email for polite pool (no key needed)
OPENALEX_EMAIL=your_email@harvard.edu
```

## Usage

### Basic Usage

```python
from utils.fulltext_fetcher import FullTextFetcher, fetch_fulltext

# Quick fetch with environment defaults
result = fetch_fulltext("10.1016/j.envint.2020.105834")

if result.success:
    print(f"PDF URL: {result.pdf_url}")
    print(f"Source: {result.source.value}")
    print(f"Open Access: {result.is_open_access}")
```

### Advanced Usage

```python
from utils.fulltext_fetcher import FullTextFetcher, FullTextSource

# Initialize with custom configuration
fetcher = FullTextFetcher(
    unpaywall_email="maurice_elhelou@gsd.harvard.edu",
    pubmed_email="maurice_elhelou@gsd.harvard.edu",
    elsevier_api_key="your-key",
    wiley_tdm_token="your-token",
    enable_publisher_apis=True,
    enable_harvard_proxy=True
)

# Fetch with preferences
result = fetcher.fetch_fulltext(
    doi="10.1002/ajim.23033",
    preferred_sources=[FullTextSource.WILEY, FullTextSource.UNPAYWALL],
    skip_sources=[FullTextSource.HARVARD_PROXY]
)

# Batch fetching
results = fetcher.fetch_batch(
    dois=["10.1016/...", "10.1002/...", "10.1371/..."],
    parallel=False  # Sequential to respect rate limits
)

# Get statistics
print(fetcher.get_stats())
# {'total_requests': 10, 'successful': 7, 'success_rate': '70.0%', 'by_source': {...}}
```

### Integration with Discovery Pipeline

```python
from pipelines.end_to_end_discovery import EndToEndDiscoveryPipelineV3

pipeline = EndToEndDiscoveryPipelineV3(
    pubmed_email="maurice_elhelou@gsd.harvard.edu",
    enable_fulltext=True,
    enable_harvard_proxy=True
)

mechanisms = pipeline.discover_mechanisms_for_topic(
    topic_query="housing quality respiratory health",
    max_papers=10,
    fetch_fulltext=True  # Attempt full-text for all papers
)

# Check full-text stats
print(pipeline.fulltext_stats)
```

## API Response Format

```python
@dataclass
class FullTextResult:
    success: bool                    # Whether retrieval succeeded
    doi: Optional[str]               # The DOI requested
    pdf_url: Optional[str]           # URL to PDF (may require auth)
    pdf_content: Optional[bytes]     # Raw PDF bytes (Elsevier/Wiley)
    xml_content: Optional[str]       # Full-text XML (PMC)
    html_content: Optional[str]      # Full-text HTML
    source: Optional[FullTextSource] # Which API succeeded
    metadata: Dict[str, Any]         # Additional metadata
    error: Optional[str]             # Error message if failed
    is_open_access: bool             # Whether freely accessible
    license: Optional[str]           # License type (cc-by, etc.)
```

## Waterfall Order

The fetcher tries sources in this order (configurable):

1. **Unpaywall** - Best for finding OA versions quickly
2. **PMC** - Authoritative for NIH-funded research
3. **Europe PMC** - European coverage, often has PMC content too
4. **CORE** - Global repository aggregator
5. **OpenAlex** - Comprehensive metadata with OA links
6. **Elsevier** - If DOI is 10.1016/* and you have API access
7. **Wiley** - If DOI is 10.1002/* or 10.1111/* and you have TDM access
8. **Semantic Scholar** - Fallback for OA PDFs
9. **Harvard Proxy** - Last resort, generates URL for manual access

## Rate Limiting

The module implements per-provider rate limiting:

| Provider | Rate Limit | Notes |
|----------|-----------|-------|
| Unpaywall | 10 req/sec | Safe limit (100k/day cap) |
| PMC | 3-10 req/sec | 10 with API key |
| Europe PMC | 5 req/sec | Conservative |
| CORE | 1 req/sec | 10 req/10sec for single articles |
| OpenAlex | 1-10 req/sec | 10 with email |
| Elsevier | 2 req/sec | Varies by license |
| Wiley | 3 req/sec | Per TDM agreement |
| Semantic Scholar | 0.33 req/sec | 100 req/5min |

## Expected Coverage

Based on typical health research literature:

| Source | Expected Coverage |
|--------|------------------|
| Unpaywall | 30-40% (finds OA versions) |
| PMC | 20-30% (NIH-funded) |
| Europe PMC | 10-15% (overlaps PMC) |
| CORE | 15-20% (repository content) |
| Elsevier | 15-20% (with subscription) |
| Wiley | 10-15% (with subscription) |
| **Combined** | **50-70%** full-text access |

## Troubleshooting

### Common Issues

1. **"Authentication failed"** (Elsevier/Wiley)
   - Check API key is correct
   - For Elsevier: Contact datasupport@elsevier.com for institutional token
   - For Wiley: Ensure TDM agreement is active

2. **"Access denied"**
   - Article not covered by your subscription
   - Try other sources or Harvard Proxy

3. **"DOI not found"**
   - DOI may be malformed
   - Try cleaning: remove `https://doi.org/` prefix

4. **Rate limit errors**
   - Module handles retries automatically
   - For bulk operations, use `parallel=False`

### Logging

Enable debug logging to see waterfall progress:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now shows which providers are tried
result = fetcher.fetch_fulltext("10.1234/example")
```

## Harvard-Specific Notes

### Getting Institutional Access

1. **Elsevier**: Contact Harvard Library or email datasupport@elsevier.com
   - Request institutional token for ScienceDirect API
   - Mention you're doing text mining research

2. **Wiley**: Go to https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining
   - Sign the click-through TDM license
   - Your Harvard subscription should qualify

3. **ProQuest**: Contact Harvard Library
   - May have Dialog API access for historical research

### Harvard Proxy URLs

When all else fails, the Harvard Proxy generates URLs like:
```
https://ezp-prod1.hul.harvard.edu/login?url=https://doi.org/10.1234/example
```

These require:
1. Opening in a browser
2. Logging in with Harvard credentials
3. Manual download

## Future Enhancements

- [ ] Add Springer Nature API integration
- [ ] Add arXiv/bioRxiv/medRxiv for preprints
- [ ] PDF text extraction for LLM processing
- [ ] Caching layer for repeated requests
- [ ] Bulk download to local storage
