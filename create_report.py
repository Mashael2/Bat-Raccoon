#!/usr/bin/env python3
import sys
import sqlite3
import datetime

def isInt(v):
    try:
        i = int(v)
    except:
        return False
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


def createReport(begDate, endDate, cur):
    """
    Create report of transactions
    Arg:
        begDate => beginning date to query
        endDate => end date to query
        cur => db cursor
    Returns:
        nothing
    """
    # convert date to correct format and error check
    newBegDate = convertBegDate(begDate)
    newEndDate = convertEndDate(endDate)
    print("Getting transaction from {} to {}".format(newBegDate, newEndDate))
    print("")
    # query DB
    query = """
            SELECT
                T.trans_id, T.trans_date, T.card_num, P.prod_num, TL.qty, TL.amt
            FROM trans T
                INNER JOIN trans_line TL ON T.trans_id = TL.trans_id
                INNER JOIN products P ON P.prod_num = TL.prod_num
            WHERE
                T.trans_date >= ? AND T.trans_date <= ?
            GROUP BY
                T.trans_id, T.trans_date, T.card_num, P.prod_num
            """
    cur.execute(query, (newBegDate, newEndDate))
    # check that query is not empty
    # if empty exit(2) else continue
    try:
        recs = cur.fetchall()
        if(len(recs) == 0):
            exit(2)
    except:
        exit(2)
    # Read through query by each row and store the data some how
    # Then filter the data so that this  next file will output in the correct
    # format
    for row in recs:
        print(row)
    # Create the output file
    name = "company_trans_"+begDate+"_"+endDate+".dat"
    myFile = open(name, 'w')

    # Input/write formatted data into myFile

    # Close the writing to output file
    myFile.close()


def main():
    """
    Test Function.
    """
    # Create connection
    conn = sqlite3.connect('hw8SQLite.db')
    if(not conn):
        exit(3)
    # Create cursor
    cur = conn.cursor()
    # Read in date params
    beg = sys.argv[1]
    end = sys.argv[2]
    # Create Report
    createReport(beg, end, cur)
    # Close cursor and DB connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Call Main
    main()

    exit(0)
