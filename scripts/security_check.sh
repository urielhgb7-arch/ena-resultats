#!/bin/bash
set -e
pip-audit -r requirements.txt
python manage.py check --deploy
bandit -r apps/ config/
