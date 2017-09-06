"""
Generate dummy CEL-Seq2 sequencing pair-end reads.
Required inputs:
- GTF of transcriptome annotation
- FASTA of genome
- Cell barcodes dictionary
"""

import itertools
import pysam
import HTSeq


def dummy_cell_barcodes():
    '''
    Returns a dict(id) -> barcode_seq
    '''
    raw_dict = {
        1: 'AGACTC',
        2: 'AGCTAG',
        3: 'AGCTCA',
        4: 'AGCTTC',
        5: 'CATGAG',
        6: 'CATGCA',
        7: 'CATGTC',
        8: 'CACTAG',
        9: 'CAGATC',
        10: 'TCACAG',
        11: 'AGGATC',
        12: 'AGTGCA',
        13: 'AGTGTC',
        14: 'TCCTAG',
        15: 'TCTGAG',
        16: 'TCTGCA',
        17: 'TCGAAG',
        18: 'TCGACA',
        19: 'TCGATC',
        20: 'GTACAG',
        21: 'GTACCA',
        22: 'GTACTC',
        23: 'GTCTAG',
        24: 'GTCTCA',
        25: 'GTTGCA',
        26: 'GTGACA',
        27: 'GTGATC',
        28: 'ACAGTG',
        29: 'ACCATG',
        30: 'ACTCTG'}
    return(raw_dict)


def umi_generator(nuc_base='ATGC', length=6):
    return(itertools.product(nuc_base, repeat=length))


def transrev(x):
    trans = str.maketrans('ATGC', 'TACG')
    return(x.translate(trans)[::-1])


def get_seq(fasta, chrm, start, end, strand):
    if type(fasta) is str:
        fasta = pysam.Fastafile(fasta)
    raw_seq = fasta.fetch(chrm, start, end)
    if strand == '-':
        return(transrev(raw_seq))
    return(raw_seq)


def fastq_line(readname, readseq, readquality):
    out = '@{}\n{}\n{}\n{}'.format(readname, readseq, '+', readquality)
    return(out)


def dummy_CELSeq2(gtf, fasta, barcodes, savetor1, savetor2, len_tx=50):
    for bcid, bc in barcodes.items():
        umi_pool = umi_generator()
        f1 = open(savetor1, 'w')
        f2 = open(savetor2, 'w')
        f3 = 'x'
