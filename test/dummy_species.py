'''
Create genome.fasta and annotation.gtf for dummy species.

There are totally 9 genes present.

Exon and intron length is fixed at 100bp and 200bp, respectively,
and inter-genic region is 300bp.

'''
import random
import argparse


def gtf_attr_str(gene_id=None, gene_name=None,
                 transcript_id=None, exon_num=None):
    '''
    Simple writer to fill 'attribute' column of GTF

    >>> gtf_attr_str()
    >>> gtf_attr_str('g1', 'dummy_gene_1', 'g1_tx1', 1)
    'gene_id "g1"; gene_name "dummy_gene_1"; transcript_id "g1_tx1"; exon_number "1";'
    >>> gtf_attr_str('g1', 'dummy_gene_1')
    'gene_id "g1"; gene_name "dummy_gene_1";'
    '''
    if not gene_id or not gene_name:
        return(None)
    out = "gene_id \"{gid}\"; gene_name \"{gname}\";".format(gid=gene_id,
                                                             gname=gene_name)
    if transcript_id:
        out += " transcript_id \"{txid}\";".format(txid=transcript_id)
    if exon_num:
        out += " exon_number \"{exidx}\";".format(exidx=exon_num)
    return(out)


def gtf_str(chrm, src, feature, start, end, score, strand, frame, attr):
    '''
    Formatter to write single GTF line.
    '''
    out = ('{chrm}\t{src}\t{feature}\t{start}\t{end}\t{score}\t'
           '{strand}\t{frame}\t{attr}').format(chrm=chrm,
                                               src=src,
                                               feature=feature,
                                               start=start,
                                               end=end,
                                               score=score,
                                               strand=strand,
                                               frame=frame,
                                               attr=attr)
    return(out)


def dummy_gtf(saveto=None, len_exon=100, len_intron=200, len_intergenic=300):
    '''
    Create dummy GTF annations.
    '''
    fout = open(saveto, 'wt')
    s_stream, e_stream = 1, 1

    src = 'celseq2'
    score = '.'
    frame = '.'
    out = []
    # g0
    g_attr = gtf_attr_str(gene_id='g0', gene_name='celseq2_gene-0')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                score=score,
                strand='+',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g0', gene_name='celseq_gene-0',
                           transcript_id='tx0')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                 score=score,
                 strand='+',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(2):
        exon_attr = gtf_attr_str(gene_id='g0', gene_name='celseq_gene-0',
                                 transcript_id='tx0', exon_num=i + 1)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr1', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='+',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    s_stream, e_stream = e_stream - 2 * len_exon - 1 * len_intron + 1, e_stream
    # g8
    g_attr = gtf_attr_str(gene_id='g8', gene_name='celseq2_gene-8')
    g = gtf_str(chrm='chr2', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                score=score,
                strand='+',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g8', gene_name='celseq_gene-8',
                           transcript_id='tx8')
    tx = gtf_str(chrm='chr2', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                 score=score,
                 strand='+',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(2):
        exon_attr = gtf_attr_str(gene_id='g8', gene_name='celseq_gene-8',
                                 transcript_id='tx8', exon_num=i + 1)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr2', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='+',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    s_stream = e_stream + 1 + len_intergenic
    # g1
    g_attr = gtf_attr_str(gene_id='g1', gene_name='celseq2_gene-1')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 3 * len_exon + 2 * len_intron - 1,
                score=score,
                strand='-',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g1', gene_name='celseq_gene-1',
                           transcript_id='tx1')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 3 * len_exon + 2 * len_intron - 1,
                 score=score,
                 strand='-',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(3, 0, -1):
        exon_attr = gtf_attr_str(gene_id='g1', gene_name='celseq_gene-1',
                                 transcript_id='tx1', exon_num=i)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr1', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='-',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    s_stream = e_stream + 1 + len_intergenic
    # g2
    g_attr = gtf_attr_str(gene_id='g2', gene_name='celseq2_gene-2')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                score=score,
                strand='-',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g2', gene_name='celseq_gene-2',
                           transcript_id='tx2.1')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                 score=score,
                 strand='-',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(2, 0, -1):
        exon_attr = gtf_attr_str(gene_id='g2', gene_name='celseq_gene-2',
                                 transcript_id='tx2', exon_num=i)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr1', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='-',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    tx_attr = gtf_attr_str(gene_id='g2', gene_name='celseq_gene-2',
                           transcript_id='tx2.2')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=int(e_stream - 1.5 * len_exon),
                 end=int(e_stream + 1.5 * len_exon),
                 score=score,
                 strand='-',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    exon_attr = gtf_attr_str(gene_id='g2', gene_name='celseq_gene-2',
                             transcript_id='tx2.2', exon_num=1)
    exon = gtf_str(chrm='chr1', src=src,
                   feature='exon',
                   start=int(e_stream - 1.5 * len_exon),
                   end=int(e_stream + 1.5 * len_exon),
                   score=score,
                   strand='-',
                   frame=frame,
                   attr=exon_attr)
    fout.write('{}\n'.format(exon))
    out.append(exon)

    s_stream = e_stream + 1 + len_intergenic
    # g3
    g_attr = gtf_attr_str(gene_id='g3', gene_name='celseq2_gene-3')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                score=score,
                strand='+',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g3', gene_name='celseq_gene-3',
                           transcript_id='tx3')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                 score=score,
                 strand='+',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(2):
        exon_attr = gtf_attr_str(gene_id='g3', gene_name='celseq_gene-3',
                                 transcript_id='tx3', exon_num=i + 1)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr1', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='+',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    s_stream = e_stream + 1 + len_intergenic

    # g4
    g_attr = gtf_attr_str(gene_id='g4', gene_name='celseq2_gene-4')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                score=score,
                strand='+',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g4', gene_name='celseq_gene-4',
                           transcript_id='tx4')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                 score=score,
                 strand='+',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(2):
        exon_attr = gtf_attr_str(gene_id='g4', gene_name='celseq_gene-4',
                                 transcript_id='tx4', exon_num=i + 1)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr1', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='+',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    # g5
    s_stream, e_stream = e_stream - len_exon + 1, e_stream
    g_attr = gtf_attr_str(gene_id='g5', gene_name='celseq2_gene-5')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=e_stream,
                score=score,
                strand='-',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g5', gene_name='celseq_gene-5',
                           transcript_id='tx5')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=e_stream,
                 score=score,
                 strand='-',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(1, 0, -1):
        exon_attr = gtf_attr_str(gene_id='g5', gene_name='celseq_gene-5',
                                 transcript_id='tx5', exon_num=i)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr1', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='-',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    s_stream = e_stream + 1 + len_intergenic
    # g6
    g_attr = gtf_attr_str(gene_id='g6', gene_name='celseq2_gene-6')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 1 * len_exon + 0 * len_intron - 1,
                score=score,
                strand='+',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g6', gene_name='celseq_gene-6',
                           transcript_id='tx6')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 1 * len_exon + 0 * len_intron - 1,
                 score=score,
                 strand='+',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    exon_attr = gtf_attr_str(gene_id='g6', gene_name='celseq_gene-6',
                             transcript_id='tx6', exon_num=1)
    exon = gtf_str(chrm='chr1', src=src,
                   feature='exon',
                   start=s_stream,
                   end=s_stream + 1 * len_exon + 0 * len_intron - 1,
                   score=score,
                   strand='+',
                   frame=frame,
                   attr=exon_attr)
    fout.write('{}\n'.format(exon))
    out.append(exon)
    # g7
    g_attr = gtf_attr_str(gene_id='g7', gene_name='celseq2_gene-7')
    g = gtf_str(chrm='chr1', src=src,
                feature='gene',
                start=s_stream,
                end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                score=score,
                strand='+',
                frame=frame,
                attr=g_attr)
    fout.write('{}\n'.format(g))
    out.append(g)
    tx_attr = gtf_attr_str(gene_id='g7', gene_name='celseq_gene-7',
                           transcript_id='tx7')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=s_stream,
                 end=s_stream + 2 * len_exon + 1 * len_intron - 1,
                 score=score,
                 strand='+',
                 frame=frame,
                 attr=tx_attr)
    fout.write('{}\n'.format(tx))
    out.append(tx)
    for i in range(2):
        exon_attr = gtf_attr_str(gene_id='g7', gene_name='celseq_gene-7',
                                 transcript_id='tx7', exon_num=i + 1)
        s_stream, e_stream = s_stream, s_stream + len_exon - 1
        exon = gtf_str(chrm='chr1', src=src,
                       feature='exon',
                       start=s_stream,
                       end=e_stream,
                       score=score,
                       strand='+',
                       frame=frame,
                       attr=exon_attr)
        fout.write('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    e_total = e_stream
    print('End of chr1 is {}'.format(e_total))
    fout.close()
    return(out)


def dummy_fasta(saveto, max_len=5000):
    '''
    Generate FASTA
    chr1: total length 5K
    chr2: same as very first 500bp
    '''
    fasta = ['A'] * int(max_len * 0.25) + \
        ['T'] * int(max_len * 0.25) + \
        ['G'] * int(max_len * 0.25) + \
        ['C'] * int(max_len * 0.25)

    random.seed(42)
    random.shuffle(fasta)
    chr1 = fasta
    chr2 = fasta[:500]
    wrap_len = 60
    with open(saveto, 'w') as fout:
        fout.write('>chr1\n')
        for i in range(0, len(chr1), wrap_len):
            j = i + wrap_len if i + wrap_len < len(chr1) else len(chr1)
            fout.write('{}\n'.format(
                ''.join(chr1[i:j])))
        fout.write('>chr2\n')
        for i in range(0, len(chr2), wrap_len):
            j = i + wrap_len if i + wrap_len < len(chr2) else len(chr2)
            fout.write('{}\n'.format(
                ''.join(chr2[i:j])))


def get_argument_parser():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '--gtf',
        metavar="FILE",
        help='Save dummy GTF to file.')
    parser.add_argument(
        '--fasta',
        metavar="FILE",
        help='Save dummy FASTA to file.')
    parser.add_argument(
        '--test',
        action='store_true', default=False,
        help='Perform doctest only.')
    return(parser)


if __name__ == '__main__':
    p = get_argument_parser()
    args = p.parse_args()

    if args.test:
        import doctest
        doctest.testmod()
    else:
        dummy_gtf(args.gtf)
        dummy_fasta(args.fasta)
