"""
Generate dummy CEL-Seq2 sequencing pair-end reads.
Required inputs:
- GTF of transcriptome annotation
- FASTA of genome
- Cell barcodes dictionary
"""
import random
from collections import defaultdict
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


def transrev(x):
    trans = str.maketrans('ATGC', 'TACG')
    return(x.translate(trans)[::-1])


def get_seq(fasta, chrm, start, end, strand):
    if isinstance(fasta, str):
        fasta = pysam.FastaFile(fasta)
    raw_seq = fasta.fetch(chrm, start, end)
    if strand == '-':
        return(transrev(raw_seq))
    return(raw_seq)


def fastq_line(readname, readseq, readquality):
    assert len(readseq) == len(readquality), ('Read sequence and quality string'
                                              ' should be same.')
    out = '@{}\n{}\n{}\n{}'.format(readname, readseq, '+', readquality)
    return(out)


def dummy_readquality(length=None, min_qual=0, max_qual=40, readseq=None):
    '''
    Create read quality string with Q-score ranged in [<min_qual>, <max_qual>].
    Its length is defined by either <length> or same as <readseq>.
    Ref: https://support.illumina.com/help/BaseSpace_OLH_009008/Content/Source/Informatics/BS/QualityScoreEncoding_swBS.htm

    >>> dummy_readquality(length=41, min_qual=0, max_qual=40)
    ';",*?<E$2")5");7*9B!B=.\'H.$$C9B>6H07C:D8='
    >>> dummy_readquality()
    TypeError: dummy_readquality() missing 1 required positional argument: 'length'
    >>> dummy_readquality(min_qual=0, max_qual=0, readseq='ATGC')
    '!!!!'
    '''
    assert 0 <= min_qual <= max_qual <= 40, 'Q-score should be [0, 40].'
    if readseq:
        length = len(readseq)
    assert not length is None, 'Specify length.'
    random.seed(42)
    q_score = random.choices(range(min_qual, max_qual + 1, 1), k=length)
    seq = ''.join(map(lambda x: chr(x + 33), q_score))
    return(seq)


def umi_generator(nuc_base='ATGC', length=6):
    '''
    Create a generator to yield UMIs

    >>> g = umi_generator()
    >>> ''.join(next(g))
    'AAAAAA'
    '''
    return(itertools.product(nuc_base, repeat=length))


def dummy_CELSeq2(gtf, fasta, barcodes, savetor1, savetor2, len_tx=50):
    default_len_min_tx = 35
    default_qual_tx = 10

    fh_fa = pysam.FastaFile(fasta)

    fh1 = open(savetor1, 'w')
    fh2 = open(savetor2, 'w')

    gene = defaultdict(list)
    fh_gtf = HTSeq.GFF_Reader(gtf)
    for gtf in fh_gtf:
        if gtf.type == 'exon':
            gene[gtf.attr['gene_id'].strip()].append(gtf)
    for k, _ in gene.items():
        gene[k].sort(key=lambda x: int(x.attr['exon_num'].strip()))

    for bcid, bc in barcodes.items():
        for gene, exons in gene.items():
            umi_pool = umi_generator()
            # umi: within exons, good quality, good length
            read_start = random.randrange(exons.iv.start, exons.iv.end - len_tx)
            read_seq = get_seq(fasta, exons.iv.chrom,
                               read_start, read_start + len_tx,
                               exons.iv.strand)
            read_qual = dummy_readquality()
            # off-keyboard



if __name__ == '__main__':
    # p = get_argument_parser()
    # args = p.parse_args()

    # if args.test:
    #     import doctest
    #     doctest.testmod()
    # else:
    #     dummy_gtf(args.gtf)
    #     dummy_fasta(args.fasta)
    pass
