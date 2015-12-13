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

with open("test_returning_citizen.json", "r") as json_reader:
    b = json_reader.read()
    test_applicant = json.loads(b)
with open("countries.json", "r") as country_reader:
    b = country_reader.read()
    countries = json.loads(b)


def test_our_test():
    assert decide("test_returning_citizen.json", "r" ) == ["Accept"]