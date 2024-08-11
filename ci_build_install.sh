#!/bin/bash

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt

# execute unittests
export PYTHONPATH=$PYTHONPATH:'bushido/'
python -m unittest discover -s tests/unittests

# static code analyzier 

# building with setuptoos 
python setup.py sdist 
# installing unichat as a pip package to venv
pip install . 

