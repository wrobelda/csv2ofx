# -*- coding: utf-8 -*-

__author__ = 'dwrobel'

from datetime import datetime

from csv2ofx.csvutils import fromCSVCol


def fromEUtoOFXDate(date):
    yearlen = len(date.split('-')[-1])
    return datetime.strptime(date, yearlen == 2 and '%d-%m-%y' or '%d-%m-%Y').strftime('%Y%m%d')


def is_multiline(row, grid):
    return not fromCSVCol(row, grid, 'Data księgowania')


def get_amount(row, grid):
    amount = fromCSVCol(row, grid, 'Kwota')

    if not amount and is_multiline(row, grid):
        amount = fromCSVCol(row, grid, 'Użytkownik')
    return amount


raiffeisenpolbank_ccard = {

    '_params': {
        'delimiter': ';',
        'encoding': 'windows-1250',
    },

    'OFX': {
        'skip': lambda row, grid: False,
        'multiline': lambda row, grid: is_multiline(row, grid),
        'BANKID': lambda row, grid: "Raiffeisen Polbank",
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 'Numer karty') if not is_multiline(row, grid) else '',
        'DTPOSTED': lambda row, grid: fromEUtoOFXDate(fromCSVCol(row, grid, 'Data transakcji')) if not is_multiline(row,
                                                                                                                    grid) else '',
        'TRNAMT': lambda row, grid: get_amount(row, grid),
        'FITID': lambda row, grid: '',
        'PAYEE': lambda row, grid: fromCSVCol(row, grid, 'Miejsce transakcji') if not is_multiline(row, grid) else '',
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 'Numer karty') if is_multiline(row, grid) else '',
        'CURDEF': lambda row, grid: 'PLN',
        'CHECKNUM': lambda row, grid: ''
    },
}