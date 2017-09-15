import pytest

from celseq2.dummy_species import dummy_gtf, dummy_fasta


@pytest.fixture(scope='session')
def instance_dummy_gtf():
    fpath = tmpdir_factory.mktemp('dummy_species').join('dummy.gtf')
    dummy_gtf(fpath)
    return fpath


@pytest.fixture(scope='session')
def instance_dummy_fasta():
    fpath = tmpdir_factory.mktemp('dummy_species').join('dummy.fasta')
    dummy_fasta(fpath)
    return fpath
