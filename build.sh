#!/bin/bash

echo "Installing all requirements"
python3.11 -m pip install -r requirements.txt

echo "Migrating"
python3.11 manage.py makemigrations --noinput
python3.11 manage.py migrate --noinput

echo "Collect Static"
python3.11 manage.py collectstatic --noinput --clear
