#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run seed data (handles db creation)
python seed_data.py
