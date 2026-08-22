@echo off
echo ===========================================
echo RUNNING SECURITY CHECKS (OWASP ASVS niveau 2)
echo ===========================================

echo.
echo [1/2] Running Pip Audit...
.\venv\Scripts\python.exe -m pip install pip-audit safety
.\venv\Scripts\pip-audit

echo.
echo [2/2] Running Django Deploy Checks...
:: On force DEBUG=False pour que SECURE_SSL_REDIRECT s'active
set DJANGO_DEBUG=False
.\venv\Scripts\python.exe manage.py check --deploy

echo.
echo Check completed.
