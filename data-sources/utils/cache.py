"""
Caching utilities for scraped data.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class Cache:
    """Simple file-based cache for scraped data."""

    def __init__(self, cache_dir: Path = Path("data-sources/cache")):
        """
        Initialize cache.

        Args:
            cache_dir: Directory for cache files
        """
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, source: str, **params) -> str:
        """
        Generate cache key from parameters.

        Args:
            source: Data source name
            **params: Parameters for the query

        Returns:
            MD5 hash as cache key
        """
        key_string = f"{source}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str, source: str) -> Path:
        """Get path to cache file."""
        source_dir = self.cache_dir / source
        source_dir.mkdir(exist_ok=True)
        return source_dir / f"{cache_key}.json"

    def get(
        self,
        source: str,
        max_age_days: int = 30,
        **params
    ) -> Optional[Any]:
        """
        Get cached data if available and fresh.

        Args:
            source: Data source name
            max_age_days: Maximum age of cache in days
            **params: Parameters for the query

        Returns:
            Cached data or None if not available/stale
        """
        cache_key = self._get_cache_key(source, **params)
        cache_path = self._get_cache_path(cache_key, source)

        if not cache_path.exists():
            logger.debug(f"Cache miss: {cache_key}")
            return None

        try:
            with open(cache_path) as f:
                cached = json.load(f)

            # Check if cache is fresh
            cached_at = datetime.fromisoformat(cached['cached_at'])
            age = datetime.utcnow() - cached_at

            if age > timedelta(days=max_age_days):
                logger.info(f"Cache expired: {cache_key} (age: {age.days} days)")
                return None

            logger.info(f"Cache hit: {cache_key}")
            return cached['data']

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Invalid cache file: {cache_path}, {e}")
            return None

    def set(self, source: str, data: Any, **params) -> None:
        """
        Store data in cache.

        Args:
            source: Data source name
            data: Data to cache
            **params: Parameters for the query
        """
        cache_key = self._get_cache_key(source, **params)
        cache_path = self._get_cache_path(cache_key, source)

        cached = {
            'source': source,
            'params': params,
            'cached_at': datetime.utcnow().isoformat(),
            'data': data
        }

        with open(cache_path, 'w') as f:
            json.dump(cached, f, indent=2)

        logger.info(f"Cached: {cache_key}")

    def clear(self, source: Optional[str] = None) -> None:
        """
        Clear cache.

        Args:
            source: Clear only this source, or all if None
        """
        if source:
            source_dir = self.cache_dir / source
            if source_dir.exists():
                for cache_file in source_dir.glob("*.json"):
                    cache_file.unlink()
                logger.info(f"Cleared cache for source: {source}")
        else:
            for cache_file in self.cache_dir.rglob("*.json"):
                cache_file.unlink()
            logger.info("Cleared all cache")
