#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py migrate

python render_seed.py

python manage.py collectstatic --noinput