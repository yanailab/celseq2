#!/usr/bin/env python3
# coding: utf-8

'''
SAM file of one cell + GFF => UMI vector of the cell
'''
import HTSeq
from collections import defaultdict, Counter


def _umi_seq(name, length=6):
    ## BC-TCTGAG_UMI-CGTTAC => CGTTAC
    try:
        out = name.split('_')[1][4:4+length]
    except Exception as e:
        raise(e)
    return(out)


def count_umi(sam_fpath, features, len_umi=6, accept_aln_qual_min=10,
             is_gapped_aligner=False):
    '''
    Single SAM + GFF => UMI (saved in Python's Counter)
    '''
    umi_cnt = defaultdict(set)
    # aln_cnt = Counter()
    fh_aln = HTSeq.SAM_Reader(sam_fpath)
    i = 0
    for aln in fh_aln:
        i += 1
        if not aln.aligned:
            # aln_cnt["_unmapped"] += 1
            continue
        if aln.aQual < accept_aln_qual_min:
            # aln_cnt["_low_qual"] += 1
            continue
        try:
            if aln.optional_field( "NH" ) > 1:
                # aln_cnt['_multimapped'] += 1
                continue
        except KeyError:
            pass

        gene_ids = set()
        if is_gapped_aligner:
            for aln_part in aln.cigar:
                if aln_part.type != 'M':
                    continue
                for _, gene_id in features[aln_part.ref_iv].steps():
                    gene_ids |= gene_id
        else:
            for _, gene_id in features[aln.iv].steps():
                gene_ids |= gene_id
        ## union model        
        if len(gene_ids) == 1:
            gene_id = list(gene_ids)[0]
            # aln_cnt[gene_id] += 1
            umi_seq = _umi_seq(aln.read.name, len_umi)
            umi_cnt[gene_id].add(umi_seq)
        # elif len(gene_ids) == 0:
        #     aln_cnt["_no_feature"] += 1
        # else:
        #     aln_cnt["_ambiguous"] += 1 
    umi_vec = Counter({x : len(umi_cnt.get(x, set())) for x in umi_cnt})
    return(umi_vec)

