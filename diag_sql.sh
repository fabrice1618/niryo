#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python code/diag_sql/diag_sql.py
