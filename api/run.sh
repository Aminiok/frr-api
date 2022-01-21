#!/bin/bash

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
export FLASK_APP=/api/api.py
flask run -h 0.0.0.0
