#!/bin/bash

# Exit on any error
set -e

echo "Running pip-audit..."
pip-audit -r requirements.txt

echo "Running Django deployment checks..."
python manage.py check --deploy

echo "Running bandit..."
bandit -r apps/ config/

echo "Security checks completed successfully."
