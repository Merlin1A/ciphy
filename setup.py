from setuptools import setup, find_packages

setup(
    name="ciphy",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ciphy = ciphy_entry:main",
        ],
    },
    install_requires=[
        "fire",  
    ],
)