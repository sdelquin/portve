#!/bin/bash

source ~/.virtualenvs/portve/bin/activate
cd "$(dirname "$0")"
exec python main.py $@
