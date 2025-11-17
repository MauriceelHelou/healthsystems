"""
Literature Search Integration

This module provides integration with academic literature databases:
- Semantic Scholar API (no key required)
- PubMed API (no key required)

Used to retrieve papers for mechanism discovery pipeline.
"""

import requests
import time
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import xml.etree.ElementTree as ET


@dataclass
class Paper:
    """Represents a scientific paper"""
    title: str
    abstract: Optional[str]
    authors: List[str]
    year: Optional[int]
    doi: Optional[str]
    pmid: Optional[str]  # PubMed ID
    semantic_scholar_id: Optional[str]
    url: Optional[str]
    citation_count: int
    venue: Optional[str]
    field_of_study: List[str]


class SemanticScholarSearch:
    """
    Search Semantic Scholar for academic papers.

    Semantic Scholar API is free and doesn't require authentication for basic use.
    Rate limit: 100 requests per 5 minutes
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Semantic Scholar client.

        Args:
            api_key: Optional API key for higher rate limits
        """
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"x-api-key": api_key})

        self.rate_limit_delay = 1.0  # seconds between requests

    def search_papers(
        self,
        query: str,
        limit: int = 10,
        fields: Optional[List[str]] = None,
        year_range: Optional[tuple] = None,
        min_citations: int = 0
    ) -> List[Paper]:
        """
        Search for papers matching query.

        Args:
            query: Search query string
            limit: Maximum number of results
            fields: Fields to retrieve (title, abstract, authors, etc.)
            year_range: Tuple of (min_year, max_year) or None
            min_citations: Minimum citation count

        Returns:
            List of Paper objects
        """
        if fields is None:
            fields = [
                "title",
                "abstract",
                "authors",
                "year",
                "externalIds",
                "citationCount",
                "venue",
                "fieldsOfStudy",
                "url"
            ]

        params = {
            "query": query,
            "limit": limit,
            "fields": ",".join(fields)
        }

        # Add year filter if specified
        if year_range:
            params["year"] = f"{year_range[0]}-{year_range[1]}"

        # Add citation filter if specified
        if min_citations > 0:
            params["minCitationCount"] = min_citations

        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(
                f"{self.BASE_URL}/paper/search",
                params=params
            )
            response.raise_for_status()

            data = response.json()

            papers = []
            for item in data.get("data", []):
                paper = self._parse_paper(item)
                if paper:
                    papers.append(paper)

            return papers

        except requests.exceptions.RequestException as e:
            print(f"Error searching Semantic Scholar: {e}")
            return []

    def get_paper_by_doi(self, doi: str) -> Optional[Paper]:
        """
        Retrieve a specific paper by DOI.

        Args:
            doi: DOI of the paper

        Returns:
            Paper object or None
        """
        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(
                f"{self.BASE_URL}/paper/DOI:{doi}",
                params={"fields": "title,abstract,authors,year,externalIds,citationCount,venue,fieldsOfStudy,url"}
            )
            response.raise_for_status()

            data = response.json()
            return self._parse_paper(data)

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving paper by DOI: {e}")
            return None

    def _parse_paper(self, data: Dict) -> Optional[Paper]:
        """Parse API response into Paper object"""
        try:
            # Extract authors
            authors = []
            for author in data.get("authors", []):
                if "name" in author:
                    authors.append(author["name"])

            # Extract external IDs
            external_ids = data.get("externalIds", {})
            doi = external_ids.get("DOI")
            pmid = external_ids.get("PubMed")

            return Paper(
                title=data.get("title", ""),
                abstract=data.get("abstract"),
                authors=authors,
                year=data.get("year"),
                doi=doi,
                pmid=pmid,
                semantic_scholar_id=data.get("paperId"),
                url=data.get("url"),
                citation_count=data.get("citationCount", 0),
                venue=data.get("venue"),
                field_of_study=data.get("fieldsOfStudy", [])
            )
        except Exception as e:
            print(f"Error parsing paper data: {e}")
            return None


class PubMedSearch:
    """
    Search PubMed for medical literature.

    PubMed E-utilities API is free and doesn't require authentication.
    Rate limit: 3 requests per second without API key, 10/sec with key
    """

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize PubMed client.

        Args:
            email: Your email (recommended by NCBI for tracking)
            api_key: Optional API key for higher rate limits
        """
        self.email = email
        self.api_key = api_key
        self.session = requests.Session()
        self.rate_limit_delay = 0.34 if api_key else 0.5  # seconds between requests

    def search_papers(
        self,
        query: str,
        limit: int = 10,
        min_date: Optional[str] = None,
        max_date: Optional[str] = None
    ) -> List[Paper]:
        """
        Search PubMed for papers.

        Args:
            query: Search query string
            limit: Maximum number of results
            min_date: Minimum publication date (YYYY/MM/DD format)
            max_date: Maximum publication date (YYYY/MM/DD format)

        Returns:
            List of Paper objects
        """
        # Step 1: Search for PMIDs
        pmids = self._search_pmids(query, limit, min_date, max_date)

        if not pmids:
            return []

        # Step 2: Fetch paper details
        papers = self._fetch_paper_details(pmids)

        return papers

    def _search_pmids(
        self,
        query: str,
        limit: int,
        min_date: Optional[str],
        max_date: Optional[str]
    ) -> List[str]:
        """Search for PMIDs matching query"""
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": limit,
            "retmode": "json"
        }

        if self.email:
            params["email"] = self.email

        if self.api_key:
            params["api_key"] = self.api_key

        if min_date:
            params["mindate"] = min_date

        if max_date:
            params["maxdate"] = max_date

        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(
                f"{self.BASE_URL}/esearch.fcgi",
                params=params
            )
            response.raise_for_status()

            data = response.json()
            pmids = data.get("esearchresult", {}).get("idlist", [])

            return pmids

        except requests.exceptions.RequestException as e:
            print(f"Error searching PubMed: {e}")
            return []

    def _fetch_paper_details(self, pmids: List[str]) -> List[Paper]:
        """Fetch detailed information for PMIDs"""
        if not pmids:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }

        if self.email:
            params["email"] = self.email

        if self.api_key:
            params["api_key"] = self.api_key

        try:
            time.sleep(self.rate_limit_delay)
            response = self.session.get(
                f"{self.BASE_URL}/efetch.fcgi",
                params=params
            )
            response.raise_for_status()

            # Parse XML
            root = ET.fromstring(response.content)

            papers = []
            for article in root.findall(".//PubmedArticle"):
                paper = self._parse_pubmed_article(article)
                if paper:
                    papers.append(paper)

            return papers

        except requests.exceptions.RequestException as e:
            print(f"Error fetching PubMed details: {e}")
            return []

    def _parse_pubmed_article(self, article_elem) -> Optional[Paper]:
        """Parse PubMed XML article into Paper object"""
        try:
            # Extract PMID
            pmid_elem = article_elem.find(".//PMID")
            pmid = pmid_elem.text if pmid_elem is not None else None

            # Extract title
            title_elem = article_elem.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else ""

            # Extract abstract
            abstract_elems = article_elem.findall(".//AbstractText")
            abstract = " ".join([elem.text or "" for elem in abstract_elems]) if abstract_elems else None

            # Extract authors
            authors = []
            for author_elem in article_elem.findall(".//Author"):
                last_name_elem = author_elem.find("LastName")
                first_name_elem = author_elem.find("ForeName")

                if last_name_elem is not None:
                    last_name = last_name_elem.text or ""
                    first_name = first_name_elem.text if first_name_elem is not None else ""
                    authors.append(f"{first_name} {last_name}".strip())

            # Extract year
            year_elem = article_elem.find(".//PubDate/Year")
            year = int(year_elem.text) if year_elem is not None else None

            # Extract DOI
            doi = None
            for article_id in article_elem.findall(".//ArticleId"):
                if article_id.get("IdType") == "doi":
                    doi = article_id.text
                    break

            # Extract venue (journal)
            venue_elem = article_elem.find(".//Journal/Title")
            venue = venue_elem.text if venue_elem is not None else None

            return Paper(
                title=title,
                abstract=abstract,
                authors=authors,
                year=year,
                doi=doi,
                pmid=pmid,
                semantic_scholar_id=None,
                url=f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None,
                citation_count=0,  # PubMed doesn't provide citation counts
                venue=venue,
                field_of_study=["Medicine"]  # Default for PubMed
            )

        except Exception as e:
            print(f"Error parsing PubMed article: {e}")
            return None


class LiteratureSearchAggregator:
    """
    Aggregates results from multiple literature databases.

    Combines Semantic Scholar and PubMed to maximize coverage.
    Deduplicates by DOI/PMID.
    """

    def __init__(
        self,
        semantic_scholar_api_key: Optional[str] = None,
        pubmed_email: Optional[str] = None,
        pubmed_api_key: Optional[str] = None
    ):
        """Initialize aggregator with both search clients"""
        self.semantic_scholar = SemanticScholarSearch(api_key=semantic_scholar_api_key)
        self.pubmed = PubMedSearch(email=pubmed_email, api_key=pubmed_api_key)

    def search(
        self,
        query: str,
        limit_per_source: int = 10,
        year_range: Optional[tuple] = None,
        min_citations: int = 0,
        sources: List[str] = ["semantic_scholar", "pubmed"]
    ) -> List[Paper]:
        """
        Search across multiple sources and deduplicate.

        Args:
            query: Search query
            limit_per_source: Max results per source
            year_range: (min_year, max_year) or None
            min_citations: Minimum citation count (Semantic Scholar only)
            sources: List of sources to search

        Returns:
            Deduplicated list of papers
        """
        all_papers = []

        # Search Semantic Scholar
        if "semantic_scholar" in sources:
            print(f"Searching Semantic Scholar for: {query}")
            ss_papers = self.semantic_scholar.search_papers(
                query=query,
                limit=limit_per_source,
                year_range=year_range,
                min_citations=min_citations
            )
            all_papers.extend(ss_papers)
            print(f"  Found {len(ss_papers)} papers")

        # Search PubMed
        if "pubmed" in sources:
            print(f"Searching PubMed for: {query}")

            # Convert year range to PubMed date format
            min_date = f"{year_range[0]}/01/01" if year_range else None
            max_date = f"{year_range[1]}/12/31" if year_range else None

            pm_papers = self.pubmed.search_papers(
                query=query,
                limit=limit_per_source,
                min_date=min_date,
                max_date=max_date
            )
            all_papers.extend(pm_papers)
            print(f"  Found {len(pm_papers)} papers")

        # Deduplicate by DOI and PMID
        deduplicated = self._deduplicate_papers(all_papers)

        print(f"\nTotal unique papers: {len(deduplicated)}")
        return deduplicated

    def _deduplicate_papers(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers based on DOI and PMID"""
        seen_dois: Set[str] = set()
        seen_pmids: Set[str] = set()
        unique_papers = []

        for paper in papers:
            # Check DOI
            if paper.doi:
                if paper.doi in seen_dois:
                    continue
                seen_dois.add(paper.doi)
                unique_papers.append(paper)
                continue

            # Check PMID
            if paper.pmid:
                if paper.pmid in seen_pmids:
                    continue
                seen_pmids.add(paper.pmid)
                unique_papers.append(paper)
                continue

            # No DOI or PMID - include anyway
            unique_papers.append(paper)

        return unique_papers


def test_literature_search():
    """Test function for literature search"""

    print("=== Testing Literature Search Integration ===\n")

    # Initialize aggregator
    aggregator = LiteratureSearchAggregator(
        pubmed_email="test@example.com"  # Replace with your email
    )

    # Test search: housing quality and respiratory health
    query = "housing quality respiratory health asthma"

    papers = aggregator.search(
        query=query,
        limit_per_source=5,
        year_range=(2010, 2024),
        min_citations=10  # Only for Semantic Scholar
    )

    # Display results
    print(f"\n=== Results for: '{query}' ===\n")

    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}] {paper.title}")
        print(f"    Authors: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
        print(f"    Year: {paper.year}")
        print(f"    DOI: {paper.doi or 'N/A'}")
        print(f"    Citations: {paper.citation_count}")
        print(f"    Venue: {paper.venue or 'N/A'}")

        if paper.abstract:
            abstract_preview = paper.abstract[:200] + "..." if len(paper.abstract) > 200 else paper.abstract
            print(f"    Abstract: {abstract_preview}")


if __name__ == "__main__":
    test_literature_search()
