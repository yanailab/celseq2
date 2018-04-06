#!/usr/bin/env python3

import pysam

import argparse

from celseq2.helper import print_logger
from celseq2.helper import join_path
from celseq2.demultiplex import bc_dict_id2seq, str2int


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
            outsam = join_path(outdir, bc + '.sam')
            fh = pysam.AlignmentFile(outsam, 'w', template=samobj)
            dict_samout[bc] = fh

        fh.write(aln)

    for _, fh in dict_samout.items():
        fh.close()


def demultiplex_sam_with_claim (samfile, outdir, bc_length, claimed_bc):
    if not samfile:
        return
    if not claimed_bc:
        return

    samobj = pysam.AlignmentFile(samfile, 'rb')

    dict_samout = {}
    for bc in claimed_bc:
        fh = pysam.AlignmentFile(
            join_path(outdir, bc + '.sam'),
            'w', template=samobj)
        dict_samout[bc] = fh

    for aln in samobj:
        bc = _cell_seq(aln.query_name, length=bc_length)
        fh = dict_samout.get(bc, None)
        if not fh:
            continue
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
    parser.add_argument('--claim', action='store_true', dest='claim')
    parser.set_defaults(claim=False)
    parser.add_argument('--bc-index', type=str, metavar='FILENAME',
                        help='File path to barcode dictionary.')
    parser.add_argument('--bc-seq-column', type=int, metavar='N',
                        default=0,
                        help=('Column of cell barcode dictionary file '
                              'which tells the actual sequences.'))
    parser.add_argument('--bc-index-used', type=str, metavar='string',
                        default='1-96',
                        help='Index of used barcode IDs (default=1-96)')

    args = parser.parse_args()

    print_logger('Demultiplexing SAM/BAM starts {} ...'.format(args.sbam))
    if args.claim:
        all_bc_dict = bc_dict_id2seq(args.bc_index, args.bc_seq_column)
        bc_index_used = str2int(args.bc_index_used)
        bc_seq_used = [all_bc_dict.get(x, None) for x in bc_index_used]
        demultiplex_sam_with_claim(
            samfile=args.sbam,
            outdir=args.savetodir,
            bc_length=args.bc_length,
            claimed_bc=bc_seq_used)
    else:
        demultiplex_sam(
            samfile=args.sbam,
            outdir=args.savetodir,
            bc_length=args.bc_length)

    print_logger('Demultiplexing SAM/BAM ends. See: {}'.format(args.savetodir))


if __name__ == "__main__":
    main()


