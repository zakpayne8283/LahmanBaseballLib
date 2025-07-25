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

pytest