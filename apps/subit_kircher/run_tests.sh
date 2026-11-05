#!/bin/sh
set -e
cd "$(dirname "$0")"
python3 kircher_data.py >/dev/null 2>&1 || python kircher_data.py >/dev/null 2>&1
python3 test_core.py -v || python test_core.py -v
