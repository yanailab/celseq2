# User Experience

We believe data digestion should be automated, and it should be done in an
user-friendly manner :key:.

---

## Easy to setup

In addition to installation, the setup of bioinformatics pipeline is another stop
that every user has to endure before launching the beautiful data analysis
journey. In context of processing CEL-Seq2 data, the setup means
telling pipeline where to find the aligner index files to align reads, where to
find the genome annotation for quantification, and what is the length of UMI or
cell barcodes, etc. These are required information to perform data digestion.

Instead of having users specify them over and over again when launching pipeline,
we aimed to bring an user experience where the setup needs done for once and
once only. This is the motivation behind configuration file, and we believe it
should be reusable for fixed type of species.

See ["Configuration"](../user_guide/setup_config.md) for details.

In addition, here is an utility tool named
[`MrY`](https://github.com/Puriney/MrY). It aimed to download and manage all the
genome FASTA files, annotations (GTF/GFF) and furthermore create aligner index
(Bowtie2 and STAR) in a painless way.

## Easy to handle complexed experiment

We aimed to design an intuitive way for users to specify the experiments
despite of its complexed layout.

A space/tab separated file called "Experiment table" is our solution. Each row
specifies a set of CEL-Seq2 data. Filling blanks of each row by following a
simple rule stated as below:

> For input reads file *X*, claim that cells with barcode indexes from *i* to *j*
come from experiment *Y*.

Take the experiment in ["Quick Start"](../index.md#quick-start) for example,
`CEL-Seq-pipeline` required a ["sample
sheet"](https://github.com/yanailab/CEL-Seq-
pipeline/blob/133912cd4ceb20af0c67627ab883dfce8b9668df/sample_sheet_example.txt)
with 36 lines to define the  experiment layout.

| #id   | flocell       | series    | lane  | il_barcode    | cel_barcode   | project   |
|-----  |-----------    |--------   |------ |------------   |-------------  |---------  |
| 1     | C5BW1ACXX     | CE_TC     | L005  | 4             | 1             | CE_1_1    |
| 2     | C5BW1ACXX     | CE_TC     | L005  | 4             | 2             | CE_1_2    |
| 3     | C5BW1ACXX     | CE_TC     | L005  | 4             | 3             | CE_1_3    |
| 4     | C5BW1ACXX     | CE_TC     | L005  | 4             | 4             | CE_1_4    |
| 5     | C5BW1ACXX     | CE_TC     | L005  | 4             | 5             | CE_1_5    |
| 6     | C5BW1ACXX     | CE_TC     | L005  | 4             | 6             | CE_1_6    |
| 7     | C5BW1ACXX     | CE_TC     | L005  | 4             | 7             | CE_1_7    |
| 8     | C5BW1ACXX     | CE_TC     | L005  | 4             | 8             | CE_1_8    |
| 9     | C5BW1ACXX     | CE_TC     | L005  | 4             | 9             | CE_1_9    |
| 1     | C5BW1ACXX     | CE_TC     | L008  | 4             | 1             | CE_1_1    |
| 2     | C5BW1ACXX     | CE_TC     | L008  | 4             | 2             | CE_1_2    |
| 3     | C5BW1ACXX     | CE_TC     | L008  | 4             | 3             | CE_1_3    |
| 4     | C5BW1ACXX     | CE_TC     | L008  | 4             | 4             | CE_1_4    |
| 5     | C5BW1ACXX     | CE_TC     | L008  | 4             | 5             | CE_1_5    |
| 6     | C5BW1ACXX     | CE_TC     | L008  | 4             | 6             | CE_1_6    |
| 7     | C5BW1ACXX     | CE_TC     | L008  | 4             | 7             | CE_1_7    |
| 8     | C5BW1ACXX     | CE_TC     | L008  | 4             | 8             | CE_1_8    |
| 9     | C5BW1ACXX     | CE_TC     | L008  | 4             | 9             | CE_1_9    |
| 10    | C5BW1ACXX     | CE_TC     | L005  | 4             | 10            | CE_2_1    |
| 11    | C5BW1ACXX     | CE_TC     | L005  | 4             | 11            | CE_2_2    |
| 12    | C5BW1ACXX     | CE_TC     | L005  | 4             | 12            | CE_2_3    |
| 13    | C5BW1ACXX     | CE_TC     | L005  | 4             | 13            | CE_2_4    |
| 14    | C5BW1ACXX     | CE_TC     | L005  | 4             | 14            | CE_2_5    |
| 15    | C5BW1ACXX     | CE_TC     | L005  | 4             | 15            | CE_2_6    |
| 16    | C5BW1ACXX     | CE_TC     | L005  | 4             | 16            | CE_2_7    |
| 17    | C5BW1ACXX     | CE_TC     | L005  | 4             | 17            | CE_2_8    |
| 18    | C5BW1ACXX     | CE_TC     | L005  | 4             | 18            | CE_2_9    |
| 10    | C5BW1ACXX     | CE_TC     | L008  | 4             | 10            | CE_2_1    |
| 11    | C5BW1ACXX     | CE_TC     | L008  | 4             | 11            | CE_2_2    |
| 12    | C5BW1ACXX     | CE_TC     | L008  | 4             | 12            | CE_2_3    |
| 13    | C5BW1ACXX     | CE_TC     | L008  | 4             | 13            | CE_2_4    |
| 14    | C5BW1ACXX     | CE_TC     | L008  | 4             | 14            | CE_2_5    |
| 15    | C5BW1ACXX     | CE_TC     | L008  | 4             | 15            | CE_2_6    |
| 16    | C5BW1ACXX     | CE_TC     | L008  | 4             | 16            | CE_2_7    |
| 17    | C5BW1ACXX     | CE_TC     | L008  | 4             | 17            | CE_2_8    |
| 18    | C5BW1ACXX     | CE_TC     | L008  | 4             | 18            | CE_2_9    |


On the contrary, user will find it only takes `celseq2` 4 lines to do the same,
and done in much more intuitive manner.

| SAMPLE_NAME               | CELL_BARCODES_INDEX   | R1                        | R2                        |
|-----------------------    |---------------------  |-------------------------  |-------------------------  |
| CE_1     | 1-9                   | path/to/lane5-R1.fastq.gz   | path/to/lane5-R2.fastq.gz   |
| CE_2     | 10-18                 | path/to/lane5-R1.fastq.gz   | path/to/lane5-R2.fastq.gz   |
| CE_1     | 1-9              | path/to/lane8-R1.fastq.gz   | path/to/lane8-R2.fastq.gz   |
| CE_2     | 10-18                 | path/to/lane8-R1.fastq.gz | path/to/lane8-R2.fastq.gz   |


See ["Specify Experiment Table"](../user_guide/experiment_table.md) for more
instructions.

## Easy to request resources

It is straightforward to run the pipeline of `celseq2` by submitting jobs to
cluster, as `celseq2` is built on top of `snakemake` which is a powerful workflow
management framework.

For example, user could run the following command to submit jobs to computing
nodes. Here it submits 10 jobs in parallel with 50G of memory requested by each.


``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    -j 10 \
    --cluster "qsub -cwd -j y -l h_vmem=50G" &
```


