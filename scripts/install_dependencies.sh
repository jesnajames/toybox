#!/bin/bash

cd /home/ec2-user/toybox

sudo yum update -y

sudo yum install -y python3
sudo yum install -y git

pip3 install virtualenv

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
