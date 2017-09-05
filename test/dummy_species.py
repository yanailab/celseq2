'''
Create genome.fasta and annotation.gtf for dummy species.

There are totally 9 genes present.

Exon and intron length is fixed at 100bp and 200bp, respectively,
and inter-genic region is 300bp.

Gene_Name   Strand  #_of_transcripts    #_of_exons
g1  -   1   3
g2  -   2   3
g3  +   1   2
g4  +   1   2
g5  -   1   1
g6  +   1   2
g7  +   1   1
g8  +   1   2
g9  +   1   2

'''


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
        fout.writer('{}\n'.format(exon))
        out.append(exon)
        s_stream = e_stream + 1 + len_intron

    tx_attr = gtf_attr_str(gene_id='g2', gene_name='celseq_gene-2',
                           transcript_id='tx2.2')
    tx = gtf_str(chrm='chr1', src=src,
                 feature='transcript',
                 start=e_stream - 1.5 * len_exon,
                 end=e_stream + 1.5 * len_exon,
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
                   start=e_stream - 1.5 * len_exon,
                   end=e_stream + 1.5 * len_exon,
                   score=score,
                   strand='-',
                   frame=frame,
                   attr=exon_attr)
    fout.write('{}\n'.format(exon))
    out.append(exon)

    s_stream = e_stream + 1 + len_intergenic
    # g3, todo
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

    # g4

    # g5

    # g6

    # g7

    # g8

    # g9


if __name__ == '__main__':
    import doctest
    doctest.testmod()
