#!/bin/bash

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export PYTHONPATH=$PYTHONPATH:'bushido/'
python -m unittest discover -s tests

