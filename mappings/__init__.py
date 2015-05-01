# mapping tells the next functions where to get the data for each row
# each key in a mapping must return a function that takes
# the current row and the SimpleCSVGrid object
# the function must return the OFX data for that field.

# NOTE I thought about simply having a dicionary from key fields to column numbers
# but that was not flexible enough to combine column data dynamically
# in order to get custom data from the CSV file.
# (example Memo/Description/BankID/Account id in the yodlee data)

"""
    Mappings API.

    csvutils provides the functions fromCSVCol,xmlize and the grid that holds the csv data.
    fromCSVCol(row,grid,column)
        row: the row number
        grid: the csv data
        column: the case sensitive column header

        returns the csv data for that location

    a mapping is a dictionary of functions.  The exporters call the function for each key
    in the dictionary.  You are free to use any functions or custom logic to return whatever
    data you prefer so that you get the correct data in the fields required by the export format.
    The format of the function that must be returned is:

    def custfunc(row,grid)

    If you have a one-to-one mapping for a key to the CSV data, you can easily just use fromCSVCol.

    Example:

    'CHECKNUM':lambda row,grid: fromCSVCol(row,grid,'Check Number')

    Special parameters for import use these keys:

        delimiters: delimiter for CSV, default to ','
        skip_last: number of lines to skip at the end of the CSV file, default to 0

    OFX export uses these keys:

        skip: not used in export but tells the exporter to skip a row.  Useful for split data (ofx can't handle split data).
        multiline: tells the exporter to treat the line as a continuation of the previous line's transaction. Values are
                    concatenated if same key is used more than once per transaction. Useful for badly formatted statements
                    coming from the banks whose IT employees can't comprehend a concept as simple as CSV file.
        BANKID: the id of the bank
        ACCTID: the account id
        DTPOSTED: date the transaction was posted (YYYYMMDD)
        TRNAMT: amount of transaction
        FITID: a unique transaction identifier (for avoiding duplicate imports)
        PAYEE: who the transaction was posted to/from
        MEMO: the memo
        CURDEF: currency def.  e.g. USD
        CHECKNUM: check number

    QIF export uses these keys:
        split: tells exporter this row is part of a parent transaction
            (row must have be preceded by parent) return True or False
        Account: The name of the account
        AccountDscr: A description for the account
        Date: date in mm/dd/YYYY or mm/dd/YY
        Payee: the transaction payee
        Memo: the memo
        Category: the category.  Imports as the expense account usually.
        Class: optional class data.  Return '' if unused
        Amount: transaction amount
        Number: check number 

    mapping dict format
    {'_params':<special parameters>, 'QIF':<the qif mapping>, 'OFX':<the ofx mapping>}

    The last line in this file tells csv2ofx.py about your mappings.
    You may add as many as you like.

    all_mappings={"Mapping Description":<the mapping>, ...}


"""

from creditunion import cu
from msmoneyreport import msmoneyrep
from ubs import ubs
from yodlee import yodlee
from tmobilekonto import tmobilepl

all_mappings = {'T-Mobile Konto': tmobilepl, 'Yodlee': yodlee, 'Credit Union': cu, 'UBS': ubs,
                'MS Money Report (CSV)': msmoneyrep}
