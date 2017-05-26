# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

setup(
    name='nanostream',
    version='0.2.0',
    description='Stream-processing patterns at small scale, no overhead',
    long_description=(
        'Set up asychronous stream processing using pure Python with minimal '
        'overhead and no heavyweight systems.'),
    author='Zachary Ernst',
    author_email='zernst@trunkclub.com',
    url='http://github.com/trunkclub/nanostream',
    include_package_data=True,
    package_data={'docs': ['*']},
    scripts=[],
    packages=['nanostream'],
    package_dir={'nanostream': 'nanostream'},

    install_requires=['pyprimes', 'networkx>=1.11,<2.0']
)
