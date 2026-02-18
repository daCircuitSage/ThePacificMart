#!/bin/bash
set -o errexit

echo "========== BUILD STARTED =========="
echo "Python version:"
python --version

echo ""
echo "========== Installing Requirements =========="
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: pip install failed!"
    exit 1
fi

echo ""
echo "========== Creating Migrations =========="
python manage.py makemigrations --no-input
if [ $? -ne 0 ]; then
    echo "ERROR: makemigrations failed!"
    exit 1
fi

echo ""
echo "========== Running Migrations =========="
python manage.py migrate --verbosity 2 --no-input
if [ $? -ne 0 ]; then
    echo "ERROR: migrate failed!"
    exit 1
fi

echo ""
echo "========== Creating Superuser =========="
echo "ADMIN_EMAIL: $ADMIN_EMAIL"
echo "ADMIN_PASSWORD length: ${#ADMIN_PASSWORD}"
python manage.py create_admin
if [ $? -ne 0 ]; then
    echo "WARNING: Superuser creation failed (may already exist)"
else
    echo "Superuser creation command executed"
fi

echo ""
echo "========== Collecting Static Files =========="
python manage.py collectstatic --no-input --clear
if [ $? -ne 0 ]; then
    echo "ERROR: collectstatic failed!"
    exit 1
fi

echo ""
echo "========== Build Completed Successfully =========="
