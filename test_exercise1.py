#!/usr/bin/env python

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

Test module for exercise3.py

"""

__author__ = 'Graham Landon'
__author__ = 'Erin Canning'
__author__ = 'Brady Williamson'

from exercise1 import selection, projection, cross_product, UnknownAttributeException, copy


###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

CARS = [["Make", "Color", "Year", "Works(y/n)"],
        ["Toyota", "Yellow", 1989, "y"],
        ["Honda", "Orange", 2011, "n"],
        ["Dodge", "Purple", 2000, "y"],
        ["Fiat", "Polka dot", 1999, "y"]]

TRUCKS = [["Make", "Color", "Year", "Works(y/n)"],
          ["Toyota","Yellow", 1989, "y"],
          ["Honda", "Red", 1998, "n"],
          ["Dodge", "Purple", 2000, "y"]]

BIKES = [["Make", "Color", "Year", "Works(y/n)"],
          ["Huffy", "Puce", 1989, "y"],
          ["Trek", "Pink", 1955, "y"],
          ["BikeCo", "Orange", 1976, "y"]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]

FISH = [["Type", "Size", "Preferred Salinity"],
        ["Trout", "Small", "Fresh"],
        ["Dogfish", "Medium", "Salt"],
        ["Great White", "Large", "Salt"]]

CHESSMEN = [["Name", "Movement"],
            ["Pawn", "Forward"],
            ["Knight", "L-Shape"]]


#####################
# HELPER FUNCTIONS ##
#####################
def is_equal(t1, t2):

    t1.sort()
    t2.sort()

    return t1 == t2


#####################
# FILTER FUNCTIONS ##
#####################
def filter_employees(row):
    """
    Check if employee represented by row
    is AT LEAST 30 years old and makes
    MORE THAN 3500.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition.
    """
    return row[-2] >= 30 and row[-1] > 3500


def filter_vehicles(row):
    """
    Check if car represented by row
    is a 1999 model or newer.
    :param row: A List in the format:
        [{Make}, {Color}, {Year}, {Works(y/n)}]
    :return: True if the row satisfies the condition.
    """
    return row[-2] >= 1999


###################
# TEST FUNCTIONS ##
###################

def test_selection():
    """
    Test select operation.
    """

    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500],
              ["Smith", "Mark", 40, 3900]]

    assert is_equal(result, selection(EMPLOYEES, filter_employees))


def test_projection():
    """
    Test projection operation.
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]

    assert is_equal(result, projection(EMPLOYEES, ["Surname", "FirstName"]))


def test_cross_product():
    """
    Test cross product operation.
    """

    result = [["Employee", "Department", "Department", "Head"],
              ["Smith", "sales", "production", "Mori"],
              ["Smith", "sales", "sales", "Brown"],
              ["Black", "production", "production", "Mori"],
              ["Black", "production", "sales", "Brown"],
              ["White", "production", "production", "Mori"],
              ["White", "production", "sales", "Brown"]]

    assert is_equal(result, cross_product(R1, R2))

################
#Student Tests##
################


def test_selection1():
    """
    Test select operation (student version)
    """
    result1 = [["Make", "Color", "Year", "Works(y/n)"],
                ["Honda", "Orange", 2011, "n"],
                ["Dodge", "Purple", 2000, "y"],
                ["Fiat", "Polka dot", 1999, "y"]]

    result2 = [["Make", "Color", "Year", "Works(y/n)"],
                ["Dodge", "Purple", 2000, "y"]]

    # Test with CARS table and filter_vehicles
    assert is_equal(result1, selection(CARS, filter_vehicles))

    # Test with TRUCKS table and filter_vehicles
    assert is_equal(result2, selection(TRUCKS, filter_vehicles))

    # Test with BIKES table and filter_vehicles (should filter out all entries and return None)
    assert selection(BIKES, filter_vehicles) == None


def test_projection1():
    """
    Test projection operation (student version)
    """
    result1 = [['Make', 'Year'],
              ['Toyota', 1989],
              ['Honda', 2011],
              ['Dodge', 2000],
              ['Fiat', 1999]]

    result2 = [["Size", "Preferred Salinity"],
                ["Small", "Fresh"],
                ["Medium", "Salt"],
                ["Large", "Salt"]]

    result3 = [["Preferred Salinity"],
                ["Fresh"],
                ["Salt"],
                ["Salt"]]

    result4 = [["Type", "Size", "Preferred Salinity"],
             ["Trout", "Small", "Fresh"],
             ["Dogfish", "Medium", "Salt"],
             ["Great White", "Large", "Salt"]]

    # Test with regular table and 2 attributes.
    assert is_equal(result1, projection(CARS,["Make", "Year"]))

    # Test with another regular table and 2 attributes
    assert is_equal(result2, projection(FISH, ["Size", "Preferred Salinity"]))

    # Test with regular table and only 1 attribute
    assert is_equal(result3, projection(FISH, ["Preferred Salinity"]))

    # Test with regular table and all included attributes
    assert is_equal(result4, projection(FISH, ["Type", "Size", "Preferred Salinity"]))

    # Test with regular table and attributes provided out of order
    assert is_equal(result4, projection(FISH, ["Size", "Preferred Salinity", "Type"]))

    # Test with attributes not included in table
    try:
       projection(FISH, ["Colour"])
    except UnknownAttributeException:
        assert True


def test_cross_product1():
    """
    Test cross_product operation (student version)
    """
    result1 = [['Make', 'Color', 'Year', 'Works(y/n)', 'Make', 'Color', 'Year', 'Works(y/n)'],
               ['Toyota', 'Yellow', 1989, 'y', 'Toyota', 'Yellow', 1989, 'y'],
               ['Toyota', 'Yellow', 1989, 'y', 'Honda', 'Red', 1998, 'n'],
               ['Toyota', 'Yellow', 1989, 'y', 'Dodge', 'Purple', 2000, 'y'],
               ['Honda', 'Orange', 2011, 'n', 'Toyota', 'Yellow', 1989, 'y'],
               ['Honda', 'Orange', 2011, 'n', 'Honda', 'Red', 1998, 'n'],
               ['Honda', 'Orange', 2011, 'n', 'Dodge', 'Purple', 2000, 'y'],
               ['Dodge', 'Purple', 2000, 'y', 'Toyota', 'Yellow', 1989, 'y'],
               ['Dodge', 'Purple', 2000, 'y', 'Honda', 'Red', 1998, 'n'],
               ['Dodge', 'Purple', 2000, 'y', 'Dodge', 'Purple', 2000, 'y'],
               ['Fiat', 'Polka dot', 1999, 'y', 'Toyota', 'Yellow', 1989, 'y'],
               ['Fiat', 'Polka dot', 1999, 'y', 'Honda', 'Red', 1998, 'n'],
               ['Fiat', 'Polka dot', 1999, 'y', 'Dodge', 'Purple', 2000, 'y']]

    result2 = [["Type", "Size", "Preferred Salinity", "Name", "Movement"],
               ["Trout", "Small", "Fresh", "Pawn", "Forward"],
               ["Trout", "Small", "Fresh", "Knight", "L-Shape"],
               ["Dogfish", "Medium", "Salt","Pawn", "Forward"],
               ["Dogfish", "Medium", "Salt", "Knight", "L-Shape"],
               ["Great White", "Large", "Salt", "Pawn", "Forward"],
               ["Great White", "Large", "Salt", "Knight", "L-Shape"]]

    result3 = [["Name", "Movement", "Type", "Size", "Preferred Salinity"],
               ["Pawn", "Forward", "Trout", "Small", "Fresh"],
               ["Pawn", "Forward", "Dogfish", "Medium", "Salt"],
               ["Pawn", "Forward", "Great White", "Large", "Salt"],
               ["Knight", "L-Shape", "Trout", "Small", "Fresh"],
               ["Knight", "L-Shape", "Dogfish", "Medium", "Salt"],
               ["Knight", "L-Shape", "Great White", "Large", "Salt"]]

    # Test cross_product of 2 regular tables
    assert is_equal(result1, cross_product(CARS, TRUCKS))

    # Test cross_product of 2 other regular tables
    assert is_equal(result2, cross_product(FISH, CHESSMEN))

    # Test cross_product of 2 tables in opposite order
    assert is_equal(result3, cross_product(CHESSMEN, FISH))
