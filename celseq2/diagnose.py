#!/usr/bin/env python3
import argparse
from .helper import print_logger
from .helper import filehandle_fastq_gz
from collections import Counter


def get_dict_bc_has_reads(r1, bc_index, bc_seq_col):
    print(r1)
    with open(bc_index, 'rt') as fin:
        # next(fin)
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
    print_logger('Processed total {:,} reads...'.format(i))
    fh_r1.close()
    return res


def main():
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        '--bc-index', metavar='FILENAME', type=str,
        help=('File path to cell barcode index.'))
    parser.add_argument(
        '--bc-seq-col', metavar='N', default=1, type=int,
        help=('Column index of cell barcode index file to find the sequence',
              ' of cell barcodes. Default: 1 (2nd column).'))
    parser.add_argument(
        '--r1', metavar='FILENAME', type=str,
        help=('File path to R1.'))
    parser.add_argument(
        '-o', '--output',
        metavar='FILENAME', type=str,
        required=True,
        help=('File path save output log.'))

    args = parser.parse_args()

    if args.r1 and args.bc_index:
        counter_bc_size = get_dict_bc_has_reads(args.r1,
                                                args.bc_index,
                                                args.bc_seq_col)
        fhout = open(args.output, 'w')
        tot = sum([counter_bc_size[x] for x in counter_bc_size])
        bc_size_max, bc_size_min = float('-inf'), float('inf')

        for bc in counter_bc_size:
            if bc != 'unknown' and counter_bc_size[bc] > bc_size_max:
                bc_size_max = counter_bc_size[bc]
            if bc != 'unknown' and counter_bc_size[bc] < bc_size_min:
                bc_size_min = counter_bc_size[bc]
            fhout.write('{:>{}}\t{:,}\t{:06.2f}\n'.format(
                bc, 20,
                counter_bc_size[bc], counter_bc_size[bc] * 100 / tot))

        valid_bc_size_val = [counter_bc_size[x]
                             for x in counter_bc_size if x != 'unknown']
        bc_size_avg = sum([x / len(valid_bc_size_val)
                           for x in valid_bc_size_val])
        fhout.write('{:>{}}\t{:,}\t{:06.2f}\n'.format(
            'bc_size_max', 20,
            bc_size_max, bc_size_max * 100 / tot))
        fhout.write('{:>{}}\t{:,}\t{:06.2f}\n'.format(
            'bc_size_min', 20,
            bc_size_min, bc_size_min * 100 / tot))
        fhout.write('{:>{}}\t{:06.2f}\t{:06.2f}\n'.format(
            'bc_size_avg', 20,
            bc_size_avg, bc_size_avg * 100 / tot))
        fhout.write('{:>{}}\t{:,}\t{:06.2f}\n'.format(
            'total', 20,
            tot, tot * 100 / tot))

        fhout.close()


if __name__ == '__main__':
    main()
