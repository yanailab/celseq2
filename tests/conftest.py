import pytest
from celseq2.dummy_species import dummy_gtf, dummy_fasta
from celseq2.dummy_CELSeq2_reads import dummy_CELSeq2
from celseq2.dummy_CELSeq2_reads import dummy_cell_barcodes
from celseq2.demultiplex import demultiplexing, write_demultiplexing
from celseq2.prepare_annotation_model import cook_anno_model
from celseq2.count_umi import count_umi, _flatten_umi_set

from pkg_resources import resource_filename


@pytest.fixture(scope='session')
def instance_dummy_gtf(tmpdir_factory):
    fpath = tmpdir_factory.mktemp('dummy_species').join('dummy.gtf')
    dummy_gtf(fpath)
    print(fpath)
    return fpath


@pytest.fixture(scope='session')
def instance_dummy_fasta(tmpdir_factory):
    fpath = tmpdir_factory.mktemp('dummy_species').join('dummy.fasta')
    dummy_fasta(fpath)
    print(fpath)
    return fpath


@pytest.fixture(scope='session')
def instance_celseq2_data(tmpdir_factory,
                          instance_dummy_gtf,
                          instance_dummy_fasta):
    fdir = tmpdir_factory.mktemp('celseq2_data')
    gtf_fpath = instance_dummy_gtf  # fdir.join('dummy.gtf')
    fasta_fpath = instance_dummy_fasta  # fdir.join('dummy.fasta')
    r1_gz = fdir.join('celseq2.r1.fq.gz')
    r2_gz = fdir.join('celseq2.r2.fq.gz')
    # dummy_gtf(gtf_fpath)
    # dummy_fasta(fasta_fpath)
    _ = dummy_CELSeq2(str(gtf_fpath), str(fasta_fpath),
                      str(r1_gz), str(r2_gz),
                      len_tx=50, gzip=True)
    return (r1_gz, r2_gz)


@pytest.fixture(scope='session')
def instance_demultiplex_stats(tmpdir_factory, instance_celseq2_data):
    fdir = tmpdir_factory.mktemp('small_fq')
    r1_gz, r2_gz = instance_celseq2_data
    dict_bc_id2seq = dummy_cell_barcodes()
    sample_counter = demultiplexing(
        read1_fpath=str(r1_gz),
        read2_fpath=str(r2_gz),
        outdir=fdir,
        dict_bc_id2seq=dict_bc_id2seq,
        start_umi=0,
        start_bc=6,
        len_umi=6,
        len_bc=6,
        len_tx=35,
        bc_qual_min=10,
        is_gzip=True)
    stats_fpath = fdir.join('demultiplexing.log')
    write_demultiplexing(sample_counter, dict_bc_id2seq, stats_fpath)
    return stats_fpath


@pytest.fixture(scope='session')
def instance_features(tmpdir_factory, instance_dummy_gtf):
    fdir = tmpdir_factory.mktemp('annotation')
    fpath = fdir.join('annotation.pkl')
    features, all_genes = cook_anno_model(str(instance_dummy_gtf),
                                          feature_atrr='gene_id',
                                          feature_type='exon',
                                          stranded=True,
                                          dumpto=str(fpath), verbose=False)
    return features


@pytest.fixture(scope='session')
def instance_count_umi(instance_features):
    sam = resource_filename('celseq2',
                            'demo/{}'.format('BC-22-GTACTC.sam'))
    umi_cnt, umi_set, aln_cnt = count_umi(sam,
                                          instance_features,
                                          len_umi=6, stranded='yes',
                                          accept_aln_qual_min=0, dumpto=None)
    return (umi_cnt, umi_set)
