# -*- coding: utf-8 -*-

__author__ = 'dwrobel'

from datetime import datetime
from csv2ofx.csvutils import fromCSVCol

ignored_transaction_types = {}

transaction_types = {"General Payment": {'is_main_trans': True, 'has_own_acc': False},
                     "Website Payment": {'is_main_trans': True, 'has_own_acc': False},
                     "Web Accept Payment Sent": {'is_main_trans': True, 'has_own_acc': False},
                     "Withdraw Funds to Bank Account": {'is_main_trans': True, 'has_own_acc': True},
                     "Payment Sent": {'is_main_trans': True, 'has_own_acc': False},
                     "Preapproved Payment Sent": {'is_main_trans': True, 'has_own_acc': False},
                     "Express Checkout Payment": {'is_main_trans': True, 'has_own_acc': False},
                     "Express Checkout Payment Sent": {'is_main_trans': True, 'has_own_acc': False},
                     "Recurring Payment Sent": {'is_main_trans': True, 'has_own_acc': False},
                     "Payment Refund": {'is_main_trans': True, 'has_own_acc': False},
                     "Refund": {'is_main_trans': True, 'has_own_acc': False},
                     "Mobile Express Checkout Payment Sent": {'is_main_trans': True, 'has_own_acc': False},
                     "Donation Sent": {'is_main_trans': True, 'has_own_acc': False},
                     "eBay Auction Payment": {'is_main_trans': True, 'has_own_acc': False},
                     "General Withdrawal": {'is_main_trans': True, 'has_own_acc': True},
                     "Donation Payment": {'is_main_trans': True, 'has_own_acc': False},
                     "Express Checkout Payment Received": {'is_main_trans': True, 'has_own_acc': False},
                     "Partially Refunded": {'is_main_trans': True, 'has_own_acc': False},
                     "Mobile Express Checkout Payment Received": {'is_main_trans': True, 'has_own_acc': False},
                     "Donation Received": {'is_main_trans': True, 'has_own_acc': False},
                     "PreApproved Payment Bill User Payment": {'is_main_trans': True, 'has_own_acc': False},
                     "General Credit Card Withdrawal": {'is_main_trans': False, 'has_own_acc': False},
                     "General Incentive/Certificate Redemption": {'is_main_trans': False, 'has_own_acc': False},
                     "General Credit Card Deposit": {'is_main_trans': False, 'has_own_acc': False},
                     "Charge From Credit Card": {'is_main_trans': False, 'has_own_acc': False},
                     "Credit to Credit Card": {'is_main_trans': False, 'has_own_acc': False},
                     "Add Funds from a Bank Account": {'is_main_trans': False, 'has_own_acc': False},
                     "General Currency Conversion": {'is_main_trans': False, 'has_own_acc': False},
                     "Currency Conversion": {'is_main_trans': False, 'has_own_acc': False},
                     "Gift Certificates and Cards Redemption": {'is_main_trans': False, 'has_own_acc': False},
                     "Voucher": {'is_main_trans': False, 'has_own_acc': True},
                     "Voucher Refund": {'is_main_trans': False, 'has_own_acc': True},
                     "Gift Certificate Redemption": {'is_main_trans': False, 'has_own_acc': False},
                     "Bank Deposit to PP Account (Obselete)": {'is_main_trans': False, 'has_own_acc': False},
                     "Payment Hold": {'is_main_trans': False, 'has_own_acc': True},
                     "Payment Release": {'is_main_trans': False, 'has_own_acc': True},
                     "Hold on Balance for Dispute Investigation": {'is_main_trans': False, 'has_own_acc': True},
                     "Cancellation of Hold for Dispute Resolution": {'is_main_trans': False, 'has_own_acc': True},
                     "Temporary Hold": {'is_main_trans': False, 'has_own_acc': True},
                     "Pending Balance Payment": {'is_main_trans': False, 'has_own_acc': True},
                     "Redemption Code": {'is_main_trans': False, 'has_own_acc': True}}


def should_skip_row(row, grid):
    return fromCSVCol(row, grid, 'Type') in ignored_transaction_types


# "Date"        "Time"      "Time Zone"
# "29-01-2015"	"15:27:38"	"PST"
def toOFXDate(row, grid):
    date = fromCSVCol(row, grid, 'Date')
    time = fromCSVCol(row, grid, 'Time')
    # timezone = fromCSVCol(row, grid, 'Time Zone') if grid.HasColumn('Time Zone') else fromCSVCol(row, grid, 'TimeZone')
    # TODO: timezone is not detected by strptime
    return datetime.strptime(date + time, paypal['_params']['date_format']).strftime('%Y%m%d')


def isReceived(row, grid):
    return True if float(get_amount(row, grid)) > 0 else False


# PayPal export has a bug that will have some transaction amounts use \xa0 instead of ' ' as a thousand delimiter
def get_amount(row, grid):
    if grid.HasColumn('Net'):
        return fromCSVCol(row, grid, 'Net').replace(paypal['_params']['decimal_point_symbol'], '.').replace(
            paypal['_params']['thousands_separator_symbol'], '').replace(u'\xa0', '')
    else:
        return fromCSVCol(row, grid, 'Amount')


def are_rows_same_transaction(first, second, grid):
    if grid.HasColumn('Time Zone'):
        return fromCSVCol(first, grid, 'Date') == fromCSVCol(second, grid, 'Date') \
               and fromCSVCol(first, grid, 'Time') == fromCSVCol(second, grid, 'Time') \
               and fromCSVCol(first, grid, 'Time Zone') == fromCSVCol(second, grid, 'Time Zone') \
               and fromCSVCol(first, grid, 'Currency') == fromCSVCol(second, grid, 'Currency')
    else:
        return fromCSVCol(first, grid, 'Date') == fromCSVCol(second, grid, 'Date') \
               and fromCSVCol(first, grid, 'Time') == fromCSVCol(second, grid, 'Time') \
               and fromCSVCol(first, grid, 'Currency') == fromCSVCol(second, grid, 'Currency')


def is_previuos_row_same_transaction(row, grid):
    return are_rows_same_transaction(row - 1, row, grid)


def is_next_row_same_transaction(row, grid):
    return are_rows_same_transaction(row, row + 1, grid)


def is_first_in_transaction(row, grid):
    return row == 0 or not is_previuos_row_same_transaction(row, grid)


def is_last_in_transaction(row, grid):
    return grid.GetRowNumber(row) == grid.GetNumberRows() or not is_next_row_same_transaction(row, grid)


def get_first_in_transaction(row, grid):
    while row > 0:
        if not is_previuos_row_same_transaction(row, grid):
            return row
        else:
            return get_first_in_transaction(row - 1, grid)
    else:
        return row


def get_row_to_return(row, grid, depth=0):
    if is_first_in_transaction(row, grid):
        if not is_next_row_same_transaction(row, grid):
            return row  # first and only operation in transaction
        else:
            if is_main_transaction_type(row, grid):
                return row  # main transaction was the first one, return
            else:
                return get_row_to_return(row + 1, grid, depth + 1)  # start looking for main transaction
    else:
        if is_main_transaction_type(row, grid):
            if depth > 0:  # found main transaction. Use that instead of first row
                return row
            else:
                return get_first_in_transaction(row, grid)  # stumbled on main trsnaction, so swap with first row
        else:
            if depth > 0:
                if is_last_in_transaction(row, grid):
                    return row - depth  # didn't find main transaction, return original row
                else:
                    return get_row_to_return(row + 1, grid, depth + 1)  # keep looking for main transdaction
            else:
                return row


def is_main_transaction_type(row, grid):
    transaction_type = fromCSVCol(row, grid, 'Type')

    if transaction_type in transaction_types:
        return transaction_types[transaction_type]['is_main_trans']
    else:
        raise Exception('Unknown transaction type')


def is_split(row, grid):
    is_previuos_row_same_transaction(row, grid) and not is_main_transaction_type(row, grid),


def get_category(row, grid):
    currency = fromCSVCol(row, grid, 'Currency')
    transaction_type = fromCSVCol(row, grid, 'Type')
    payee = fromCSVCol(row, grid, 'Name')

    if transaction_types[transaction_type]['has_own_acc']:
        category_format = "{transaction_type}: {currency}"
    else:
        category_format = "Imbalance-{currency}"
    return category_format.format(**locals())


def get_payee(row, grid):
    name = fromCSVCol(row, grid, 'Name')
    transaction_type = fromCSVCol(row, grid, 'Type')

    if name:
        return name
    else:
        return transaction_type


def get_memo(row, grid):
    transaction_type = fromCSVCol(row, grid, 'Type')

    auction_site = (' | ' + fromCSVCol(row, grid, 'Auction Site')) \
        if grid.HasColumn('Auction Site') and fromCSVCol(row, grid, 'Auction Site') else ''
    item_title = (' | ' + fromCSVCol(row, grid, 'Item Title')) \
        if grid.HasColumn('Item Title') and fromCSVCol(row, grid, 'Item Title') else ''
    item_id = (' | Item ID: ' + fromCSVCol(row, grid, 'Item ID')) \
        if grid.HasColumn('Item ID') and fromCSVCol(row, grid, 'Item ID') else ''

    return '{}{}{}{}'.format(transaction_type, auction_site, item_title, item_id)


# 1. Set PayPal export encoding to UTF-8 here: https://www.paypal.com/cgi-bin/customerprofileweb?cmd=_profile-language-encoding (click More Options)
# 2. Make sure 'All currencies' filter is selected
# 3. Download "Tab delimeted - balance affecting payments" report from here: https://history.paypal.com/pl/cgi-bin/webscr?cmd=_history

paypal = {

    '_params': {
        'delimiter': '\t',
        'skip_initial_space': True,
        'encoding': "UTF-8-sig",
        'row_substitution': {},
        'date_format': '%d-%m-%Y%H:%M:%S',
        'decimal_point_symbol': ',',
        'thousands_separator_symbol': ' '
    },

    'OFX': {
        'skip': lambda row, grid: False,
        'BANKID': lambda row, grid: "PayPal",
        'ACCTID': lambda row, grid: 'PayPal ' + fromCSVCol(row, grid, 'Currency'),
        'DTPOSTED': lambda row, grid: toOFXDate(row, grid),
        'TRNAMT': lambda row, grid: get_amount(row, grid),
        'FITID': lambda row, grid: fromCSVCol(row, grid, 'Transaction ID'),
        'PAYEE': lambda row, grid: get_payee(row, grid),
        'MEMO': lambda row, grid: get_memo(row, grid),
        'CURDEF': lambda row, grid: fromCSVCol(row, grid, 'Currency'),
        'CHECKNUM': lambda row, grid: ''
    },
    'QIF': {
        'skip': lambda row, grid: should_skip_row(row, grid),
        'split': lambda row, grid: False,
        'Account': lambda row, grid: 'PayPal ' + fromCSVCol(get_row_to_return(row, grid), grid, 'Currency'),
        'AccountDscr': lambda row, grid: '',
        'Date': lambda row, grid: fromCSVCol(get_row_to_return(row, grid), grid, 'Date'),
        'Payee': lambda row, grid: get_payee(get_row_to_return(row, grid), grid),
        'Memo': lambda row, grid: get_memo(get_row_to_return(row, grid), grid),
        'Category': lambda row, grid: get_category(get_row_to_return(row, grid), grid),
        'Class': lambda row, grid: '',
        'Amount': lambda row, grid: get_amount(get_row_to_return(row, grid), grid),
        'Number': lambda row, grid: ''
    }
}
