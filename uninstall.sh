#!/bin/bash

# Uninstall the package
pip uninstall -y ciphy

# Remove the cloned repository if it exists in the expected directory
if [ -d "ciphy" ]; then
    rm -r ciphy
fi

# Remove configuration files and encrypted data
rm ~/.passwords.enc
rm ~/.passwords.csv
rm -r ~/.ciphy

# Print uninstallation complete
echo "Uninstallation complete."
