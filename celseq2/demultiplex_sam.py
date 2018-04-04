#!/usr/bin/env python3

import pysam

import argparse

from celseq2.helper import print_logger
from celseq2.helper import join_path

def _cell_seq (name, length=6):
    # BC-TCTGAG_UMI-CGTTAC => TCTGAG
    try:
        out = name.split('_')[0][3:3 + length]
    except Exception as e:
        raise(e)
    return(out)


def demultiplex_sam (samfile, outdir, bc_length):
    if not samfile:
        return
    samobj = pysam.AlignmentFile(samfile, 'rb')
    dict_samout = {}

    for aln in samobj:
        bc = _cell_seq(aln.query_name, length=bc_length)
        fh = dict_samout.get(bc, None)
        if not fh:
            outsam = join_path(outdir, bc + '.sam1')
            fh = pysam.AlignmentFile(outsam, 'w', template=samobj)
            dict_samout[bc] = fh

        fh.write(aln)

    for _, fh in dict_samout.items():
        fh.close()


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--sbam', type=str, metavar='FILENAME',
                        help='File path to SAM/BAM file')
    parser.add_argument('--savetodir', type=str, metavar='DIRNAME',
                        help='Directory path to save the demultiplexed SAMs.',
                        default='.')
    parser.add_argument('--bc-length', type=int, metavar='N',
                        help='Length of cell barcode.', default=6)
    args = parser.parse_args()

    print_logger('Demultiplexing SAM/BAM starts {} ...'.format(args.sbam))
    demultiplex_sam(samfile=args.sbam, outdir=args.savetodir,
                    bc_length=args.bc_length)
    print_logger('Demultiplexing SAM/BAM ends. See: {}.'.format(args.savetodir))


if __name__ == "__main__":
    main()


