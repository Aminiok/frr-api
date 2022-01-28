#!/bin/bash

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
#export FLASK_APP=api.py
#flask run -h 0.0.0.0 -p 5001
uvicorn main:app --reload --host 0.0.0.0 --port 8080
