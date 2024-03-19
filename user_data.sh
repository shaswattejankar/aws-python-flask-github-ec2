#!/bin/bash
sudo su -
apt-get update
apt-get install git python3 python3-pip -y
git clone YOUR_GITHUB_REPO_LINK
cd py-flask-ec2/
pip install flask
python3 -m flask run --host=0.0.0.0
