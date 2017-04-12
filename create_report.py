#!/usr/bin/env python3
import sys
# import datetime


def convertBegDate(date):
    """
    Change the start date format from YYYYMMDD to YYYY-MM-DD hh:mm
    """
    # Bad input
    if len(date) != 8:
        print("Incorrect input")
        exit(1)

    date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 00:00'
    return date


def convertEndDate(date):
    """
    Change the end date format from YYYYMMDD to YYYY-MM-DD hh:mm
    """
    # Bad input
    if len(date) != 8:
        print("Incorrect input")
        exit(1)

    date = date[:4] + '-' + date[4:6] + '-' + date[6:] + ' 23:59'
    return date


def createRepo(beg, end):
    """
    Create report of transactions
    """
    # newBegDate = convertBegDate(begDate)
    # newEndDate = convertEndDate(endDate)


def main():
    """
    Test Function.
    """
    beg = sys.argv[1]
    end = sys.argv[2]
    createRepo(beg, end)
    name = "company_trans_"+beg+"_"+end+".dat"
    myFile = open(name, 'w')
    myFile.close()
    exit(0)

if __name__ == "__main__":
    # Call Main
    main()

    exit(0)
