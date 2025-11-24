"""
Main CLI entry point for healthsystems command
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.cli.commands.classify import ClassifyCommand
from backend.cli.commands.extract import ExtractCommand
from backend.cli.commands.regrade import RegradeCommand
from backend.cli.commands.validate import ValidateCommand

__version__ = "1.0.0"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='healthsystems',
        description='HealthSystems Platform CLI Tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Classify nodes in inventory
  healthsystems classify Nodes/COMPLETE_NODE_INVENTORY.md --dry-run

  # Run generic extraction
  healthsystems extract generic --config config.json --phases 1,2,3

  # Regrade mechanisms
  healthsystems regrade --input mechanism-bank/ --dry-run

  # Validate mechanism YAML files
  healthsystems validate mechanism-bank/mechanisms/

For more information on each command, use:
  healthsystems <command> --help
        """
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'healthsystems {__version__}'
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Register commands
    commands = [
        ClassifyCommand(),
        ExtractCommand(),
        RegradeCommand(),
        ValidateCommand(),
    ]

    for cmd in commands:
        cmd_parser = subparsers.add_parser(
            cmd.get_name(),
            help=cmd.get_description(),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        cmd.add_arguments(cmd_parser)
        cmd_parser.set_defaults(func=cmd.run)

    # Parse and execute
    args = parser.parse_args()

    # Setup logging for selected command
    for cmd in commands:
        if cmd.get_name() == args.command:
            cmd.setup_logging(getattr(args, 'verbose', False))
            break

    # Execute command
    try:
        exit_code = args.func(args)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nAborted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
