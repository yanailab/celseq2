import pytest
import pickle
from pkg_resources import resource_filename


def test_umi(instance_count_umi):
    ans_umi_cnt = resource_filename(
        'celseq2',
        'demo/{}'.format('BC-22-GTACTC.counter.pkl'))
    ans_umi_cnt = pickle.load(open(ans_umi_cnt, 'rb'))
    ans_umi_set = resource_filename(
        'celseq2',
        'demo/{}'.format('BC-22-GTACTC.set.pkl'))
    ans_umi_set = pickle.load(open(ans_umi_set, 'rb'))

    umi_cnt, umi_set = instance_count_umi

    assert umi_cnt == ans_umi_cnt
    # for calc, ans in zip(umi_set, ans_umi_set):
    #     assert c
    assert umi_set == ans_umi_set
