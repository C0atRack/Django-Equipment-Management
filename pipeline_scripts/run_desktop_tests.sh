#!/bin/bash
source djvenv/bin/activate;
./manage.py makemigrations && ./manage.py migrate
exec coverage run ./manage.py test --verbosity 2