#!/bin/bash
source djvenv/bin/activate;
./manage.py makemigrations && ./manage.py migrate
exec BROWSER_WIDTH=414 BROWSER_HEIGHT=896 ./manage.py test --verbosity 2 equipment_app.tests.test_integrations