# -*- coding: utf-8 -*-
import re

import dateutil

from csv2ofx.csvutils import fromCSVCol
from csv2ofx.utils import setlocale


def toOFXDate(date):
    with setlocale('C'):
        return dateutil.parser.parse(date, dayfirst=False).strftime('%Y%m%d')


def get_payee(row, grid):
    payee = (re.sub('\s+', ' ', fromCSVCol(row, grid, '#Nadawca/Odbiorca')).strip() + ' ' + \
           re.sub('\s+', ' ', fromCSVCol(row, grid, '#Numer konta')).replace("'", '').strip()).strip()

    return payee if payee else fromCSVCol(row, grid, '#Opis operacji')


mBank_current = {

    '_params': {
        'skip_initial_space': True,
        'skip_first': 31,
        'skip_last': 2,
        'encoding': 'windows-1250',
        'delimiter': ';',
    },

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "mBank",
        'ACCTID': lambda row, grid: "Konto",
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, '#Data operacji')),
        'TRNAMT': lambda row, grid: fromCSVCol(row, grid, '#Kwota').replace(',', '.').replace(' ', ''),
        'FITID': lambda row, grid: '',
        'PAYEE': lambda row, grid: get_payee(row, grid),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, '#Tytuł'),
        'CURDEF': lambda row, grid: 'PLN',
        'CHECKNUM': lambda row, grid: ''
    },
}

mBank_eMakler = {

    '_params': {
        'skip_initial_space': True,
        'skip_first': 19,
        'skip_last': 0,
        'encoding': 'windows-1250',
        'delimiter': ';',
        'has_header': False,  # the file has header but is missing one of the columns
    },

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "mBank",
        'ACCTID': lambda row, grid: "eMakler",
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 0)),
        'TRNAMT': lambda row, grid: (fromCSVCol(row, grid, 3) if not fromCSVCol(row, grid, 2) else fromCSVCol(row, grid, 2)).replace(',', '.').replace(' ', ''),
        'FITID': lambda row, grid: '',
        'PAYEE': lambda row, grid: fromCSVCol(row, grid, 1),
        'MEMO': lambda row, grid: '',
        'CURDEF': lambda row, grid: 'PLN',
        'CHECKNUM': lambda row, grid: ''
    },
}
