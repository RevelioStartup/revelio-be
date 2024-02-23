#!/bin/bash

echo "Installing all requirements"
python3.10 -m pip install -r requirements.txt

echo "Migrating"
python3.10 manage.py makemigrations --noinput
python3.10 manage.py migrate --noinput

echo "Collect Static"
python3.10 manage.py collectstatic --noinput --clear
