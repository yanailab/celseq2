#!/usr/bin/env bash
#$ -S /usr/bin/bash
#$ -wd /ifs/home/yy1533/Lab/cel-seq-pipe/qsub
#$ -M yun.yan@nyumc.org
#$ -m abe
#$ -j y
#$ -l h_vmem=30G
#$ -l mem_token=30G
#$ -N BC_Y

# cd /ifs/home/yy1533/Lab/cel-seq-pipe/src/celseq

# source activate py27
# python --version

bc_index_fpath='/ifs/data/yanailab/refs/barcodes/barcodes_cel-seq_umis96.tab'
r1_fpath='/ifs/home/yy1533/Lab/cel-seq-pipe/demo/data/7_S1_L001_R1_001.fastq.gz'
r2_fpath='/ifs/home/yy1533/Lab/cel-seq-pipe/demo/data/7_S1_L001_R2_001.fastq.gz'
outdir='/ifs/home/yy1533/Lab/cel-seq-pipe/demo/bc_split_YY'

mkdir $outdir
cd $outdir

date
# python barcode.py \
bc_demultiplex \
$r1_fpath \
$r2_fpath \
--bc_index $bc_index_fpath \
--min-bc-quality 10 \
--umi-length 6 \
--bc-length 6 \
--cut-length 35 \
--out-dir $outdir \
--is-gzip \
--verbose

date


