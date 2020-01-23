#!/bin/bash
apt-get update
apt-get install -y python3 python3-pip git

mkdir flask
git clone https://github.com/pallets/flask.git flask
cd flask/examples/tutorial
python3 setup.py install
pip3 install -e .

apt-get install -y python3-pika python3-pillow python3-redis
pip3 install numpy
pip3 install jsonpickle

cd /Lab8
python3 server.py