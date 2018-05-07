#!/usr/bin/env python3
import sys
import argparse
from celseq2.version import __version__
from snakemake import snakemake
from celseq2.cook_config import get_workflow_file_fpath

'''
Thanks snakemake for kindly providing general API.

Required parameter:
    * -s
    * --configfile

Select top-used parameters from snakemake.snakemake():
    * -p
    * -r
    * -T
    * -w 300 # 5min
    # * --keep-going (no longer True)
    * --restart-times 2

Select optional parameters from snakemake.snakemake():
    * --ri v.s. --ii
    * --nolock
    * --unlock
    * -j
    * --cluster
    * -n
    * --notemp (--nt)

Name of rules to request outputs:
    * all (default)
    * TAG_FASTQ
    * ANNOTATION
    * ALIGNMENT
    * COUNT_MATRIX
    * QC_COUNT_MATRIX
    * CELSEQ2_TO_ST (only available for ST data)

Refs:
    - https://snakemake.readthedocs.io/en/stable/api_reference/snakemake.html
    - https://bitbucket.org/snakemake/snakemake/src/e11a57fe1f62f3f56c815d95d82871811dae81b3/snakemake/__init__.py?at=master&fileviewer=file-view-default#__init__.py-580:1127
'''


def get_argument_parser():
    desc = ('celseq2: A Python Package for Processing CEL-Seq2 RNA-Seq Data.')
    parser = argparse.ArgumentParser(description=desc, add_help=True)

    parser.add_argument(
        "target",
        nargs="*",
        default=None,
        help="Targets to build. May be rules or files.",
        choices=[None, 'all', 'TAG_FASTQ', 'ANNOTATION', 'ALIGNMENT',
                 'COUNT_MATRIX', 'QC_COUNT_MATRIX', 'CELSEQ2_TO_ST'])
    parser.add_argument(
        "--config-file",
        metavar="FILE",
        required=True,
        help=("Configurations of the details of CEL-Seq2 "
              " and running environment."))
    parser.add_argument(
        "--experiment-table",
        metavar="FILE",
        required=True,
        help=("Space/Tab separated file specifying the R1/R2 reads "
              "and the experiment design."))
    parser.add_argument(
        "--output-dir",
        metavar="DIRECTORY",
        required=True,
        help=("All results are saved here as root directory."))

    parser.add_argument(
        "--reverse-stranded", "--rs",
        action="store_true", default=False,
        help="Reads have to be mapped to the opposite strand of the feature.")

    parser.add_argument(
        "--celseq2-to-st", "--st",
        action="store_true", default=False,
        help="Rotate the UMI-count matrix to a shape of spots by genes.")

    parser.add_argument(
        "--cores", "--jobs", "-j",
        action="store",
        nargs="?",
        metavar="N",
        type=int,
        default=1,
        help=("Use at most N cores in parallel (default: 1). "))
    cluster_group = parser.add_mutually_exclusive_group()
    cluster_group.add_argument(
        "--cluster", "-c",
        metavar="CMD",
        help=("Execute pipeline by taking tasks as jobs running in cluster, "
              "e.g. --cluster 'qsub -cwd -j y'"))

    parser.add_argument("--dryrun", "-n",
                        action="store_true",
                        help="Do not execute anything.")
    parser.add_argument("--nolock",
                        action="store_true",
                        help="Do not lock the working directory")
    parser.add_argument("--unlock",
                        action="store_true",
                        help="Remove a lock on the working directory.")

    parser.add_argument(
        "--rerun-incomplete", "--ri",
        action="store_true",
        help=("Re-run all "
              "jobs the output of which is recognized as incomplete."))
    parser.add_argument(
        "--ignore-incomplete", "--ii",
        action="store_true",
        help="Do not check for incomplete output files.")
    parser.add_argument(
        "--keep-temp", dest='keep_temp',
        action="store_true",
        help="Keep the intermediate files after run.")
    parser.set_defaults(keep_temp=False)
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=__version__)

    return(parser)


def main():
    p = get_argument_parser()
    args = p.parse_args()
    stranded = "reverse" if args.reverse_stranded else "yes"
    workflow_fpath = get_workflow_file_fpath()

    success = snakemake(
        snakefile=workflow_fpath,
        targets=args.target,

        configfile=args.config_file,
        config={'output_dir': args.output_dir,
                'experiment_table': args.experiment_table,
                'stranded': stranded,
                'run_celseq2_to_st': args.celseq2_to_st,
                'keep_intermediate': args.keep_temp},

        printshellcmds=True,
        printreason=True,
        timestamp=True,
        latency_wait=300,
        jobname="celseq2_job.{rulename}.{jobid}.sh",
        keepgoing=False,
        restart_times=2,

        dryrun=args.dryrun,
        lock=not args.nolock,
        unlock=args.unlock,

        cluster=args.cluster,
        cores=args.cores,
        nodes=args.cores,

        force_incomplete=args.rerun_incomplete,
        ignore_incomplete=args.ignore_incomplete,
        notemp=args.keep_temp)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
