"""
Database seeding script for Railway deployment.

This script:
1. Loads ONLY nodes defined in nodes/by_scale/ directory
2. Loads ONLY mechanisms from mechanism-bank/mechanisms/{category}/ where:
   - The mechanism file does NOT have a NEW: prefix
   - BOTH from_node and to_node exist in nodes/by_scale/
3. Supports quality filtering (min_quality parameter)
4. Supports topic filtering (e.g., alcohol-related mechanisms)
5. Idempotent - can be run multiple times safely

IMPORTANT: Mechanisms referencing undefined nodes are skipped.
The NEW: prefix indicates proposed/candidate mechanisms not yet validated.

Valid mechanism categories:
- behavioral, built_environment, economic, healthcare_access,
  political, social_environment, biological

Usage:
    # Seed all valid mechanisms (no filters):
    python seed_database.py

    # Seed only high-quality mechanisms (A or B rating):
    python seed_database.py --min-quality B

    # Seed only alcohol-related mechanisms:
    python seed_database.py --topic alcohol

    # Seed alcohol mechanisms with quality B or better:
    python seed_database.py --min-quality B --topic alcohol
"""

import os
import sys
import yaml
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import Base
from models.mechanism import Node, Mechanism
from config.database import DatabaseConfig

# Quality rating hierarchy (A is best, C is worst)
QUALITY_HIERARCHY = {'A': 1, 'B': 2, 'C': 3}

# Topic keywords for filtering
TOPIC_KEYWORDS = {
    'alcohol': [
        'alcohol', 'aud', 'drinking', 'binge', 'liver_disease', 'cirrhosis',
        'intoxication', 'withdrawal', 'ethanol', 'liquor', 'beer', 'wine',
        'dui', 'dwi', 'hangover', 'detox', 'sobriety', 'abstinence'
    ],
    'housing': [
        'housing', 'homeless', 'eviction', 'rent', 'mortgage', 'foreclosure',
        'shelter', 'dwelling', 'residence', 'landlord', 'tenant'
    ],
    'respiratory': [
        'asthma', 'copd', 'respiratory', 'lung', 'breathing', 'air_quality',
        'pm25', 'pollution', 'ventilation', 'mold'
    ],
}

# Valid mechanism category subdirectories
VALID_MECHANISM_CATEGORIES = [
    'behavioral',
    'built_environment',
    'economic',
    'healthcare_access',
    'political',
    'social_environment',
    'biological'
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """Seeds database with mechanisms from YAML files."""

    def __init__(
        self,
        database_url: Optional[str] = None,
        min_quality: Optional[str] = None,
        topic: Optional[str] = None
    ):
        """
        Initialize seeder with database connection and filters.

        Args:
            database_url: Database connection URL
            min_quality: Minimum evidence quality (A, B, or C). If set, only
                        mechanisms with this quality or better are loaded.
                        A is best, C is lowest.
            topic: Topic filter (e.g., 'alcohol', 'housing', 'respiratory').
                   If set, only mechanisms related to this topic are loaded.
        """
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "sqlite:///./healthsystems.db"
        )
        self.min_quality = min_quality
        self.topic = topic

        # Create engine
        self.engine = create_engine(
            self.database_url,
            echo=False,
            pool_pre_ping=True
        )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        # Track unique nodes (loaded from nodes/by_scale/)
        self.nodes_cache: Dict[str, Node] = {}
        # Set of valid node IDs (only nodes from YAML files are valid)
        self.valid_node_ids: Set[str] = set()

    def passes_quality_filter(self, mech_data: Dict) -> bool:
        """Check if mechanism passes quality filter."""
        if not self.min_quality:
            return True

        evidence = mech_data.get('evidence', {})
        quality = evidence.get('quality_rating', 'C')

        # Compare quality ratings (lower number = better quality)
        mech_rank = QUALITY_HIERARCHY.get(quality.upper(), 3)
        min_rank = QUALITY_HIERARCHY.get(self.min_quality.upper(), 3)

        return mech_rank <= min_rank

    def passes_topic_filter(self, mech_data: Dict) -> bool:
        """Check if mechanism passes topic filter."""
        if not self.topic:
            return True

        keywords = TOPIC_KEYWORDS.get(self.topic.lower(), [])
        if not keywords:
            logger.warning(f"Unknown topic '{self.topic}'. Available: {list(TOPIC_KEYWORDS.keys())}")
            return True

        # Check mechanism ID, from_node, to_node, description
        mech_id = mech_data.get('id', '').lower()
        description = mech_data.get('description', '').lower()

        # Extract node IDs
        from_node_id, to_node_id = '', ''
        if '_to_' in mech_id:
            parts = mech_id.split('_to_')
            from_node_id = parts[0].lower()
            to_node_id = '_to_'.join(parts[1:]).lower()

        # Check if any keyword matches
        text_to_search = f"{mech_id} {from_node_id} {to_node_id} {description}"
        return any(keyword in text_to_search for keyword in keywords)

    def has_valid_node_references(self, mech_data: Dict) -> bool:
        """
        Check if mechanism references nodes that exist in nodes/by_scale/.

        Returns False if:
        - Either node has NEW: prefix (proposed/candidate node)
        - Either node doesn't exist in valid_node_ids set
        """
        # Get node IDs from mechanism data structure
        from_node = mech_data.get('from_node', {})
        to_node = mech_data.get('to_node', {})

        from_node_id = from_node.get('node_id', '')
        to_node_id = to_node.get('node_id', '')

        # If no from_node/to_node structure, try to parse from ID
        if not from_node_id or not to_node_id:
            mech_id = mech_data.get('id', '')
            if '_to_' in mech_id:
                parts = mech_id.split('_to_')
                from_node_id = from_node_id or parts[0]
                to_node_id = to_node_id or '_to_'.join(parts[1:])

        # Skip if either contains NEW: prefix
        if 'NEW:' in from_node_id or 'NEW:' in to_node_id:
            return False

        # Check both nodes exist in valid set
        return from_node_id in self.valid_node_ids and to_node_id in self.valid_node_ids

    def init_tables(self, drop_existing: bool = False):
        """Create all database tables."""
        from sqlalchemy import text, inspect
        if drop_existing:
            logger.info("Dropping existing database tables...")
            # Drop all indexes first via SQLAlchemy inspector (database-agnostic)
            with self.engine.connect() as conn:
                inspector = inspect(conn)
                dialect_name = conn.dialect.name

                # Get all tables and their indexes
                for table_name in inspector.get_table_names():
                    for index in inspector.get_indexes(table_name):
                        index_name = index['name']
                        if index_name and index_name.startswith('ix_'):
                            try:
                                if dialect_name == 'postgresql':
                                    conn.execute(text(f'DROP INDEX IF EXISTS "{index_name}"'))
                                else:
                                    conn.execute(text(f"DROP INDEX IF EXISTS {index_name}"))
                            except Exception as e:
                                logger.debug(f"Could not drop index {index_name}: {e}")
                conn.commit()
            Base.metadata.drop_all(bind=self.engine)
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=self.engine, checkfirst=True)
        logger.info("Database tables created successfully")

    def load_mechanism_files(self) -> List[Path]:
        """
        Load valid mechanism YAML files from mechanism-bank categories.

        Only loads files from valid category subdirectories and excludes:
        - Files with NEW: prefix (proposed/candidate mechanisms)
        - JSON files (metadata files)
        - Files not in valid category directories
        """
        mechanism_bank_path = Path(__file__).parent.parent.parent / "mechanism-bank" / "mechanisms"

        if not mechanism_bank_path.exists():
            logger.error(f"Mechanism bank not found at {mechanism_bank_path}")
            return []

        yaml_files = []
        new_prefix_count = 0

        # Only load from valid category subdirectories
        for category in VALID_MECHANISM_CATEGORIES:
            category_path = mechanism_bank_path / category
            if not category_path.exists():
                logger.debug(f"Category directory not found: {category}")
                continue

            # Find YAML files in this category (not recursive - only direct children)
            for pattern in ["*.yaml", "*.yml"]:
                for f in category_path.glob(pattern):
                    # Skip files with NEW: prefix
                    if f.name.startswith('NEW:'):
                        new_prefix_count += 1
                        continue
                    yaml_files.append(f)

        logger.info(f"Found {len(yaml_files)} valid mechanism files")
        logger.info(f"Skipped {new_prefix_count} files with NEW: prefix")
        return yaml_files

    def load_node_files(self) -> List[Path]:
        """Load all node YAML files from nodes/by_scale/ directory."""
        nodes_path = Path(__file__).parent.parent.parent / "nodes" / "by_scale"

        if not nodes_path.exists():
            logger.warning(f"Nodes directory not found at {nodes_path}")
            return []

        # Find all YAML files recursively
        yaml_files = list(nodes_path.glob("**/*.yml")) + \
                     list(nodes_path.glob("**/*.yaml"))

        logger.info(f"Found {len(yaml_files)} node definition files")
        return yaml_files

    def extract_scale_from_path(self, file_path: Path) -> int:
        """Extract scale level from node file path (e.g., scale_5_behaviors -> 5)."""
        path_str = str(file_path)

        # Look for scale_N pattern in path
        import re
        match = re.search(r'scale_(\d+)', path_str)
        if match:
            return int(match.group(1))

        # Fallback to default
        return 4

    def load_node_from_yaml(self, session: Session, file_path: Path) -> Optional[Node]:
        """Load a node from a YAML definition file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data or 'id' not in data:
                return None

            node_id = data.get('id')

            # Check if node already exists
            stmt = select(Node).where(Node.id == node_id)
            existing_node = session.execute(stmt).scalar_one_or_none()

            if existing_node:
                # Update existing node with YAML data
                existing_node.name = data.get('name', node_id.replace('_', ' ').title())
                existing_node.scale = data.get('scale', self.extract_scale_from_path(file_path))
                existing_node.category = data.get('category', 'built_environment')
                existing_node.description = data.get('description', '')
                existing_node.node_type = data.get('type', 'stock').lower()
                self.nodes_cache[node_id] = existing_node
                return existing_node

            # Create new node
            new_node = Node(
                id=node_id,
                name=data.get('name', node_id.replace('_', ' ').title()),
                node_type=data.get('type', 'stock').lower(),
                category=data.get('category', 'built_environment'),
                scale=data.get('scale', self.extract_scale_from_path(file_path)),
                description=data.get('description', '')
            )

            session.add(new_node)
            self.nodes_cache[node_id] = new_node
            return new_node

        except Exception as e:
            logger.warning(f"Error loading node from {file_path}: {e}")
            return None

    def seed_nodes_from_yaml(self, session: Session) -> int:
        """
        Load all nodes from YAML definition files.

        This also populates self.valid_node_ids with all node IDs
        that are loaded, so mechanisms can be validated against this set.
        """
        node_files = self.load_node_files()
        nodes_loaded = 0

        for file_path in node_files:
            node = self.load_node_from_yaml(session, file_path)
            if node:
                nodes_loaded += 1
                # Add to valid node IDs set
                self.valid_node_ids.add(node.id)

            # Commit every 50 nodes
            if nodes_loaded % 50 == 0:
                session.commit()
                logger.info(f"Loaded {nodes_loaded}/{len(node_files)} node definitions...")

        session.commit()
        logger.info(f"Loaded {nodes_loaded} nodes from YAML definitions")
        logger.info(f"Valid node IDs registered: {len(self.valid_node_ids)}")
        return nodes_loaded

    def parse_yaml_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a single YAML file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

                # Validate minimum required fields
                if not data:
                    logger.warning(f"Empty YAML file: {file_path.name}")
                    return None

                if 'id' not in data:
                    logger.warning(f"Missing 'id' field in {file_path.name}")
                    return None

                return data
        except yaml.YAMLError as e:
            logger.warning(f"YAML syntax error in {file_path.name}: {e} - skipping")
            return None
        except Exception as e:
            logger.warning(f"Error parsing {file_path.name}: {e} - skipping")
            return None

    def infer_direction(self, mech_data: Dict) -> str:
        """Infer mechanism direction (positive/negative)."""
        # Check for explicit direction field
        direction = mech_data.get('direction', '').lower()
        if direction in ['positive', 'negative']:
            return direction

        # Try to infer from effect size or description
        effect_size = mech_data.get('effect_size', {})
        point_estimate = effect_size.get('point_estimate')

        if point_estimate:
            return 'positive' if point_estimate > 1 or point_estimate > 0 else 'negative'

        # Default to positive
        return 'positive'

    def parse_date(self, date_value) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_value:
            return None

        if isinstance(date_value, datetime):
            return date_value

        if isinstance(date_value, str):
            try:
                # Try parsing ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
                if 'T' in date_value:
                    return datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                else:
                    return datetime.strptime(date_value, '%Y-%m-%d')
            except:
                logger.warning(f"Could not parse date: {date_value}")
                return None

        return None

    def get_node_ids_from_mechanism(self, mech_data: Dict) -> tuple[str, str]:
        """
        Extract from_node_id and to_node_id from mechanism data.

        Tries to get IDs from:
        1. from_node.node_id and to_node.node_id (preferred structure)
        2. Parsing the mechanism ID (fallback)
        """
        # Try from_node/to_node structure first
        from_node = mech_data.get('from_node', {})
        to_node = mech_data.get('to_node', {})

        from_node_id = from_node.get('node_id', '')
        to_node_id = to_node.get('node_id', '')

        # If not found, try parsing from mechanism ID
        if not from_node_id or not to_node_id:
            mech_id = mech_data.get('id', '')
            if '_to_' in mech_id:
                parts = mech_id.split('_to_')
                from_node_id = from_node_id or parts[0]
                to_node_id = to_node_id or '_to_'.join(parts[1:])

        return from_node_id, to_node_id

    def create_mechanism(self, session: Session, mech_data: Dict) -> Optional[Mechanism]:
        """
        Create mechanism from YAML data.

        IMPORTANT: Does NOT create nodes - only uses existing nodes from cache.
        Mechanisms referencing non-existent nodes will return None.
        """
        try:
            mech_id = mech_data.get('id')
            if not mech_id:
                logger.warning("Mechanism missing ID, skipping")
                return None

            # Check if mechanism already exists
            stmt = select(Mechanism).where(Mechanism.id == mech_id)
            existing_mech = session.execute(stmt).scalar_one_or_none()

            if existing_mech:
                logger.debug(f"Mechanism {mech_id} already exists, skipping")
                return existing_mech

            # Get node IDs from mechanism data
            from_node_id, to_node_id = self.get_node_ids_from_mechanism(mech_data)
            category = mech_data.get('category', 'built_environment')

            # Lookup nodes from cache (do NOT create new nodes)
            if from_node_id not in self.nodes_cache:
                logger.debug(f"Skipping mechanism {mech_id}: from_node '{from_node_id}' not in valid nodes")
                return None
            if to_node_id not in self.nodes_cache:
                logger.debug(f"Skipping mechanism {mech_id}: to_node '{to_node_id}' not in valid nodes")
                return None

            from_node = self.nodes_cache[from_node_id]
            to_node = self.nodes_cache[to_node_id]

            # Extract evidence data
            evidence = mech_data.get('evidence', {})

            # Create mechanism
            mechanism = Mechanism(
                id=mech_id,
                name=mech_data.get('name', mech_id),
                from_node_id=from_node_id,
                to_node_id=to_node_id,
                direction=self.infer_direction(mech_data),
                category=category,
                mechanism_pathway=mech_data.get('mechanism_pathway', []),
                evidence_quality=evidence.get('quality_rating', 'C'),
                evidence_n_studies=evidence.get('n_studies', 1),
                evidence_primary_citation=evidence.get('primary_citation', evidence.get('citation', 'No citation provided')).strip(),
                evidence_supporting_citations=evidence.get('supporting_citations', []),
                evidence_doi=evidence.get('doi'),
                varies_by_geography=mech_data.get('varies_by_geography', False),
                variation_notes=mech_data.get('variation_notes'),
                relevant_geographies=mech_data.get('relevant_geographies', []),
                moderators=mech_data.get('moderators', []),
                structural_competency_root_cause=mech_data.get('structural_competency', {}).get('root_cause'),
                structural_competency_avoids_victim_blaming=mech_data.get('structural_competency', {}).get('avoids_victim_blaming', True),
                structural_competency_equity_implications=mech_data.get('structural_competency', {}).get('equity_implications'),
                version=str(mech_data.get('version', '1.0')),
                last_updated=self.parse_date(mech_data.get('last_updated')),
                validated_by=mech_data.get('validated_by', []),
                description=mech_data.get('description', '').strip(),
                assumptions=mech_data.get('assumptions', []),
                limitations=mech_data.get('limitations', [])
            )

            session.add(mechanism)
            logger.debug(f"Created mechanism: {mech_id}")

            return mechanism

        except Exception as e:
            logger.error(f"Error creating mechanism {mech_data.get('id', 'unknown')}: {e}")
            return None

    def seed(self, skip_if_data_exists: bool = True) -> Dict[str, int]:
        """
        Main seeding function.

        Args:
            skip_if_data_exists: If True, skip seeding if data already exists

        Returns:
            Dictionary with counts of nodes and mechanisms created

        IMPORTANT: Only seeds nodes from nodes/by_scale/ and mechanisms
        where both from_node and to_node exist in that directory.
        """
        stats = {
            'nodes_from_yaml': 0,
            'mechanisms_created': 0,
            'mechanisms_filtered_invalid_nodes': 0,
            'mechanisms_filtered_quality': 0,
            'mechanisms_filtered_topic': 0,
            'files_processed': 0,
            'files_failed': 0
        }

        session = self.SessionLocal()

        try:
            # Check if data already exists
            if skip_if_data_exists:
                existing_count = session.query(Mechanism).count()
                if existing_count > 0:
                    logger.info(f"Database already contains {existing_count} mechanisms. Skipping seed.")
                    return stats

            # Log filter settings
            if self.min_quality:
                logger.info(f"Quality filter: {self.min_quality} or better")
            if self.topic:
                logger.info(f"Topic filter: {self.topic}")

            # Step 1: Load nodes from YAML definitions
            logger.info("=" * 60)
            logger.info("STEP 1: Loading node definitions from YAML files")
            logger.info("=" * 60)
            stats['nodes_from_yaml'] = self.seed_nodes_from_yaml(session)

            # Step 2: Load mechanism files
            logger.info("=" * 60)
            logger.info("STEP 2: Loading mechanisms from mechanism-bank")
            logger.info("=" * 60)
            yaml_files = self.load_mechanism_files()

            if not yaml_files:
                logger.warning("No mechanism files found to seed")
                return stats

            # Process each file
            for yaml_file in yaml_files:
                try:
                    mech_data = self.parse_yaml_file(yaml_file)

                    if not mech_data:
                        stats['files_failed'] += 1
                        continue

                    # Check for valid node references FIRST
                    if not self.has_valid_node_references(mech_data):
                        stats['mechanisms_filtered_invalid_nodes'] += 1
                        stats['files_processed'] += 1
                        continue

                    # Apply quality filter
                    if not self.passes_quality_filter(mech_data):
                        stats['mechanisms_filtered_quality'] += 1
                        stats['files_processed'] += 1
                        continue

                    # Apply topic filter
                    if not self.passes_topic_filter(mech_data):
                        stats['mechanisms_filtered_topic'] += 1
                        stats['files_processed'] += 1
                        continue

                    # Create mechanism (only uses existing nodes from cache)
                    mechanism = self.create_mechanism(session, mech_data)

                    if mechanism:
                        stats['mechanisms_created'] += 1

                    stats['files_processed'] += 1

                    # Commit every 10 files to avoid large transactions
                    if stats['files_processed'] % 10 == 0:
                        session.commit()
                        logger.info(f"Processed {stats['files_processed']}/{len(yaml_files)} files...")

                except Exception as e:
                    logger.error(f"Error processing {yaml_file}: {e}")
                    stats['files_failed'] += 1
                    session.rollback()

            # Final commit
            session.commit()

            # Get final counts
            total_nodes = session.query(Node).count()
            total_mechanisms = session.query(Mechanism).count()

            logger.info("=" * 60)
            logger.info("DATABASE SEEDING COMPLETE")
            logger.info("=" * 60)
            logger.info(f"Filters applied:")
            logger.info(f"  - Quality: {self.min_quality or 'None'}")
            logger.info(f"  - Topic: {self.topic or 'None'}")
            logger.info("-" * 60)
            logger.info(f"Node definitions loaded from YAML: {stats['nodes_from_yaml']}")
            logger.info(f"Mechanisms created: {stats['mechanisms_created']}")
            logger.info(f"Mechanisms filtered (invalid nodes): {stats['mechanisms_filtered_invalid_nodes']}")
            logger.info(f"Mechanisms filtered (quality): {stats['mechanisms_filtered_quality']}")
            logger.info(f"Mechanisms filtered (topic): {stats['mechanisms_filtered_topic']}")
            logger.info(f"Files failed: {stats['files_failed']}")
            logger.info("-" * 60)
            logger.info(f"TOTAL nodes in database: {total_nodes}")
            logger.info(f"TOTAL mechanisms in database: {total_mechanisms}")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"Fatal error during seeding: {e}")
            session.rollback()
            raise
        finally:
            session.close()

        return stats


def main():
    """Run database seeding with command-line options."""
    parser = argparse.ArgumentParser(
        description="Seed the HealthSystems database with nodes and mechanisms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Seed all mechanisms (no filters):
  python seed_database.py

  # Seed only high-quality mechanisms (A or B rating):
  python seed_database.py --min-quality B

  # Seed only alcohol-related mechanisms:
  python seed_database.py --topic alcohol

  # Seed alcohol mechanisms with quality B or better:
  python seed_database.py --min-quality B --topic alcohol

  # Keep existing data (don't drop tables):
  python seed_database.py --no-drop

Available topics: alcohol, housing, respiratory
Quality ratings: A (best), B, C (lowest)
        """
    )

    parser.add_argument(
        '--min-quality', '-q',
        choices=['A', 'B', 'C'],
        help='Minimum evidence quality rating (A=best, C=lowest)'
    )

    parser.add_argument(
        '--topic', '-t',
        choices=list(TOPIC_KEYWORDS.keys()),
        help='Filter mechanisms by topic'
    )

    parser.add_argument(
        '--no-drop',
        action='store_true',
        help='Do not drop existing tables before seeding'
    )

    parser.add_argument(
        '--skip-if-exists',
        action='store_true',
        help='Skip seeding if data already exists'
    )

    args = parser.parse_args()

    logger.info("Starting database seeding process...")
    logger.info(f"Options: min_quality={args.min_quality}, topic={args.topic}")

    # Initialize seeder with filters
    seeder = DatabaseSeeder(
        min_quality=args.min_quality,
        topic=args.topic
    )

    # Create tables
    seeder.init_tables(drop_existing=not args.no_drop)

    # Seed data
    stats = seeder.seed(skip_if_data_exists=args.skip_if_exists)

    total_created = stats.get('nodes_from_yaml', 0) + stats.get('mechanisms_created', 0)
    if total_created > 0:
        logger.info("Database seeded successfully!")
    else:
        logger.info("Database already seeded or no data to seed")

    return 0


def seed_base_system():
    """Convenience function to seed the base system with all mechanisms."""
    logger.info("Seeding BASE system (all nodes, all mechanisms)...")
    seeder = DatabaseSeeder()
    seeder.init_tables(drop_existing=True)
    return seeder.seed(skip_if_data_exists=False)


def seed_alcohol_system(min_quality: str = 'C'):
    """Convenience function to seed only alcohol-related mechanisms."""
    logger.info(f"Seeding ALCOHOL system (quality >= {min_quality})...")
    seeder = DatabaseSeeder(min_quality=min_quality, topic='alcohol')
    seeder.init_tables(drop_existing=True)
    return seeder.seed(skip_if_data_exists=False)


if __name__ == "__main__":
    sys.exit(main())
