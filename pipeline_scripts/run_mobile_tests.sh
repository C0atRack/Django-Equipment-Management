#!/bin/bash
source djvenv/bin/activate;
./manage.py makemigrations && ./manage.py migrate
BROWSER_WIDTH=414 BROWSER_HEIGHT=896 exec env ./manage.py test --verbosity 2 equipment_app.tests.test_integrations
