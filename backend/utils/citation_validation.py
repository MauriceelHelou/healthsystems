"""
Citation Validation Utilities

Provides functions to validate and verify academic citations:
- DOI validation via Crossref API
- Citation metadata extraction
- Author/year/journal verification
"""

import requests
import re
import time
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class CitationValidator:
    """Validates academic citations and DOIs"""

    def __init__(self, rate_limit: float = 0.5):
        """
        Initialize validator

        Args:
            rate_limit: Seconds to wait between API calls (be nice to Crossref)
        """
        self.rate_limit = rate_limit
        self.last_request_time = 0

    def _rate_limit_delay(self):
        """Ensure we don't exceed API rate limits"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def clean_doi(self, doi: str) -> str:
        """
        Clean and normalize DOI string

        Args:
            doi: DOI string (may include URL prefix)

        Returns:
            Cleaned DOI (e.g., "10.1056/NEJMra1611832")
        """
        if not doi:
            return ""

        # Remove URL prefixes
        doi = doi.strip()
        doi = doi.replace("https://doi.org/", "")
        doi = doi.replace("http://doi.org/", "")
        doi = doi.replace("doi:", "")

        return doi.strip()

    def validate_doi_format(self, doi: str) -> bool:
        """
        Validate DOI format (basic pattern matching)

        Args:
            doi: DOI string

        Returns:
            True if format is valid
        """
        doi = self.clean_doi(doi)

        # DOI pattern: 10.xxxx/xxxxx
        doi_pattern = r'^10\.\d{4,}/[^\s]+$'
        return bool(re.match(doi_pattern, doi))

    def verify_doi(self, doi: str, timeout: int = 10) -> Dict[str, any]:
        """
        Verify DOI exists and retrieve metadata via Crossref API

        Args:
            doi: DOI string
            timeout: Request timeout in seconds

        Returns:
            Dict with:
                - valid: bool
                - metadata: dict with title, authors, year, journal, doi
                - error: str or None
        """
        doi = self.clean_doi(doi)

        if not doi:
            return {
                "valid": False,
                "error": "Empty DOI",
                "metadata": None
            }

        # Validate format first
        if not self.validate_doi_format(doi):
            return {
                "valid": False,
                "error": "Invalid DOI format (should be 10.xxxx/xxxxx)",
                "metadata": None
            }

        # Query Crossref API
        try:
            self._rate_limit_delay()

            url = f"https://api.crossref.org/works/{doi}"
            headers = {
                'User-Agent': 'HealthSystemsPlatform/1.0 (mailto:research@example.org)'
            }

            response = requests.get(url, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                message = data.get("message", {})

                # Extract metadata
                metadata = {
                    "title": message.get("title", [None])[0],
                    "authors": self._extract_authors(message),
                    "year": self._extract_year(message),
                    "journal": message.get("container-title", [None])[0],
                    "doi": message.get("DOI"),
                    "volume": message.get("volume"),
                    "issue": message.get("issue"),
                    "pages": message.get("page"),
                    "type": message.get("type")
                }

                logger.info(f"DOI verified: {doi}")
                return {
                    "valid": True,
                    "metadata": metadata,
                    "error": None
                }

            elif response.status_code == 404:
                logger.warning(f"DOI not found: {doi}")
                return {
                    "valid": False,
                    "error": "DOI not found in Crossref database",
                    "metadata": None
                }

            else:
                logger.error(f"Crossref API error {response.status_code} for DOI: {doi}")
                return {
                    "valid": False,
                    "error": f"Crossref API returned HTTP {response.status_code}",
                    "metadata": None
                }

        except requests.exceptions.Timeout:
            logger.error(f"Timeout verifying DOI: {doi}")
            return {
                "valid": False,
                "error": "API request timeout",
                "metadata": None
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error verifying DOI {doi}: {e}")
            return {
                "valid": False,
                "error": f"Network error: {str(e)}",
                "metadata": None
            }

        except Exception as e:
            logger.error(f"Unexpected error verifying DOI {doi}: {e}")
            return {
                "valid": False,
                "error": f"Unexpected error: {str(e)}",
                "metadata": None
            }

    def _extract_authors(self, crossref_message: dict) -> List[str]:
        """Extract author names from Crossref metadata"""
        authors = []
        for author in crossref_message.get("author", []):
            given = author.get("given", "")
            family = author.get("family", "")

            if family:
                # Format: "Family, G." or "Family, Given"
                if given:
                    # Use first initial
                    initial = given[0] if given else ""
                    authors.append(f"{family}, {initial}.")
                else:
                    authors.append(family)

        return authors

    def _extract_year(self, crossref_message: dict) -> Optional[int]:
        """Extract publication year from Crossref metadata"""
        # Try published date first
        published = crossref_message.get("published", {})
        date_parts = published.get("date-parts", [[]])

        if date_parts and len(date_parts[0]) > 0:
            return date_parts[0][0]

        # Try other date fields
        for date_field in ["published-online", "published-print", "created"]:
            date_obj = crossref_message.get(date_field, {})
            date_parts = date_obj.get("date-parts", [[]])
            if date_parts and len(date_parts[0]) > 0:
                return date_parts[0][0]

        return None

    def format_chicago_citation(self, metadata: dict) -> str:
        """
        Format citation metadata as Chicago-style citation

        Args:
            metadata: Dict with title, authors, year, journal, etc.

        Returns:
            Chicago-style citation string
        """
        parts = []

        # Authors
        authors = metadata.get("authors", [])
        if authors:
            if len(authors) == 1:
                parts.append(authors[0])
            elif len(authors) == 2:
                parts.append(f"{authors[0]} and {authors[1]}")
            elif len(authors) > 2:
                parts.append(f"{authors[0]} et al.")

        # Year
        year = metadata.get("year")
        if year:
            parts.append(f"{year}.")

        # Title
        title = metadata.get("title")
        if title:
            parts.append(f'"{title}."')

        # Journal
        journal = metadata.get("journal")
        if journal:
            journal_part = f"*{journal}*"

            # Add volume/issue/pages
            volume = metadata.get("volume")
            issue = metadata.get("issue")
            pages = metadata.get("pages")

            if volume:
                journal_part += f" {volume}"
            if issue:
                journal_part += f" ({issue})"
            if pages:
                journal_part += f": {pages}"

            journal_part += "."
            parts.append(journal_part)

        # DOI
        doi = metadata.get("doi")
        if doi:
            parts.append(f"https://doi.org/{doi}")

        return " ".join(parts)

    def compare_citations(
        self,
        extracted_citation: str,
        doi_metadata: dict
    ) -> Dict[str, any]:
        """
        Compare extracted citation against verified DOI metadata

        Args:
            extracted_citation: Citation string extracted by LLM
            doi_metadata: Metadata from DOI verification

        Returns:
            Dict with:
                - matches: bool
                - mismatches: list of str (issues found)
                - warnings: list of str (potential issues)
        """
        mismatches = []
        warnings = []

        # Extract year from citation
        extracted_year = self._extract_year_from_string(extracted_citation)
        actual_year = doi_metadata.get("year")

        if extracted_year and actual_year:
            if extracted_year != actual_year:
                mismatches.append(
                    f"Year mismatch: citation has {extracted_year}, DOI shows {actual_year}"
                )
        elif not extracted_year:
            warnings.append("Could not extract year from citation")

        # Check title presence
        title = doi_metadata.get("title", "")
        if title and title.lower() not in extracted_citation.lower():
            warnings.append("Citation title doesn't match DOI metadata")

        # Check journal presence
        journal = doi_metadata.get("journal", "")
        if journal and journal.lower() not in extracted_citation.lower():
            warnings.append("Citation journal doesn't match DOI metadata")

        matches = len(mismatches) == 0 and len(warnings) <= 1

        return {
            "matches": matches,
            "mismatches": mismatches,
            "warnings": warnings
        }

    def _extract_year_from_string(self, text: str) -> Optional[int]:
        """Extract 4-digit year from text"""
        match = re.search(r'\b(19|20)\d{2}\b', text)
        if match:
            return int(match.group(0))
        return None


# Convenience functions
_validator = CitationValidator()


def verify_doi(doi: str) -> Dict[str, any]:
    """
    Verify a DOI (convenience function)

    Args:
        doi: DOI string

    Returns:
        Verification result dict
    """
    return _validator.verify_doi(doi)


def validate_doi_format(doi: str) -> bool:
    """
    Check if DOI format is valid (convenience function)

    Args:
        doi: DOI string

    Returns:
        True if format is valid
    """
    return _validator.validate_doi_format(doi)


def format_chicago_citation(metadata: dict) -> str:
    """
    Format metadata as Chicago citation (convenience function)

    Args:
        metadata: Citation metadata dict

    Returns:
        Chicago-style citation string
    """
    return _validator.format_chicago_citation(metadata)
