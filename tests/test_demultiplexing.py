import pytest
from celseq2.helper import md5sum

'''
Test demultiplexing.
Expectation is from the stats.log of demultiplexing.
'''

def test_demultiplexing(instance_demultiplex_stats):
    calc = md5sum(instance_demultiplex_stats)
    # e.g. 0027-GTGATC   18  003.333
    assert calc == '7ed86eb8520bc17bd3f91c1e136cf2b1'
