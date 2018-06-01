#!/usr/bin/env python3
# coding: utf-8
from collections import Counter

import argparse

from celseq2.helper import filehandle_fastq_gz, print_logger
from celseq2.helper import join_path, mkfolder, base_name

import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd


def str2int(s):
    """
    str('1-3,6,89-90,67') => [1,2,3,6,67,89,90]
    """
    intervals = list(map(lambda x: x.strip().split('-'),
                         s.strip().split(',')))
    out = []
    for x in intervals:
        try:
            p, q = map(int, x)
        except ValueError:
            out += [int(x[0])]
            continue
        if p > q:
            p, q = q, p
        out += list(range(p, q + 1))
    return(sorted(list(set(out))))


def bc_dict_seq2id(bc_index_fpath, col_seq=None):
    """ dict[barcode_seq] = barcode_id """
    if col_seq is None:
        col_seq = 0
    out = dict()
    with open(bc_index_fpath, 'rt') as fin:
        # next(fin)  # remove header
        # out = list(map(lambda row: row.strip().split(), fin))
        # out = {row[1]: int(row[0]) for row in out}
        row_num = 1
        for row in fin:
            if row.startswith('#'):
                continue
            row = row.strip().split()
            # print('{}:{}'.format(row_num, row))
            row_val = row[col_seq]
            row_key = row_num
            out[row_key] = row_val
            row_num += 1
    return(out)


def bc_dict_id2seq(bc_index_fpath, col_seq=None):
    """ dict[barcode_id] =  barcode_seq"""
    if col_seq is None:
        col_seq = 0
    out = dict()
    with open(bc_index_fpath, 'rt') as fin:
        # next(fin)  # remove header
        # out = map(lambda row: row.strip().split(), fin)
        # out = {int(row[0]): row[1] for row in out}
        row_num = 1
        for row in fin:
            if row.startswith('#'):
                continue
            row = row.strip().split()
            # print('{}:{}'.format(row_num, row))
            row_val = row[col_seq]
            row_key = row_num
            out[row_key] = row_val
            row_num += 1
    return(out)


def demultiplexing(read1_fpath, read2_fpath, dict_bc_id2seq,
                   outdir,
                   start_umi=0, start_bc=6,
                   len_umi=6, len_bc=6, len_tx=35,
                   bc_qual_min=10,
                   is_gzip=True,
                   save_unknown_bc_fastq=False,
                   tagging_only=False,
                   do_bc_rev_complement=False,
                   do_tx_rev_complement=False,
                   verbose=False):
    """
    Demultiplexing to fastq files based on barcode sequence.


    """
    if is_gzip:
        fh_umibc = filehandle_fastq_gz(read1_fpath)
        fh_tx = filehandle_fastq_gz(read2_fpath)
    else:
        fh_umibc = open(read1_fpath, 'rt')
        fh_tx = open(read2_fpath, 'rt')

    sample_counter = Counter()

    bc_fhout = dict()
    for bc_id, bc_seq in dict_bc_id2seq.items():
        # bc_id = '[{}]'.format('-'.join(map(str, bc_id)))
        bc_fhout[bc_seq] = join_path(outdir,
                                     'BC-{}-{}.fastq'.format(bc_id, bc_seq))
    mkfolder(join_path(outdir, 'UNKNOWN'))
    bc_fhout['UNKNOWNBC_R1'] = join_path(outdir, 'UNKNOWN',
                                         'UNKNOWNBC_R1.fq')
    bc_fhout['UNKNOWNBC_R2'] = join_path(outdir, 'UNKNOWN',
                                         'UNKNOWNBC_R2.fq')

    if tagging_only:
        out_fpath_tagged_fq = join_path(outdir, 'tagged.fastq')
        out_fh_tagged_fq = open(out_fpath_tagged_fq, 'w')

    for bc_seq, v in bc_fhout.items():
        if bc_seq.startswith('UNKNOWN'):
            bc_fhout[bc_seq] = open(v, 'w')
            continue
        if tagging_only:
            bc_fhout[bc_seq] = out_fh_tagged_fq
        else:
            bc_fhout[bc_seq] = open(v, 'w')

    i = 0
    while(True):
        if verbose and i % 1000000 == 0:
            print_logger('Processing {:,} reads...'.format(i))
        try:
            umibc_name = next(fh_umibc).rstrip()
            umibc_seq = next(fh_umibc).rstrip()
            next(fh_umibc)
            umibc_qualstr = next(fh_umibc).rstrip()
            tx_name = next(fh_tx).rstrip()
            tx_seq = next(fh_tx).rstrip()
            next(fh_tx)
            tx_qualstr = next(fh_tx).rstrip()
            i += 1
        except StopIteration:
            break

#         Quality check? or user should feed good files
#         if not (umibc_name and umibc_seq and umibc_qualstr and tx_name and tx_seq and tx_qualstr):
#             raise Exception('FastQError: Possible Broken Fastq. Check pair-{}.\n'.format(i+1))
#         if len(umibc_seq) != len(umibc_qualstr) or len(tx_seq) != len(tx_qualstr):
#             raise Exception('FastQError: Possible multi-line Fastq. Convert to 4-line please.\n')
#         if umibc_name.split()[0] != tx_name.split()[0]:
#             raise Exception('FastQError: Reads are not paired at pair-{}.\n'.format(i+1))

        sample_counter['total'] += 1

        umibc_idx = sorted(list(set(range(start_umi, start_umi + len_umi)) |
                                set(range(start_bc, start_bc + len_bc))))

        if len(umibc_seq) < len(umibc_idx):
            continue

        umibc_min_qual = min((ord(umibc_qualstr[i]) - 33 for i in umibc_idx))

        if umibc_min_qual < bc_qual_min:
            continue

        sample_counter['qualified'] += 1

        umi = umibc_seq[start_umi:(start_umi + len_umi)]
        cell_bc = umibc_seq[start_bc:(start_bc + len_bc)]
        try:
            fhout = bc_fhout[cell_bc]
        except KeyError:
            if save_unknown_bc_fastq:
                fhout = bc_fhout['UNKNOWNBC_R1']
                fhout.write('{}\n{}\n{}\n{}\n'.format(umibc_name, umibc_seq,
                                                      "+", umibc_qualstr))
                fhout = bc_fhout['UNKNOWNBC_R2']
                fhout.write('{}\n{}\n{}\n{}\n'.format(tx_name, tx_seq,
                                                      "+", tx_qualstr))
            sample_counter['unknown'] += 1
            continue

#         if len(tx_seq) < len_tx:
#             continue
        if len(tx_seq) > len_tx:
            tx_seq, tx_qualstr = tx_seq[:len_tx], tx_qualstr[:len_tx]
        read_name = '@BC-{}_UMI-{}'.format(cell_bc, umi)
        fhout.write('{}\n{}\n{}\n{}\n'.format(read_name, tx_seq,
                                              "+", tx_qualstr))
        sample_counter[cell_bc] += 1
        sample_counter['saved'] += 1

    sample_counter['unqualified'] = sample_counter['total'] - \
        sample_counter['qualified']
    for _, v in bc_fhout.items():
        v.close()
    fh_umibc.close()
    fh_tx.close()

    return(sample_counter)


def write_demultiplexing(stats, dict_bc_id2seq, stats_fpath):
    if stats_fpath is None:
        stats_fpath = 'demultiplexing.csv'
    try:
        fh_stats = open(stats_fpath, 'w')
    except Exception as e:
        raise Exception(e)
    fh_stats.write('BC,Reads(#),Reads(%)\n')

    for bc_id, bc_seq in dict_bc_id2seq.items():
        # bc_id = '[{:04d}]'.format('-'.join(map(str, bc_id)))
        formatter = '{:04d}-{},{},{:07.3f}\n'
        fh_stats.write(formatter.format(bc_id, bc_seq, stats[bc_seq],
                                        stats[bc_seq] / stats['total'] * 100))

    formatter = '{},{},{:07.3f}\n'
    fh_stats.write(formatter.format('saved', stats['saved'],
                                    stats['saved'] / stats['total'] * 100))
    fh_stats.write(formatter.format('unknown', stats['unknown'],
                                    stats['unknown'] / stats['total'] * 100))
    fh_stats.write(formatter.format('qualified', stats['qualified'],
                                    stats['qualified'] / stats['total'] * 100))
    fh_stats.write(formatter.format('unqualified', stats['unqualified'],
                                    stats['unqualified'] / stats['total'] * 100))
    fh_stats.write(formatter.format('total', stats['total'],
                                    stats['total'] / stats['total'] * 100))


def plotly_demultiplexing_stats(fpaths=[], saveto='', fnames=[]):
    '''
    Save a plotly box graph with a list of demultiplexing stats files

    Parameters
    ----------
    fpaths : list
        A list of file paths
    saveto : str
        File path to save the html file as the plotly box graph
    fnames : list
        A list of strings to label each ``fpaths``

    Returns
    -------
    bool
        True if saving successfully, False otherwise
    '''

    if not fnames:
        fnames = [base_name(f) for f in fpaths]
    if len(fnames) != len(fpaths):
        fnames = [base_name(f) for f in fpaths]

    num_reads_data = []
    for i in range(len(fpaths)):
        f = fpaths[i]
        fname = fnames[i]

        stats = pd.read_csv(f, index_col=0)
        cell_stats = stats.iloc[:-5, :]
        # tail 5 lines are fixed as the overall stats
        overall_stats = stats.iloc[-5:, :]
        num_reads_data.append(
            go.Box(
                y=cell_stats['Reads(#)'],
                name='{} (#Saved={}/#Total={})'.format(
                    fname,
                    overall_stats.loc['saved', 'Reads(#)'],
                    overall_stats.loc['total', 'Reads(#)'])))

    layout = go.Layout(
        # legend=dict(x=-.1, y=-.2),
        xaxis=dict(showticklabels=False),
        title='Number of reads saved per BC per item')
    fig = go.Figure(data=num_reads_data, layout=layout)
    try:
        plot(fig, filename=saveto, auto_open=False)
        return(True)
    except Exception as e:
        print(e, flush=True)
        return(False)


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('read1_fpath', type=str)
    parser.add_argument('read2_fpath', type=str)
    parser.add_argument('--bc-index', type=str, metavar='FILENAME',
                        help='File path to barcode dictionary')
    parser.add_argument('--bc-seq-column', type=int, metavar='N',
                        default=0,
                        help=('Column of cell barcode dictionary file '
                              'which tells the actual sequences.'))
    parser.add_argument('--bc-index-used', type=str, metavar='string',
                        default='1-96',
                        help='Index of used barcode IDs (default=1-96)')
    parser.add_argument('--min-bc-quality', metavar='N', type=int, default=10,
                        help='Minimal quality for barcode reads (default=10)')
    parser.add_argument('--out-dir', metavar='DIRNAME', type=str, default='.',
                        help='Output directory. Defaults to current directory')
    parser.add_argument('--is-gzip', dest='is_gzip', action='store_true')
    parser.add_argument('--not-gzip', dest='is_gzip', action='store_false')
    parser.set_defaults(is_gzip=True)
    parser.add_argument('--stats-file', metavar='STATFILE',
                        type=str, default='demultiplexing.log',
                        help='Statistics (default: demultiplexing.log)')
    parser.add_argument('--umi-start-position',
                        metavar='N', type=int, default=0,
                        help=('Start index of UMI on R1. '
                              'Default: 0. (0-based).'))
    parser.add_argument('--umi-length', metavar='N', type=int, default=6,
                        help='Length of UMI (default=6)')
    parser.add_argument('--bc-start-position',
                        metavar='N', type=int, default=6,
                        help=('Start index of cell barcode on R1. '
                              'Default: 6. (0-based).'))
    parser.add_argument('--bc-length', metavar='N', type=int, default=6,
                        help='Length of CELSeq barcode (default=6)')
    parser.add_argument('--cut-length', metavar='N', type=int, default=35,
                        help='Length of read on R2 to be mapped. (default=35)')
    parser.add_argument('--save-unknown-bc-fastq',
                        dest='save_unknown_bc_fastq', action='store_true')
    parser.set_defaults(save_unknown_bc_fastq=False)
    parser.add_argument('--tagging-only',
                        dest='tagging_only', action='store_true',
                        help=('Demultiplexed reads are merged to a file named'
                              ' \"tagged.fastq\" under --out-dir.'))
    parser.set_defaults(tagging_only=False)
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)

    args = parser.parse_args()

    bc_dict = bc_dict_id2seq(args.bc_index, args.bc_seq_column)

    bc_index_used = str2int(args.bc_index_used)
    bc_dict = {x: bc_dict.get(x, None) for x in bc_index_used}

    print_logger('Demultiplexing starts {}--{} ...'.format(args.read1_fpath,
                                                           args.read2_fpath))
    out = demultiplexing(read1_fpath=args.read1_fpath,
                         read2_fpath=args.read2_fpath,
                         outdir=args.out_dir, dict_bc_id2seq=bc_dict,
                         start_umi=args.umi_start_position,
                         start_bc=args.bc_start_position,
                         len_umi=args.umi_length,
                         len_bc=args.bc_length,
                         len_tx=args.cut_length,
                         bc_qual_min=args.min_bc_quality,
                         is_gzip=args.is_gzip,
                         save_unknown_bc_fastq=args.save_unknown_bc_fastq,
                         tagging_only=args.tagging_only,
                         do_bc_rev_complement=False,
                         do_tx_rev_complement=False,
                         verbose=args.verbose)
    print_logger('Demultiplexing ends {}--{}.'.format(args.read1_fpath,
                                                      args.read2_fpath))
    write_demultiplexing(out, bc_dict, args.stats_file)


if __name__ == "__main__":
    main()
