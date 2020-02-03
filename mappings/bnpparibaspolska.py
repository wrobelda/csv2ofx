# -*- coding: utf-8 -*-
import dateutil

from csv2ofx.utils import setlocale

__author__ = 'dwrobel'

from csv2ofx.csvutils import fromCSVCol

def toOFXDate(date):
    with setlocale('C'):
        return dateutil.parser.parse(date, dayfirst=False).strftime('%Y%m%d')

def get_payee(row, grid):
    payee = fromCSVCol(row, grid, 'Nadawca / odbiorca')

    return payee if payee else fromCSVCol(row, grid, 'Opis')

def get_memo(row, grid):
    memo = fromCSVCol(row, grid, 'Opis')

    return memo if memo else fromCSVCol(row, grid, 'Typ transakcji')

bnpparibaspolska = {

    '_params': {
        'encoding': "UTF-8",
        'decimal_point_symbol': '.',
        'thousands_separator_symbol': ' '
    },

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "BNP Paribas Polska",
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 'Produkt'),
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Data zlecenia operacji')),
        'TRNAMT': lambda row, grid: fromCSVCol(row, grid, 'Kwota'),
        'FITID': lambda row, grid: '',
        'PAYEE': lambda row, grid: get_payee(row, grid),
        'MEMO': lambda row, grid: get_memo(row, grid),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 'Waluta'),
        'CHECKNUM': lambda row, grid: ''
    },
}
