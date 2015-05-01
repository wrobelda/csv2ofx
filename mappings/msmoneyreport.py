from csv2ofx.ofx import toOFXDate
from csv2ofx.csvutils import fromCSVCol


def msmoney_memo(row, grid):
    memo = fromCSVCol(row, grid, 'Memo')  # sometimes None
    cat = fromCSVCol(row, grid, 'Category')
    cls = fromCSVCol(row, grid, 'Projects')
    if len(memo) > 0:
        return "%s - %s - %s" % ( memo, cat, cls )
    return "%s - %s" % (cat, cls)


msmoneyrep = {

    'OFX': {
        'skip': lambda row, grid: fromCSVCol(row, grid, 'Split Type') == 'Split',
        'BANKID': lambda row, grid: fromCSVCol(row, grid, 'Account Name').split(' - ')[0],
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 'Account Name').split(' - ')[-1],
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Date')),
        'TRNAMT': lambda row, grid: fromCSVCol(row, grid, 'Amount'),
        'FITID': lambda row, grid: fromCSVCol(row, grid, 'Num'),
        'PAYEE': lambda row, grid: fromCSVCol(row, grid, 'Payee'),
        'MEMO': lambda row, grid: msmoney_memo(row, grid),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 'Currency'),
        'CHECKNUM': lambda row, grid: fromCSVCol(row, grid, 'Num')
    },
    'QIF': {
        'split': lambda row, grid: fromCSVCol(row, grid, 'Date') == '',
        # split should be determined by absence of date and other fields.
        'Account': lambda row, grid: fromCSVCol(row, grid, 'Account'),
        'AccountDscr': lambda row, grid: fromCSVCol(row, grid, 'Account'),
        'Date': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Date')),
        'Payee': lambda row, grid: parse_payee(row, grid),
        'Memo': lambda row, grid: fromCSVCol(row, grid, 'C') + ': ' + fromCSVCol(row, grid, 'Memo'),
        'Category': lambda row, grid: fromCSVCol(row, grid, 'Category'),
        'Class': lambda row, grid: fromCSVCol(row, grid, 'Projects'),
        'Amount': lambda row, grid: fromCSVCol(row, grid, 'Amount'),
        'Number': lambda row, grid: fromCSVCol(row, grid, 'Num')
    }
}