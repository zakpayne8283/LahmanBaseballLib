#!/bin/bash

# Optional: Activate virtualenv
if [ -d ".venv" ]; then
    source .venv/Scripts/activate
else
    echo "⚠️  No .venv found. Did you run setup.sh?"
    exit 1
fi

# Set the python path correctly
export PYTHONPATH=$(pwd)/src

echo "Checking code coverage..."
echo "## ✅ Test Results & Coverage" > tests/README.md
echo '```' >> tests/README.md
python -m pytest --cov=src --cov-config=.coveragerc --cov-report=term-missing >> tests/README.md
echo '```' >> tests/README.md