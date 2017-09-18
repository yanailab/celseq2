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
import argparse
import pysam
import HTSeq

from celseq2.helper import popen_communicate, base_name, dir_name, join_path


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
    prefix = '@MN00336:{}:00CELSEQ2:1:{}:{}:{}'.format(
        random.choice(range(1, 10)),
        random.choice(range(1, 100000)),
        random.choice(range(1, 100000)),
        random.choice(range(1, 1000)))
    suffix = '1:N:0:{}'.format('ATGCGC')
    name_r1 = prefix + ' ' + suffix
    if not is_PE:
        return((name_r1, None))
    suffix = '2' + suffix[1:]
    name_r2 = prefix + ' ' + suffix
    return((name_r1, name_r2))


def fastq_line(readname, readseq, readquality):
    assert len(readseq) == len(readquality), ('Read sequence and quality string'
                                              ' should be same.')
    out = '{}\n{}\n{}\n{}'.format(readname, readseq, '+', readquality)
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
    # random.seed(42)
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


def _remove_gz_suffix(x):
    xbasename = base_name(x)
    xdirname = dir_name(x)
    return join_path(xdirname, xbasename.replace('.gz', ''))


def dummy_CELSeq2(gtf, fasta, savetor1, savetor2, len_tx=50, gzip=True):
    default_len_min_tx = 35
    default_qual = 10

    barcodes = dummy_cell_barcodes()

    fh_fa = pysam.FastaFile(fasta)

    if gzip:
        savetor1 = _remove_gz_suffix(savetor1)
        savetor2 = _remove_gz_suffix(savetor2)

    fh1 = open(savetor1, 'w')
    fh2 = open(savetor2, 'w')

    gene_content = defaultdict(list)
    fh_gtf = HTSeq.GFF_Reader(gtf)
    for gtf in fh_gtf:
        if gtf.type == 'exon':
            gene_content[gtf.attr['gene_id'].strip()].append(gtf)
    for k, _ in gene_content.items():
        gene_content[k].sort(key=lambda x: int(x.attr['exon_number'].strip()))

    rand_seed = 42
    bc_read_coord = defaultdict(list)
    for bcid, bc in barcodes.items():
        rand_seed += 1
        random.seed(rand_seed)
        r1_seq_fmt = '{umi}' + bc
        for gene, exons in gene_content.items():
            # nuc_base = list('ATGC')
            # random.shuffle(nuc_base)
            # nuc_base = ''.join(nuc_base)
            umi_pool = umi_generator(nuc_base='ATGC', length=6)
            for exon in exons:
                umi_seq = ''.join(next(umi_pool))
                r1_seq = r1_seq_fmt.format(umi=umi_seq)
                r1_qual = dummy_readquality(readseq=r1_seq,
                                            min_qual=default_qual)
                for i in range(1):
                    # umi - read within exons, good quality, good length
                    # r2_start = random.randrange(
                    #     exon.iv.start, exon.iv.end - len_tx)
                    r2_start = exon.iv.start + i
                    r2_end = r2_start + len_tx
                    r2_seq = get_seq(fasta, exon.iv.chrom,
                                     r2_start, r2_end,
                                     exon.iv.strand)
                    r2_qual = dummy_readquality(readseq=r2_seq,
                                                min_qual=default_qual)

                    r1_name, r2_name = dummy_read_name()
                    r1 = fastq_line(readname=r1_name,
                                    readseq=r1_seq, readquality=r1_qual)
                    r2 = fastq_line(readname=r2_name,
                                    readseq=r2_seq, readquality=r2_qual)

                    fh1.write('{}\n'.format(r1))
                    fh2.write('{}\n'.format(r2))

                    expected_align = (exon.iv.chrom, r2_start, r2_end,
                                      exon.iv.strand)
                    bc_read_coord[bcid].append(expected_align)
    fh1.close()
    fh2.close()

    # gzip
    if gzip:
        # https://unix.stackexchange.com/a/31009
        # get rid of header of gzip
        _ = popen_communicate('gzip -n {} '.format(savetor1))
        _ = popen_communicate('gzip -n {} '.format(savetor2))

    return(bc_read_coord)


def get_argument_parser():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '--gtf',
        metavar="FILE",
        help='GTF file path.')
    parser.add_argument(
        '--fasta',
        metavar="FILE",
        help='FASTA file path.')

    parser.add_argument(
        '--savetor1',
        required=True, metavar="FILE",
        help='Save to R1 (UMI+BC)')
    parser.add_argument(
        '--savetor2',
        required=True, metavar="FILE",
        help='Save to R2 (transcript)')

    parser.add_argument(
        '--expected-alignment', '-ea',
        metavar='FILE',
        help='Save to expected alignment positions (bed6 format).')
    parser.add_argument(
        '--gzip',
        action='store_true', default=False,
        help='Gzip reads.fq to reads.fq.gz')

    parser.add_argument(
        '--test',
        action='store_true', default=False,
        help='Perform doctest only.')
    parser.add_argument(
        '--verbose', '-v',
        action='count', default=0,
        help='Verbose')
    return(parser)


def main():
    p = get_argument_parser()
    args = p.parse_args()

    if args.verbose >= 4:
        print(args)

    if args.test:
        import doctest
        doctest.testmod()
    else:
        out = dummy_CELSeq2(args.gtf, args.fasta,
                            args.savetor1, args.savetor2,
                            len_tx=50,
                            gzip=args.gzip)
        if not args.expected_alignment:
            return
        fhout = open(args.expected_alignment, 'w')
        bed6_fmt = '{chrom}\t{s}\t{e}\t{id}\t{score}\t{strand}'
        for bcname, reads in out.items():
            for i, read in enumerate(reads):
                bed_id = '{}_{}'.format(bcname, i + 1)
                bed_line = bed6_fmt.format(
                    chrom=read[0],
                    s=read[1],
                    e=read[2],
                    id=bed_id,
                    score=255,
                    strand=read[3])
                fhout.write('{}\n'.format(bed_line))
        fhout.close()


if __name__ == '__main__':
    main()
