#! /usr/bin/python
# -*-  coding: utf-8 -*-
"""
Provides utility functions.
"""

from PyQt5.QtCore import (
    QDate
)

def month_diff(date1, date2):
    """
    Calculates the time difference abs(date1 - date2) between two dates in months.
    Day is neglected.

    :param date1 (QDate): First date
    :param date2 (QDate): Second date

    :returns: The time difference in months
    :rtype: int
    """
    # First make sure, that date2 > date1
    if date1.daysTo(date2) < 0:
        date_tmp = date1
        date1 = date2
        date2 = date_tmp
    years = date2.year() - date1.year()
    months = date2.month() - date1.month()
    if months < 0:
        years -= 1
        months += 12
    return 12 * years + months
