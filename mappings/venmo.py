# -*- coding: utf-8 -*-

__author__ = 'dwrobel'

from datetime import datetime

from csv2ofx.csvutils import fromCSVCol
from csv2ofx.utils import setlocale


# example Venmo CSV date: Mon Aug 31 12:43:42 +0000 2015
def toOFXDate(date):
    with setlocale('C'):
        return datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y").strftime('%Y%m%d')

def getPayee(row, grid):
    fromUsername = fromCSVCol(row, grid, 'from_full_name')
    toUsername = fromCSVCol(row, grid, 'to_full_name')
    return '"%s" to "%s"' % (fromUsername, toUsername)

venmo = {

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "Venmo",
        'ACCTID': lambda row, grid: "Venmo",
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'created_at')),
        'TRNAMT': lambda row, grid: fromCSVCol(row, grid, 'amount'),
        'FITID': lambda row, grid: fromCSVCol(row, grid, 'transaction_id'),
        'PAYEE': lambda row, grid: getPayee(row, grid),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 'note'),
        'CURDEF': lambda row, grid: 'USD',
        'CHECKNUM': lambda row, grid: ''
    },
}