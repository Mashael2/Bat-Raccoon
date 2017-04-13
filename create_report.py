#!/usr/bin/env python3
import sys
import sqlite3
import datetime
import time

def isInt(v):
    try:    i = int(v)
    except:  return False
    return True

def convertBegDate(date):
    """
    Change the start date format from YYYYMMDD to YYYY-MM-DD hh:mm
    """
    # Bad input
    if len(date) != 8:
        # print("Incorrect input")
        exit(1)

    # check that input params are digit and between 0 and 99991231
    if(isInt(date)):
        if(int(date) < 0 or int(date) > 99991231):
            exit(1)
    else:
        exit(1)

    date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 00:00'
    return date


def convertEndDate(date):
    """
    Change the end date format from YYYYMMDD to YYYY-MM-DD hh:mm
    """
    # Bad input
    if len(date) != 8:
        # print("Incorrect input")
        exit(1)

    # check that input params are digit and between 0 and 99991231
    if(isInt(date)):
        if(int(date) < 0 or int(date) > 99991231):
            exit(1)
    else:
        exit(1)

    date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 23:59'
    return date


def createReport(begDate, endDate):
    """
    Create report of transactions
    """
    # convert date to correct format and error check
    newBegDate = convertBegDate(begDate)
    newEndDate = convertEndDate(endDate)
    # query DB

    # check that query is not empty
    # if empty exit(2) else continue

    name = "company_trans_"+begDate+"_"+endDate+".dat"
    myFile = open(name, 'w')
    myFile.close()


def main():
    """
    Test Function.
    """
    beg = sys.argv[1]
    end = sys.argv[2]
    createReport(beg, end)


if __name__ == "__main__":
    # Call Main
    main()

    exit(0)
