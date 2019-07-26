import os


def export(output_filename, mapping, params, grid):
    """
        path: file path to save file
        mapping: mapping for grid data
        grid: csv data
    """

    accounts = {}
    cur_parent = None
    for row in range(grid.GetNumberRows()):
        if mapping['skip'](row, grid): continue

        has_multiple_transactions_per_line = params[
            'has_multiple_transactions_per_line'] if 'has_multiple_transactions_per_line' in params else False

        extra_row_iterations_to_do = mapping['extra_row_iterations_to_do'](row,
                                                                           grid) if 'extra_row_iterations_to_do' in mapping else 0
        iterations = 1 + extra_row_iterations_to_do

        all_keys = {m: mapping[m] for m in mapping if m not in ('skip', 'extra_row_iterations_to_do')}

        for iteration in range(0, iterations):
            if has_multiple_transactions_per_line:
                all_values = {k: mapping[k](row, grid, iteration) for k in all_keys}
            else:
                all_values = {k: mapping[k](row, grid) for k in all_keys}

            tran = {k: all_values[k] for k in ('Date', 'Payee', 'Memo', 'Category', 'Class', 'Amount', 'Number')}

            if not all_values['split']:
                acct = accounts.setdefault(all_values['Account'], {})
                acct['Account'] = all_values['Account']
                acct['AccountDscr'] = all_values['AccountDscr']
                trans = acct.setdefault('trans', [])
                trans.append(tran)
                cur_parent = tran
            else:
                splits = cur_parent.setdefault('splits', [])
                splits.append(tran)
            ++iteration

    for a in list(accounts.values()):
        account_name = a['Account'].encode("ascii", 'ignore').decode("utf-8")
        output_file_path = output_filename + ' ' + account_name + '.qif'
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        output_file = open(output_file_path, 'w', encoding='UTF-8')
        output_file.write("!Account\n"
                          "N%(Account)s\n"
                          "D%(AccountDscr)s\n"
                          "^\n"
                          "!Type:Bank\n" % a)
        for t in a['trans']:
            output_file.write("D%(Date)s\n"
                              "T%(Amount)s\n"
                              "P%(Payee)s\n"
                              "M%(Memo)s\n"
                              "L%(Category)s/%(Class)s\n" % t)
            for s in t.get('splits', []):
                output_file.write("S%(Category)s/%(Class)s\n"
                                  "E%(Memo)s\n$"
                                  "%(Amount)s\n" % s)
            output_file.write("^\n")

        output_file.close()
