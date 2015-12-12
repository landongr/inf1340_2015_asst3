#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = "Graham Landon, Erin Canning, and Brady Williamson"

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]

TRUCKS = [["Make", "Color", "Year", "Works(y/n)"],
          ["Toyota","Yellow", 1989, "y"],
          ["Honda", "Red", 1998, "n"],
          ["Dodge", "Purple", 2000, "y"]]

BIKES = [["Make", "Color", "Year", "Works(y/n)"],
          ["Huffy","Puce", 1989, "y"],
          ["Trek", "Pink", 1955, "y"],
          ["BikeCo", "Orange", 1976, "y"]]


import copy


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

#####################
# HELPER FUNCTIONS ##
#####################

TABLE = [["number 1", "number 2", "number 3"],
         [4,5,6],
         [7,8,9],
         [6,1,2]]


def remove_duplicates(l):
    """
    Removes duplicates from l, where l is a List of Lists.
    :param l: a List
    """

    d = {}
    result = []
    for row in l:
        if tuple(row) not in d:
            result.append(row)
            d[tuple(row)] = True

    return result


class UnknownAttributeException(Exception):
    """
    Raised when attempting set operations on a table
    that does not contain the named attribute
    """
    pass


def fun(table):
    table2 = [] + table[0]
    count = 1
    while count < len(table) - 1:
        if table[count] > table[-1]:
            table2.append(table[-1])
        count += 1
    else:
        print table2

##########################
##Real code Starts Here!##
##########################


def selection(t, f):
    """
    Perform select operation on table t that satisfy condition f.
    :param: t: a table (list of lists)
    :param: f: a function to apply to t
    :returns: new_table: a table (list of lists) that results from applying function f to table t.
    If result is an empty table, returns None.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True iff
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]

    """
    new_table = []
    # iterate though rows of the table
    for row in t:
        # checks which rows return True after being run through the function
        if f(row) is True:
            # If they return True they are appended to a new table
            new_table.append(row)
    # If only first row was added to table, return None
    if len(new_table) == 1:
        return None
    # Otherwise, return the new_table
    else:
        return new_table



def projection(q, r):

    """
    Perform projection operation on table q
    using the attributes subset r.
    :param: q: a table (list of lists)
    :param: r: a list of attributes
    :returns: t: a table (list of lists)
    :raises: UnknownAttributeException if attribute r is not included in table q
    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """
    t = []
    t = copy.deepcopy(q)

    new_list = []
    # iterate though the headings of the schema
    for item in t[0]:
        # checks if any headings match the attributes in subset r
        if item not in r:
            # if a heading is not in the subset its index will be stored in a new list
            x = (t[0].index(item))
            new_list.append(x)
    # iterates though the new list, these are the index points for the columns that will be removed
    for i in new_list:
        # iterates though each list in the table
        for target in t:
            # marks any index that matches the column to be removed by changing it to the targeted string
            target[i] = "Marked_for_kill"
    # iterates though each list in the table again
    for lists in t:
        # iterates though each list looking for targeted indexes and removes them
        for targets in range(lists.count("Marked_for_kill")):
            lists.remove("Marked_for_kill")
    # Checks to make sure the attributes in r actually return a list, and will throw an error if the list is empty
    for lists in t:
        if len(lists) == 0:
            raise UnknownAttributeException
    # Returns the modified table
    else:
        return t


def cross_product(t1, t2):
    """
    Return the cross-product of tables t1 and t2.
    :param: t1: a table (list of lists)
    :param: t2: a list of attributes
    :returns: new2_table: a table (list of lists)that is the cross-product of t1 and t2
    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]


    """
    # Combines and pulls the schema headings to be put on the final table
    new_table = t1[0] + t2[0]
    new2_table = []
    # Removes the Schema headings from the 2 tables
    # Iterates though the lists in both tables
    for list1 in t1[1:]:
        for list2 in t2[1:]:
            # Combines the lists for each table (excluding schemas that have been removed)
            t3 = list1 + list2
            # Appends combined tables to a new list, this stops the lists from overwriting themselves
            new2_table.append(t3)
    # Inserts the Schema headings back at the top of the table
    new2_table.insert(0,new_table)
    return new2_table



CARS = [["Make", "Color", "Year", "Works(y/n)"],
        ["Toyota","Yellow", 1989, "y"],
        ["Honda", "Orange", 2011, "n"],
        ["Dodge", "Purple", 2000, "y"],
        ["Fiat", "Polka dot", 1999, "y"]]

TRUCKS = [["Make", "Color", "Year", "Works(y/n)"],
          ["Toyota","Yellow", 1989, "y"],
          ["Honda", "Red", 1998, "n"],
          ["Dodge", "Purple", 2000, "y"]]
