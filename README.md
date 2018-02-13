## Overview

This is `celseq2`, a Python framework for generating the UMI count matrix
from CEL-Seq2 [\*] sequencing data. We believe data digestion
should be automated, and it should be done in a manner not just computational
efficient, but also user-friendly and developer-friendly.

## Install `celseq2`

``` bash
git clone git@github.com:yanailab/celseq2.git
cd celseq2
pip install ./
```

## Quick Start

Running `celseq2` pipeline is as easy as 1-2-3. Below is the visualization of
the experiment design as same as the
[sample sheet](https://github.com/yanailab/CEL-Seq-pipeline/blob/133912cd4ceb20af0c67627ab883dfce8b9668df/sample_sheet_example.txt)
used in last generation of the pipeline ([CEL-Seq-pipeline](https://github.com/yanailab/CEL-Seq-pipeline)) as example.

![experiment-old-pipeline-visualize](https://i.imgur.com/ntJVTYM.gif)

The user had two biological samples which could come from two different
experiments, two time-points, two types of tissues, or even two labs. They were
denoted as squares and circles, respectively. Each sample had 9 cells.

In principle, what the user would expect as final output was one UMI count matrix
for each sample, which meant two UMI matrices in total in this example.

During the CEL-Seq2 experiment, all cells were placed in one 96-well cell plate.
They were labeled with same sequencing barcodes (shown as orange plate)
but each cell was labeled with its own CEL-Seq2 cell barcode, so that all of them
could be sequenced together without losing identities. In details, the
nine cells from Experiment-1 were labeled with CEL-Seq2 cell barcodes indexed
from 1 to 9, respectively, while the other nine cells from Experiment-2 were
labeled with cell barcodes 10 to 18.

Finally the library was distributed in two lanes (purple and dark gray bar) of a
sequencer, and got sequenced, which resulted in two sets of CEL-Seq2 data (per
lane per sequencing barcode).

What would the pipeline of `celseq2` do for the user was to generate UMI-count
matrix per experiment with the two sets of CEL-Seq2 data as input.

### Step-1: Specify Global Configuration of Workflow

Run `new-configuration-file` command to initiate configuration file (YAML
format), which specifies the details of CEL-Seq2 techniques the users perform,
e.g. the cell barcodes sequence dictionary, and transcriptome annotation
information for quantifying UMIs, etc.

This configuration can be shared and used more than once as long as user is
running pipeline on same species.

``` bash
new-configuration-file -o /path/to/wonderful_CEL-Seq2_config.yaml
```

Example of configuration is [here](https://github.com/yanailab/celseq2/blob/master/example/config.yaml).

Example of CEL-Seq2 cell barcodes sequence dictionary is [here](https://github.com/yanailab/celseq2/blob/master/example/barcodes_cel-seq_umis96.tab).

Read ["Setup Configuration"](https://yanailab.github.io/celseq2/user_guide/setup_config/)
for full instructions.

### Step-2: Define Experiment Table

Run `new-experiment-table` command to initiate a table (space/tab separated
file format) specifying the experiment layout.

``` bash
new-experiment-table -o /path/to/wonderful_experiment_table.txt
```

Fill information into the generated experiment table file row by row.

The content of experiment table in this example could be:

| SAMPLE_NAME               | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-----------------------    |---------------------  |-------------------------  |-------------------------  |
| wonderful_experiment1     | 1-9                   | path/to/lane1-R1.fastq.gz   | path/to/lane1-R2.fastq.gz   |
| wonderful_experiment2     | 10-18                 | path/to/lane1-R1.fastq.gz   | path/to/lane1-R2.fastq.gz   |
| wonderful_experiment1     | 1-9              | path/to/lane2-R1.fastq.gz   | path/to/lane2-R2.fastq.gz   |
| wonderful_experiment2     | 10-18                 | path/to/lane2-R1.fastq.gz | path/to/lane2-R2.fastq.gz   |

Read ["Experiment Table Specification"](https://yanailab.github.io/celseq2/user_guide/experiment_table/)
for full instructions when more complexed experiment designs take place.

### Step-3: Run Pipeline of `celseq2`

Launch pipeline in the computing node which performs 10 tasks in parallel.

``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    -j 10
```

Read ["Launch Pipeline"](https://yanailab.github.io/celseq2/user_guide/launch_pipeline/)
for full instructions to see how to submit jobs to cluster, or preview how many
tasks are going to be scheduled.

### Results

All the results are saved under <kbd>/path/to/result_dir</kbd> that user
specified, which has folder structure:

```
├── annotation
├── expr                  # <== Here saves all the UMI count matrices
├── input
├── small_diagnose
├── small_fq
├── small_log
├── small_sam
├── small_umi_count
└── small_umi_set
```

In particular, **UMI count matrix** for each of the experiments is
saved in both CSV and HDF5 format and exported to <kbd>expr/</kbd> folder.

```
expr/
├── wonderful_experiment1
│   ├── expr.csv          # <== UMI count matrix for cells denoted as squares
│   ├── expr.h5
│   ├── item-1
│   │   ├── expr.csv
│   │   └── expr.h5
│   └── item-3
│       ├── expr.csv
│       └── expr.h5
└── wonderful_experiment2
    ├── expr.csv          # <== UMI count matrix for cells denoted as circles
    ├── expr.h5
    ├── item-2
    │   ├── expr.csv
    │   └── expr.h5
    └── item-4
        ├── expr.csv
        └── expr.h5
```

Results of <kbd>item-X</kbd> are useful to assess technical variation when FASTQ
files from multiple lanes, or technical/biological replicates are present.

## About

Authors: See <https://github.com/yanailab/celseq2/blob/master/AUTHORS>

License: See <https://github.com/yanailab/celseq2/blob/master/LICENSE>

---

[\*] Hashimshony, T. et al. CEL-Seq2: sensitive highly-
multiplexed single-cell RNA-Seq. Genome Biol. 17, 77 (2016).
<https://doi.org/10.1186/s13059-016-0938-8>

