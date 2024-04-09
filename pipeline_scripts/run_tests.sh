#!/bin/bash
mv "$(echo $ENVFILE | sed s/\\\'//g)" .
source djvenv/bin/activate;
./manage.py makemigrations && ./manage.py migrate
exec ./manage.py test --verbosity 2