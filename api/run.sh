#!/bin/bash

export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
uvicorn main:app --reload --host 0.0.0.0 --port 8080
