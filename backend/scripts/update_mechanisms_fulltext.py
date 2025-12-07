"""
Mechanism Bank Full-Text Update Script

This script:
1. Scans all existing mechanism YAML files
2. Extracts DOIs from citations
3. Fetches full-text via multi-source API
4. Updates mechanisms with enhanced metadata
5. Re-validates and grades evidence

Usage:
    python backend/scripts/update_mechanisms_fulltext.py
    python backend/scripts/update_mechanisms_fulltext.py --dry-run
    python backend/scripts/update_mechanisms_fulltext.py --category built_environment
"""

import os
import sys
import re
import yaml
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Setup paths
SCRIPT_DIR = Path(__file__).parent
BACKEND_DIR = SCRIPT_DIR.parent
PROJECT_DIR = BACKEND_DIR.parent

# Load environment
load_dotenv(BACKEND_DIR / '.env')

# Add backend to path
sys.path.insert(0, str(BACKEND_DIR))

from utils.fulltext_fetcher import FullTextFetcher, FullTextResult
from utils.citation_validation import CitationValidator, verify_doi

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class MechanismUpdate:
    """Tracks updates to a mechanism"""
    file_path: Path
    mechanism_id: str
    original_doi: Optional[str] = None
    extracted_doi: Optional[str] = None
    doi_verified: bool = False
    fulltext_found: bool = False
    fulltext_source: Optional[str] = None
    fulltext_url: Optional[str] = None
    updates_made: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    skipped: bool = False
    skip_reason: Optional[str] = None


class MechanismBankUpdater:
    """Updates mechanism bank with full-text data and enhanced metadata"""

    def __init__(
        self,
        mechanism_dir: Optional[Path] = None,
        dry_run: bool = False,
        backup: bool = True
    ):
        self.mechanism_dir = mechanism_dir or (PROJECT_DIR / "mechanism-bank" / "mechanisms")
        self.dry_run = dry_run
        self.backup = backup

        # Initialize tools
        self.fulltext_fetcher = FullTextFetcher()
        self.citation_validator = CitationValidator()

        # Tracking
        self.updates: List[MechanismUpdate] = []
        self.stats = {
            "total_files": 0,
            "processed": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
            "dois_found": 0,
            "dois_verified": 0,
            "fulltext_found": 0,
            "by_source": {}
        }

        logger.info(f"Initialized updater (dry_run={dry_run})")
        logger.info(f"Full-text providers: {self.fulltext_fetcher.get_available_providers()}")

    def scan_mechanisms(self, category: Optional[str] = None) -> List[Path]:
        """Scan mechanism directory for YAML files"""
        if category:
            search_dir = self.mechanism_dir / category
            if not search_dir.exists():
                logger.error(f"Category directory not found: {search_dir}")
                return []
            pattern = "*.yml"
        else:
            search_dir = self.mechanism_dir
            pattern = "**/*.yml"

        files = list(search_dir.glob(pattern))
        self.stats["total_files"] = len(files)
        logger.info(f"Found {len(files)} mechanism files")
        return files

    def extract_doi_from_citation(self, citation: str) -> Optional[str]:
        """Extract DOI from citation string"""
        if not citation:
            return None

        # Pattern 1: https://doi.org/...
        match = re.search(r'https?://doi\.org/(10\.\d{4,}/[^\s]+)', citation)
        if match:
            return match.group(1).rstrip('.')

        # Pattern 2: doi:10.xxxx/...
        match = re.search(r'doi:\s*(10\.\d{4,}/[^\s]+)', citation, re.IGNORECASE)
        if match:
            return match.group(1).rstrip('.')

        # Pattern 3: DOI 10.xxxx/...
        match = re.search(r'DOI\s+(10\.\d{4,}/[^\s]+)', citation, re.IGNORECASE)
        if match:
            return match.group(1).rstrip('.')

        # Pattern 4: bare DOI
        match = re.search(r'(10\.\d{4,}/[^\s,]+)', citation)
        if match:
            return match.group(1).rstrip('.')

        return None

    def load_mechanism(self, file_path: Path) -> Optional[Dict]:
        """Load mechanism YAML file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return None

    def save_mechanism(self, file_path: Path, data: Dict) -> bool:
        """Save mechanism YAML file"""
        if self.dry_run:
            logger.info(f"[DRY RUN] Would save: {file_path}")
            return True

        try:
            # Backup original
            if self.backup:
                backup_path = file_path.with_suffix('.yml.bak')
                if file_path.exists():
                    import shutil
                    shutil.copy2(file_path, backup_path)

            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    data,
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                    allow_unicode=True,
                    width=100
                )
            return True
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")
            return False

    def process_mechanism(self, file_path: Path) -> MechanismUpdate:
        """Process a single mechanism file"""
        update = MechanismUpdate(
            file_path=file_path,
            mechanism_id=file_path.stem
        )

        # Load mechanism
        data = self.load_mechanism(file_path)
        if not data:
            update.errors.append("Failed to load YAML")
            update.skipped = True
            update.skip_reason = "Load error"
            return update

        # Extract evidence section
        evidence = data.get('evidence', {})

        # Check for existing DOI
        existing_doi = evidence.get('doi')
        update.original_doi = existing_doi

        # Try to extract DOI from citation if not present
        if not existing_doi:
            primary_citation = evidence.get('primary_citation', '')
            extracted_doi = self.extract_doi_from_citation(primary_citation)
            if extracted_doi:
                update.extracted_doi = extracted_doi
                self.stats["dois_found"] += 1

        # Use best available DOI
        doi = existing_doi or update.extracted_doi

        if not doi:
            update.skipped = True
            update.skip_reason = "No DOI found"
            return update

        # Verify DOI
        doi_result = verify_doi(doi)
        if doi_result["valid"]:
            update.doi_verified = True
            self.stats["dois_verified"] += 1

            # Update with verified metadata if not already present
            metadata = doi_result.get("metadata", {})
            if metadata:
                if not evidence.get('doi'):
                    evidence['doi'] = metadata.get('doi', doi)
                    update.updates_made.append("Added DOI")

                if not evidence.get('journal') and metadata.get('journal'):
                    evidence['journal'] = metadata['journal']
                    update.updates_made.append("Added journal")

                if not evidence.get('year') and metadata.get('year'):
                    evidence['year'] = metadata['year']
                    update.updates_made.append("Added year")

        # Fetch full-text
        fulltext_result = self.fulltext_fetcher.fetch_fulltext(doi)

        if fulltext_result.success:
            update.fulltext_found = True
            update.fulltext_source = fulltext_result.source.value if fulltext_result.source else None
            update.fulltext_url = fulltext_result.pdf_url
            self.stats["fulltext_found"] += 1

            # Track by source
            source_name = update.fulltext_source or "unknown"
            self.stats["by_source"][source_name] = self.stats["by_source"].get(source_name, 0) + 1

            # Add fulltext metadata to evidence
            if 'fulltext' not in evidence:
                evidence['fulltext'] = {}

            evidence['fulltext']['available'] = True
            evidence['fulltext']['source'] = update.fulltext_source
            evidence['fulltext']['url'] = update.fulltext_url
            evidence['fulltext']['is_open_access'] = fulltext_result.is_open_access
            evidence['fulltext']['fetched_date'] = datetime.now().strftime('%Y-%m-%d')

            if fulltext_result.license:
                evidence['fulltext']['license'] = fulltext_result.license

            update.updates_made.append(f"Added fulltext via {update.fulltext_source}")

        # Update citation_verified flag
        evidence['citation_verified'] = update.doi_verified
        if update.doi_verified and 'citation_verified' not in str(data):
            update.updates_made.append("Verified citation")

        # Update last_updated
        data['last_updated'] = datetime.now().strftime('%Y-%m-%d')

        # Save if updates were made
        if update.updates_made:
            data['evidence'] = evidence
            if self.save_mechanism(file_path, data):
                self.stats["updated"] += 1
            else:
                update.errors.append("Failed to save")

        return update

    def run(self, category: Optional[str] = None) -> Dict:
        """Run the update process"""
        print(f"\n{'='*80}")
        print("MECHANISM BANK FULL-TEXT UPDATE")
        print(f"{'='*80}\n")

        if self.dry_run:
            print("[DRY RUN MODE - No files will be modified]\n")

        # Scan for files
        files = self.scan_mechanisms(category)
        if not files:
            print("No mechanism files found")
            return self.stats

        print(f"Processing {len(files)} mechanism files...\n")

        # Process each file
        for i, file_path in enumerate(files, 1):
            rel_path = file_path.relative_to(self.mechanism_dir)
            print(f"[{i}/{len(files)}] {rel_path}")

            try:
                update = self.process_mechanism(file_path)
                self.updates.append(update)
                self.stats["processed"] += 1

                if update.skipped:
                    self.stats["skipped"] += 1
                    print(f"  -> Skipped: {update.skip_reason}")
                elif update.updates_made:
                    updates_str = ", ".join(update.updates_made)
                    print(f"  -> Updated: {updates_str}")
                else:
                    print(f"  -> No changes needed")

                if update.errors:
                    self.stats["errors"] += 1
                    for err in update.errors:
                        print(f"  -> ERROR: {err}")

            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                self.stats["errors"] += 1

        # Print summary
        self._print_summary()

        return self.stats

    def _print_summary(self):
        """Print update summary"""
        print(f"\n{'='*80}")
        print("UPDATE SUMMARY")
        print(f"{'='*80}\n")

        print(f"Total files:     {self.stats['total_files']}")
        print(f"Processed:       {self.stats['processed']}")
        print(f"Updated:         {self.stats['updated']}")
        print(f"Skipped:         {self.stats['skipped']}")
        print(f"Errors:          {self.stats['errors']}")
        print()
        print(f"DOIs found:      {self.stats['dois_found']}")
        print(f"DOIs verified:   {self.stats['dois_verified']}")
        print(f"Full-text found: {self.stats['fulltext_found']}")

        if self.stats["by_source"]:
            print("\nFull-text by source:")
            for source, count in sorted(self.stats["by_source"].items(), key=lambda x: x[1], reverse=True):
                print(f"  {source}: {count}")

        # Success rate
        if self.stats["processed"] > 0:
            update_rate = self.stats["updated"] / self.stats["processed"] * 100
            fulltext_rate = self.stats["fulltext_found"] / self.stats["processed"] * 100
            print(f"\nUpdate rate:     {update_rate:.1f}%")
            print(f"Full-text rate:  {fulltext_rate:.1f}%")

    def generate_report(self, output_file: Optional[Path] = None) -> Dict:
        """Generate detailed update report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "stats": self.stats,
            "updates": [
                {
                    "file": str(u.file_path.relative_to(self.mechanism_dir)),
                    "mechanism_id": u.mechanism_id,
                    "original_doi": u.original_doi,
                    "extracted_doi": u.extracted_doi,
                    "doi_verified": u.doi_verified,
                    "fulltext_found": u.fulltext_found,
                    "fulltext_source": u.fulltext_source,
                    "updates_made": u.updates_made,
                    "errors": u.errors,
                    "skipped": u.skipped,
                    "skip_reason": u.skip_reason
                }
                for u in self.updates
            ]
        }

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"Report saved to: {output_file}")

        return report


def main():
    parser = argparse.ArgumentParser(description="Update mechanism bank with full-text data")
    parser.add_argument('--dry-run', action='store_true', help="Don't modify files, just report")
    parser.add_argument('--category', type=str, help="Only process specific category")
    parser.add_argument('--no-backup', action='store_true', help="Don't create backup files")
    parser.add_argument('--report', type=str, help="Output report file path")

    args = parser.parse_args()

    updater = MechanismBankUpdater(
        dry_run=args.dry_run,
        backup=not args.no_backup
    )

    stats = updater.run(category=args.category)

    # Generate report
    report_path = args.report or f"mechanism_update_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    updater.generate_report(Path(report_path))

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
