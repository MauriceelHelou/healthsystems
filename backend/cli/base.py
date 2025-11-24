"""
Base CLI infrastructure for consistent command-line tools
"""

import argparse
import logging
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseCLI(ABC):
    """Base class for CLI commands with consistent interface."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_name(self) -> str:
        """Command name (e.g., 'classify', 'extract')."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Command description for help text."""
        pass

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser):
        """Add command-specific arguments to parser."""
        pass

    @abstractmethod
    def run(self, args: argparse.Namespace) -> int:
        """Execute command. Return 0 for success, non-zero for error."""
        pass

    def setup_logging(self, verbose: bool = False):
        """Configure logging based on verbosity."""
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def error_exit(self, message: str, code: int = 1):
        """Print error and exit."""
        self.logger.error(message)
        sys.exit(code)

    def validate_file_exists(self, file_path: Path, description: str = "File") -> None:
        """Validate that a file exists, exit with error if not."""
        if not file_path.exists():
            self.error_exit(f"{description} not found: {file_path}")
        if not file_path.is_file():
            self.error_exit(f"{description} is not a file: {file_path}")

    def validate_dir_exists(self, dir_path: Path, description: str = "Directory") -> None:
        """Validate that a directory exists, exit with error if not."""
        if not dir_path.exists():
            self.error_exit(f"{description} not found: {dir_path}")
        if not dir_path.is_dir():
            self.error_exit(f"{description} is not a directory: {dir_path}")


def add_common_arguments(parser: argparse.ArgumentParser):
    """Add arguments common to all commands."""
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
