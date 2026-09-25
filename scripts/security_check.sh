#!/bin/bash

# Exit on first error
set -e

echo "=== Running pip-audit ==="
pip-audit -r requirements.txt

echo "=== Running Django deployment checks ==="
python manage.py check --deploy

echo "=== Running bandit on source code ==="
bandit -r apps/ config/

echo "=== Security checks completed successfully! ==="
