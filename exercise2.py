#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = 'Graham Landon'
__author__ = 'Erin Canning'
__author__ = 'Brady Williamson'

import re
import datetime
import json


######################
## global constants ##
######################
REQUIRED_FIELDS = ["passport", "first_name", "last_name",
                   "birth_date", "home", "entry_reason", "from"]

######################
## global variables ##
######################
'''
countries:
dictionary mapping country codes (lowercase strings) to dictionaries
containing the following keys:
"code","name","visitor_visa_required",
"transit_visa_required","medical_advisory"
'''
COUNTRIES = None

def decide(test_applicant, countries):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """


    # for person in test_applicant:
    #     for item in person:
    #         if item == "":
    #             return ["Reject"]
    #         for things in item:
    #             if things == "":
    #                 return ["Reject"]
    visa_code = ""
    date_string = ""
    advisory3 = ""
    country = ""
    country1 = test_applicant["home"]["country"]
    country2 = test_applicant["from"]["country"]
    country3 = ""
    if "via" in test_applicant:
        country3 = test_applicant["via"]["country"]
        advisory3 = countries[country3]["medical_advisory"]
    if country1 != "KAN":
        advisory = countries[country1]["medical_advisory"]
    advisory2 = countries[country2]["medical_advisory"]
    passport_number = test_applicant["passport"]
    if "visa" in test_applicant:
        date_string = test_applicant["visa"]["date"]
        visa_code = test_applicant["visa"]["code"]
    home_country = test_applicant["home"]["country"]
    if "via" in test_applicant:
        country = test_applicant["via"]["country"]
    reason = test_applicant["entry_reason"]

    #Validity Checks
    valid_passport_format(passport_number)
    if valid_passport_format(passport_number) == False:
        return ["Reject"]
    #Buggy
    if "visa" in test_applicant:
        valid_visa_format(visa_code)
        if valid_visa_format(visa_code) == False:
            return ["Reject"]
        valid_date_format(date_string)
        if valid_date_format(date_string) == False:
            return ["Reject"]
    kan_check(home_country)
    if kan_check(home_country) == True:
        return ["Accept"]
        exit
    check_medical_advise(advisory, advisory2, advisory3)
    if check_medical_advise(advisory, advisory2,advisory3) == False:
        return ["Quarantine"]
        exit
    if "via" in test_applicant:
        location_check(country)
        if location_check(country) == False:
            return ["Reject"]
        check_reason(reason,test_applicant, countries)
        if check_reason(reason,test_applicant, countries)== True:
            return ["Accept"]
        else:
            return ["False"]
    else:
        return "Accept"




#####################
# HELPER FUNCTIONS ##
#####################
def is_more_than_2_years_ago(date_string):
    """
    Check if date is less than 2 years ago.

    :param x: int representing years
    :param date_string: a date string in format "YYYY-mm-dd"
    :return: True if date is less than x years ago; False otherwise.
    """

    now = datetime.datetime.now()
    two_years_ago = now.replace(year=now.year - 2)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    return (date - two_years_ago).total_seconds() > 0


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    #THIS IS BUGGY
    passport_format_regex = re.compile(r"(\w{5}-){4}\w{5}")
    passport_match = passport_format_regex.search(passport_number)
    if passport_match is None:
        return False
#valid_passport_format("JMZ0S-89IA9-OTCLY-MQILJ-P7CTY")

def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """

    visa_format_regex = re.compile(r"\w{5}-\w{5}")
    visa_match = visa_format_regex.search(visa_code)
    if visa_match is None:
        return False
    else:
        return True


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """

    date_format_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
    date_match = date_format_regex.search(date_string)
    if date_match is None:
        return False
    else:
        return True

def location_check(country1):
    json_data = open("countries.json").read()
    contents = json.loads(json_data)
    for key in contents:
        if country1 == "KAN":
            return True
        elif country1 == key:
            return True
    else:
        return False


def kan_check(home_country):
    if home_country == "KAN":
        return True
    else:
        False


def check_reason(reason,test_applicant, countries):
    date_string = test_applicant["visa"]["date"]
    if reason == "visit":
        country = test_applicant["home"]["country"]
        if countries[country]["visitor_visa_required"] == "0":
            return True
        else:
            if is_more_than_2_years_ago(date_string) == True:
                return True
            else:
                return False
    elif reason == "returning":
        return True
    else:
        return False

def check_medical_advise(advisory, advisory2, advisory3):
    if advisory != "":
        return False
    elif advisory2 != "":
        return False
    elif advisory3 != "":
        return False
    else:
        return True

with open("JSONtest.json","r") as json_reader:
    applicant = json.load(json_reader)
with open("countries.json","r") as country_reader:
    ctry = json.load(country_reader)

#app = json.loads("JSONtest.json")
#cry = json.loads("countries.json")

print decide(applicant, ctry)