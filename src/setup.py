import os
from setuptools import setup, find_packages

directory = os.path.dirname(os.path.realpath(__file__))
requirements_txt = f'{directory}/requirements.txt'
install_requires = []
if os.path.isfile(requirements_txt):
    with open(requirements_txt) as f:
        install_requires = [
            line
            for line in map(lambda x: x.lstrip(), f.read().splitlines())
            if len(line) != 0 and line[0] != '#'
        ]

setup(
    name='chord DHT-Assignment 2',
    version='1.0.0',
    packages=find_packages(include=['app', 'app.*', 'test', 'test.*']),
    install_requires=install_requires
)
