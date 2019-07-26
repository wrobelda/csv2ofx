# -*- coding: utf-8 -*-
import dateutil

from csv2ofx.csvutils import fromCSVCol
from csv2ofx.utils import setlocale

__author__ = 'dwrobel'


def toOFXDate(date):
    with setlocale('C'):
        return dateutil.parser.parse(date, dayfirst=True).strftime('%Y%m%d')



def is_split_transaction(row, grid):
    return row > 0 and \
        fromCSVCol(row, grid, "Data transakcji") == fromCSVCol(row - 1, grid, "Data transakcji") and \
        fromCSVCol(row, grid, "Data księgowania") == fromCSVCol(row - 1, grid, "Data księgowania") and \
        fromCSVCol(row, grid, "Odbiorca / Nadawca") == fromCSVCol(row - 1, grid, "Odbiorca / Nadawca") and \
        fromCSVCol(row, grid, "Tytuł operacji") == fromCSVCol(row - 1, grid, "Tytuł operacji") and \
        get_amount(row, grid) == -1 * get_amount(row -1, grid) and \
        get_currency(row, grid) == get_currency(row - 1, grid)

def get_category(row, grid):
    if is_split_transaction(row, grid):
        return fromCSVCol(row, grid, "Nazwa konta")
    else:
        return "Imbalance-" + fromCSVCol(row, grid, 'Kwota').split()[1]

def get_currency(row, grid):
    return fromCSVCol(row, grid, 'Kwota').split()[1]

def get_amount(row, grid):
    return float(fromCSVCol(row, grid, 'Kwota').split()[0])

nest = {

        '_params': {
            'delimiter': ',',
            'skip_initial_space': True,
            'encoding': "UTF-8",
            'decimal_point_symbol': '.',
            'thousands_separator_symbol': ''
        },

        'QIF': {
            'skip': lambda row, grid: False,
            'split': lambda row, grid: is_split_transaction(row, grid),
            'Account': lambda row, grid: fromCSVCol(row, grid, "Nazwa konta"),
            'AccountDscr': lambda row, grid: '',
            'Date': lambda row, grid: fromCSVCol(row, grid, 'Data transakcji'),
            'Payee': lambda row, grid: fromCSVCol(row, grid, 'Odbiorca / Nadawca'),
            'Memo': lambda row, grid: fromCSVCol(row, grid, 'Tytuł operacji'),
            'Category': lambda row, grid: get_category(row, grid),
            'Class': lambda row, grid: '',
            'Amount': lambda row, grid: get_amount(row, grid),
            'Number': lambda row, grid: ''
        }
    }
