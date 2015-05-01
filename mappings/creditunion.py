from csv2ofx.ofx import toOFXDate
from csv2ofx.csvutils import fromCSVCol

cu = {
    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: 'Credit Union',
        'ACCTID': lambda row, grid: 'My Account',
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Date')),
        'TRNAMT': lambda row, grid: fromCSVCol(row, grid, 'Amount').replace('$', ''),
        'FITID': lambda row, grid: row,
        'PAYEE': lambda row, grid: fromCSVCol(row, grid, 'Description'),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 'Comments'),
        'CURDEF': lambda row, grid: 'USD',
        'CHECKNUM': lambda row, grid: fromCSVCol(row, grid, 'Check Number')
    },
    'QIF': {
        'split': lambda row, grid: False,
        'Account': lambda row, grid: 'Credit Union',
        'AccountDscr': lambda row, grid: 'Credit Union Account',
        'Date': lambda row, grid: fromCSVCol(row, grid, 'Date'),
        'Payee': lambda row, grid: fromCSVCol(row, grid, 'Description'),
        'Memo': lambda row, grid: fromCSVCol(row, grid, 'Comments'),
        'Category': lambda row, grid: 'Unclassified',
        'Class': lambda row, grid: '',
        'Amount': lambda row, grid: fromCSVCol(row, grid, 'Amount'),
        'Number': lambda row, grid: fromCSVCol(row, grid, 'Check Number')
    }
}