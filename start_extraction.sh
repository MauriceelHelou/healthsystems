#!/bin/bash
# Alcohol Mechanism Batch Extraction Launcher
# This script helps you set up and run the extraction pipeline

echo "================================================================================"
echo "ALCOHOL MECHANISM BATCH EXTRACTION"
echo "================================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.10+ and try again"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "WARNING: ANTHROPIC_API_KEY environment variable is not set"
    echo ""
    echo "You need to set your Anthropic API key to run this extraction."
    echo ""
    echo "Option 1: Set it for this session only:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo "  ./start_extraction.sh"
    echo ""
    echo "Option 2: Set it permanently (add to ~/.bashrc or ~/.zshrc):"
    echo "  echo 'export ANTHROPIC_API_KEY=\"your-key-here\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    echo ""
    read -p "Enter your Anthropic API key now (or press Enter to exit): " API_KEY

    if [ -z "$API_KEY" ]; then
        echo "Cancelled."
        exit 1
    fi

    export ANTHROPIC_API_KEY="$API_KEY"
    echo ""
    echo "API key set for this session."
    echo ""
fi

echo "API Key: ${ANTHROPIC_API_KEY:0:10}..."
echo ""

# Show menu
echo "What would you like to do?"
echo ""
echo "[1] Test extraction (single query, validates pipeline)"
echo "[2] Run Phase 1 only (Direct health consequences, ~15-20 mechanisms)"
echo "[3] Run Phases 1-3 (Health + Risk + Social, ~45-50 mechanisms)"
echo "[4] Run ALL phases (Complete extraction, ~90-130 mechanisms, 3-6 hours, \$50-100)"
echo "[5] Run in TEST mode (2 queries per phase, validates all phases)"
echo "[0] Exit"
echo ""

read -p "Enter your choice (0-5): " CHOICE

case $CHOICE in
    0)
        echo "Cancelled."
        exit 0
        ;;
    1)
        echo ""
        echo "Running test extraction..."
        echo ""
        cd backend
        python3 scripts/test_extraction.py
        ;;
    2)
        echo ""
        echo "Running Phase 1 (Direct Health Consequences)..."
        echo "This will take approximately 30-60 minutes"
        echo "Cost: ~\$10-15"
        echo ""
        read -p "Proceed? (y/n): " CONFIRM
        if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
            echo "Cancelled."
            exit 0
        fi
        cd backend
        python3 scripts/run_alcohol_extraction.py --phases 1 --limit 10
        ;;
    3)
        echo ""
        echo "Running Phases 1-3..."
        echo "This will take approximately 1-2 hours"
        echo "Cost: ~\$25-35"
        echo ""
        read -p "Proceed? (y/n): " CONFIRM
        if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
            echo "Cancelled."
            exit 0
        fi
        cd backend
        python3 scripts/run_alcohol_extraction.py --phases 1 2 3 --limit 10
        ;;
    4)
        echo ""
        echo "WARNING: Full extraction will:"
        echo "- Run all 6 phases (90 queries)"
        echo "- Retrieve 300-500 papers"
        echo "- Extract 90-130 mechanisms"
        echo "- Take 3-6 hours"
        echo "- Cost \$50-100 in API credits"
        echo ""
        read -p "Are you sure? (yes/no): " CONFIRM
        if [ "$CONFIRM" != "yes" ]; then
            echo "Cancelled."
            exit 0
        fi
        cd backend
        python3 scripts/batch_alcohol_mechanisms.py
        ;;
    5)
        echo ""
        echo "Running TEST mode (2 queries per phase)..."
        echo "This will validate all phases with minimal cost (~\$5-10)"
        echo ""
        read -p "Proceed? (y/n): " CONFIRM
        if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
            echo "Cancelled."
            exit 0
        fi
        cd backend
        python3 scripts/run_alcohol_extraction.py --test --phases 1 2 3 4 5 6
        ;;
    *)
        echo "Invalid choice."
        exit 1
        ;;
esac

echo ""
echo "================================================================================"
echo ""
echo "Next steps:"
echo "1. Validate mechanisms: python3 mechanism-bank/validation/validate_mechanisms.py"
echo "2. Review extracted mechanisms in mechanism-bank/mechanisms/"
echo "3. Load to database: curl -X POST http://localhost:8000/api/mechanisms/admin/load-from-yaml"
echo "4. Commit to git"
echo ""
echo "See backend/scripts/README_ALCOHOL_EXTRACTION.md for full guide"
echo ""
echo "================================================================================"
