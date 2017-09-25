
Examine how many tasks to be performed before actually executing the pipeline:

``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    --dryrun
```

Launch pipeline in the computing node which performs 10 tasks in parallel.

``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    -j 10
```

Alternatively, it is straightforward to run the pipeline of `celseq2` by
submitting jobs to cluster, as `celseq2` is built on top of `snakemake` which is
a powerful workflow management framework. For example, in login node on server,
user could run the following command to submit jobs to computing nodes. Here it
submits 10 jobs in parallel with 50G of memory requested by each.

``` bash
celseq2 --config-file /path/to/wonderful_CEL-Seq2_config.yaml \
    --experiment-table /path/to/wonderful_experiment_table.txt \
    --output-dir /path/to/result_dir \
    -j 10 \
    --cluster "qsub -cwd -j y -l h_vmem=50G" &
```
