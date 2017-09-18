import pytest
import HTSeq
from celseq2.helper import md5sum


def test_simulate_celseq2(instance_celseq2_data):
    r1_gz, r2_gz = instance_celseq2_data

    assert md5sum(r1_gz) == '2a633d13fa343211a02bea6a4e14183b'
    assert md5sum(r2_gz) == '97f490bf9929f1b64d7e0142ade72576'
