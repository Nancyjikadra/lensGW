#!/usr/bin/env python

import setuptools 
import os
from codecs import open

def readme():
    with open('README.md') as f:
        return f.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()
    
def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setuptools.setup(name                          = "ll",
                 version                       = get_version("lensGW/__init__.py"),
                 description                   = 'lensGW: Python package for gravitational wave lensing using PyCBC',
                 long_description_content_type = "text/markdown",
                 long_description              = readme(),
                 keywords                      = ['pycbc', 'gravitational wave lensing'],
                 author                        = 'Shashwat Singh',
                 author_email                  = 'shashwat98singh@gmail.com',
                 url                           = 'https://github.com/SSingh087/ll',
                 license                       = 'GNU General Public License v3',
                 packages                      = setuptools.find_packages(),
                 python_requires               = '>=3.6',
                 include_package_data          = True,
                 install_requires              = ['pycbc>=1.16.13','lenstronomy>=1.7.0','mpmath'],
                 classifiers                   = ['Intended Audience :: Science/Research',
                                                  'Natural Language :: English',
                                                  'License :: OSI Approved :: GNU General Public License v3',
                                                  'Programming Language :: Python :: 3.6',
                                                  'Topic :: Lensing :: Physics'])
