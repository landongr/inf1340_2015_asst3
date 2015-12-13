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


def test_returning():
     """
     Travellers are returning to KAN.
     """
     assert decide("test_returning_citizen.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]


def test_our_test():

    assert decide("JSONtest2.json", "countries.json") == ["Accept"]


def test_fraud_check():

    # Tests for instances or seemingly instances of fraud
    # 1) Missing name in the first name section, 2) Strange capital letters in the first name,
    # 3) Missing entry in the city section, 4) Missing entry reason
    # 5) Extra letters and numbers in passport code, 6) Missing letters and number in passport code

    assert decide("JSONtestFRAUD.json", "countries.json") == ["Reject","Accept","Reject","Reject","Reject","Reject"]


def test_medical_check():

    # Test for instances where a person may need to be Quarantined
    # 1) Traveler has come from a quarantined country, 2) Traveler has traveled via a quarantined country
    # 3) Kanadian traveler has come via a quarantined country, 4) Home country is a quarantined country

    assert decide("JSONtestMEDICAL.json", "countries.json") == ["Quarantine","Quarantine","Quarantine","Accept"]