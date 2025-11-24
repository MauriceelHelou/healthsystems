"""
Database Audit Script
Query current state of nodes and scales in the database
"""
from sqlalchemy import create_engine, text
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.database import db_config

def audit_database():
    engine = create_engine(db_config.database_url)

    with engine.connect() as conn:
        # Count total nodes
        result = conn.execute(text('SELECT COUNT(DISTINCT node_id) as node_count FROM nodes'))
        total_nodes = result.fetchone()[0]
        print(f'\n=== DATABASE AUDIT ===')
        print(f'\nTotal nodes in database: {total_nodes}')

        # Check which scales are in use
        result = conn.execute(text('SELECT DISTINCT scale FROM nodes ORDER BY scale'))
        scales = [row[0] for row in result.fetchall()]
        print(f'\nScales in use: {scales}')

        # Count nodes per scale
        result = conn.execute(text('SELECT scale, COUNT(*) as count FROM nodes GROUP BY scale ORDER BY scale'))
        print(f'\nNodes per scale:')
        for row in result.fetchall():
            print(f'  Scale {row[0]}: {row[1]} nodes')

        # Count mechanisms
        result = conn.execute(text('SELECT COUNT(*) as count FROM mechanisms'))
        total_mechanisms = result.fetchone()[0]
        print(f'\nTotal mechanisms: {total_mechanisms}')

        # Check categories
        result = conn.execute(text('SELECT DISTINCT category FROM nodes ORDER BY category'))
        categories = [row[0] for row in result.fetchall()]
        print(f'\nCategories in use: {", ".join(categories)}')

        # Sample some node IDs
        result = conn.execute(text('SELECT node_id, label, scale, category FROM nodes LIMIT 10'))
        print(f'\nSample nodes:')
        for row in result.fetchall():
            print(f'  {row[0]} | scale={row[2]} | {row[3]} | {row[1][:50]}')

if __name__ == '__main__':
    audit_database()
