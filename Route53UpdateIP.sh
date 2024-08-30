#!/bin/bash
set -e

# Update package list and install dependencies
sudo apt update
sudo apt install -y python3-pip

# Install project dependencies
pip install -r requirements.txt

# Set up the configuration file
cp Route53UpdateIP.conf.example Route53UpdateIP.conf
echo "Please update Route53UpdateIP.conf with your AWS credentials and FQDN."