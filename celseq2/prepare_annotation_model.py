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
    parser = argparse.ArgumentParser()
    parser.add_argument('--gff-file', type=str, metavar='FILENAME',
                       help='File path to GFF')
    parser.add_argument('--feature-atrr', type=str, default='gene_id',
                       help='Reserved word for feature_atrr in GFF to be called a \'gene\'.')
    parser.add_argument('--feature-type', type=str, default='exon',
                       help='Reserved word for feature type in GFF to be the components of \'gene\'.')
    parser.add_argument('--strandless', dest='stranded', action='store_false')
    parser.set_defaults(stranded=True)
    parser.add_argument('--anno-store-fpath', type=str, metavar='FILENAME', default='annotation.pickle',
                       help='File path to save cooked annotation model')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()
    _ = cook_anno_model(gff_fpath=args.gff_file, 
                        feature_atrr=args.feature_atrr, 
                        feature_type=args.feature_type,
                        stranded=args.stranded,
                        anno_store_fpath=args.anno_store_fpath, 
                        verbose=args.verbose)
    
    
if __name__ == "__main__":
    main()    