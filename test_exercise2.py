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


test_1 = "test_returning_citizen.json"
test_2 = "countries.json"

# def test_returning():
#     """
#     Travellers are returning to KAN.
#     """
#     assert decide("test_returning_citizen.json", "countries.json") ==\
#         ["Accept", "Accept", "Quarantine"]

"""
with open("JSONtest2.json","r") as json_reader:
      applicant = json.load(json_reader)
with open("countries.json","r") as country_reader:
     ctry = json.load(country_reader)
"""

def test_our_test():
    assert decide("JSONtest2.json", "r" ) == ["Accept"]