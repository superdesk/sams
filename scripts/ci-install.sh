#!/usr/bin/env bash

# Install python package dependencies
sudo apt-get -y update
sudo apt-get -y install libxml2-dev libxmlsec1-dev libxmlsec1-openssl

# install libmagic
wget http://launchpadlibrarian.net/433926958/libmagic-mgc_5.37-3_amd64.deb
wget http://launchpadlibrarian.net/433926961/libmagic1_5.37-3_amd64.deb
sudo dpkg -i libmagic-mgc_5.37-3_amd64.deb
sudo dpkg -i libmagic1_5.37-3_amd64.deb

# Update python core packages
python -m pip install --upgrade pip wheel setuptools

if [ "$SERVER" == "true" ]; then
    cd src/server
    pip install -r dev-requirements.txt
    pip install -e .
    cd ../../
fi

if [ "$SERVICES" == "true" ]; then
    cd src/server
    pip install -r requirements.txt
    cd ../../
fi

if [ "$CLIENT" == "true" ]; then
    cd src/clients/python
    pip install -r dev-requirements.txt
    pip install -e .
    cd ../../../
fi

if [ "$BEHAVE" == "true" ]; then
    pip install -r tests/features/requirements.txt
fi
