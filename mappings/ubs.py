from datetime import datetime

from csv2ofx.csvutils import fromCSVCol


def ubs_fromUStoOFXDate(date):
    return datetime.strptime(date, '%d.%m.%Y').strftime('%Y%m%d')


def ubs_toQIFDate(date):
    return datetime.strptime(date, '%d.%m.%Y').strftime('%m/%d/%Y')


def ubs_toAmount(debit, credit):
    amount = 0
    if debit:
        amount -= float(debit.replace('\'', ''))
    if credit:
        amount += float(credit.replace('\'', ''))
    return amount


def ubs_toPayee(enteredby, recipient, description):
    if enteredby:
        return enteredby
    elif recipient:
        return recipient
    elif description:
        return description
    else:
        return 'UBS'


def ubs_toDescription(desc1, desc2, desc3):
    return ' / '.join(filter(None, [desc1, desc2, desc3]))


ubs = {
    '_params': {
        'delimiter': ';',
        'skip_last': 1
    },
    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: 'UBS',
        'ACCTID': lambda row, grid: fromCSVCol(row, grid, 'Description'),
        'DTPOSTED': lambda row, grid: ubs_fromUStoOFXDate(fromCSVCol(row, grid, 'Value date')),
        'TRNAMT': lambda row, grid: ubs_toAmount(fromCSVCol(row, grid, 'Debit'), fromCSVCol(row, grid, 'Credit')),
        'FITID': lambda row, grid: row,
        'PAYEE': lambda row, grid: ubs_toPayee(fromCSVCol(row, grid, 'Entered by'), fromCSVCol(row, grid, 'Recipient')),
        'MEMO': lambda row, grid: ubs_toDescription(fromCSVCol(row, grid, 'Description 1'),
                                                    fromCSVCol(row, grid, 'Description 2'),
                                                    fromCSVCol(row, grid, 'Description 3')),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 'Ccy.'),
        'CHECKNUM': lambda row, grid: ''
    },
    'QIF': {
        'split': lambda row, grid: False,
        'Account': lambda row, grid: 'UBS',
        'AccountDscr': lambda row, grid: fromCSVCol(row, grid, 'Description'),
        'Date': lambda row, grid: ubs_toQIFDate(fromCSVCol(row, grid, 'Value date')),
        'Payee': lambda row, grid: ubs_toPayee(fromCSVCol(row, grid, 'Entered by'),
                                               fromCSVCol(row, grid, 'Recipient'),
                                               fromCSVCol(row, grid, 'Description 3')),
        'Memo': lambda row, grid: ubs_toDescription(fromCSVCol(row, grid, 'Description 1'),
                                                    fromCSVCol(row, grid, 'Description 2'),
                                                    fromCSVCol(row, grid, 'Description 3')),
        'Category': lambda row, grid: 'Unclassified',
        'Class': lambda row, grid: '',
        'Amount': lambda row, grid: ubs_toAmount(fromCSVCol(row, grid, 'Debit'), fromCSVCol(row, grid, 'Credit')),
        'Number': lambda row, grid: ''
    }
}