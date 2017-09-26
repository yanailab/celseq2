# Configuration

Specify global parameters of CEL-Seq2 and `celseq2`.

---

## Why configuration

Global configuration file has 3 purposes:

1. Tell `celseq2` how CEL-Seq2 is performed. For example, what are the sequences
   of the cell barcodes in use?
2. Specify bioinformatics details for `celseq2`. For example, what is the
   absolute path to the genome annotation on your computer?
3. Configuration file is *reusable* as long as both experimental and
   bioinformatics protocol are applied on same type of species.


## Example
Here is a [real
example](https://github.com/Puriney/celseq2/blob/master/example/config.yaml) of
global configuration file.

```yaml
###########################
## CEL-seq2 Tech Setting
###########################
BC_INDEX_FPATH: 'yanailab/refs/barcodes/barcodes_cel-seq_umis96.tab'
BC_IDs_DEFAULT: '1-96'
UMI_LENGTH: 6
BC_LENGTH: 6

###########################
## Bowties Index
###########################
BOWTIE2_INDEX_PREFIX: 'yanailab/refs/danio_rerio/danRer10_87/genome/Danio_rerio.GRCz10.dna.toplevel'
BOWTIE2: '/local/apps/bowtie2/2.3.1/bowtie2'

###########################
## Annotations
###########################
GFF: 'yanailab/refs/danio_rerio/danRer10_87/gtf/Danio_rerio.GRCz10.87.gtf.gz'

###########################
## Demultiplexing
###########################
FASTQ_QUAL_MIN_OF_BC: 10
CUT_LENGTH: 35

###########################
## Alignment
###########################
ALIGNER: 'bowtie2'

###########################
## UMI Count
###########################
ALN_QUAL_MIN: 0
```

## Explanations

- `BC_INDEX_FPATH`

Absolute file path to the space/tab separated file which saves all the sequences
for cell barcodes.

Here are first 11 lines of the content of
[`BC_INDEX_FPATH`](https://github.com/Puriney/celseq2/blob/master/example/barcodes_cel-seq_umis96.tab)

``` text
#barcode_id sequence
1   AGACTC
2   AGCTAG
3   AGCTCA
4   AGCTTC
5   CATGAG
6   CATGCA
7   CATGTC
8   CACTAG
9   CAGATC
10  TCACAG
```

- `UMI_LENGTH`, `BC_LENGTH`, `CUT_LENGTH`

CEL-Seq2 sequences in a pair-end manner. Read-1 records the sequences of UMI and
cell barcodes, while read-2 records the sequences of RNA transcripts. `celseq2`
will cut a subsequence with length of `CUT_LENGTH` since the left-most end of
read-2, which will be ready for alignment.
