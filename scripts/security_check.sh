#!/bin/bash

# Security checks script as requested

echo "Running pip-audit..."
pip-audit -r requirements.txt

echo "Running deploy checks..."
python manage.py check --deploy

echo "Running bandit..."
bandit -r apps/ config/

echo "Security checks completed."
