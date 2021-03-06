# -*- coding: utf-8 -*-

__author__ = 'dwrobel'

from datetime import datetime

from csv2ofx.csvutils import fromCSVCol

# example of Square Cash CSV date: 2016-02-02 15:12:02 EST
def toOFXDate(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S %Z").strftime('%Y%m%d')

def getPayee(row, grid):
    me = "me"
    them = fromCSVCol(row, grid, 'Name')
    payee, receiver = (them, me) if isReceived(row, grid) else (me, them)
    return '{payee} to {receiver}'.format(**locals())

def getAmount(row, grid):
    return fromCSVCol(row, grid, 'Amount').replace('$', '')

def isReceived(row, grid):
    return True if float(getAmount(row, grid)) > 0 else False


squarecash = {

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "Square Cash",
        'ACCTID': lambda row, grid: "Square Cash",
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Date')),
        'TRNAMT': lambda row, grid: getAmount(row, grid),
        'FITID': lambda row, grid: fromCSVCol(row, grid, 'Transaction ID'),
        'PAYEE': lambda row, grid: getPayee(row, grid),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 'Notes'),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 'Currency'),
        'CHECKNUM': lambda row, grid: ''
    },
}