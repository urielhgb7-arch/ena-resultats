#!/bin/bash

echo "Running pip-audit..."
pip-audit -r requirements.txt

echo "Running Django deployment checks..."
python manage.py check --deploy

echo "Running Bandit security checks..."
bandit -r apps/ config/
