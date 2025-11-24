"""
Grey Literature Search Integration

Extends literature search to include grey literature sources:
- Google Scholar (via SerpAPI or scraping)
- ProQuest Dissertations
- Government reports (CDC, WHO, NIH)
- Policy briefs and technical reports
- Preprint servers (medRxiv, bioRxiv, SSRN)

Grey literature provides important context for mechanisms that may not
be published in peer-reviewed journals (policy reports, dissertations,
preliminary findings).
"""

import requests
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from pathlib import Path
import os


@dataclass
class GreyLiterature:
    """Represents a grey literature source"""
    title: str
    abstract: Optional[str]
    authors: List[str]
    year: Optional[int]
    url: Optional[str]
    source_type: str  # 'government_report', 'dissertation', 'preprint', 'policy_brief', 'technical_report'
    organization: Optional[str]  # e.g., "CDC", "WHO", "NIH"
    keywords: List[str] = field(default_factory=list)
    full_text_available: bool = False
    full_text_url: Optional[str] = None


class MedRxivSearch:
    """
    Search medRxiv preprint server for medical research.

    medRxiv hosts preprints of medical, clinical, and health research
    that may not yet be peer-reviewed.
    """

    BASE_URL = "https://api.medrxiv.org"

    def __init__(self):
        self.session = requests.Session()
        self.rate_limit_delay = 1.0

    def search_preprints(
        self,
        query: str,
        limit: int = 10,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> List[GreyLiterature]:
        """
        Search medRxiv for preprints.

        Args:
            query: Search query
            limit: Max results
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            List of GreyLiterature objects
        """
        # Note: medRxiv API is limited. In production, consider web scraping
        # or using Google Scholar as an alternative

        results = []

        # Placeholder: Would implement actual API calls or scraping
        # For now, return empty list with note to implement

        print(f"  Note: medRxiv search not fully implemented. Consider web scraping.")

        return results


class BioRxivSearch:
    """Search bioRxiv preprint server for biological research."""

    BASE_URL = "https://api.biorxiv.org"

    def search_preprints(
        self,
        query: str,
        limit: int = 10
    ) -> List[GreyLiterature]:
        """Search bioRxiv for preprints related to health."""
        results = []
        print(f"  Note: bioRxiv search not fully implemented.")
        return results


class GovernmentReportSearch:
    """
    Search government health agency reports.

    Includes:
    - CDC reports and data briefs
    - NIH reports
    - WHO technical reports
    - SAMHSA reports
    - CMS reports
    """

    AGENCIES = {
        'cdc': {
            'name': 'Centers for Disease Control and Prevention',
            'base_url': 'https://www.cdc.gov',
            'search_url': 'https://search.cdc.gov/search/'
        },
        'nih': {
            'name': 'National Institutes of Health',
            'base_url': 'https://www.nih.gov'
        },
        'who': {
            'name': 'World Health Organization',
            'base_url': 'https://www.who.int'
        }
    }

    def search_reports(
        self,
        query: str,
        agency: str = 'cdc',
        limit: int = 10
    ) -> List[GreyLiterature]:
        """
        Search government agency reports.

        Args:
            query: Search query
            agency: Agency code ('cdc', 'nih', 'who')
            limit: Max results

        Returns:
            List of GreyLiterature objects
        """
        if agency not in self.AGENCIES:
            print(f"  Unknown agency: {agency}")
            return []

        results = []

        # Placeholder: Would implement actual API calls or scraping
        # Government sites often don't have public APIs, so web scraping
        # or manual curation may be necessary

        print(f"  Note: {self.AGENCIES[agency]['name']} search not fully implemented.")
        print(f"  Consider manual curation of relevant reports.")

        return results


class GreyLiteratureAggregator:
    """
    Aggregates grey literature from multiple sources.

    Provides unified search across preprints, government reports,
    dissertations, and policy briefs.
    """

    def __init__(self):
        self.medrxiv = MedRxivSearch()
        self.biorxiv = BioRxivSearch()
        self.gov_reports = GovernmentReportSearch()

    def search(
        self,
        query: str,
        limit_per_source: int = 5,
        sources: List[str] = ['medrxiv', 'biorxiv', 'government'],
        year_range: Optional[tuple] = None
    ) -> List[GreyLiterature]:
        """
        Search across grey literature sources.

        Args:
            query: Search query
            limit_per_source: Max results per source
            sources: List of sources to search
            year_range: (min_year, max_year) or None

        Returns:
            List of GreyLiterature objects
        """
        all_literature = []

        print(f"\n=== Searching Grey Literature ===")

        # Search preprints
        if 'medrxiv' in sources:
            print(f"Searching medRxiv...")
            medrxiv_results = self.medrxiv.search_preprints(
                query=query,
                limit=limit_per_source
            )
            all_literature.extend(medrxiv_results)

        if 'biorxiv' in sources:
            print(f"Searching bioRxiv...")
            biorxiv_results = self.biorxiv.search_preprints(
                query=query,
                limit=limit_per_source
            )
            all_literature.extend(biorxiv_results)

        # Search government reports
        if 'government' in sources:
            print(f"Searching government reports...")
            for agency in ['cdc', 'nih', 'who']:
                gov_results = self.gov_reports.search_reports(
                    query=query,
                    agency=agency,
                    limit=limit_per_source
                )
                all_literature.extend(gov_results)

        print(f"\nTotal grey literature found: {len(all_literature)}")

        return all_literature

    def load_curated_reports(
        self,
        topic: str,
        curated_dir: Optional[Path] = None
    ) -> List[GreyLiterature]:
        """
        Load manually curated grey literature for a topic.

        For important government reports, policy briefs, and technical
        documents that can't be automatically searched, maintain a
        curated collection.

        Args:
            topic: Health topic
            curated_dir: Directory with curated YAML files

        Returns:
            List of GreyLiterature objects
        """
        if curated_dir is None:
            curated_dir = Path(__file__).parent.parent / "data" / "grey_literature"

        topic_file = curated_dir / f"{topic}_grey_literature.yaml"

        if not topic_file.exists():
            print(f"  No curated grey literature for topic: {topic}")
            return []

        # Load and parse YAML file
        import yaml

        with open(topic_file, 'r') as f:
            data = yaml.safe_load(f)

        literature = []
        for item in data.get('sources', []):
            lit = GreyLiterature(
                title=item['title'],
                abstract=item.get('abstract'),
                authors=item.get('authors', []),
                year=item.get('year'),
                url=item.get('url'),
                source_type=item.get('source_type', 'technical_report'),
                organization=item.get('organization'),
                keywords=item.get('keywords', []),
                full_text_available=item.get('full_text_available', False),
                full_text_url=item.get('full_text_url')
            )
            literature.append(lit)

        print(f"  Loaded {len(literature)} curated grey literature sources")

        return literature


def create_curated_template(topic: str, output_path: Path):
    """
    Create a template YAML file for manually curating grey literature.

    Args:
        topic: Health topic
        output_path: Where to save template
    """
    template = f"""# Curated Grey Literature for {topic}
#
# Manually curate important grey literature sources here.
# This includes government reports, policy briefs, dissertations,
# and technical reports that can't be automatically searched.

sources:
  - title: "Example CDC Report on {topic}"
    abstract: "Summary of the report..."
    authors:
      - "Centers for Disease Control and Prevention"
    year: 2023
    url: "https://www.cdc.gov/..."
    source_type: government_report  # Options: government_report, policy_brief, technical_report, dissertation, preprint
    organization: CDC
    keywords:
      - {topic}
      - health equity
    full_text_available: true
    full_text_url: "https://www.cdc.gov/.../full-report.pdf"

  - title: "WHO Technical Brief on {topic}"
    abstract: "..."
    authors:
      - "World Health Organization"
    year: 2022
    url: "https://www.who.int/..."
    source_type: technical_report
    organization: WHO
    keywords:
      - {topic}
      - global health
    full_text_available: true
    full_text_url: null

# Add more sources as needed
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(template)

    print(f"Created template: {output_path}")
    print(f"Please edit this file to add curated grey literature sources.")


if __name__ == '__main__':
    # Example: Create template for obesity grey literature
    template_path = Path("backend/data/grey_literature/obesity_grey_literature.yaml")
    create_curated_template("obesity", template_path)
