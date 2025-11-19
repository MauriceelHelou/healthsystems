# Claude Code Behavior Instructions

## After Code Changes - DO NOT

When you make code changes, follow these important restrictions:

1. **DO NOT create documentation** - Do not automatically generate or update documentation files after code changes unless explicitly requested by the user

2. **DO NOT run Docker commands** - Do not attempt to run Docker, docker-compose, or any container-related commands

3. **DO NOT run Python commands** - Do not execute Python scripts or commands directly

4. **DO NOT run SQLite commands** - Do not attempt to run SQLite or any database commands

5. **DO NOT do database migrations** - Do not attempt to run Alembic migrations, database schema updates, or any migration-related commands

## General Guidelines

- Focus on making the requested code changes
- Only run commands that are explicitly requested by the user
- Avoid being overly proactive with follow-up actions
- Let the user decide when to run tests, migrations, or other operations
