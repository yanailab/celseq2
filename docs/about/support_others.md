# List of supported techniques

Though `celseq2` is dedicated to process CEL-Seq2 sequencing data, it is also
compatible to data generated in following contexts, because of the similar design
principles of the UMI and cell barcodes.

1. Spatial transcriptome data. `celseq2` works similar to
   [st_pipeline](https://github.com/SpatialTranscriptomicsResearch/st_pipeline),
   except that `celseq2` uses Bowtie2 for aligment while `st_pipeline` uses STAR.