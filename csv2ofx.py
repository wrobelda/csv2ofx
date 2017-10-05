#!/usr/bin/env python

import sys
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
    parser.add_argument('infile', type=lambda s: file_choices(("csv", "txt", "xlsx", "xls"), s),
                        help='input CSV file name; use stdin if empty')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType(mode='w', encoding='UTF-8'),
                        default=sys.stdout, help='output file name; use stdout if empty')
    args = parser.parse_args()

    # convert
    c.OpenFile(args.bank_name, args.infile)
    c.ExportFiles(args.bank_name, args.format, args.outfile)
