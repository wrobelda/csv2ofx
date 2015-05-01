# -*- coding: utf-8 -*-

from datetime import datetime
from re import search

from csv2ofx.csvutils import fromCSVCol


def fromEUtoOFXDate(date):
    yearlen = len(date.split('-')[-1])
    return datetime.strptime(date, yearlen == 2 and '%d-%m-%y' or '%d-%m-%Y').strftime('%Y%m%d')


def tmobilepl_amount(row, grid):
    amount = fromCSVCol(row, grid, 'Kwota').split(' ')[0]
    currency = fromCSVCol(row, grid, 'Kwota').split(' ')[1]
    memo = fromCSVCol(row, grid, 'Tytuł płatności')
    match = search('Kurs wymiany: (?P<currate>[0-9.]+)', memo)
    if match:
        currate = match.group('currate')
        amount = float(amount) * float(currate)
    return amount


tmobilepl = {

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "T-Mobile",
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 'Rachunek'),
        'DTPOSTED': lambda row, grid: fromEUtoOFXDate(fromCSVCol(row, grid, 'Data')),
        'TRNAMT': lambda row, grid: tmobilepl_amount(row, grid),
        'FITID': lambda row, grid: '',
        'PAYEE': lambda row, grid: fromCSVCol(row, grid, 'Nazwa odbiorcy/nadawcy'),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 'Tytuł płatności'),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 'Kwota').split(' ')[1],
        'CHECKNUM': lambda row, grid: ''
    },
}