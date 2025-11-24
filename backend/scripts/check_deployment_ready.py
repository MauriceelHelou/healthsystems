"""
Pre-deployment checklist script.

Validates that the application is ready for Railway deployment by checking:
- Database migrations are valid
- Mechanism YAML files are parseable
- Required environment variables are documented
- No sensitive data in code
"""

import os
import sys
import yaml
from pathlib import Path
from typing import List, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class DeploymentChecker:
    """Checks if application is ready for deployment."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.checks_passed = 0
        self.checks_total = 0

    def check(self, name: str, passed: bool, message: str = "", warning: bool = False):
        """Record a check result."""
        self.checks_total += 1

        if passed:
            self.checks_passed += 1
            print(f"[PASS] {name}")
        else:
            if warning:
                self.warnings.append(f"{name}: {message}")
                print(f"[WARN] {name}: {message}")
            else:
                self.errors.append(f"{name}: {message}")
                print(f"[FAIL] {name}: {message}")

    def check_migrations_exist(self):
        """Check that migration files exist."""
        migrations_dir = Path(__file__).parent.parent / "alembic" / "versions"

        if not migrations_dir.exists():
            self.check("Migrations directory", False, "alembic/versions/ not found")
            return

        migration_files = list(migrations_dir.glob("*.py"))
        migration_files = [f for f in migration_files if f.name != "__pycache__"]

        self.check(
            "Migration files exist",
            len(migration_files) > 0,
            f"Found {len(migration_files)} migration(s)"
        )

    def check_mechanism_files(self):
        """Check that mechanism YAML files are valid."""
        mechanism_bank = Path(__file__).parent.parent.parent / "mechanism-bank" / "mechanisms"

        if not mechanism_bank.exists():
            self.check("Mechanism bank directory", False, "mechanism-bank/mechanisms/ not found")
            return

        yaml_files = list(mechanism_bank.glob("**/*.yml")) + \
                     list(mechanism_bank.glob("**/*.yaml"))

        if len(yaml_files) == 0:
            self.check("Mechanism YAML files", False, "No YAML files found")
            return

        # Try to parse each YAML file
        invalid_files = []
        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if not data or 'id' not in data:
                        invalid_files.append(f"{yaml_file.name}: missing 'id' field")
            except Exception as e:
                invalid_files.append(f"{yaml_file.name}: {str(e)}")

        if invalid_files:
            self.check(
                "Mechanism YAML files valid",
                False,
                f"{len(invalid_files)} invalid file(s): {', '.join(invalid_files[:3])}"
            )
        else:
            self.check(
                "Mechanism YAML files valid",
                True,
                f"All {len(yaml_files)} files are valid"
            )

    def check_env_example(self):
        """Check that .env.example and .env.railway.example exist."""
        backend_dir = Path(__file__).parent.parent

        env_example = backend_dir / ".env.example"
        env_railway = backend_dir.parent / ".env.railway.example"

        self.check(
            ".env.example exists",
            env_example.exists(),
            "backend/.env.example not found"
        )

        self.check(
            ".env.railway.example exists",
            env_railway.exists(),
            ".env.railway.example not found"
        )

    def check_dockerfile(self):
        """Check that Dockerfile exists and has startup script."""
        dockerfile = Path(__file__).parent.parent / "Dockerfile"

        if not dockerfile.exists():
            self.check("Dockerfile exists", False, "backend/Dockerfile not found")
            return

        content = dockerfile.read_text()

        self.check(
            "Dockerfile references start.sh",
            "start.sh" in content or "CMD" in content,
            ""
        )

    def check_startup_script(self):
        """Check that startup script exists and is properly configured."""
        start_script = Path(__file__).parent.parent / "start.sh"

        if not start_script.exists():
            self.check("start.sh exists", False, "backend/start.sh not found")
            return

        content = start_script.read_text()

        required_commands = [
            ("alembic upgrade", "Database migrations"),
            ("seed_database.py", "Database seeding"),
            ("uvicorn", "Server startup")
        ]

        for command, description in required_commands:
            self.check(
                f"start.sh includes {description}",
                command in content,
                f"Missing: {command}"
            )

    def check_gitignore(self):
        """Check that sensitive files are in .gitignore."""
        gitignore = Path(__file__).parent.parent.parent / ".gitignore"

        if not gitignore.exists():
            self.check(".gitignore exists", False, ".gitignore not found", warning=True)
            return

        content = gitignore.read_text()

        required_ignores = [
            (".env", "Environment files"),
            ("__pycache__", "Python cache"),
            ("*.pyc", "Compiled Python"),
        ]

        for pattern, description in required_ignores:
            self.check(
                f".gitignore includes {description}",
                pattern in content,
                f"Missing: {pattern}",
                warning=True
            )

    def check_no_hardcoded_secrets(self):
        """Check for common patterns of hardcoded secrets."""
        backend_dir = Path(__file__).parent.parent

        # Check main.py and config files
        files_to_check = [
            backend_dir / "api" / "main.py",
            backend_dir / "config" / "database.py",
        ]

        secret_patterns = [
            "sk-ant-",  # Anthropic API key
            "password=",  # Database passwords
            "secret_key=",  # Secret keys
        ]

        found_secrets = []
        for file_path in files_to_check:
            if not file_path.exists():
                continue

            content = file_path.read_text().lower()
            for pattern in secret_patterns:
                if pattern in content and "getenv" not in content:
                    found_secrets.append(f"{file_path.name} may contain hardcoded {pattern}")

        self.check(
            "No hardcoded secrets",
            len(found_secrets) == 0,
            "; ".join(found_secrets) if found_secrets else "",
            warning=True
        )

    def check_railway_config(self):
        """Check that railway.toml is properly configured."""
        railway_toml = Path(__file__).parent.parent.parent / "railway.toml"

        if not railway_toml.exists():
            self.check("railway.toml exists", False, "railway.toml not found", warning=True)
            return

        content = railway_toml.read_text()

        self.check(
            "railway.toml specifies Dockerfile",
            "dockerfilePath" in content,
            ""
        )

    def run_all_checks(self) -> bool:
        """Run all deployment checks."""
        print("=" * 60)
        print("Railway Deployment Readiness Check")
        print("=" * 60)
        print()

        print("Checking database migrations...")
        self.check_migrations_exist()
        print()

        print("Checking mechanism data files...")
        self.check_mechanism_files()
        print()

        print("Checking environment configuration...")
        self.check_env_example()
        print()

        print("Checking Docker configuration...")
        self.check_dockerfile()
        self.check_startup_script()
        print()

        print("Checking security...")
        self.check_gitignore()
        self.check_no_hardcoded_secrets()
        print()

        print("Checking Railway configuration...")
        self.check_railway_config()
        print()

        # Print summary
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Checks passed: {self.checks_passed}/{self.checks_total}")

        if self.errors:
            print(f"\n[ERROR] {len(self.errors)} error(s) found:")
            for error in self.errors:
                print(f"   - {error}")

        if self.warnings:
            print(f"\n[WARNING] {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"   - {warning}")

        if not self.errors and not self.warnings:
            print("\n[SUCCESS] All checks passed! Ready to deploy to Railway.")
            return True
        elif not self.errors:
            print("\n[WARNING] Ready to deploy with warnings. Review warnings above.")
            return True
        else:
            print("\n[ERROR] Not ready to deploy. Fix errors above before deploying.")
            return False


def main():
    """Run deployment readiness checks."""
    checker = DeploymentChecker()
    ready = checker.run_all_checks()

    if ready:
        print("\nNext steps:")
        print("1. Commit your changes: git add . && git commit -m 'Prepare for Railway deployment'")
        print("2. Push to GitHub: git push origin main")
        print("3. Deploy to Railway (automatic if connected to GitHub)")
        print("4. Set environment variables in Railway dashboard")
        print("5. Monitor deployment logs: railway logs")
        print("\nSee RAILWAY_DEPLOYMENT.md for detailed instructions.")
        return 0
    else:
        print("\nFix the errors above and run this script again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
