#!/usr/bin/env python

import sys
import argparse

from csv2ofx import converter
import mappings

if __name__ == '__main__':
    c = converter.Converter()

    # standalone parent parameters
    parent_parser = argparse.ArgumentParser(description='CSV to OFX financial statement converter.', add_help=False)
    parent_parser.add_argument('-b', '--bank-name', metavar='NAME', help='name of a bank or account type: %(choices)s',
                               required=True,
                               choices=list(mappings.all_mappings.keys()))
    parent_parser.add_argument('-f', '--format', help='output file format: %(choices)s', required=True,
                               choices=['OFX', 'QIF'])

    # add dummy file arguments on top of parent_parser and get the encoding
    dummy_parser = argparse.ArgumentParser(parents=[parent_parser])
    dummy_parser.add_argument('infile', default="dummy")
    dummy_parser.add_argument('outfile', default="dummy")
    encoding = c.GetFileEncoding(dummy_parser.parse_args().bank_name)

    # create final_parser with infile argument that actually performs (encoding aware) file reading
    final_parser = argparse.ArgumentParser(parents=[parent_parser])
    parent_parser.add_argument('infile',
                               type=argparse.FileType(mode='r', encoding=encoding),
                               default=sys.stdin, help='input CSV file name; use stdin if empty')
    parent_parser.add_argument('outfile', nargs='?', type=argparse.FileType(mode='w', encoding='UTF-8'),
                               default=sys.stdout, help='output file name; use stdout if empty')
    args = parent_parser.parse_args()

    # convert
    c.OpenFile(args.bank_name, args.infile)
    c.ExportFiles(args.bank_name, args.format, args.outfile)
