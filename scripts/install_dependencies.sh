#!/bin/bash

cd /home/ec2-user/toybox


if [ -d "/home/ec2-user/toybox/Command" ]; then
  rm -rf /home/ec2-user/toybox/Command
fi

sudo yum update -y

sudo yum install -y python3
sudo yum install -y git

pip3 install virtualenv

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
