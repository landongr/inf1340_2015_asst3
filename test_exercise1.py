#!/usr/bin/env python

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

Test module for exercise3.py

"""

__author__ = "Graham Landon"


from exercise1 import selection, projection, cross_product, copy


###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

CARS = [["Make", "Color", "Year", "Works(y/n)"],
        ["Toyota","Yellow", 1989, "y"],
        ["Honda", "Orange", 2011, "n"],
        ["Dodge", "Purple", 2000, "y"],
        ["Fiat", "Polka dot", 1999, "y"]]

TRUCKS = [["Make", "Color", "Year", "Works(y/n)"],
          ["Toyota","Yellow", 1989, "y"],
          ["Honda", "Red", 1998, "n"],
          ["Dodge", "Purple", 2000, "y"]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]


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

#################
##Student Tests##
#################

def test_projection1():

    # Test the projection function

    result = [['Make', 'Year'],
              ['Toyota', 1989],
              ['Honda', 2011],
              ['Dodge', 2000],
              ['Fiat', 1999]]

    assert is_equal(result, projection(CARS,["Make", "Year"]))



def test_cross_product1():
    #BUGGY NOT WORKING!
    result = [['Make', 'Color', 'Year', 'Works(y/n)', 'Make', 'Color', 'Year', 'Works(y/n)'],
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

    result2 = [['Make', 'Color', 'Year', 'Works(y/n)', 'Make', 'Color', 'Year', 'Works(y/n)'],
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

    assert is_equal(result, cross_product(CARS, TRUCKS))
    #assert is_equal(result2, cross_product(CARS, TRUCKS))


