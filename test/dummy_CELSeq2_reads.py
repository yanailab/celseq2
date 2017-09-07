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


def dummy_read_name(is_PE=True):
    # @MN00336:10:000H23YMF:1:12102:15294:5115 1:N:0:CAGATC
    # @MN00336:10:000H23YMF:1:12102:15294:5115 2:N:0:CAGATC
    x = '@MN00336:{}:00CELSEQ2:1:{}:{}:{}'.format(
        random.choice(range(1, 10)),
        random.choice(range(1, 100000)),
        random.choice(range(1, 100000)))
    xx = '1:N:0:{}'.format()
    if is_PE:
        r1 = x + ' ' + xx
    return(r1)


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
    default_qual = 10

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

    rand_seed = 42
    for bcid, bc in barcodes.items():
        random.seed(rand_seed)
        r1_seq_fmt = '{umi}' + bc
        for gene, exons in gene.items():
            umi_pool = umi_generator()
            for exon in exons:
                umi_seq = ''.join(next(umi_pool))
                r1_seq = r1_seq_fmt.format(umi=umi_seq)
                r1_qual = dummy_readquality(readseq=r1_seq,
                                            min_qual=default_qual)
                for _ in range(3):
                    # umi - read within exons, good quality, good length
                    r2_start = random.randrange(
                        exon.iv.start, exon.iv.end - len_tx)
                    r2_seq = get_seq(fasta, exon.iv.chrom,
                                     r2_start, r2_start + len_tx,
                                     exon.iv.strand)
                    r2_qual = dummy_readquality(readseq=r2_seq,
                                                min_qual=default_qual)

                    r1 = fastq_line(readname='xxx',
                                    readseq=r1_seq, readquality=r1_qual)
                    r2 = fastq_line(readname='xxx',
                                    readseq=r2_seq, readquality=r2_qual)

                    fh1.write('{}\n'.format(r1))
                    fh2.write('{}\n'.format(r2))


        rand_seed += 1


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
