# -*- coding: utf-8 -*-

__author__ = 'dwrobel'

from datetime import datetime

from csv2ofx.csvutils import fromCSVCol


def toOFXDate(row, grid, iteration):
    date = fromCSVCol(row, grid, 'Date')
    return datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')


def is_settling_transaction(row, grid):
    return fromCSVCol(row, grid, 'Description') == 'Settle all balances'


def is_total_balance_summary(row, grid):
    return fromCSVCol(row, grid, 'Description') == 'Total balance'


def is_payment_transaction(row, grid):
    return fromCSVCol(row, grid, 'Category') == 'Payment'


def does_owner_receive_payment(row, grid):
    return is_payment_transaction(row, grid) and float(fromCSVCol(row, grid, get_owners_column_name())) < 0


def does_owner_send_payment(row, grid):
    return is_payment_transaction(row, grid) and float(fromCSVCol(row, grid, get_owners_column_name())) > 0


def should_skip_row(row, grid):
    return not is_owner_involved(row, grid) or is_settling_transaction(row, grid) or is_total_balance_summary(row, grid)


def get_owners_column_name():
    return splitwise['_params']['owners_name']


def find_who_paid(row, grid):
    participants = get_all_participants_and_amounts(row, grid)

    return max(participants, key=lambda item: item[1])


def is_owner_involved(row, grid):
    return float(fromCSVCol(row, grid, get_owners_column_name())) != 0


def has_owner_paid(row, grid):
    return find_who_paid(row, grid)[0] == get_owners_column_name()


def does_owner_owe(row, grid):
    if is_payment_transaction(row, grid):
        return float(fromCSVCol(row, grid, get_owners_column_name())) > 0
    else:
        return float(fromCSVCol(row, grid, get_owners_column_name())) < 0


def has_owner_paid_and_spent(row, grid):
    return has_owner_paid(row, grid) and float(fromCSVCol(row, grid, 'Cost')) - float(
        fromCSVCol(row, grid, get_owners_column_name())) > 0


def get_memo(row, grid):
    return fromCSVCol(row, grid, 'Category')


def get_payee(row, grid):
    return fromCSVCol(row, grid, 'Description')


def get_account(row, grid):
    return get_all_transaction_splits(row, grid)[0][0]


def get_category(row, grid, iteration):
    return get_all_transaction_splits(row, grid)[iteration][0]


def get_amount(row, grid, iteration):
    return get_all_transaction_splits(row, grid)[iteration][1]


def get_all_transaction_splits(row, grid):
    splitwise_main_acc_name = 'Splitwise ' + fromCSVCol(row, grid, 'Currency')
    payee_account_name = find_who_paid(row, grid)[0] + ' ' + fromCSVCol(row, grid, 'Currency')
    imbalance_acc_name = 'Imbalance-' + fromCSVCol(row, grid, 'Currency')

    splits = []

    # add main transaction entry

    if does_owner_owe(row, grid) and not is_payment_transaction(row, grid):
        main_id = payee_account_name
        main_value = float(fromCSVCol(row, grid, get_owners_column_name())) * -1
    elif does_owner_receive_payment(row, grid):
        main_id = find_who_paid(row, grid)[0] + ' ' + fromCSVCol(row, grid, 'Currency')
        main_value = float(fromCSVCol(row, grid, get_owners_column_name())) * -1
    elif does_owner_send_payment(row, grid):
        main_id = payee_account_name
        main_value = float(fromCSVCol(row, grid, get_owners_column_name()))
    else:
        main_id = splitwise_main_acc_name
        main_value = float(fromCSVCol(row, grid, 'Cost'))

    splits.append((main_id, main_value))

    # add splits
    for participant_and_amount in get_all_participants_and_amounts(row, grid):
        participant_acc_name = participant_and_amount[0] + ' ' + fromCSVCol(row, grid, 'Currency')

        if participant_and_amount[0] == get_owners_column_name():
            if has_owner_paid_and_spent(row, grid):
                split_value = round(participant_and_amount[1] - main_value, 2)
                split_id = imbalance_acc_name
            elif does_owner_owe(row, grid) and not is_payment_transaction(row, grid):
                split_value = participant_and_amount[1] * -1
                split_id = imbalance_acc_name
            elif is_payment_transaction(row, grid):
                if does_owner_send_payment(row, grid):
                    continue  # owner split is already reflected in main transaction

                split_value = participant_and_amount[1] * -1
                split_id = splitwise_main_acc_name
            else:
                continue
        elif does_owner_owe(row, grid) and not is_payment_transaction(row, grid):
            continue
        elif does_owner_receive_payment(row, grid):
            continue
        elif does_owner_send_payment(row, grid):
            split_id = participant_acc_name
            split_value = participant_and_amount[1] * -1
        else:
            split_id = participant_acc_name
            split_value = participant_and_amount[1]

        splits.append((split_id, split_value))

    return splits


def get_extra_iterations_to_do(row, grid):
    return len(get_all_transaction_splits(row, grid)) - 1


def get_all_participants_and_amounts(row, grid):
    participants = []

    starting_column_index = splitwise['_params']['participants_columns_start_index']

    for column_index in range(starting_column_index, grid.GetNumberCols()):
        column_id = grid.GetColLabelValue(column_index)
        column_value = float(fromCSVCol(row, grid, column_id))

        if column_value == 0:
            continue
        else:
            participants.append((column_id, column_value))

    return participants


# 1. Export CSV for both groups *and* friends, as each CSV will contain unique transactions
# 2. Set your owners name

splitwise = {

    '_params': {
        'delimiter': ',',
        'skip_initial_space': True,
        'has_multiple_transactions_per_line': True,
        'encoding': "UTF-8",
        'owners_name': 'Dawid Wróbel',
        'participants_columns_start_index': 5
    },

    'QIF': {
        'skip': lambda row, grid: should_skip_row(row, grid),
        'extra_row_iterations_to_do': lambda row, grid: get_extra_iterations_to_do(row, grid),
        'split': lambda row, grid, iteration: iteration > 0,
        'Account': lambda row, grid, iteration: get_account(row, grid),
        'AccountDscr': lambda row, grid, iteration: '',
        'Date': lambda row, grid, iteration: fromCSVCol(row, grid, 'Date'),
        'Payee': lambda row, grid, iteration: get_payee(row, grid),
        'Memo': lambda row, grid, iteration: get_memo(row, grid),
        'Category': lambda row, grid, iteration: get_category(row, grid, iteration),
        'Class': lambda row, grid, iteration: '',
        'Amount': lambda row, grid, iteration: float(get_amount(row, grid, iteration)) * -1,
        'Number': lambda row, grid, iteration: ''
    }
}
