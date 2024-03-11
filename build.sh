#!/bin/bash

echo "Installing all requirements"
python3.9 -m pip install -r requirements.txt

echo "Migrating"
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static"
python3.9 manage.py collectstatic --noinput --clear