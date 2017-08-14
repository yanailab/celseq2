# Overview

This is `celseq2`, a Python package for generating the UMI count matrix
from **CEL-Seq2**[ref?] sequencing data.

# What is `celseq2`, actually?

1. A bioinformatics pipeline which is seamless, parallelized, and easily
extended to run on computing cluster. It reduces the burden of creating work
flow and speeds up data digestion.
2. A list of independent tools which are robust and computational efficient.
Pipeline is not always the need. Package `celseq2` provides a list of versatile
and stand-alone bash commands to address independent tasks, for example,
`count-umi` is able to quantify the UMIs present in the SAM/BAM file of single
cell.

# Dependencies

## Install Python 3 by conda

Visit <https://conda.io/miniconda.html> to find suitable scripts for your platform to install Python 3.

## Install `snakemake`

Visit <http://snakemake.readthedocs.io/en/stable/getting_started/installation.html> to intall `snakemake`.

```
conda install -c bioconda snakemake
```

# Install

``` bash
git clone git@gitlab.com:Puriney/celseq2.git
cd celseq2
pip install ./
```

# Quick Start

Running `celseq2` pipeline is easy as 1-2-3, and here is a quick start tutorial
based on an example. Suppose user performed CEL-Seq2 and got samples sequenced
in the way shown as figure below.

![experiment_example](http://i.imgur.com/kBOWcdl.png)

The user had two biological samples with 8 and 96 cells respectively, which could come
from two time-points or two tissues. To reduce the batch effect as much as
possible, the user could possibly add different Illumina sequencing barcodes
to the two plates (shown as blue and orange dots), mix them and subsequently get
samples sequenced together but in three lanes (shown as red, green and purple
rectangles). Finally, the sequencer would generate totally 6 FASTQ reads files.

By running the pipeline of `celseq2`, the users would get two types of UMI count
matrix:

- UMI count matrix per biological sample. Here 2 matrices in this example.
- UMI count matrix per lane per sample. Here 6 matrices in this example. This is
to allow assessment on reproducibility or possible batch effect.

## Step-1: Define Experiment Table

Run `new-experiment-table` command to initiate table file (space/tab separated
file) of the experiment design.

```bash
new-experiment-table -o /path/to/wonderful_experiment_table.txt
```

Fill information into the generated experiment table file.

:warning: Note: Column names cannot be changes at all.

:warning: Note: Each slot cannot contain any space.

The content of experiment table in this example could be:

| SAMPLE_NAME               | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-----------------------    |---------------------  |-------------------------  |-------------------------  |
| wonderful_experiment1     | 1,8,2-7               | path/to/x-1-r1.fastq.gz   | path/to/x-1-r2.fastq.gz   |
| wonderful_experiment1     | 1-8                   | path/to/x-3-r1.fastq.gz   | path/to/x-3-r2.fastq.gz   |
| wonderful_experiment1     | 8,7,6,5,4,3,2,1       | path/to/x-2-r1.fastq.gz   | path/to/x-2-r2.fastq.gz   |
| wonderful_experiment2     | 95-96,94-1,10         | path/to/y-2-r1.fastq.gz   | path/to/y-2-r2.fastq.gz   |
| wonderful_experiment2     | 1-96                  | path/to/y-1-r1.fastq.gz   | path/to/y-2-r2.fastq.gz   |
| wonderful_experiment2     | 1-96                  | path/to/y-3-r1.fastq.gz   | path/to/y-3-r2.fastq.gz   |

Each row records one pair of FASTQ reads.

To ease the pain of manually specifying `CELL_BARCODES_INDEX`, `celseq2`
recognizes human inputs in various way. Examples of specification of barcodes
indexed from 1 to 8 that present in experiment-1 are listed and are all allowed.

1. `1-8`: the most straightforward way.
2. `1,8,2-7` or `1,8,7-2`: combination of individual and range assignment.
3. `8,1,7-2,6`: redundancy is tolerant.


## Step-2: Specify Configuration of Workflow

Run `new-configuration-file` command to initiate configuration file
(YAML format) of CEL-Seq2.

```
new-configuration-file -o /path/to/wonderful_CEL-Seq2_config.yaml
```


## Step-3: Running `celseq2`


# Documents


