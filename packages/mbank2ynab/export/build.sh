#!/bin/bash

set -e

# python -m venv virtualenv
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
deactivate