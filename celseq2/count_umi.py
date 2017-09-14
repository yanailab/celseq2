#!/usr/bin/env python3
# coding: utf-8

'''
SAM file of one cell + GFF => UMI vector of the cell
'''
import HTSeq
import pickle
import argparse
from collections import defaultdict, Counter


def invert_strand(iv):
    # https://github.com/simon-anders/htseq/blob/78f955fc2007e5d861c54336095c383502086687/python3/HTSeq/scripts/count.py#L184-L190
    new_iv = iv.copy()
    if new_iv.strand == "+":
        new_iv.strand = "-"
    elif new_iv.strand == "-":
        new_iv.strand = "+"
    else:
        raise ValueError("Illegal strand")
    return new_iv


def _umi_seq(name, length=6):
    # BC-TCTGAG_UMI-CGTTAC => CGTTAC
    try:
        out = name.split('_')[1][4:4 + length]
    except Exception as e:
        raise(e)
    return(out)


def count_umi(sam_fpath, features, stranded='yes',
              len_umi=6, accept_aln_qual_min=10,
              dumpto=None):
    '''
    Single SAM + GFF => UMI (saved in Python's Counter)
    '''
    umi_cnt = defaultdict(set)
    aln_cnt = Counter()
    fh_aln = HTSeq.SAM_Reader(sam_fpath)
    if type(features) is str:
        with open(features, 'rb') as fh:
            features = pickle.load(fh)

    i = 0
    for aln in fh_aln:
        aln_cnt["_total"] += 1
        i += 1
        if not aln.aligned:
            aln_cnt["_unmapped"] += 1
            continue

        try:
            if aln.optional_field("NH") > 1:
                aln_cnt['_multimapped'] += 1
                continue
        except KeyError:
            pass

        if aln.aQual < accept_aln_qual_min:
            aln_cnt["_low_map_qual"] += 1
            continue

        if not (aln.iv.chrom in features.chrom_vectors):
            aln_cnt["_no_feature"] += 1
            continue

        gene_ids = set()

        for aln_part in aln.cigar:
            if aln_part.type != 'M':
                continue
            aln_ref_iv = invert_strand(
                aln_part.ref_iv) if stranded == 'reverse' else aln_part.ref_iv
            for _, gene_id in features[aln_ref_iv].steps():
                gene_ids |= gene_id

        # union model
        if len(gene_ids) == 1:
            gene_id = list(gene_ids)[0]
            aln_cnt["_uniquemapped"] += 1
            umi_seq = _umi_seq(aln.read.name, len_umi)
            umi_cnt[gene_id].add(umi_seq)
        elif len(gene_ids) == 0:
            aln_cnt["_no_feature"] += 1
        else:
            aln_cnt["_ambiguous"] += 1
    umi_vec = Counter({x: len(umi_cnt.get(x, set())) for x in umi_cnt})
    if dumpto:
        pickle.dump(umi_vec, open(dumpto, 'wb'))
    return((umi_vec, umi_cnt, aln_cnt))


def _flatten_umi_set(umi_set):
    umi_vec = Counter({x: len(umi_set.get(x, set())) for x in umi_set})
    return(umi_vec)

# def umi_matrix(sam_fpath, features, len_umi=6, accept_aln_qual_min=10,
#               is_gapped_aligner=False, dumpto=None):
#     pass


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--sam_fpath', type=str, metavar='FILENAME',
                        required=True,
                        help='File path to SAM file')
    parser.add_argument('--features', metavar='FILENAME.pickle|Counter',
                        required=True,
                        help=('Either file path (pickle format only) '
                              'or Python object in counter'))
    parser.add_argument('--stranded', metavar='VAL',
                        choices=['yes', 'reverse'],
                        default='yes',
                        help=('Either file path (pickle format only) '
                              'or Python object in counter'))
    parser.add_argument('--umi-length', type=int, metavar='N',
                        default=6,
                        help='Length of UMI (default=6)')
    parser.add_argument('--aln-qual-min', type=int, metavar='N',
                        default=10,
                        help='Acceptable min alignment quality (default=10)')
    # parser.add_argument('--is-gapped-aligner', dest='is_gapped_aligner', action='store_true')
    # parser.set_defaults(is_gapped_aligner=False)
    parser.add_argument('--dumpto', type=str, metavar='FILENAME', default=None,
                        help='File path to save umi count in pickle')
    args = parser.parse_args()

    _ = count_umi(sam_fpath=args.sam_fpath,
                  features=args.features,
                  len_umi=args.umi_length,
                  stranded=args.stranded,
                  accept_aln_qual_min=args.aln_qual_min,
                  dumpto=args.dumpto)
