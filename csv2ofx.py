#!/usr/bin/env python

import argparse
import os

from csv2ofx import converter
import mappings

if __name__ == '__main__':

    def file_choices(choices, fname):
        ext = os.path.splitext(fname)[1][1:].lower()
        if ext not in choices:
            parser.error("file doesn't end with one of {}".format(choices))
        return fname

    c = converter.Converter()

    # standalone parent parameters
    parser = argparse.ArgumentParser(description='CSV to OFX financial statement converter.', add_help=False)
    parser.add_argument('-b', '--bank-name', metavar='NAME', help='name of a bank or account type: %(choices)s',
                        required=True,
                        choices=list(mappings.all_mappings.keys()))
    parser.add_argument('-f', '--format', help='output file format: %(choices)s', required=True,
                        choices=['OFX', 'QIF'])
    parser.add_argument('input_file_path', type=lambda s: file_choices(("csv", "txt", "xlsx", "xls"), s),
                        help='input CSV file name; use stdin if empty')
    args = parser.parse_args()

    # convert
    c.OpenFile(args.bank_name, args.input_file_path)

    # export
    output_file_path = os.path.splitext(os.path.abspath(args.input_file_path))[0] if args.input_file_path else 'csv2ofx_parsed'
    c.ExportFiles(args.bank_name, args.format, output_file_path)
