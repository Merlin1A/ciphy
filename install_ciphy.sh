#!/bin/bash

# Clone Ciphify 
git clone https://github.com/Merlin1A/ciphify.git

# Change to the Ciphify directory
cd ciphify

# Install the package
pip install --user --editable .
