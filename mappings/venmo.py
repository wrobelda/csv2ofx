# -*- coding: utf-8 -*-
import dateutil

__author__ = 'dwrobel'

from csv2ofx.csvutils import fromCSVCol
from csv2ofx.utils import setlocale
from re import sub

# example Venmo CSV date: Mon Aug 31 12:43:42 +0000 2015
def toOFXDate(date):
    with setlocale('C'):
        return dateutil.parser.parse(date).strftime("%Y%m%dT")

def getPayee(row, grid):
    type = fromCSVCol(row, grid, 'Type')
    fromUsername = fromCSVCol(row, grid, 'From')
    toUsername = fromCSVCol(row, grid, 'To')
    destination = fromCSVCol(row, grid, 'Destination')
    fundingSource = fromCSVCol(row, grid, 'Funding Source')

    if type.lower() in ('transfer to bank', 'standard transfer'):
        payee = '%s: %s' % (type, destination)
    elif type.lower() == "payment":
        payee = 'Payment from "%s" to "%s" using "%s"' % (fromUsername, toUsername, fundingSource)
    elif type.lower() == "charge":
        payee = '"%s" charged "%s"' % (fromUsername, toUsername)
    else:
        raise Exception("Unknown transaction type")
    return payee

def get_amount(row, grid):
    return sub('[$ +]', '', fromCSVCol(row, grid, 'Amount (total)')).replace(venmo['_params']['decimal_point_symbol'], '.').replace(venmo['_params']['thousands_separator_symbol'], '')

venmo = {

    '_params': {
        'skip_initial_space': True,
        'encoding': "UTF-8",
        'decimal_point_symbol': '.',
        'thousands_separator_symbol': ',',
        'skip_first': 0,
        'skip_last': 3
    },

    'OFX': {
        'skip': lambda row, grid: not fromCSVCol(row, grid, 'Datetime'),
        'BANKID': lambda row, grid: "Venmo",
        'ACCTID': lambda row, grid: "Venmo",
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Datetime')),
        'TRNAMT': lambda row, grid: get_amount(row, grid),
        'FITID': lambda row, grid: fromCSVCol(row, grid, 'ID'),
        'PAYEE': lambda row, grid: getPayee(row, grid),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 'Note'),
        'CURDEF': lambda row, grid: 'USD',
        'CHECKNUM': lambda row, grid: ''
    },
}