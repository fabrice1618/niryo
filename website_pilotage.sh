#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python code/website_pilotage/app.py "$@"
