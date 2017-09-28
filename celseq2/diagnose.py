#!/usr/bin/env python3
import argparse
from celseq2 import filehandle_fastq_gz, print_logger
from collections import Counter


def get_dict_bc_has_reads(r1, bc_index, bc_seq_col):
    with open(bc_index, 'rt') as fin:
        next(fin)
        rows = map(lambda row: row.strip().split(), fin)
        known_bc = set([row[bc_seq_col] for row in rows])

    print_logger('There are {} different cell barcodes.'.format(len(known_bc)))

    res = Counter({bc: 0 for bc in known_bc})

    bc_len = len(next(iter(res)))
    fh_r1 = filehandle_fastq_gz(r1) if r1.endswith('.gz') else open(r1, 'r')
    i = 0
    while True:
        if i % 1000000 == 0:
            print_logger('Processing {:,} reads...'.format(i))
        try:
            _ = next(fh_r1).rstrip()
            r1_seq = next(fh_r1).rstrip()
            _ = next(fh_r1).rstrip()
            _ = next(fh_r1).rstrip()
            i += 1
            r1_bc = r1_seq[:bc_len]
            if not r1_bc:
                continue
            if r1_bc in known_bc:
                res[r1_bc] += 1
            else:
                res['unknown'] += 1

        except StopIteration:
            break

    fh_r1.close()
    return res


def get_argument_parser():
    desc = ('celseq2 diagnose')
    parser = argparse.ArgumentParser(
        description=desc,
        add_help=True)

    parser.add_argument(
        '--bc-index', metavar='FILE', type=str,
        help=('File path to cell barcode index.'))
    parser.add_argument(
        '--bc-seq-col', metavar='N', default=1, type=int,
        help=('Column index of cell barcode index file to find the sequence',
              ' of cell barcodes. Default: 1 (2nd column).'))
    parser.add_argument(
        '--r1', metavar='FILE', type=str,
        help=('File path to R1.'))

    return parser


def main():
    p = get_argument_parser()
    args = p.parse_args()

    if args.r1 and args.bc_index and args.bc_seq_col:
        counter_bc_size = get_dict_bc_has_reads(args.r1,
                                                args.bc_index,
                                                args.bc_seq_col)
    for bc in counter_bc_size:
        print('{:>{}}\t{:,}'.format(bc, len(bc), counter_bc_size[bc]))


if __name__ == '__main__':
    main()
