#!./venv/bin/python3
'''
Created on 20220926
Update on 20251110
@author: Eduardo Pagotto
'''

from setuptools import setup, find_packages

import os
import sys
sys.path.append(os.path.join(os.getcwd(), './src'))

from sjsonrpc import __version__ as VERSION

PACKAGE = "sjsonrpc"

# listar os packages
#python -c "from setuptools import setup, find_packages; print(find_packages())"

setup(
    name="sjsonrpc",
    version=VERSION,
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="Json RPC Wrapper",
    long_description="Classes to build simple RPC's",
    long_description_content_type="text/markdown",
    url="https://github.com/EduardoPagotto/sJsonRpc.git",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['setuptools',
                      'typing_extensions',
                      'wheel'])
