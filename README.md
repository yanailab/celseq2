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
based on an arbitrary example. Suppose user performed CEL-Seq2 and got samples
designed in the way shown as figure below.

![experiment_2plates_1lane](http://i.imgur.com/Vi2cD6e.png)

The user had two biological samples with 8 and 96 cells respectively, which could come
from two time-points, two tissues, or even two labs. Samples were marked with
two different Illumina sequencing barcodes (blue and orange dots), mixed
together, and subsequently sequenced in the same lane, which finally resulted
to 2 FASTQ files.

By running the pipeline of `celseq2` with the them, the users would get
UMI count matrix for each of the two plates.

## Step-1: Define Experiment Table

Run `new-experiment-table` command to initiate table file (space/tab separated
file) to specify the experiment layout.

``` bash
new-experiment-table -o /path/to/wonderful_experiment_table.txt
```

Fill information into the generated experiment table file.

:warning: Note: Column names cannot be changes at all.

:warning: Note: Each slot cannot contain any space.

The content of experiment table in this example could be:

| SAMPLE_NAME               | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-----------------------    |---------------------  |-------------------------  |-------------------------  |
| wonderful_experiment1     | 1,8,2-7               | path/to/x-1-r1.fastq.gz   | path/to/x-1-r2.fastq.gz   |
| wonderful_experiment2     | 1-96                  | path/to/y-1-r1.fastq.gz   | path/to/y-2-r2.fastq.gz   |

Each row records one pair of FASTQ reads.

To ease the pain of manually specifying `CELL_BARCODES_INDEX`, `celseq2`
recognizes human inputs in various way. Examples of specification of barcodes
indexed from 1 to 8 that present in experiment-1 are listed and are all allowed.

1. `1-8`: the most straightforward way.
2. `1,8,2-7` or `1,8,7-2`: combination of individual and range assignment.
3. `8,1,7-2,6`: redundancy is tolerant.


## Step-2: Specify Configuration of Workflow

Run `new-configuration-file` command to initiate configuration file (YAML
format) which specify the details of CEL-Seq2 techniques the users perform.

``` bash
new-configuration-file -o /path/to/wonderful_CEL-Seq2_config.yaml
```

Example of configuration is [here](https://gitlab.com/Puriney/celseq2/blob/master/example/config.yaml).


## Step-3: Run Pipeline of `celseq2`

Examine how many tasks to be performed before actually executing the pipeline:

``` bash
celseq2 --configfile /path/to/wonderful_CEL-Seq2_config.yaml --dryrun
```

Run pipeline:

``` bash
celseq2 --configfile /path/to/wonderful_CEL-Seq2_config.yaml
```

Alternatively, it is straightforward to run the pipeline of `celseq2` by
submitting jobs to cluster, as `celseq2` is built on top of `snakemake` which is
a powerful workflow management framework. For example, in login node on server,
user could run the following command to submit jobs to computing nodes. Here it
submits 10 jobs in parallel with total maximum memory 50G requested.

``` bash
celseq2 --configfile /path/to/wonderful_CEL-Seq2_config.yaml \
    -j 10 \
    --cluster "qsub -cwd -j y -l h_vmem=50G" &
```

# Documents

