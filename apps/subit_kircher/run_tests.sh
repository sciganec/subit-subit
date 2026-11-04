#!/bin/sh
cd "$(dirname "$0")" && python3 kircher_data.py >/dev/null && python3 build_atlas.py && python3 -m unittest discover -s tests -v && python3 tests/browser_check.py
