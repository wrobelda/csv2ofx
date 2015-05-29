#!/usr/bin/env python

import sys
import argparse

from csv2ofx import converter
import mappings

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSV to OFX financial statement converter.')
    parser.add_argument('-b', '--bank-name', metavar='NAME', help='name of a bank or account type', required=True,
                        choices=mappings.all_mappings.keys())
    parser.add_argument('-f', '--format', help='output file format', required=True, choices=['OFX', 'QIF'])
    parser.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin,
                        help='input CSV file name; use stdin if empty')
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='output file name; use stdout if empty')

    args = parser.parse_args()

    c = converter.Converter()
    c.OpenFile(args.bank_name, args.infile)
    c.ExportFiles(args.bank_name, args.format, args.outfile)
