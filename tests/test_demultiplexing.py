import pytest
from celseq2.helper import md5sum

'''
Test demultiplexing.
Expectation is from the stats.log of demultiplexing.
'''

def test_demultiplexing(instance_demultiplex_stats):
    calc = md5sum(instance_demultiplex_stats)
    assert calc == 'a402efb27ac74bf3441fcd60c809d9c3'
