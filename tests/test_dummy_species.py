import pytest
from celseq2.helper import md5sum


def test_dummy_gtf(instance_dummy_gtf):
    calc = md5sum(instance_dummy_gtf)
    assert calc == '3e2a544354a222e381636999587fb7dd',
    'Dummy GTF is not as expected.'


def test_dummy_fasta(instance_dummy_fasta):
    calc = md5sum(instance_dummy_fasta)
    assert calc == 'fe7e821e07b95b1ef4e7700d700ceb6b',
    'Dummy FASTA is not as expected.'
