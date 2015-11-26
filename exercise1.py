#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = 'Graham Landon'

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


def selection(t, f):
    new_table = []
    """
    Perform select operation on table t that satisfy condition f.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True iff
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]

    """
    for row in t:
        if f(row) is True:
            new_table.append(row)
    return new_table



selection(EMPLOYEES, filter_employees)


def projection(t, r):
    new_list = []

    """
    Perform projection operation on table t
    using the attributes subset r.

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """
    for item in t[0]:
        if item not in r:
            x = (t[0].index(item))
            new_list.append(x)
    for i in new_list:
        for target in t:
            target[i] = "Marked_for_kill"
    for lists in t:
        for targets in range(lists.count("Marked_for_kill")):
            lists.remove("Marked_for_kill")
    for lists in t:
        if len(lists) == 0:
            raise UnknownAttributeException
    else:
        return t



def cross_product(t1, t2):
    """
    Return the cross-product of tables t1 and t2.

    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]


    """
    new_table = t1[0] + t2[0]
    new2_table = []
    del t1[0]
    del t2[0]
    for list1 in t1:
        for list2 in t2:
            t3 = list1 + list2
            new2_table.append(t3)
    new2_table.insert(0,new_table)
    return new2_table



print cross_product(R1, R2)
