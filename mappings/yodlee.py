from csv2ofx.ofx import toOFXDate
from csv2ofx.csvutils import fromCSVCol


def yodlee_dscr(row, grid):
    " use user description for payee 1st, the original description"
    od = fromCSVCol(row, grid, 'Original Description')
    ud = fromCSVCol(row, grid, 'User Description')
    if len(ud) > 0:
        return "%s - %s" % (od, ud)
    return od


def yodlee_memo(row, grid):
    memo = fromCSVCol(row, grid, 'Memo')  # sometimes None
    cat = fromCSVCol(row, grid, 'Category')
    cls = fromCSVCol(row, grid, 'Classification')
    if len(memo) > 0:
        return "%s - %s - %s" % ( memo, cat, cls)
    return "%s - %s" % ( cat, cls )


yodlee = {

    'OFX': {
        'skip': lambda row, grid: fromCSVCol(row, grid, 'Split Type') == 'Split',
        'BANKID': lambda row, grid: fromCSVCol(row, grid, 'Account Name').split(' - ')[0],
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 'Account Name').split(' - ')[-1],
        'DTPOSTED': lambda row, grid: toOFXDate(fromCSVCol(row, grid, 'Date')),
        'TRNAMT': lambda row, grid: fromCSVCol(row, grid, 'Amount'),
        'FITID': lambda row, grid: fromCSVCol(row, grid, 'Transaction Id'),
        'PAYEE': lambda row, grid: yodlee_dscr(row, grid),
        'MEMO': lambda row, grid: yodlee_memo(row, grid),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 'Currency'),
        'CHECKNUM': lambda row, grid: fromCSVCol(row, grid, 'Transaction Id')
    },
    'QIF': {
        'split': lambda row, grid: fromCSVCol(row, grid, 'Split Type') == 'Split',
        'Account': lambda row, grid: fromCSVCol(row, grid, 'Account Name'),
        'AccountDscr': lambda row, grid: ' '.join(fromCSVCol(row, grid, 'Account Name').split('-')[1:]),
        'Date': lambda row, grid: fromCSVCol(row, grid, 'Date'),
        'Payee': lambda row, grid: fromCSVCol(row, grid, 'Original Description'),
        'Memo': lambda row, grid: fromCSVCol(row, grid, 'User Description') + ' ' + fromCSVCol(row, grid, 'Memo'),
        'Category': lambda row, grid: fromCSVCol(row, grid, 'Category') + '-' + fromCSVCol(row, grid, 'Classification'),
        'Class': lambda row, grid: '',
        'Amount': lambda row, grid: fromCSVCol(row, grid, 'Amount'),
        'Number': lambda row, grid: fromCSVCol(row, grid, 'Transaction Id')
    }
}