#!/bin/bash

echo "Running pip-audit..."
pip-audit -r requirements.txt

echo "Running manage.py check --deploy..."
python manage.py check --deploy

echo "Running bandit..."
bandit -r apps/ config/
