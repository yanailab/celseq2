# Release Note


<!-- ## :fa-flag-checkered: **v0.0.0**

:fa-calendar: **YYYY-MM-DD**

:fa-code: []()

:fa-star: **Features**
 -->

---

## :fa-flag-checkered: **v0.5.3**

:fa-calendar: **2018-05-10**

:fa-code: [2be1954](https://github.com/yanailab/celseq2/tree/2be195470f6b98e42f5d86f4f2736f29a543103f)

:fa-star: **Features**


- Plot demultiplexing and alignment stats to help users assess their data.
- Column names of UMI-count matrix is named in a format of 'BC-i-xxxx' to suit users needs.


---

## :fa-flag-checkered: **v0.5.2**

:fa-calendar: **2018-04-16**

:fa-star: **Features**

- Generate QC plots for UMI-counts matrices. If ST is performed, an extra QC plot masked on grid is generated.
- Allow experienced users to feed extra parameters to align. See issue #10.

---

## :fa-flag-checkered: **v0.5.1**

:fa-calendar: **2018-04-05**

:fa-star: **Features**

- Get rid of the possible limitation about "shared memory" when STAR is used on
  servers.
- SpatialTranscriptomics (ST) processing is able to use STAR aligner practically.
- Optionally remove intermediate files in a robust way.

---

## :fa-flag-checkered: **v0.4.8**

:fa-calendar: **2018-03-26**

:fa-star: **Features**

- Robust selection on type of genes, e.g., protein coding, lincRNA.
    - Handle the case when all genes are needed.
    - The gene names are consistent to the in-house inDrop pipeline using
      `genometools`.
    - Handle the GTF/GFF where "gene_biotype" attribute is not available.
- Automatically remove intermediate files by `snakemake`'s `temp()` function.

---

## :fa-flag-checkered: **v0.4.7**

:fa-calendar: **2018-03-23**

:fa-star: **Features**

- Support "gene_biotype" selection.
- Better support SpatialTranscriptome data.
    - `celseq2-to-st` understands `expr.csv` file
    - `celseq2-to-st` recognizes "(1 out of many)" annotation inside GTF/GFF.
- Robust design of work flow.

---

## :fa-flag-checkered: **v0.4.4**

:fa-calendar: **2018-02-13**

:fa-star: **Features**

- Improve the design of `snakemake` pipeline to avoid silent pre-inhibition.
- Improve running with STAR to avoid memory over-use.

---

## :fa-flag-checkered: **v0.4.1**

:fa-calendar: **2017-12-20**

:fa-star: **Features**

- Support `STAR` aligner.
- Update docs.


---

## :fa-flag-checkered: **v0.4.0**

:fa-calendar: **2017-10-04**

:fa-star: **Features**

- More general API to specify UMI-BC design.
- Support
  [st_pipeline](https://github.com/SpatialTranscriptomicsResearch/st_pipeline).

---

## :fa-flag-checkered: **v0.3.0**

:fa-calendar: **2017-09-18**

:fa-star: **Features**

- Simulate CEL-Seq2 reads.
- :gun: Release package tests.

---

## :fa-flag-checkered: **v0.2.6**

:fa-calendar: **2017-09-14**

:fa-star: **Features**

- Support "reverse" stranded by adding`stranded` parameter.

---

## :fa-flag-checkered: **v0.2.5**

:fa-calendar: **2017-08-22**

:fa-star: **Features**

- Add `celseq2-slim` to do storage management.

---

## :fa-flag-checkered: **v0.2.0**

:fa-calendar: **2017-08-12**

:fa-star: **Features**

- Release command to generate templates to keep consistency.


