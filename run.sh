#!/bin/bash

# Setting up the venv:
# python3 -m venv venv
# pip freeze > requirements.txt
# pip install -r requirements.txt


#source $CONDA_PREFIX/etc/profile.d/conda.sh
#conda deactivate
source ./token
source ./venv/bin/activate
export FLASK_APP=flow
export FLASK_ENV=development

flask run
