#!/usr/bin/env python

import os
import glob
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pylatex2doc",
    version="1.0",
    author="Eduardo dos Santos Pereira",
    author_email="pereira.somoza@gmail.com",
    description=("Tool for Convert latex to doc and html"),
    license="GNU v3",
    keywords="latex, doc, html",
    url="https://github.com/duducosmos/pylatex2doc",
    install_requires=['easygui'],
    py_modules = ['pylatex2doc'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: GNU V3",
    ],
    entry_points = {"console_scripts":
                    ["pylatex2doc = pylatex2doc:main", ]},
)
