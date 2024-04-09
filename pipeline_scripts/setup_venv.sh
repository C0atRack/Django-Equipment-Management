#!/bin/bash
python -m venv djvenv
source djvenv/bin/activate
pip install -r requirements.txt > /dev/null