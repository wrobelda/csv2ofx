from csv2ofx.csvutils import fromCSVCol

abnamro = {

    '_params': {
        'delimiter': '\t',
        'has_header': False,
    },

    'OFX': {
        'skip': lambda row, grid: False,
        'multiline': lambda row, grid: False,
        'BANKID': lambda row, grid: 'ABN Amro',
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 0),
        'DTPOSTED': lambda row, grid: fromCSVCol(row, grid, 2),
        'TRNAMT': lambda row, grid: fromCSVCol(row, grid, 6).replace(",", "."),
        'FITID': lambda row, grid: '',
        'PAYEE': lambda row, grid: fromCSVCol(row, grid, 7),
        'MEMO': lambda row, grid: fromCSVCol(row, grid, 7),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 1),
        'CHECKNUM': lambda row, grid: '',
    },
    'QIF': {
        'split': lambda row, grid: False,
        'Account': lambda row, grid: fromCSVCol(row, grid, 0),
        'AccountDscr': lambda row, grid: '',
        # TODO: date should be in mm/dd/YYYY or mm/dd/YY, is now YYYYMMDD
        'Date': lambda row, grid: fromCSVCol(row, grid, 2),
        'Payee': lambda row, grid: '',
        'Memo': lambda row, grid: fromCSVCol(row, grid, 7),
        'Category': lambda row, grid: '',
        'Class': lambda row, grid: '',
        'Amount': lambda row, grid: fromCSVCol(row, grid, 6).replace(",", "."),
        'Number': lambda row, grid: '',
    }
}
