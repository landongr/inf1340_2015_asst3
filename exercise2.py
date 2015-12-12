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


def decide(test_applicant, countries):
    """
    Decides whether a traveller's entry into Kanadia should be accepted, rejected, or if they should be quarantined.

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

    #########################
    ###CREATING VARIABLES####
    #########################

    #??????  do we need it?  mentioned in the check_reason function; seems to do same thing as country3
    country = ""

    #Variable for Applicant's Home Country
    country1 = test_applicant["home"]["country"]

    #Variable for Country Applicant Traveling From
    country2 = test_applicant["from"]["country"]

    #Variable for first name (for entry record completeness check)
    first_name = test_applicant["first_name"]

    #variable for last name (for entry record completeness check)
    last_name = test_applicant["last_name"]

    #variable for birth date (for entry record completeness check)
    birth_date = test_applicant["birth_date"]

    #Variable for Applicant passport number
    passport_number = test_applicant["passport"]

    #variable for home city (for entry record completeness check)
    home_city = test_applicant["home"]["city"]

    #variable for home region (for entry record completeness check)
    home_region = test_applicant["home"]["region"]

    #variable for city applicant arriving from (for entry record completeness check)
    from_city = test_applicant["from"]["city"]

    #variable for region applicant arriving from (for entry record completeness check)
    from_region = test_applicant["from"]["region"]

    #Variable for Applicant's reason for entering the country
    reason = test_applicant["entry_reason"]

    #Variable for if Applicant's home country has medical advisory
    #If home country is Kanadia, assign empty string

    #Variable for if Country Applicant traveled from has Medical Advisory
    advisory2 = countries[country2]["medical_advisory"]

    #Variable for Applicant passport number
    passport_number = test_applicant["passport"]

    #Assign empty string for Applicant's Visa Number
    visa_code = ""

    #Assign empty string for Applicant's Visa Date
    date_string = ""

    #If Applicant has visa, reassign variables with visa date and number
    if "visa" in test_applicant:
        date_string = test_applicant["visa"]["date"]
        visa_code = test_applicant["visa"]["code"]

    #Assign empty string for via country medical advisory
    advisory3 = ""

    #Assign empty string for Country Applicant Traveled via
    country3 = ""

    #If applicant traveled via another country, reassign the empty strings
    if "via" in test_applicant:
        #Variable for name of via country
        country3 = test_applicant["via"]["country"]
        #Variable for if via country has Medical Advisory
        advisory3 = countries[country3]["medical_advisory"]

    #Variable for country test Applicant's traveled via (DO WE NEED IT? Already have Country3 variable)
    if "via" in test_applicant:
       country = test_applicant["via"]["country"]




    ####################
    #Validity Checks####
    ####################

    #I think we need to have it do the quarantine check before anything else,
    # since that is the first in the priority list of immig decisions
    #To make it work with people whose home is Kanadia, I changed the lines above to assign
    #a blank string to "advisory" variable for Kanadians (since KAN is not on the list of countries)
    #I tested it and it will now quarantine a Kanadian applicant

    #Check if there are medical advisories in home country (advisory); from country (advisory2); via country (advisory3)
    check_medical_advise(advisory2, advisory3)
    if check_medical_advise(advisory2,advisory3) == False:
        return ["Quarantine"]
        exit

    #I think the second thing we need to do is check that no info on entry record is missing
        #Might be better as a function? but how? can't pass all these things to it...
    #Check that no required fields on the entry record are blank.

    fields = (first_name, last_name, birth_date, country1, home_city, home_region, country2, from_region, from_city,
              reason)

#    if entry in fields == "":
#        return ["Reject"]

    #Check if passport_number included and correctly formatted; reject if blank or invalid format
    valid_passport_format(passport_number)
    if valid_passport_format(passport_number) == False:
        return ["Reject"]


    #Then we need to check if any mentioned location is Unknown
    #but when I try an unknown country key, everything crashes
        #even with a try-except block in the location check function, things like the medical advisory lines break it
        #medical advisory lines, etc


    #Check if applicant has traveled via other countries
    #Check whether the via countries are valid country codes
    #Check whether reason for entering Kanadia valid
    #altered to use the country3 variable instead of just "country"
    if "via" in test_applicant:
        location_check(country3)
        if location_check(country3) == False:
            return ["Reject"]
        check_reason(reason,test_applicant, countries)
        if check_reason(reason,test_applicant, countries)== True:
            return ["Accept"]
        else:
            return ["Reject"]

    #Test if Applicant's home is Kanadia; accept them if it is
    #I switched this to use country1 so we could eliminate home_country variable
    #no need for a function to do this; shorter if we just use an if statement
    #ALSO moved this closer to the bottom, because you could have a case of Kanadian traveling via an invalid country;
    # you'd have to reject them, right?
    #kan_check(country1)
    #if kan_check(country1) == True:
        #return ["Accept"]
        #exit
    if country1 == "KAN":
        return ["Accept"]


    #Check if applicant has visa
    #Buggy
    if "visa" in test_applicant:
        #Test if visa_code correctly formatted; reject if invalid format
        valid_visa_format(visa_code)
        if valid_visa_format(visa_code) == False:
            return ["Reject"]

        #Test if visa's date_string correctly formatted; reject if invalid format
        valid_date_format(date_string)
        if valid_date_format(date_string) == False:
            return ["Reject"]

    else:
        return "Accept"


    #Test if Applicant's home is Kanadia; accept them if it is
    #I switched this to use country1 so we could eliminate home_country variable
    #no need for a function to do this; shorter if we just use an if statement
    #kan_check(country1)
    #if kan_check(country1) == True:
        #return ["Accept"]
        #exit

#####################
# HELPER FUNCTIONS ##
#####################

#### SHOULD WE RENAME THIS?  It's confusing that a function that is called is_more_than_2_years_ago returns True
#### if it is LESS than 2 years old
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
    #Brady tested it and it seems to work just fine
    #EXCEPT it allows passports with underscores.  do we have to consider the chance of underscores?
    passport_format_regex = re.compile(r"(\w{5}-){4}\w{5}")
    passport_match = passport_format_regex.search(passport_number)
    if passport_match is None:
        #take out print statement after testing
        #print False
        return False
    #Brady added the "true" option for testing and to match the reqs of the docstring return line.
    #we may be able to delete the else statement and fix the docstring at the end
    else:
         #take out print statement after testing
        #print True
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

    visa_format_regex = re.compile(r"\w{5}-\w{5}")
    visa_match = visa_format_regex.search(visa_code)
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
    date_match = date_format_regex.search(date_string)
    if date_match is None:
        return False
    else:
        return True


def location_check(country):
    """
    Checks whether provided home country of an applicant is valid
    :param country: 3-letter string representing a country.
    :return: Boolean; True if Country1 is KAN or other legitimate country key; False otherwise
    """

    json_data = open("countries.json").read()
    contents = json.loads(json_data)
    for key in contents:
        if country == "KAN":
            return True
        elif country == key:
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

    #Retrieve test_applicant's visa date
    date_string = test_applicant["visa"]["date"]

    if reason == "visit":
        #Retrieve test_applicant home country; if does not require a visa, return True
        country = test_applicant["home"]["country"]
        if countries[country]["visitor_visa_required"] == "0":
            return True

        #If visa date (date_string) less than 2 years old, return True
        else:
            if is_more_than_2_years_ago(date_string) == True:
                return True
            else:
                return False
    #If reason for entry is returning, return True
    elif reason == "returning":
        return True
    else:
        return False


def check_medical_advise(advisory2, advisory3):
    """
    Checks whether there are medical advisories in
    :param advisory: a string to indicate whether there is a medical advisory in applicant's home country
    :param advisory2: a string to indicate whether there is a medical advisory in country applicant traveled from
    :param advisory3: a string to indicate whether there is a medical advisory in country applicant traveled via
    :return: Boolean; False if any advisories exist; otherwise, True.
    """

    #The instructions say "if the traveller is coming from or traveling through a country with a medical advisory
    #But we also check their home country.  Is that correct?  I would argue that we're right here,
    #but i don't know if it's in line with the assignment

    if advisory2 != "":
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
    #should this be ctry instead of cry?

print decide(applicant, ctry)
