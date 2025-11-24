#!/usr/bin/env python3
"""
Verify test setup for HealthSystems backend.

This script checks that all testing dependencies are installed
and the test environment is configured correctly.

Usage:
    python verify_test_setup.py
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check Python version is 3.8+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependency(module_name, import_name=None):
    """Check if a Python module is installed."""
    if import_name is None:
        import_name = module_name

    try:
        __import__(import_name)
        print(f"✅ {module_name}")
        return True
    except ImportError:
        print(f"❌ {module_name}")
        return False


def check_pytest():
    """Check pytest is installed and working."""
    try:
        result = subprocess.run(
            ["pytest", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ pytest - {version}")
            return True
    except FileNotFoundError:
        pass

    print("❌ pytest not found")
    return False


def check_test_files():
    """Check that test files exist."""
    test_dir = Path(__file__).parent / "tests"

    required_files = [
        "test_nodes_api.py",
        "conftest.py",
        "README_TESTING.md",
        "TESTING_QUICK_REFERENCE.md",
        "requirements-test.txt"
    ]

    all_exist = True
    for filename in required_files:
        filepath = test_dir / filename
        if filepath.exists():
            print(f"✅ {filename}")
        else:
            print(f"❌ {filename}")
            all_exist = False

    return all_exist


def main():
    """Run all checks."""
    print("=" * 60)
    print("  HealthSystems Backend Test Setup Verification")
    print("=" * 60)
    print()

    checks = []

    # Check Python version
    print("Checking Python version...")
    checks.append(check_python_version())
    print()

    # Check pytest
    print("Checking pytest...")
    checks.append(check_pytest())
    print()

    # Check core dependencies
    print("Checking core dependencies...")
    checks.append(check_dependency("pytest"))
    checks.append(check_dependency("pytest-cov", "pytest_cov"))
    checks.append(check_dependency("pytest-mock", "pytest_mock"))
    checks.append(check_dependency("fastapi"))
    checks.append(check_dependency("networkx"))
    checks.append(check_dependency("sqlalchemy"))
    print()

    # Check test files
    print("Checking test files...")
    checks.append(check_test_files())
    print()

    # Summary
    print("=" * 60)
    if all(checks):
        print("✅ All checks passed! Test environment is ready.")
        print()
        print("Next steps:")
        print("  1. Run tests: python run_tests.py")
        print("  2. With coverage: python run_tests.py --coverage")
        print("  3. View coverage: open htmlcov/index.html")
        print("=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please install missing dependencies:")
        print("   pip install -r tests/requirements-test.txt")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
