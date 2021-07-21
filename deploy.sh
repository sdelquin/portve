#!/bin/bash

source ~/.virtualenvs/portve/bin/activate
cd "$(dirname "$0")"
git pull
pip install -r requirements.txt
