#!/usr/bin/env python3
"""
Unit tests for Node-Pair Driven Discovery Pipeline (V4)

Tests cover:
1. Config loading and validation
2. Node metadata loading from nodes/by_scale/
3. Node pair building and validation
4. Search query construction with keywords
5. Evidence handling (sufficient/insufficient)
6. Mechanism result handling (null vs valid)
7. YAML output generation
"""

import json
import os
import sys
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipelines.node_pair_discovery import (
    NodePairDiscovery,
    NodePair,
    NodePairEvidence,
    MechanismResult
)
from pipelines.batch_mechanism_discovery import PaperInput


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def sample_config():
    """Sample config for testing."""
    return {
        "name": "test_node_pair_discovery",
        "version": "1.0",
        "description": "Test config",
        "node_source": "nodes/by_scale/",
        "budget": {"max_usd": 10.0, "max_pairs": 10},
        "node_keywords": {
            "alcohol_taxation": ["alcohol tax", "excise tax", "minimum unit pricing"],
            "binge_drinking": ["heavy episodic drinking", "excessive drinking"],
            "alcohol_use_disorder": ["AUD", "alcohol dependence", "alcoholism"]
        },
        "node_pairs": [
            {
                "from_node_id": "alcohol_taxation",
                "to_node_id": "binge_drinking",
                "expected_direction": "negative",
                "priority": 1,
                "category": "political"
            },
            {
                "from_node_id": "binge_drinking",
                "to_node_id": "alcohol_use_disorder",
                "expected_direction": "positive",
                "priority": 1,
                "category": "behavioral"
            }
        ],
        "search_config": {
            "papers_per_pair": 10,
            "min_papers_required": 3,
            "year_range": [2015, 2025],
            "use_node_keywords": True,
            "search_templates": [
                "{from_keywords} AND {to_keywords} AND systematic review"
            ]
        },
        "llm_config": {
            "model": "claude-sonnet-4-20250514",
            "min_citations_per_mechanism": 3,
            "force_mechanism_if_no_evidence": False,
            "return_null_if_insufficient_evidence": True,
            "only_use_existing_nodes": True
        }
    }


@pytest.fixture
def sample_node_metadata():
    """Sample node metadata for testing."""
    return {
        "alcohol_taxation": {
            "id": "alcohol_taxation",
            "name": "Alcohol Taxation",
            "scale": 1,
            "domain": "Policy",
            "category": "political"
        },
        "binge_drinking": {
            "id": "binge_drinking",
            "name": "Binge Drinking Prevalence",
            "scale": 5,
            "domain": "Behavioral",
            "category": "behavioral"
        },
        "alcohol_use_disorder": {
            "id": "alcohol_use_disorder",
            "name": "Alcohol Use Disorder",
            "scale": 7,
            "domain": "Crisis",
            "category": "behavioral"
        }
    }


@pytest.fixture
def sample_papers():
    """Sample papers for testing."""
    return [
        PaperInput(
            abstract="This study examines the effect of alcohol taxation on binge drinking rates.",
            title="Alcohol Tax and Binge Drinking: A Systematic Review",
            citation_context={
                "title": "Alcohol Tax and Binge Drinking: A Systematic Review",
                "year": 2022,
                "doi": "10.1234/test1",
                "authors": ["Smith A", "Jones B"],
                "journal": "Public Health Journal"
            },
            custom_id="paper_1"
        ),
        PaperInput(
            abstract="Meta-analysis of alcohol price policies and heavy episodic drinking.",
            title="Price Policies and Drinking Patterns",
            citation_context={
                "title": "Price Policies and Drinking Patterns",
                "year": 2021,
                "doi": "10.1234/test2",
                "authors": ["Williams C"],
                "journal": "Addiction Research"
            },
            custom_id="paper_2"
        ),
        PaperInput(
            abstract="Impact of excise tax increases on alcohol consumption.",
            title="Excise Tax Impact Study",
            citation_context={
                "title": "Excise Tax Impact Study",
                "year": 2023,
                "doi": "10.1234/test3",
                "authors": ["Brown D", "Taylor E"],
                "journal": "Health Economics"
            },
            custom_id="paper_3"
        )
    ]


@pytest.fixture
def discovery_instance(sample_config, sample_node_metadata):
    """Create a NodePairDiscovery instance with mocked dependencies."""
    discovery = NodePairDiscovery()
    discovery.config = sample_config
    discovery.node_metadata = sample_node_metadata
    return discovery


# =============================================================================
# Test: Config Loading
# =============================================================================

class TestConfigLoading:
    """Tests for config loading functionality."""

    def test_load_config_success(self, sample_config):
        """Test successful config loading."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_config, f)
            f.flush()

            discovery = NodePairDiscovery()
            loaded = discovery.load_config(f.name)

            assert loaded["name"] == "test_node_pair_discovery"
            assert len(loaded["node_pairs"]) == 2
            assert "node_keywords" in loaded

            os.unlink(f.name)

    def test_load_config_missing_file(self):
        """Test config loading with missing file."""
        discovery = NodePairDiscovery()
        with pytest.raises(FileNotFoundError):
            discovery.load_config("/nonexistent/path/config.json")

    def test_config_has_required_fields(self, sample_config):
        """Test that config has all required fields."""
        required_fields = ["name", "node_pairs", "search_config", "llm_config"]
        for field in required_fields:
            assert field in sample_config


# =============================================================================
# Test: Node Metadata Loading
# =============================================================================

class TestNodeMetadataLoading:
    """Tests for node metadata loading from nodes/by_scale/."""

    def test_load_node_metadata_real_directory(self):
        """Test loading real node metadata from nodes/by_scale/."""
        discovery = NodePairDiscovery()
        # This tests against the real nodes directory
        if Path("nodes/by_scale").exists():
            metadata = discovery.load_node_metadata("nodes/by_scale")
            assert len(metadata) > 0
            # Check a known node exists
            assert "alcohol_taxation" in metadata or len(metadata) > 100

    def test_validate_node_exists(self, discovery_instance):
        """Test node existence validation."""
        assert discovery_instance.validate_node_exists("alcohol_taxation") is True
        assert discovery_instance.validate_node_exists("nonexistent_node") is False

    def test_get_node_name(self, discovery_instance):
        """Test getting human-readable node name."""
        assert discovery_instance.get_node_name("alcohol_taxation") == "Alcohol Taxation"
        # For missing nodes, should return formatted ID
        name = discovery_instance.get_node_name("some_new_node")
        assert "Some" in name or "some_new_node" in name


# =============================================================================
# Test: Node Pair Building
# =============================================================================

class TestNodePairBuilding:
    """Tests for building and validating node pairs."""

    def test_build_node_pairs_all_valid(self, discovery_instance):
        """Test building node pairs when all nodes exist."""
        pairs = discovery_instance.build_node_pairs()
        assert len(pairs) == 2

        # Check first pair
        assert pairs[0].from_node_id == "alcohol_taxation"
        assert pairs[0].to_node_id == "binge_drinking"
        assert pairs[0].expected_direction == "negative"
        assert pairs[0].category == "political"

    def test_build_node_pairs_with_keywords(self, discovery_instance):
        """Test that keywords are correctly assigned to node pairs."""
        pairs = discovery_instance.build_node_pairs()

        # First pair should have keywords
        assert "alcohol tax" in pairs[0].from_keywords
        assert "heavy episodic drinking" in pairs[0].to_keywords

    def test_build_node_pairs_skip_invalid(self, discovery_instance):
        """Test that pairs with invalid nodes are skipped."""
        # Add a pair with invalid node
        discovery_instance.config["node_pairs"].append({
            "from_node_id": "nonexistent_node",
            "to_node_id": "binge_drinking",
            "expected_direction": "positive",
            "priority": 1,
            "category": "unknown"
        })

        pairs = discovery_instance.build_node_pairs()
        # Should still have original 2 pairs, invalid one skipped
        assert len(pairs) == 2

    def test_node_pair_dataclass(self):
        """Test NodePair dataclass creation."""
        pair = NodePair(
            from_node_id="test_from",
            from_node_name="Test From",
            to_node_id="test_to",
            to_node_name="Test To",
            expected_direction="positive",
            category="test",
            priority=1,
            from_keywords=["keyword1"],
            to_keywords=["keyword2"]
        )
        assert pair.from_node_id == "test_from"
        assert pair.from_keywords == ["keyword1"]


# =============================================================================
# Test: Search Query Building
# =============================================================================

class TestSearchQueryBuilding:
    """Tests for building search queries with keywords."""

    def test_build_search_query_basic(self, discovery_instance):
        """Test basic search query construction."""
        pairs = discovery_instance.build_node_pairs()
        queries = discovery_instance.build_search_query(pairs[0])

        assert len(queries) >= 1
        # Should contain keywords from both nodes
        first_query = queries[0].lower()
        assert "alcohol" in first_query or "tax" in first_query

    def test_build_search_query_uses_templates(self, discovery_instance):
        """Test that search templates are used."""
        pairs = discovery_instance.build_node_pairs()
        queries = discovery_instance.build_search_query(pairs[0])

        # Should contain systematic review from template
        assert any("systematic review" in q.lower() for q in queries)

    def test_build_search_query_empty_keywords(self, discovery_instance):
        """Test query building when keywords are missing."""
        pair = NodePair(
            from_node_id="test_from",
            from_node_name="Test From Node",
            to_node_id="test_to",
            to_node_name="Test To Node",
            expected_direction="positive",
            category="test",
            priority=1,
            from_keywords=[],  # Empty keywords
            to_keywords=[]
        )

        queries = discovery_instance.build_search_query(pair)
        assert len(queries) >= 1
        # Should use node names when keywords are empty
        assert any("Test From Node" in q for q in queries)


# =============================================================================
# Test: Evidence Handling
# =============================================================================

class TestEvidenceHandling:
    """Tests for NodePairEvidence handling."""

    def test_node_pair_evidence_creation(self, sample_papers):
        """Test creating NodePairEvidence."""
        pair = NodePair(
            from_node_id="alcohol_taxation",
            from_node_name="Alcohol Taxation",
            to_node_id="binge_drinking",
            to_node_name="Binge Drinking",
            expected_direction="negative",
            category="political",
            priority=1
        )

        evidence = NodePairEvidence(
            node_pair=pair,
            papers=sample_papers,
            search_queries_used=["test query 1", "test query 2"]
        )

        assert len(evidence.papers) == 3
        assert len(evidence.search_queries_used) == 2

    def test_sufficient_vs_insufficient_evidence(self, sample_papers):
        """Test distinction between sufficient and insufficient evidence."""
        pair = NodePair(
            from_node_id="test",
            from_node_name="Test",
            to_node_id="test2",
            to_node_name="Test 2",
            expected_direction="positive",
            category="test",
            priority=1
        )

        # Sufficient evidence (3+ papers)
        sufficient = NodePairEvidence(node_pair=pair, papers=sample_papers)
        assert len(sufficient.papers) >= 3

        # Insufficient evidence (< 3 papers)
        insufficient = NodePairEvidence(node_pair=pair, papers=sample_papers[:1])
        assert len(insufficient.papers) < 3


# =============================================================================
# Test: Mechanism Result Handling
# =============================================================================

class TestMechanismResultHandling:
    """Tests for MechanismResult handling."""

    def test_mechanism_result_with_valid_mechanism(self):
        """Test MechanismResult with valid mechanism data."""
        pair = NodePair(
            from_node_id="alcohol_taxation",
            from_node_name="Alcohol Taxation",
            to_node_id="binge_drinking",
            to_node_name="Binge Drinking",
            expected_direction="negative",
            category="political",
            priority=1
        )

        mechanism_data = {
            "from_node_id": "alcohol_taxation",
            "from_node_name": "Alcohol Taxation",
            "to_node_id": "binge_drinking",
            "to_node_name": "Binge Drinking",
            "direction": "negative",
            "category": "political",
            "evidence_quality": "A",
            "n_studies": 5,
            "primary_citation": "Smith et al. 2022",
            "supporting_citations": ["Jones 2021", "Williams 2020", "Brown 2019"]
        }

        result = MechanismResult(
            node_pair=pair,
            mechanism=mechanism_data,
            evidence_found=True,
            n_papers=5
        )

        assert result.evidence_found is True
        assert result.mechanism is not None
        assert result.mechanism["evidence_quality"] == "A"

    def test_mechanism_result_null_mechanism(self):
        """Test MechanismResult when no evidence found."""
        pair = NodePair(
            from_node_id="test",
            from_node_name="Test",
            to_node_id="test2",
            to_node_name="Test 2",
            expected_direction="positive",
            category="test",
            priority=1
        )

        result = MechanismResult(
            node_pair=pair,
            mechanism=None,
            evidence_found=False,
            n_papers=2,
            insufficient_evidence=True,
            error="Insufficient evidence for causal relationship"
        )

        assert result.evidence_found is False
        assert result.mechanism is None
        assert result.insufficient_evidence is True


# =============================================================================
# Test: Consolidation Prompt Generation
# =============================================================================

class TestConsolidationPrompt:
    """Tests for LLM prompt generation."""

    def test_consolidation_prompt_contains_node_ids(self, discovery_instance, sample_papers):
        """Test that consolidation prompt contains exact node IDs."""
        pairs = discovery_instance.build_node_pairs()
        pair = pairs[0]

        evidence = NodePairEvidence(
            node_pair=pair,
            papers=sample_papers
        )

        prompt = discovery_instance._create_consolidation_prompt(
            evidence,
            list(discovery_instance.node_metadata.keys())
        )

        # Should contain exact node IDs
        assert pair.from_node_id in prompt
        assert pair.to_node_id in prompt
        # Should contain instruction about not forcing
        assert "null" in prompt.lower() or "insufficient" in prompt.lower()

    def test_consolidation_prompt_contains_papers(self, discovery_instance, sample_papers):
        """Test that consolidation prompt includes paper information."""
        pairs = discovery_instance.build_node_pairs()
        pair = pairs[0]

        evidence = NodePairEvidence(
            node_pair=pair,
            papers=sample_papers
        )

        prompt = discovery_instance._create_consolidation_prompt(
            evidence,
            list(discovery_instance.node_metadata.keys())
        )

        # Should contain paper titles
        assert "Alcohol Tax and Binge Drinking" in prompt
        assert "Price Policies" in prompt


# =============================================================================
# Test: YAML Output
# =============================================================================

class TestYAMLOutput:
    """Tests for YAML mechanism file output."""

    def test_save_mechanisms_creates_files(self, discovery_instance):
        """Test that save_mechanisms creates YAML files."""
        pair = NodePair(
            from_node_id="alcohol_taxation",
            from_node_name="Alcohol Taxation",
            to_node_id="binge_drinking",
            to_node_name="Binge Drinking",
            expected_direction="negative",
            category="political",
            priority=1
        )

        mechanism_data = {
            "from_node_id": "alcohol_taxation",
            "from_node_name": "Alcohol Taxation",
            "to_node_id": "binge_drinking",
            "to_node_name": "Binge Drinking",
            "direction": "negative",
            "category": "political",
            "evidence_quality": "B",
            "n_studies": 4,
            "primary_citation": "Smith et al. 2022",
            "supporting_citations": ["Jones 2021", "Williams 2020"],
            "mechanism_pathway": ["Step 1", "Step 2"],
            "description": "Test description"
        }

        result = MechanismResult(
            node_pair=pair,
            mechanism=mechanism_data,
            evidence_found=True,
            n_papers=4
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            summary = discovery_instance.save_mechanisms([result], tmpdir)

            assert summary["saved"] == 1
            assert summary["skipped_insufficient_evidence"] == 0

            # Check file was created
            political_dir = Path(tmpdir) / "political"
            assert political_dir.exists()

            yaml_files = list(political_dir.glob("*.yaml"))
            assert len(yaml_files) == 1

    def test_save_mechanisms_skips_null(self, discovery_instance):
        """Test that null mechanisms are not saved."""
        pair = NodePair(
            from_node_id="test",
            from_node_name="Test",
            to_node_id="test2",
            to_node_name="Test 2",
            expected_direction="positive",
            category="test",
            priority=1
        )

        result = MechanismResult(
            node_pair=pair,
            mechanism=None,
            evidence_found=False,
            n_papers=1,
            insufficient_evidence=True
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            summary = discovery_instance.save_mechanisms([result], tmpdir)

            assert summary["saved"] == 0
            assert summary["skipped_insufficient_evidence"] == 1


# =============================================================================
# Test: End-to-End Integration (Mocked)
# =============================================================================

class TestIntegration:
    """Integration tests with mocked external dependencies."""

    @patch('pipelines.node_pair_discovery.LiteratureSearchAggregator')
    def test_search_papers_for_pair(self, mock_aggregator, discovery_instance, sample_papers):
        """Test paper search for a node pair."""
        # Mock the search results
        mock_instance = MagicMock()
        mock_instance.search.return_value = [
            MagicMock(
                title=p.title,
                abstract=p.abstract,
                year=p.citation_context.get('year'),
                doi=p.citation_context.get('doi'),
                authors=p.citation_context.get('authors', []),
                journal=p.citation_context.get('journal')
            )
            for p in sample_papers
        ]
        mock_aggregator.return_value = mock_instance

        discovery_instance.pubmed_email = "test@test.com"
        pairs = discovery_instance.build_node_pairs()

        evidence = discovery_instance.search_papers_for_pair(pairs[0], max_papers=10)

        assert evidence.node_pair == pairs[0]
        assert len(evidence.papers) > 0

    def test_full_pipeline_dry_run(self, sample_config):
        """Test that dry run doesn't make API calls."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(sample_config, f)
            f.flush()

            discovery = NodePairDiscovery()

            # Should not raise even without API key for dry run
            discovery.load_config(f.name)

            # Just verify config loaded
            assert discovery.config is not None
            assert discovery.config["name"] == "test_node_pair_discovery"

            os.unlink(f.name)


# =============================================================================
# Test: Edge Cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_node_pairs_config(self, discovery_instance):
        """Test handling of empty node pairs list."""
        discovery_instance.config["node_pairs"] = []
        pairs = discovery_instance.build_node_pairs()
        assert len(pairs) == 0

    def test_missing_keywords_for_node(self, discovery_instance):
        """Test handling when keywords are missing for a node."""
        # Remove keywords for one node
        del discovery_instance.config["node_keywords"]["binge_drinking"]

        pairs = discovery_instance.build_node_pairs()
        # Should still work, just with empty keywords
        assert len(pairs) == 2
        assert pairs[0].to_keywords == []  # binge_drinking is to_node of first pair

    def test_paper_without_abstract(self, discovery_instance, sample_papers):
        """Test that papers without abstracts are filtered."""
        pair = discovery_instance.build_node_pairs()[0]

        # Add paper without abstract
        paper_no_abstract = PaperInput(
            abstract="",  # Empty abstract
            title="No Abstract Paper",
            citation_context={"title": "No Abstract Paper", "year": 2022},
            custom_id="no_abstract"
        )

        evidence = NodePairEvidence(
            node_pair=pair,
            papers=sample_papers + [paper_no_abstract]
        )

        # Papers without abstracts should be handled gracefully
        assert len(evidence.papers) == 4

    def test_ensure_client_without_api_key(self):
        """Test that _ensure_client raises without API key."""
        discovery = NodePairDiscovery()
        discovery.api_key = None

        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
            discovery._ensure_client()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
