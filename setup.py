import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 4):
    raise RuntimeError('Monitor bot requires Python3')

requires = [
    "slackclient"
]

setup(
    name="monitor_bot",
    version="0.0.2",
    install_requires=requires,
)
