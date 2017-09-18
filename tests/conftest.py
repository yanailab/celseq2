import pytest
from celseq2.dummy_species import dummy_gtf, dummy_fasta
from celseq2.dummy_CELSeq2_reads import dummy_CELSeq2


@pytest.fixture(scope='function')
def instance_dummy_gtf(tmpdir_factory):
    fpath = tmpdir_factory.mktemp('dummy_species').join('dummy.gtf')
    dummy_gtf(fpath)
    print(fpath)
    return fpath


@pytest.fixture(scope='function')
def instance_dummy_fasta(tmpdir_factory):
    fpath = tmpdir_factory.mktemp('dummy_species').join('dummy.fasta')
    dummy_fasta(fpath)
    print(fpath)
    return fpath


@pytest.fixture(scope='session')
def instance_celseq2_data(tmpdir_factory):
    fdir = tmpdir_factory.mktemp('celseq2_data')
    gtf_fpath = fdir.join('dummy.gtf')
    fasta_fpath = fdir.join('dummy.fasta')
    r1_gz = fdir.join('celseq2.r1.fq.gz')
    r2_gz = fdir.join('celseq2.r2.fq.gz')
    dummy_gtf(gtf_fpath)
    dummy_fasta(fasta_fpath)
    _ = dummy_CELSeq2(str(gtf_fpath), str(fasta_fpath),
                      str(r1_gz), str(r2_gz),
                      len_tx=50, gzip=True)
    return (r1_gz, r2_gz)
