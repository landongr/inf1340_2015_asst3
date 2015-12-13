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


# Student test begin here


def test_fraud_check():

    # Tests for instances or seemingly instances of fraud
    # 1) Missing name in the first name section, 2) Strange capital letters in the first name,
    # 3) Missing entry in the city section, 4) Missing entry reason
    # 5) Extra letters and numbers in passport code, 6) Missing letters and number in passport code

    assert decide("JSONtestFRAUD.json", "countries.json") == ["Reject", "Accept", "Reject", "Reject", "Reject", "Reject"]


def test_medical_check():

    # Test for instances where a person may need to be Quarantined
    # 1) Traveler has come from a quarantined country, 2) Traveler has traveled via a quarantined country
    # 3) Kanadian traveler has come via a quarantined country, 4) Home country is a quarantined country

    assert decide("JSONtestMEDICAL.json", "countries.json") == ["Quarantine", "Quarantine", "Quarantine", "Accept"]


def test_visa_check():
    # Test for issues with a travellers visa code
    # 1) Traveler has their visa code missing, 2) Traveler has their visa date missing
    # 3) Traveler has their visa code and date missing, 4) Visa code has too many letters
    # 5) Visa code has too few letters

    assert decide("JSONtest VISA.json", "countries.json") == ["Reject", "Reject", "Reject", "Reject", "Reject"]


def test_accepted():
    # Tests for travellers who will make it into the country
    # 1) Is a Kanadian Traveler 2) The home country is HRJ
    # 3) The home country is CFR and they have an up to date visa

    assert decide("jsontestACCEPTABLE.json", "countries.json") == ["Accept", "Accept", "Accept"]