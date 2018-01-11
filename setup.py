#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for qas.
"""

import sys
import os
import io
import contextlib
from setuptools import setup, find_packages


@contextlib.contextmanager
def chdir(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        sys.path.insert(0, new_dir)
        yield
    finally:
        del sys.path[0]
        os.chdir(old_dir)


def setup_package():

    base_dir = os.path.abspath(os.path.dirname(__file__))

    with chdir(base_dir):
        with io.open(os.path.join(base_dir, 'qas', 'about.py'), encoding='utf8') as fp:
            about = {}
            exec(fp.read(), about)

    with io.open(os.path.join(base_dir, 'README.rst'), encoding='utf8') as f:
        readme = f.read()

    setup(name=about['__title__'],
          packages=find_packages(),
          description=about['__summary__'],
          long_description=readme,
          version=about['__version__'],
          author=about['__author__'],
          author_email=about['__email__'],
          url=about['__uri__'],
          license=about['__license__'],
          install_requires=[
              "autocorrect>=0.3.0",
              "gensim>=3.0.1",
              "lxml>=4.1.0",
              "pandas>=0.21",
              "pyenchant>=2.0.0",
              "requests>=2.18.0",
              "spaCy>=2.0.3",
              "scikit-learn>=v0.19.1",
              "wikipedia>=1.4.0"]
          )


if __name__ == "__main__":
    setup_package()
