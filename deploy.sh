#!/bin/bash

cd "$(dirname "$0")"
git pull
pip install -r requirements.txt
