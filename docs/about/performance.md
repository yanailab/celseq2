# Performance


## Introduction

Generally speaking, there are two different ways to improve the runtime of a pipeline: 1) Provide more computational resources (e.g., CPPU cores or nodes in a cluster) and improve the parallelization of the pipeline. 2) Optimize the code of each pipeline step in order to make it more computationally efficient. I aimed to develop a new CEL-Seq2 pipeline using both strategies in combination. Here, I describe the results of a runtime comparison between the previous CEL-Seq2 pipeline (`CEL-Seq-pipeline`) and the new pipeline (`celseq2`).

## Comparison of runtimes in serial mode

To compare the raw runtimes of each step (demultiplexing, alignment, and UMI counting) in both pipelines, I ran them in "serial" mode, where every single pipeline step is performed one after the other. The two pipelines were run for one CEL-Seq2 dataset which consisted of ~40M read pairs (read-1 and read-2 has length of 13 and 61 nucleotides, respectively). Each run was performed three times independently to account for the fluctuation of run-time.

The results indicate that the new pipeline improved the speed of demultiplexing by **3-fold**, and the speed of the UMI counting step by almost **4-fold**. These improvements can be attributed solely to code optimization of these steps.

Note that in this comparison, `CEL-Seq-pipeline` had an unfair advantage because it internally used 15 threads for parallelizing alignment with `bowtie2`, while the new pipeline only used one thread. Nevertheless, `celseq2` gave an overall speed-up of more than **2-fold** compared to `CEL-Seq-pipeline`. With only a single thread for alignment, I would expect the speed-up to be larger than **2.5-fold**.

<img src='/uploads/aad4b7080da3760fb1565a0f65c5f33f/efficiency_single.png' width=600>

## Comparison of runtimes in parallel mode

In practice, pipeline users usually have multiple CPU cores available, and pipelines can take advantage of this fact by splitting up data into smaller chunks and processing them in parallel, and/or by running individual processes (e.g., alignment) using multiple threads. I therefore aimed to perform a more realistic performance comparison of the two pipelines by running them on a 32-core server, and testing them on a dataset that consisted of two lanes (pairs of FASTQ files), each consisting of 40M read pairs.

The results showed a **9-fold** improvement in the runtime of the demultiplexing step for the `celseq2` pipeline, which was the combined result of code optimization (see above) and the use of the snakemake framework, which allowed the reads from both lanes to be demultiplexed in parallel.

Note that in this comparison, `CEL-Seq-pipeline` used more computational resources than `celseq2` for UMI counting (50 parallel jobs instead of 30, see details [here](https://gitlab.com/Puriney/celseq2/wikis/Efficiency#how-the-parallelization-in-previous-generation-pipeline-is-performed)). Nevertheless, `celseq2` achieved a more than **3.5-fold** overall speed-up compared to `CEL-Seq-pipeline`.

<img src='/uploads/f37fbf04b9947b18bd9faf31473f24a5/efficiency_2libs.png' width=600>