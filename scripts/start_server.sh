#!/bin/bash

cd /home/ec2-user/toybox

source venv/bin/activate

uvicorn app:app --host 0.0.0.0 --port 8000 --daemon
