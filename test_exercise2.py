#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = "Graham Landon, Erin Canning, and Brady Williamson"
__status__ = "Prototype"




# imports one per line
import pytest
import os
import json
import re
from exercise2 import decide


DIR = "test_jsons/"
os.chdir(DIR)



# def test_returning():
#     """
#     Travellers are returning to KAN.
#     """

def test_our_test():
    assert decide("test_returning_citizen.json", "countries") == ["Accept", "Accept", "Quarantine"]

def test_our_test():
    assert decide("JSONtest2.json", "countries" ) == ["Accept"]