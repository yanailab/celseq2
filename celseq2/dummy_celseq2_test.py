#!/usr/bin/env python3
import argparse
from pkg_resources import resource_filename
from celseq2.helper import md5sum

'''
Final UMI expression matrix should be same as the demo/expr.csv
'''


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '-i', '--input',
        metavar='FILENAME', required=True,
        help='UMI-count matrix (expr.csv) of dummy CEL-Seq2 data.')
    args = parser.parse_args()

    expected_csv = resource_filename('celseq2', 'demo/{}'.format('expr.csv'))
    assert md5sum(args.input) == md5sum(expected_csv)


if __name__ == '__main__':
    main()
