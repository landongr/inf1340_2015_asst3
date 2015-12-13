#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = "Graham Landon, Erin Canning, and Brady Williamson"

import re
import datetime
import json


def decide(test_applicant, countries):
    results = []
    for person in test_applicant:
        decision = decide(person,countries)
        if decision == ["Quarantine"]:
            results.append("Quarantine")
        elif decision == ["Reject"]:
            results.append("Reject")
        elif decision == ["Accept"]:
            results.append("Accept")
    return results


def decide_one(test_applicant, countries):
    """
    Decides whether a traveller's entry into Kanadia should be accepted, rejected, or if they should be quarantined.

    :param test_applicant
    :param countries
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """

    ######################
    ###Local Constants####
    ######################

    # Variable for Applicant's Home Country
    home_country = test_applicant["home"]["country"]

    # Variable for Country Applicant Traveling From
    from_country = test_applicant["from"]["country"]

    # Variable for first name (for entry record completeness check)
    first_name = test_applicant["first_name"]

    # variable for last name (for entry record completeness check)
    last_name = test_applicant["last_name"]

    # variable for birth date (for entry record completeness check)
    birth_date = test_applicant["birth_date"]

    # variable for home city (for entry record completeness check)
    home_city = test_applicant["home"]["city"]

    # variable for home region (for entry record completeness check)
    home_region = test_applicant["home"]["region"]

    # variable for city applicant arriving from (for entry record completeness check)
    from_city = test_applicant["from"]["city"]

    # variable for region applicant arriving from (for entry record completeness check)
    from_region = test_applicant["from"]["region"]

    # Variable for Applicant's reason for entering the country
    reason = test_applicant["entry_reason"]

    # Variable for if Country Applicant traveled from has Medical Advisory
    try:
         countries[from_country]["medical_advisory"]
    except KeyError:
         return ["Reject"]
    advisory2 = countries[from_country]["medical_advisory"]

    # Variable for Applicant passport number
    passport_number = test_applicant["passport"]

    # Assign empty string for Applicant's Visa Number
    visa_code = ""

    # Assign empty string for Applicant's Visa Date
    date_string = ""

    # If Applicant has visa, reassign variables with visa date and number
    if "visa" in test_applicant:
        date_string = test_applicant["visa"]["date"]
        visa_code = test_applicant["visa"]["code"]

    # Assign empty string for via country medical advisory
    advisory3 = ""

    # Assign empty string for Country Applicant Traveled via
    via_country = ""

    # If applicant traveled via another country, reassign the empty strings
    if "via" in test_applicant:
        # Variable for name of via country
        via_country = test_applicant["via"]["country"]
        # Variable for if via country has Medical Advisory
        try:
            countries[via_country]["medical_advisory"]
        except KeyError:
             return ["Reject"]
        advisory3 = countries[via_country]["medical_advisory"]

    ####################
    ##Validity Checks###
    ####################

    # Check if there are medical advisories in home country (advisory); from country (advisory2);
    # via country (advisory3)
    if check_medical_advise(advisory2,advisory3) == False:
        return ["Quarantine"]

    # Check that no required fields on the entry record are blank.
    fields = (first_name, last_name, birth_date, home_country, home_city, home_region, from_country, from_region, from_city,
              reason)

    for entry in fields:
        if entry == "":
            return ["Reject"]

    # Check if passport_number included and correctly formatted; reject if blank or invalid format
    if valid_passport_format(passport_number) == False:
        return ["Reject"]

    # Check if applicant has traveled via other countries
    # Check whether the via countries are valid country codes
    # Check whether reason for entering Kanadia valid
    # altered to use the via_country variable instead of just "country"
    if "via" in test_applicant:
        location_check(via_country)
        if location_check(via_country) == False:
            return ["Reject"]
        check_reason(reason,test_applicant, countries)
        if check_reason(reason,test_applicant, countries) == False:
            return ["Reject"]

    # Test if Applicant's home is Kanadia; accept them if it is
    if home_country == "KAN":
        return ["Accept"]

    # Check if applicant has visa
    if "visa" in test_applicant:
        # Test if visa_code correctly formatted; reject if invalid format
        if valid_visa_format(visa_code) == False:
            return ["Reject"]

        # Test if visa's date_string correctly formatted; reject if invalid format
        if valid_date_format(date_string) == False:
            return ["Reject"]
        else:
            return ["Accept"]

#####################
# HELPER FUNCTIONS ##
#####################


def is_more_than_2_years_ago(date_string):
    """
    Check if date is less than two years ago.

    :param date_string: a date string in format "YYYY-MM-DD"
    :return: True if date is less than two years ago; False otherwise.
    """

    now = datetime.datetime.now()
    two_years_ago = now.replace(year=now.year - 2)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return (date - two_years_ago).total_seconds() > 0

#is_more_than_2_years_ago("1986-05-08")
    #returns False

#is_more_than_2_years_ago("2015-05-08")
    #returns True

def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five groups of five alpha-numeric characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format_regex = re.compile(r"(\w{5}-){4}\w{5}")
    passport_match = passport_format_regex.match(passport_number)
    if passport_match is None:
        return False
    else:
        return True
#valid_passport_format("JMZ0S-89IA9-OTCLY-MQ4LJ-P7CTY")
    #no problem with correct format

#valid_passport_format("jMz0s-89IA9-OTCLY-MQ4LJ-P7CTY")
    #no problem with this correct format mix of caps/nocaps/numbers

#valid_passport_format("89IA9-OTCLY-MQ4LJ-P7CTY-uuuu_")
    #UHOH it allows underscores

#valid_passport_format("7")
    #no problem, False because it's not even close

#valid_passport_format("89IA9-OTCLY-MQ4LJ-P7CTY-uuuu.")
    #no problem, False because of period

#valid_passport_format("JJJJ-OTCLY-MQ4LJ-P7CTY-uuuuu")
    #no problem, false because of too few in first block


def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """

    visa_format_regex = re.compile(r"\w{5}-\w{5}$")
    visa_match = visa_format_regex.match(visa_code)
    if visa_match is None:
        return False
    else:
        return True


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-MM-DD in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """

    date_format_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
    date_match = date_format_regex.match(date_string)
    if date_match is None:
        return False
    else:
        return True


def location_check(check_country):
    """
    Checks whether provided home country of an applicant is valid
    :param check_country: 3-letter string representing a country.
    :return: Boolean; True if home_country is KAN or other legitimate country key; False otherwise
    """

    json_data = open("countries.json").read()
    contents = json.loads(json_data)
    for key in contents:
        if check_country == "KAN":
            return True
        elif check_country == key:
            return True
    else:
        return False


def check_reason(reason, test_applicant, countries):
    """
    Checks reason for test_applicant's entry to Kanadia; if it is visit, checks whether visitors from that country
     need a visitor visa; if they do, checks whether that visa is less than two years old.
    :param reason: 3-letter string indicating home country of applicant
    :param test_applicant:
    :param countries:
    :return: Boolean;
    """

    # Retrieve test_applicant's visa date
    date_string = test_applicant["visa"]["date"]

    if reason == "visit":
        # Retrieve test_applicant home country; if does not require a visa, return True
        country = test_applicant["home"]["country"]
        if countries[country]["visitor_visa_required"] == "0":
            return True

        # If visa date (date_string) less than 2 years old, return True
        else:
            if is_more_than_2_years_ago(date_string) == True:
                return True
            else:
                return False
    # If reason for entry is returning, return True
    elif reason == "returning":
        return True
    else:
        return False


def check_medical_advise(advisory2, advisory3):
    """
    Checks whether there are medical advisories in
    :param advisory2: a string to indicate whether there is a medical advisory in country applicant traveled from
    :param advisory3: a string to indicate whether there is a medical advisory in country applicant traveled via
    :return: Boolean; False if any advisories exist; otherwise, True.
    """

    if advisory2 != "":
        return False
    elif advisory3 != "":
        return False
    else:
        return True

with open("JSONtest2.json","r") as json_reader:
    applicant = json.load(json_reader)
with open("countries.json","r") as country_reader:
    ctry = json.load(country_reader)

#print decide(applicant, ctry)
