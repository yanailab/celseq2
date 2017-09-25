This post aims to demonstrate **self-consistency** of `celseq2`, the new pipeline:

- UMI count matrix of single one pair of read files is self-consistent regardless of different runs.
- UMI count matrix of multiple pairs of read files is self-consistent regardless of different runs.

## Data and experiment design

Suppose two plates were available, named E1 and E2, and were linked to different Illumina sequencing barcodes shown in blue and orange.

<img src='http://i.imgur.com/qUDbAI7.png' width=450 alt='self-consistency-multi'>

- item-1: Cells indexed 1-6 of E1 were sequenced in Lane-1
- item-2: Cells indexed 7-9 of E1 were sequenced in Lane-2
- item-3: Cells indexed 10 of E1 were sequenced in Lane-3
- item-4: Cells indexed 1-96 of E2 were sequenced in Lane-1
- item-5: Cells indexed 1-13 of E2 were claimed present, though cells indexed 1-96 were all sequenced in Lane-2.

Further suppose the sequencer reported reads file per lane per Illumina sequencing barcode. Accordingly, the experiment table for `celseq2` pipeline was defined as:

| SAMPLE_NAME   | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-------------  |---------------------  |-------------------------  |-------------------------  |
| E1            | 1-3,6,4-5             | S1_L001_R1_001.fastq.gz   | S1_L001_R2_001.fastq.gz   |
| E1            | 7,8,9                 | S1_L002_R1_001.fastq.gz   | S1_L002_R2_001.fastq.gz   |
| E1            | 10                    | S1_L003_R1_001.fastq.gz   | S1_L003_R2_001.fastq.gz   |
| E2            | 1-96                  | S2_L001_R1_001.fastq.gz   | S2_L001_R2_001.fastq.gz   |
| E2            | 1-13                  | S2_L002_R1_001.fastq.gz   | S2_L002_R2_001.fastq.gz   |

In order to create such an arbitrary set of complexed experiments, actual raw data was just one set of CEL-Seq2 sequencing read FASTQ files (40 million pairs of reads), but was duplicated to 5 pairs. In other words, all the reads listed in `R1` column were same, so was the `R2` list.

## How to validate self-consistency

UMI count matrices were generated in <kbd>expr</kbd>.
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
    └── item-5
        ├── expr.csv
        └── expr.h5
```
By examining the following comparisons, the self-consistency can be proved.

- E2-item5 v.s. E2-item4 on cells 1-13: self-consistency with **one** pair of read files
- E1 v.s. E2 on cells 1-10: self-consistency with **multiple** pairs of read files

## Self-consistency was validated

:white_check_mark: Test script [manual_test_expr_consistency.R](https://gitlab.com/Puriney/celseq2/blob/master/test/consistent2legacy/manual_test_expr_consistency.R) quantified the difference among the intact matrices. It ended up as zero which led to validation of self-consistency.

Furthermore, the heatmap on UMI count matrices where 200 randomly selected genes were rows and cells were columns would greatly help visualize the consistency.

### Self-consistency: E2-item5 v.s. E2-item4

<img src='http://i.imgur.com/hoaTQjn.png' width=450>

*Comparison E2-item5 v.s. E2-item4, focusing on cells 1-13, demonstrated self-consistency when one pair of read files was input. Rows were 200 randomly selected genes, and columns were all available cells. Left panel is cells 1-13 in E2-item5, middle panel is cells 1-13 in E2-item4, and right panel is rest of cells in E2-item4.*

### Self-consistency: E1 v.s. E2

<img src="http://i.imgur.com/WcFserh.png" width=450>

*Comparison E1 v.s. E2, focusing on cells 1-10, demonstrated self-consistency when one pair of reads was input. Rows were 200 randomly selected genes, and columns were all available cells. Left panel is cells 1-10 in E1, middle panel is cells 1-10 in E2, and right panel is rest of cells in E2.*