# -*- coding: utf-8 -*-

from datetime import datetime
from csv2ofx.csvutils import fromCSVCol
from csv2ofx.utils import setlocale
import dateutil.parser

def toOFXDate(date):
    with setlocale('C'):
        return dateutil.parser.parse(date).strftime('%Y%m%d')

def getAmount(row, grid):
    return invert_value(fromCSVCol(row, grid, 'Amount').replace('$', ''))

def invert_value(value):
    try:
        return str(float(value) * -1)
    except ValueError:
        return value

ebay = {

    '_params': {
        'skip_initial_space': True,
        'skip_first': 5,
        'skip_last': 2,
        'encoding': "UTF-8-sig",
    },

    'OFX': {
        'skip': lambda row, grid: not fromCSVCol(row, grid, 'Amount') or float(getAmount(row, grid)) == 0,
        'BANKID': lambda row, grid: "eBay",
        'ACCTID': lambda row, grid: "Invoice",
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Date')),
        'TRNAMT': lambda row, grid: getAmount(row, grid),
        'FITID': lambda row, grid: '',
        'PAYEE': lambda row, grid: fromCSVCol(row, grid, 'Fee Type'),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 'Title'),
        'CURDEF': lambda row, grid: 'USD',
        'CHECKNUM': lambda row, grid: ''
    },
}