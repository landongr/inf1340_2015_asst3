#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = "Graham Landon"
__status__ = "Prototype"

# imports one per line
import pytest
import os
from exercise2 import decide

DIR = "test_jsons/"
os.chdir(DIR)


def test_returning():
    """
    Travellers are returning to KAN.
    """
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]

