#!/usr/bin/env python3
import sys
import sqlite3

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
    # print("New dates beg: {} end: {}".format(newBegDate, newEndDate))
    # query DB
    query = """
            SELECT
                T.trans_id, T.trans_date, T.card_num, P.prod_num, P.prod_desc, TL.qty, TL.amt
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
    # Read through query by each row and store the data in a dictionary
    # data is formated into key value pairs so we can format the output
    # when writing to the output file
    myDict = {}
    # print("trans_id , trans_date, card_num, prod_num, prod_desc, qty, amt")
    for row in recs:
        # print(row)
        key = ""
        key += formatTransId(row[0])
        key += formatDate(row[1])
        key += formatCreditCard(row[2])
        # print("Key: ",key)
        myDict[key] = []
    for row in recs:
        # print(row)
        key = ""
        key += formatTransId(row[0])
        key += formatDate(row[1])
        key += formatCreditCard(row[2])
        val = ""
        val += formatQty(row[5])
        val += formatAmt(row[6])
        val += row[4]
        # print("Val: ",val)
        myDict[key].append(val)
    # Now add zeros to places that dont have a 1st-3rd product
    for key in myDict:
        length = len(myDict[key])
        if length == 0:
            myDict[key].append("00000000")
            myDict[key].append("00000000")
            myDict[key].append("00000000")
        if length == 1:
            myDict[key].append("00000000")
            myDict[key].append("00000000")
        if length == 2:
            myDict[key].append("00000000")
    # Now sum the total amounts for each key and append it to the end of their
    # value
    tot = 0
    for key in myDict:
        tot = 0
        for val in myDict[key]:
            sval = str(val)
            tot += int(sval[2:6])
        tot = formatTotal(tot)
        myDict[key].append(tot)

    # Create the output file
    name = "company_trans_"+begDate+"_"+endDate+".dat"
    myFile = open(name, 'w')
    # Input/write formatted data into myFile / output file
    for  key in myDict:
        count = 0
        line = key
        for val in myDict[key]:
            if count == 0:
                line += str(val)
            else:
                line += "\t"+str(val)
            count += 1
        myFile.write(line+"\n")
        print("["+line+"]")
    # Close the writing to output file
    myFile.close()


def formatTransId(transId):
    trans = str(transId)
    length = len(trans)
    if length < 5:
        trans = "0" * (5-length) + trans
    # print("Trans: ",trans )
    return trans



def formatDate(date):
    fdate = date[:4]+date[5:7]+date[8:10]+date[11:13]+date[14:16]
    fdate = str(fdate)
    # print("Date: ", date)
    return fdate


def formatCreditCard(card):
    lastSix = card[len(card)-6:]
    lastSix = str(lastSix)
    # print("Last six: ", lastSix)
    return lastSix


def formatQty(qty):
    fqty = int(qty)
    fqty = str(fqty)
    length = len(fqty)
    if length < 2:
        fqty = "0"+fqty
    # print("Qty: ",fqty )
    return fqty


def formatAmt(amt):
    famt = str(amt)
    famt = famt.replace(".", "")
    length = len(famt)
    if length < 6:
        famt = "0" * (6-length) + famt
    # print("Amt: ", famt)
    return famt

def formatTotal(total):
    ftot = str(total)
    length = len(ftot)
    if length < 6:
        ftot = "0" * (6-length) + ftot
    return ftot

def main():
    """
    Test Function.
    """
    # Create connection
    conn = sqlite3.connect('hw8SQLite.db')
    if(not conn):
        exit(1)
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
