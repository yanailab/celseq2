This post aims to guide user to :
1. specify experiment table which is one of the required input files to run `celseq2`,
2. find right folder to get UMI count matrix.

Experiment table is used to translate the overall design of experiment to layout that `celseq2` understands. By doing so, it can recognize which groups of inputs are technical or biological replicates and subsequently create correct UMI count matrix.

## Example-1

:dart: In this example borrowed from post [Quick start](https://gitlab.com/Puriney/celseq2/wikis/Quick-Start), user will learn about what is **item** and the UMI count matrix created under **<kbd>item-#</kbd>** of <kbd>expr</kbd> result folder.

There are 2 pairs of read files in this set of experiment.

<img alt='experiment_2plates_1lane' src='http://i.imgur.com/Vi2cD6e.png' width=400>

:memo: In experiment table, each row is one pair of read file, and is interpreted as **item** by `celseq2`. The numbering of items is following the increasing order of rows inside experiment table.

| SAMPLE_NAME               | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-----------------------    |---------------------  |-------------------------  |-------------------------  |
| wonderful_experiment1     | 1,8,2-7               | path/to/sampleX-lane2-R1.fastq.gz   | path/to/sampleX-lane2-R2.fastq.gz   |
| wonderful_experiment2     | 1-96                  | path/to/sampleY-lane2-R1.fastq.gz   | path/to/sampleY-lane2-R2.fastq.gz   |

Each item is going to be demultiplexed to a list of CEL-Seq2 reads based on the list of claimed cell barcodes index. Subsequently the reads of single cells are aligned, and have UMI counted so each item has its own UMI count matrix saved.

Finally, `celseq2` digests the experiment table, groups, merges and counts the UMIs from different items but same experiment, which leads to count matrix per experiment.

```
expr/
├── wonderful_experiment1
│   ├── expr.csv           # <== UMI count matrix (CSV format) for experiment-1
│   ├── expr.h5
│   └── item-1
│       ├── expr.csv       # <== UMI count matrix (CSV format) for item-1
│       └── expr.h5
└── wonderful_experiment2
    ├── expr.csv
    ├── expr.h5
    └── item-2
        ├── expr.csv       # <== UMI count matrix (CSV format) for item-2
        └── expr.h5
```

In this example, UMI matrix of item-1 <kbd>expr/wonderful_experiment1/item-1/expr.csv</kbd> is same as the one of experiment-1 <kbd>expr/wonderful_experiment1/expr.csv</kbd>.

## Example-2

:dart: Example-2 is conceived on top of Example-1. Here users will know about how **technical replicates** are specified to `celseq2`. The two libraries of different experiments are mixed together but were sequenced in 3 lanes, which finally leads to 6 pairs of FASTQ files.

<img alt='multiple-lane' src='http://i.imgur.com/dwowlHb.png' width=400>


The content of experiment table in this example could be:


| SAMPLE_NAME               | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-----------------------    |---------------------  |-------------------------  |-------------------------  |
| wonderful_experiment1 :large_blue_diamond:     | 1,8,2-7               | path/to/x-1-r1.fastq.gz   | path/to/x-1-r2.fastq.gz   |
| wonderful_experiment1 :large_blue_diamond:     | 1-8                   | path/to/x-3-r1.fastq.gz   | path/to/x-3-r2.fastq.gz   |
| wonderful_experiment1 :large_blue_diamond:     | 8,7,6,5,4,3,2,1       | path/to/x-2-r1.fastq.gz   | path/to/x-2-r2.fastq.gz   |
| wonderful_experiment2 :large_orange_diamond:    | 95-96,94-1,10         | path/to/y-2-r1.fastq.gz   | path/to/y-2-r2.fastq.gz   |
| wonderful_experiment2 :large_orange_diamond:    | 1-96                  | path/to/y-1-r1.fastq.gz   | path/to/y-2-r2.fastq.gz   |
| wonderful_experiment2 :large_orange_diamond:     | 1-96                  | path/to/y-3-r1.fastq.gz   | path/to/y-3-r2.fastq.gz   |

:memo: Technical replicates within same experiment have same `SAMPLE_NAME`, so that `celseq2` groups replicates together to one experiment and generated UMI matrix for each experiment. Result structure is:

```
expr/
├── E1
│   ├── expr.csv
│   ├── expr.h5
│   ├── item-1
│   │   ├── expr.csv
│   │   └── expr.h5
│   ├── item-2
│   │   ├── expr.csv
│   │   └── expr.h5
│   └── item-3
│       ├── expr.csv
│       └── expr.h5
└── E2
    ├── expr.csv
    ├── expr.h5
    ├── item-4
    │   ├── expr.csv
    │   └── expr.h5
    ├── item-5
    │   ├── expr.csv
    │   └── expr.h5
    └── item-6
        ├── expr.csv
        └── expr.h5

```

:beers: As each item has its own UMI count matrix, user can assess the variations across technical replicates to possibly quantify batch effect. This is a new feature that the previous generation pipeline cannot do.

:memo: Furthermore, the concept of "lane" is not fixed in the experiment table. "Lane" could be any other type of techinical replicates. The flexibility allows user run `celseq2` on experiments with complexed design.

## Example-3

:dart: Example-3 is conceived on top of Example-2. Here user will learn about how to specify or claim **cell barcode** indexes present in each item, which brings flexibility to `celseq2`. Example-3 is also used to demonstrate self-consistency of `celseq2` (see [post](https://gitlab.com/Puriney/celseq2/wikis/Consistency:-self-consistency))

<img alt='multiple-lane-selective-cell' src='http://i.imgur.com/qUDbAI7.png' width=400>

- item-1: Cells indexed 1-6 of E1 are sequenced in Lane-1. Shown as dark blue dots.
- item-2: Cells indexed 7-9 of E1 are sequenced in Lane-2. Shown as blue dots.
- item-3: Cells indexed 10 of E1 are sequenced in Lane-3. Shown as light blue dots.
- item-4: Cells indexed 1-96 of E2 are sequenced in Lane-1. Shown as orange dots, and wider arrows.
- item-5: Cells indexed 1-13 of E2 are claimed present in Lane-2, though cells indexed 1-96 are all sequenced. Shown as orange dots.
- item-6: None of E2 are claimed present in Lane-3, though cells indexed 1-96 are all sequenced. Since nothing is claimed, this pair of FASTQ file is excluded in experiment table.

:memo: User will get 6 but specify 5 pairs of FASTQ files with claimed cell barcodes index to the experiment table:

| SAMPLE_NAME   | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-------------  |---------------------  |-------------------------  |-------------------------  |
| E1            | **1-3,6,4-5**             | S1_L001_R1.fastq.gz   | S1_L001_R2.fastq.gz   |
| E1            | **7,8,9**                 | S1_L002_R1.fastq.gz   | S1_L002_R2.fastq.gz   |
| E1            | **10**                    | S1_L003_R1.fastq.gz   | S1_L003_R2.fastq.gz   |
| E2            | **1-96**                  | S2_L001_R1.fastq.gz   | S2_L001_R2.fastq.gz   |
| E2            | **1-13**                  | S2_L002_R1.fastq.gz   | S2_L002_R2.fastq.gz   |


```
expr/
├── E1
│   ├── expr.csv             # <== matrix with 10 cells on columns
│   ├── expr.h5
│   ├── item-1
│   │   ├── expr.csv         # <== matrix with 6 cells on columns
│   │   └── expr.h5
│   ├── item-2
│   │   ├── expr.csv         # <== matrix with 3 cells on columns
│   │   └── expr.h5
│   └── item-3
│       ├── expr.csv         # <== matrix with 1 cells on columns
│       └── expr.h5
└── E2
    ├── expr.csv             # <== matrix with 96 cells on columns
    ├── expr.h5
    ├── item-4
    │   ├── expr.csv         # <== matrix with 96 cells on columns
    │   └── expr.h5
    └── item-5
        ├── expr.csv         # <== matrix with 13 cells on columns
        └── expr.h5
```

## Example-4
:dart: Example-4 will put experiment names, claimed cell barcodes, biological/technical replicates in one place, so here user will learn about how to specify experiment table of a more real experiment.

![Imgur](http://i.imgur.com/73StoL8.png)

Here the user has 2 experiments from two different time points. Each has 96 cells. To reduce
batch effect, 48 cells of each experiment are placed in one same 96-well plate, as shown as above diagram where squares and dots are from the two experiments. Two plates are added their own Illumina sequencing barcodes (shown as yellow and green background) and finally get sequenced in multiple lanes to create 4 pairs of FASTQ files to user.

:memo: The source of each well is possible to be traced back based on cell barcodes per lane per plate. The experiment table is specified as below:

| SAMPLE_NAME   | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-------------  |---------------------  |-------------------------  |-------------------------  |
| E1 :white_medium_square:            | 1-48                  | S1_L001_R1.fastq.gz   | S1_L001_R2.fastq.gz   |
| E2  :white_circle:          | 49-96                 | S1_L001_R1.fastq.gz   | S1_L001_R2.fastq.gz   |
| E1 :white_medium_square:            | 1-48                  | S1_L002_R1.fastq.gz   | S1_L002_R2.fastq.gz   |
| E2  :white_circle:          | 49-96                 | S1_L002_R1.fastq.gz   | S1_L002_R2.fastq.gz   |
| E1 :white_medium_square:            | 49-96                 | S2_L001_R1.fastq.gz   | S2_L001_R2.fastq.gz   |
| E2     :white_circle:       | 1-48                  | S2_L001_R1.fastq.gz       | S2_L001_R2.fastq.gz       |
| E1 :white_medium_square:           | 49-96                 | S2_L002_R1.fastq.gz   | S2_L002_R2.fastq.gz   |
| E2 :white_circle:           | 1-48                  | S2_L002_R1.fastq.gz   | S2_L002_R2.fastq.gz   |

Results structure is:

```
expr/
├── E1
│   ├── expr.csv             # <== matrix with cells (1-96) on columns
│   ├── expr.h5
│   ├── item-1
│   │   ├── expr.csv         # <== matrix with cells (1-48) on columns
│   │   └── expr.h5
│   ├── item-3
│   │   ├── expr.csv         # <== matrix with cells (1-48) on columns
│   │   └── expr.h5
│   ├── item-5
│   │   ├── expr.csv         # <== matrix with cells (49-96) on columns
│   │   └── expr.h5
│   └── item-7
│       ├── expr.csv         # <== matrix with cells (49-96) on columns
│       └── expr.h5
└── E2
    ├── expr.csv             # <== matrix with cells (1-96) on columns
    ├── expr.h5
    ├── item-2
    │   ├── expr.csv         # <== matrix with cells (49-96) on columns
    │   └── expr.h5
    ├── item-4
    │   ├── expr.csv         # <== matrix with cells (49-96) on columns
    │   └── expr.h5
    ├── item-6
    │   ├── expr.csv         # <== matrix with cells (1-48) on columns
    │   └── expr.h5
    └── item-8
        ├── expr.csv         # <== matrix with cells (1-48) on columns
        └── expr.h5


```