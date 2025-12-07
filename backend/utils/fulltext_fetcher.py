"""
Full-Text Paper Fetcher - Multi-Source Academic Paper Access

This module provides a unified interface to fetch full-text academic papers
from multiple sources using a waterfall approach:

1. Unpaywall - Free open access links
2. PubMed Central (PMC) - NIH open access repository
3. Europe PMC - European open access repository
4. CORE - Global open access aggregator
5. OpenAlex - Open scholarly metadata with PDF links
6. Elsevier ScienceDirect - Publisher API (requires institutional access)
7. Wiley TDM - Publisher API (requires institutional access)
8. Semantic Scholar - Fallback for open access PDFs

Configuration:
    Set these environment variables in .env:
    - UNPAYWALL_EMAIL: Your email for Unpaywall API
    - ELSEVIER_API_KEY: Elsevier ScienceDirect API key
    - WILEY_TDM_TOKEN: Wiley Text & Data Mining token
    - CORE_API_KEY: CORE API key (optional, for higher limits)
    - SEMANTIC_SCHOLAR_API_KEY: S2 API key (optional)

Usage:
    from utils.fulltext_fetcher import FullTextFetcher

    fetcher = FullTextFetcher()
    result = fetcher.fetch_fulltext(doi="10.1234/example")

    if result.success:
        print(f"PDF URL: {result.pdf_url}")
        print(f"Source: {result.source}")
"""

import os
import re
import time
import json
import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class FullTextSource(Enum):
    """Enumeration of full-text sources"""
    UNPAYWALL = "unpaywall"
    PMC = "pubmed_central"
    EUROPE_PMC = "europe_pmc"
    CORE = "core"
    OPENALEX = "openalex"
    ELSEVIER = "elsevier"
    WILEY = "wiley"
    SPRINGER = "springer"
    SEMANTIC_SCHOLAR = "semantic_scholar"
    CROSSREF = "crossref"
    HARVARD_PROXY = "harvard_proxy"


@dataclass
class FullTextResult:
    """Result of a full-text fetch attempt"""
    success: bool
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    pdf_content: Optional[bytes] = None
    xml_content: Optional[str] = None
    html_content: Optional[str] = None
    source: Optional[FullTextSource] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    is_open_access: bool = False
    license: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "doi": self.doi,
            "pdf_url": self.pdf_url,
            "source": self.source.value if self.source else None,
            "is_open_access": self.is_open_access,
            "license": self.license,
            "error": self.error,
            "metadata": self.metadata
        }


class RateLimiter:
    """Simple rate limiter for API calls"""

    def __init__(self, calls_per_second: float = 1.0):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0

    def wait(self):
        """Wait if necessary to respect rate limit"""
        elapsed = time.time() - self.last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_call = time.time()


class BaseProvider(ABC):
    """Abstract base class for full-text providers"""

    def __init__(self, rate_limit: float = 1.0, timeout: int = 30):
        self.rate_limiter = RateLimiter(rate_limit)
        self.timeout = timeout
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    @abstractmethod
    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch full-text for a given DOI"""
        pass

    @property
    @abstractmethod
    def source(self) -> FullTextSource:
        """Return the source enum for this provider"""
        pass


class UnpaywallProvider(BaseProvider):
    """
    Unpaywall API - Free open access link finder

    API Documentation: https://unpaywall.org/products/api
    Rate Limit: 100,000 requests/day
    """

    def __init__(self, email: str, **kwargs):
        super().__init__(rate_limit=10.0, **kwargs)  # 10 req/sec is safe
        self.email = email
        self.base_url = "https://api.unpaywall.org/v2"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.UNPAYWALL

    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch open access PDF link from Unpaywall"""
        self.rate_limiter.wait()

        try:
            url = f"{self.base_url}/{doi}"
            params = {"email": self.email}

            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.status_code == 404:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="DOI not found in Unpaywall"
                )

            response.raise_for_status()
            data = response.json()

            # Find best open access location
            best_oa = data.get("best_oa_location")

            if best_oa and best_oa.get("url_for_pdf"):
                return FullTextResult(
                    success=True,
                    doi=doi,
                    pdf_url=best_oa["url_for_pdf"],
                    source=self.source,
                    is_open_access=data.get("is_oa", False),
                    license=best_oa.get("license"),
                    metadata={
                        "title": data.get("title"),
                        "year": data.get("year"),
                        "journal": data.get("journal_name"),
                        "oa_status": data.get("oa_status"),
                        "host_type": best_oa.get("host_type"),
                        "version": best_oa.get("version")
                    }
                )

            # Check all OA locations
            oa_locations = data.get("oa_locations", [])
            for loc in oa_locations:
                if loc.get("url_for_pdf"):
                    return FullTextResult(
                        success=True,
                        doi=doi,
                        pdf_url=loc["url_for_pdf"],
                        source=self.source,
                        is_open_access=True,
                        license=loc.get("license"),
                        metadata={
                            "title": data.get("title"),
                            "host_type": loc.get("host_type")
                        }
                    )

            return FullTextResult(
                success=False,
                doi=doi,
                error="No open access PDF found",
                metadata={"is_oa": data.get("is_oa", False)}
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Unpaywall error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class PMCProvider(BaseProvider):
    """
    PubMed Central Open Access API

    API Documentation: https://www.ncbi.nlm.nih.gov/pmc/tools/oa-service/
    Rate Limit: 3 req/sec without key, 10 req/sec with NCBI API key
    """

    def __init__(self, email: str, api_key: Optional[str] = None, **kwargs):
        rate = 10.0 if api_key else 3.0
        super().__init__(rate_limit=rate, **kwargs)
        self.email = email
        self.api_key = api_key
        self.oa_service_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi"
        self.efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        self.esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.PMC

    def _doi_to_pmcid(self, doi: str) -> Optional[str]:
        """Convert DOI to PMCID using E-utilities"""
        self.rate_limiter.wait()

        try:
            params = {
                "db": "pmc",
                "term": f"{doi}[doi]",
                "retmode": "json",
                "email": self.email
            }
            if self.api_key:
                params["api_key"] = self.api_key

            response = self.session.get(self.esearch_url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])

            if id_list:
                return f"PMC{id_list[0]}"
            return None

        except Exception as e:
            logger.warning(f"Failed to convert DOI to PMCID: {e}")
            return None

    def fetch(self, doi: str, pmcid: Optional[str] = None, **kwargs) -> FullTextResult:
        """Fetch full-text from PMC"""
        # Get PMCID if not provided
        if not pmcid:
            pmcid = self._doi_to_pmcid(doi)

        if not pmcid:
            return FullTextResult(
                success=False,
                doi=doi,
                error="Could not find PMCID for DOI"
            )

        self.rate_limiter.wait()

        try:
            # Try OA service first for PDF link
            params = {"id": pmcid}
            response = self.session.get(self.oa_service_url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                # Parse XML response for PDF link
                content = response.text

                # Look for PDF link in response
                pdf_match = re.search(r'<link[^>]*format="pdf"[^>]*href="([^"]+)"', content)
                if pdf_match:
                    pdf_url = pdf_match.group(1)
                    return FullTextResult(
                        success=True,
                        doi=doi,
                        pdf_url=pdf_url,
                        source=self.source,
                        is_open_access=True,
                        metadata={"pmcid": pmcid}
                    )

                # Check for tgz (archive) link as fallback
                tgz_match = re.search(r'<link[^>]*format="tgz"[^>]*href="([^"]+)"', content)
                if tgz_match:
                    return FullTextResult(
                        success=True,
                        doi=doi,
                        pdf_url=tgz_match.group(1),
                        source=self.source,
                        is_open_access=True,
                        metadata={"pmcid": pmcid, "format": "tgz"}
                    )

            # Fallback: Try to get XML full-text
            self.rate_limiter.wait()
            xml_params = {
                "db": "pmc",
                "id": pmcid.replace("PMC", ""),
                "rettype": "full",
                "retmode": "xml",
                "email": self.email
            }
            if self.api_key:
                xml_params["api_key"] = self.api_key

            xml_response = self.session.get(self.efetch_url, params=xml_params, timeout=self.timeout)

            if xml_response.status_code == 200 and "<article" in xml_response.text:
                return FullTextResult(
                    success=True,
                    doi=doi,
                    xml_content=xml_response.text,
                    source=self.source,
                    is_open_access=True,
                    metadata={"pmcid": pmcid, "format": "xml"}
                )

            return FullTextResult(
                success=False,
                doi=doi,
                error="Article not in PMC Open Access subset",
                metadata={"pmcid": pmcid}
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"PMC error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class EuropePMCProvider(BaseProvider):
    """
    Europe PMC API

    API Documentation: https://europepmc.org/developers
    Full-text available via RESTful API and FTP
    """

    def __init__(self, **kwargs):
        super().__init__(rate_limit=5.0, **kwargs)
        self.base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.EUROPE_PMC

    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch full-text from Europe PMC"""
        self.rate_limiter.wait()

        try:
            # Search for article
            search_url = f"{self.base_url}/search"
            params = {
                "query": f'DOI:"{doi}"',
                "format": "json",
                "resultType": "core"
            }

            response = self.session.get(search_url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            results = data.get("resultList", {}).get("result", [])

            if not results:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="DOI not found in Europe PMC"
                )

            article = results[0]
            pmcid = article.get("pmcid")

            if not pmcid:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="No PMCID - article not in open access",
                    metadata={
                        "title": article.get("title"),
                        "source": article.get("source")
                    }
                )

            # Get full-text XML
            self.rate_limiter.wait()
            fulltext_url = f"{self.base_url}/{article.get('source', 'PMC')}/{pmcid}/fullTextXML"

            ft_response = self.session.get(fulltext_url, timeout=self.timeout)

            if ft_response.status_code == 200 and "<article" in ft_response.text:
                # Construct PDF URL (Europe PMC pattern)
                pdf_url = f"https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmcid}&blobtype=pdf"

                return FullTextResult(
                    success=True,
                    doi=doi,
                    pdf_url=pdf_url,
                    xml_content=ft_response.text,
                    source=self.source,
                    is_open_access=True,
                    metadata={
                        "pmcid": pmcid,
                        "title": article.get("title"),
                        "journal": article.get("journalTitle")
                    }
                )

            return FullTextResult(
                success=False,
                doi=doi,
                error="Full-text not available in Europe PMC"
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Europe PMC error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class COREProvider(BaseProvider):
    """
    CORE API - Global open access aggregator

    API Documentation: https://core.ac.uk/documentation/api
    200M+ open access papers
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        # Without key: 10 req/10sec for single articles
        super().__init__(rate_limit=1.0, **kwargs)
        self.api_key = api_key
        self.base_url = "https://api.core.ac.uk/v3"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.CORE

    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch full-text from CORE"""
        self.rate_limiter.wait()

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            # Search by DOI
            search_url = f"{self.base_url}/search/works"
            params = {"q": f'doi:"{doi}"', "limit": 1}

            response = self.session.get(
                search_url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            results = data.get("results", [])

            if not results:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="DOI not found in CORE"
                )

            article = results[0]
            core_id = article.get("id")

            # Check for downloadable PDF
            download_url = article.get("downloadUrl")

            if download_url:
                return FullTextResult(
                    success=True,
                    doi=doi,
                    pdf_url=download_url,
                    source=self.source,
                    is_open_access=True,
                    metadata={
                        "core_id": core_id,
                        "title": article.get("title"),
                        "year": article.get("yearPublished"),
                        "repository": article.get("dataProvider", {}).get("name")
                    }
                )

            # Try direct download endpoint
            if core_id:
                pdf_url = f"{self.base_url}/outputs/{core_id}/download"
                return FullTextResult(
                    success=True,
                    doi=doi,
                    pdf_url=pdf_url,
                    source=self.source,
                    is_open_access=True,
                    metadata={
                        "core_id": core_id,
                        "title": article.get("title")
                    }
                )

            return FullTextResult(
                success=False,
                doi=doi,
                error="No downloadable PDF in CORE"
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"CORE error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class OpenAlexProvider(BaseProvider):
    """
    OpenAlex API - Open scholarly metadata

    API Documentation: https://docs.openalex.org/
    225M+ works with open access links
    """

    def __init__(self, email: Optional[str] = None, **kwargs):
        # With email (polite pool): 10 req/sec
        super().__init__(rate_limit=10.0 if email else 1.0, **kwargs)
        self.email = email
        self.base_url = "https://api.openalex.org"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.OPENALEX

    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch open access PDF link from OpenAlex"""
        self.rate_limiter.wait()

        try:
            # Clean DOI
            clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")

            url = f"{self.base_url}/works/doi:{clean_doi}"
            headers = {}
            if self.email:
                headers["User-Agent"] = f"HealthSystemsPlatform/1.0 (mailto:{self.email})"

            response = self.session.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 404:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="DOI not found in OpenAlex"
                )

            response.raise_for_status()
            data = response.json()

            # Check for open access PDF
            oa_info = data.get("open_access", {})
            oa_url = oa_info.get("oa_url")

            # Also check primary_location and best_oa_location
            locations = data.get("locations", [])
            pdf_url = None

            for loc in locations:
                if loc.get("is_oa") and loc.get("pdf_url"):
                    pdf_url = loc["pdf_url"]
                    break

            if not pdf_url and oa_url:
                pdf_url = oa_url

            if pdf_url:
                return FullTextResult(
                    success=True,
                    doi=doi,
                    pdf_url=pdf_url,
                    source=self.source,
                    is_open_access=oa_info.get("is_oa", False),
                    license=oa_info.get("oa_status"),
                    metadata={
                        "title": data.get("title"),
                        "year": data.get("publication_year"),
                        "type": data.get("type"),
                        "cited_by_count": data.get("cited_by_count"),
                        "openalex_id": data.get("id")
                    }
                )

            return FullTextResult(
                success=False,
                doi=doi,
                error="No open access PDF in OpenAlex",
                metadata={
                    "is_oa": oa_info.get("is_oa", False),
                    "oa_status": oa_info.get("oa_status")
                }
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"OpenAlex error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class ElsevierProvider(BaseProvider):
    """
    Elsevier ScienceDirect API

    API Documentation: https://dev.elsevier.com/
    Requires API key and institutional access for full-text
    """

    def __init__(self, api_key: str, institutional_token: Optional[str] = None, **kwargs):
        super().__init__(rate_limit=2.0, **kwargs)
        self.api_key = api_key
        self.institutional_token = institutional_token
        self.base_url = "https://api.elsevier.com/content"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.ELSEVIER

    def _is_elsevier_doi(self, doi: str) -> bool:
        """Check if DOI belongs to Elsevier"""
        elsevier_prefixes = ["10.1016/", "10.1006/", "10.1053/", "10.1054/"]
        return any(doi.startswith(prefix) for prefix in elsevier_prefixes)

    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch full-text from Elsevier ScienceDirect"""
        if not self._is_elsevier_doi(doi):
            return FullTextResult(
                success=False,
                doi=doi,
                error="Not an Elsevier DOI"
            )

        self.rate_limiter.wait()

        headers = {
            "X-ELS-APIKey": self.api_key,
            "Accept": "application/pdf"
        }

        if self.institutional_token:
            headers["X-ELS-Insttoken"] = self.institutional_token

        try:
            # Article retrieval endpoint
            url = f"{self.base_url}/article/doi/{doi}"

            response = self.session.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 200:
                # Check if we got PDF content
                content_type = response.headers.get("Content-Type", "")

                if "pdf" in content_type.lower():
                    return FullTextResult(
                        success=True,
                        doi=doi,
                        pdf_content=response.content,
                        source=self.source,
                        is_open_access=False,
                        metadata={"content_type": content_type}
                    )

                # Got metadata instead of PDF - construct ScienceDirect URL
                sd_url = f"https://www.sciencedirect.com/science/article/pii/{doi.split('/')[-1]}"
                return FullTextResult(
                    success=True,
                    doi=doi,
                    pdf_url=sd_url,
                    source=self.source,
                    is_open_access=False,
                    metadata={"note": "Redirect to ScienceDirect"}
                )

            elif response.status_code == 401:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="Authentication failed - check API key"
                )

            elif response.status_code == 403:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="Access denied - institutional access required"
                )

            else:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error=f"Elsevier API returned {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"Elsevier error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class WileyProvider(BaseProvider):
    """
    Wiley TDM (Text & Data Mining) API

    API Documentation: https://onlinelibrary.wiley.com/library-info/resources/text-and-datamining
    Requires TDM token from institutional subscription
    Rate Limit: 3 requests/second
    """

    def __init__(self, tdm_token: str, **kwargs):
        super().__init__(rate_limit=3.0, **kwargs)
        self.tdm_token = tdm_token
        self.base_url = "https://api.wiley.com/onlinelibrary/tdm/v1/articles"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.WILEY

    def _is_wiley_doi(self, doi: str) -> bool:
        """Check if DOI belongs to Wiley"""
        wiley_prefixes = ["10.1002/", "10.1111/", "10.1046/", "10.1113/"]
        return any(doi.startswith(prefix) for prefix in wiley_prefixes)

    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch full-text from Wiley TDM"""
        if not self._is_wiley_doi(doi):
            return FullTextResult(
                success=False,
                doi=doi,
                error="Not a Wiley DOI"
            )

        self.rate_limiter.wait()

        headers = {
            "Wiley-TDM-Client-Token": self.tdm_token,
            "Accept": "application/pdf"
        }

        try:
            url = f"{self.base_url}/{doi}"

            response = self.session.get(url, headers=headers, timeout=self.timeout)

            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")

                if "pdf" in content_type.lower():
                    return FullTextResult(
                        success=True,
                        doi=doi,
                        pdf_content=response.content,
                        source=self.source,
                        is_open_access=False,
                        metadata={"content_type": content_type}
                    )

                # Check for XML
                if "xml" in content_type.lower():
                    return FullTextResult(
                        success=True,
                        doi=doi,
                        xml_content=response.text,
                        source=self.source,
                        is_open_access=False,
                        metadata={"format": "xml"}
                    )

            elif response.status_code == 401:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="TDM authentication failed - check token"
                )

            elif response.status_code == 403:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="Access denied - article not covered by subscription"
                )

            return FullTextResult(
                success=False,
                doi=doi,
                error=f"Wiley TDM returned {response.status_code}"
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Wiley error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class SemanticScholarProvider(BaseProvider):
    """
    Semantic Scholar API - Fallback for open access PDFs

    API Documentation: https://www.semanticscholar.org/product/api
    """

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        # 100 req/5min without key
        super().__init__(rate_limit=0.33, **kwargs)
        self.api_key = api_key
        self.base_url = "https://api.semanticscholar.org/graph/v1"

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.SEMANTIC_SCHOLAR

    def fetch(self, doi: str, **kwargs) -> FullTextResult:
        """Fetch open access PDF from Semantic Scholar"""
        self.rate_limiter.wait()

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        try:
            url = f"{self.base_url}/paper/DOI:{doi}"
            params = {"fields": "paperId,title,year,openAccessPdf,isOpenAccess"}

            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code == 404:
                return FullTextResult(
                    success=False,
                    doi=doi,
                    error="DOI not found in Semantic Scholar"
                )

            response.raise_for_status()
            data = response.json()

            oa_pdf = data.get("openAccessPdf")

            if oa_pdf and oa_pdf.get("url"):
                return FullTextResult(
                    success=True,
                    doi=doi,
                    pdf_url=oa_pdf["url"],
                    source=self.source,
                    is_open_access=data.get("isOpenAccess", True),
                    metadata={
                        "paper_id": data.get("paperId"),
                        "title": data.get("title"),
                        "year": data.get("year")
                    }
                )

            return FullTextResult(
                success=False,
                doi=doi,
                error="No open access PDF in Semantic Scholar",
                metadata={"is_oa": data.get("isOpenAccess", False)}
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Semantic Scholar error for {doi}: {e}")
            return FullTextResult(success=False, doi=doi, error=str(e))


class HarvardProxyProvider(BaseProvider):
    """
    Harvard Library Proxy URL Generator

    Generates EZProxy URLs for Harvard-authenticated access.
    Does not fetch content directly - provides authenticated URLs.
    """

    PROXY_BASE = "https://ezp-prod1.hul.harvard.edu/login?url="

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def source(self) -> FullTextSource:
        return FullTextSource.HARVARD_PROXY

    def fetch(self, doi: str, publisher_url: Optional[str] = None, **kwargs) -> FullTextResult:
        """Generate Harvard proxy URL for authenticated access"""
        if publisher_url:
            proxy_url = f"{self.PROXY_BASE}{publisher_url}"
        else:
            # Default to doi.org which will redirect to publisher
            proxy_url = f"{self.PROXY_BASE}https://doi.org/{doi}"

        return FullTextResult(
            success=True,
            doi=doi,
            pdf_url=proxy_url,
            source=self.source,
            is_open_access=False,
            metadata={
                "note": "Harvard proxy URL - requires Harvard authentication in browser",
                "original_url": publisher_url or f"https://doi.org/{doi}"
            }
        )


class FullTextFetcher:
    """
    Unified full-text fetcher with waterfall approach

    Tries multiple sources in priority order:
    1. Unpaywall (free OA links)
    2. PubMed Central (NIH OA)
    3. Europe PMC (European OA)
    4. CORE (global OA aggregator)
    5. OpenAlex (OA metadata)
    6. Elsevier (if institutional access)
    7. Wiley (if institutional access)
    8. Semantic Scholar (fallback)
    9. Harvard Proxy (last resort - manual browser access)
    """

    def __init__(
        self,
        unpaywall_email: Optional[str] = None,
        pubmed_email: Optional[str] = None,
        pubmed_api_key: Optional[str] = None,
        elsevier_api_key: Optional[str] = None,
        elsevier_inst_token: Optional[str] = None,
        wiley_tdm_token: Optional[str] = None,
        core_api_key: Optional[str] = None,
        semantic_scholar_api_key: Optional[str] = None,
        enable_publisher_apis: bool = True,
        enable_harvard_proxy: bool = True
    ):
        """
        Initialize the full-text fetcher with API credentials.

        Credentials can be passed directly or loaded from environment variables:
        - UNPAYWALL_EMAIL
        - PUBMED_EMAIL
        - PUBMED_API_KEY
        - ELSEVIER_API_KEY
        - ELSEVIER_INST_TOKEN
        - WILEY_TDM_TOKEN
        - CORE_API_KEY
        - SEMANTIC_SCHOLAR_API_KEY
        """
        # Load from env if not provided
        self.unpaywall_email = unpaywall_email or os.getenv("UNPAYWALL_EMAIL")
        self.pubmed_email = pubmed_email or os.getenv("PUBMED_EMAIL")
        self.pubmed_api_key = pubmed_api_key or os.getenv("PUBMED_API_KEY")
        self.elsevier_api_key = elsevier_api_key or os.getenv("ELSEVIER_API_KEY")
        self.elsevier_inst_token = elsevier_inst_token or os.getenv("ELSEVIER_INST_TOKEN")
        self.wiley_tdm_token = wiley_tdm_token or os.getenv("WILEY_TDM_TOKEN")
        self.core_api_key = core_api_key or os.getenv("CORE_API_KEY")
        self.s2_api_key = semantic_scholar_api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY")

        self.enable_publisher_apis = enable_publisher_apis
        self.enable_harvard_proxy = enable_harvard_proxy

        # Initialize providers
        self.providers: List[BaseProvider] = []
        self._init_providers()

        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "by_source": {}
        }

        logger.info(f"FullTextFetcher initialized with {len(self.providers)} providers")

    def _init_providers(self):
        """Initialize available providers in priority order"""

        # 1. Unpaywall (best free OA source)
        if self.unpaywall_email:
            self.providers.append(UnpaywallProvider(email=self.unpaywall_email))
            logger.info("Enabled: Unpaywall")

        # 2. PubMed Central
        if self.pubmed_email:
            self.providers.append(PMCProvider(
                email=self.pubmed_email,
                api_key=self.pubmed_api_key
            ))
            logger.info("Enabled: PubMed Central")

        # 3. Europe PMC
        self.providers.append(EuropePMCProvider())
        logger.info("Enabled: Europe PMC")

        # 4. CORE
        self.providers.append(COREProvider(api_key=self.core_api_key))
        logger.info("Enabled: CORE")

        # 5. OpenAlex
        self.providers.append(OpenAlexProvider(email=self.unpaywall_email or self.pubmed_email))
        logger.info("Enabled: OpenAlex")

        # 6. Publisher APIs (if enabled and credentials available)
        if self.enable_publisher_apis:
            if self.elsevier_api_key:
                self.providers.append(ElsevierProvider(
                    api_key=self.elsevier_api_key,
                    institutional_token=self.elsevier_inst_token
                ))
                logger.info("Enabled: Elsevier ScienceDirect")

            if self.wiley_tdm_token:
                self.providers.append(WileyProvider(tdm_token=self.wiley_tdm_token))
                logger.info("Enabled: Wiley TDM")

        # 7. Semantic Scholar (fallback)
        self.providers.append(SemanticScholarProvider(api_key=self.s2_api_key))
        logger.info("Enabled: Semantic Scholar")

        # 8. Harvard Proxy (last resort)
        if self.enable_harvard_proxy:
            self.providers.append(HarvardProxyProvider())
            logger.info("Enabled: Harvard Proxy (manual access)")

    def fetch_fulltext(
        self,
        doi: str,
        stop_on_first: bool = True,
        preferred_sources: Optional[List[FullTextSource]] = None,
        skip_sources: Optional[List[FullTextSource]] = None
    ) -> FullTextResult:
        """
        Fetch full-text PDF for a DOI using waterfall approach.

        Args:
            doi: The DOI to fetch
            stop_on_first: Stop after first successful fetch (default: True)
            preferred_sources: Try these sources first
            skip_sources: Skip these sources

        Returns:
            FullTextResult with PDF URL, content, or error
        """
        self.stats["total_requests"] += 1

        # Clean DOI
        doi = self._clean_doi(doi)

        if not doi:
            return FullTextResult(success=False, error="Invalid or empty DOI")

        # Reorder providers if preferred sources specified
        providers = self._order_providers(preferred_sources, skip_sources)

        all_errors = []

        for provider in providers:
            try:
                logger.debug(f"Trying {provider.source.value} for {doi}")
                result = provider.fetch(doi)

                if result.success:
                    self.stats["successful"] += 1
                    source_name = provider.source.value
                    self.stats["by_source"][source_name] = \
                        self.stats["by_source"].get(source_name, 0) + 1

                    logger.info(f"Found full-text for {doi} via {source_name}")

                    if stop_on_first:
                        return result

                else:
                    all_errors.append(f"{provider.source.value}: {result.error}")

            except Exception as e:
                logger.error(f"Error with {provider.source.value}: {e}")
                all_errors.append(f"{provider.source.value}: {str(e)}")

        # No provider succeeded
        return FullTextResult(
            success=False,
            doi=doi,
            error=f"No full-text found. Tried: {', '.join(all_errors)}"
        )

    def fetch_batch(
        self,
        dois: List[str],
        parallel: bool = False,
        max_workers: int = 4
    ) -> Dict[str, FullTextResult]:
        """
        Fetch full-text for multiple DOIs.

        Args:
            dois: List of DOIs to fetch
            parallel: Use parallel fetching (default: False to respect rate limits)
            max_workers: Number of parallel workers if parallel=True

        Returns:
            Dict mapping DOI to FullTextResult
        """
        results = {}

        if parallel:
            from concurrent.futures import ThreadPoolExecutor, as_completed

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_doi = {
                    executor.submit(self.fetch_fulltext, doi): doi
                    for doi in dois
                }

                for future in as_completed(future_to_doi):
                    doi = future_to_doi[future]
                    try:
                        results[doi] = future.result()
                    except Exception as e:
                        results[doi] = FullTextResult(
                            success=False,
                            doi=doi,
                            error=str(e)
                        )
        else:
            for doi in dois:
                results[doi] = self.fetch_fulltext(doi)

        return results

    def _clean_doi(self, doi: str) -> str:
        """Clean and normalize DOI"""
        if not doi:
            return ""

        doi = doi.strip()
        doi = doi.replace("https://doi.org/", "")
        doi = doi.replace("http://doi.org/", "")
        doi = doi.replace("doi:", "")

        return doi.strip()

    def _order_providers(
        self,
        preferred: Optional[List[FullTextSource]],
        skip: Optional[List[FullTextSource]]
    ) -> List[BaseProvider]:
        """Reorder providers based on preferences"""
        skip_set = set(skip) if skip else set()

        filtered = [p for p in self.providers if p.source not in skip_set]

        if not preferred:
            return filtered

        # Move preferred to front
        preferred_providers = []
        other_providers = []

        for provider in filtered:
            if provider.source in preferred:
                preferred_providers.append(provider)
            else:
                other_providers.append(provider)

        # Sort preferred by the order in the preferred list
        preferred_providers.sort(key=lambda p: preferred.index(p.source))

        return preferred_providers + other_providers

    def get_stats(self) -> Dict:
        """Get fetcher statistics"""
        success_rate = (
            self.stats["successful"] / self.stats["total_requests"] * 100
            if self.stats["total_requests"] > 0 else 0
        )

        return {
            **self.stats,
            "success_rate": f"{success_rate:.1f}%"
        }

    def get_available_providers(self) -> List[str]:
        """Get list of available provider names"""
        return [p.source.value for p in self.providers]


# Convenience function for quick access
def fetch_fulltext(doi: str, **kwargs) -> FullTextResult:
    """
    Quick fetch function using default configuration from environment.

    Args:
        doi: The DOI to fetch
        **kwargs: Additional arguments passed to FullTextFetcher.fetch_fulltext

    Returns:
        FullTextResult
    """
    fetcher = FullTextFetcher()
    return fetcher.fetch_fulltext(doi, **kwargs)


# CLI for testing
if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO)

    # Test with a known open access DOI
    test_dois = [
        "10.1371/journal.pone.0000000",  # PLOS (should be OA)
        "10.1016/j.envint.2020.105834",   # Elsevier
        "10.1002/ajim.23033",              # Wiley
    ]

    if len(sys.argv) > 1:
        test_dois = [sys.argv[1]]

    fetcher = FullTextFetcher()

    print(f"\nAvailable providers: {fetcher.get_available_providers()}\n")

    for doi in test_dois:
        print(f"\n{'='*60}")
        print(f"Testing DOI: {doi}")
        print('='*60)

        result = fetcher.fetch_fulltext(doi)

        if result.success:
            print(f"SUCCESS via {result.source.value}")
            print(f"  PDF URL: {result.pdf_url}")
            print(f"  Open Access: {result.is_open_access}")
            print(f"  License: {result.license}")
        else:
            print(f"FAILED: {result.error}")

    print(f"\n\nStatistics: {fetcher.get_stats()}")
