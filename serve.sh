#!/bin/bash
DIRECTORY=./venv

if [ ! -d "$DIRECTORY" ]; then
  python3 -m venv venv

  source ./venv/bin/activate

  pip install -r requirements.txt
else
  source ./venv/bin/activate
fi

python3 ./Run.py