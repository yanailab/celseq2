#!/usr/bin/env python3
# coding: utf-8
import HTSeq
import argparse
import pickle

from celseq2.helper import print_logger

def cook_anno_model(gff_fpath, feature_atrr='gene_id', feature_type='exon',
                    stranded=True,
                    anno_store_fpath=None, verbose=False):
    features = HTSeq.GenomicArrayOfSets("auto", stranded=stranded)
    fh_gff = HTSeq.GFF_Reader(gff_fpath)
    if verbose: i=0
    for gff in fh_gff:            
        if gff.type != feature_type:
            continue
        features[gff.iv] += gff.attr[feature_atrr]
        if verbose and i % 100000 == 0:
            print_logger('Processing {:,} lines of GFF...'.format(i))
        if verbose: i+=1
    if anno_store_fpath:
        pickle.dump(features, open(anno_store_fpath, 'wb'))
    return(features)
    
    
def main():
    # gff_fpath='/ifs/data/yanailab/refs/danio_rerio/danRer10_87/gtf/Danio_rerio.GRCz10.87.gtf.gz'
    pass
    
    
if __name__ == "__main__":
    main()    