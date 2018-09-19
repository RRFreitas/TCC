#!/bin/bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libgtk-3-dev
sudo apt-get install libboost-all-dev

pip3 install setuptools
pip3 install wheel
pip3 install numpy
pip3 install scipy
pip3 install scikit-image
pip3 install Pillow
pip3 install dlib
pip3 install face_recognition
