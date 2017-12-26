#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from qas.skeleton import fib

__author__ = "Shirish Kadam"
__copyright__ = "Copyright (C) 2017  Shirish Kadam"
__license__ = "GNU General Public License v3 (GPLv3)"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
