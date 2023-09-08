#!/bin/bash

# Clone Ciphify 
git clone https://github.com/Merlin1A/ciphy.git

# Change to the Ciphify directory
cd ciphy

# Install the package
pip install --user --editable .

# Add local user's pip binary directory to PATH, if it's not already
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
fi
