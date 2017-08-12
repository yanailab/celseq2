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
    * -w 1800 # 30min

Select optional parameters from snakemake.snakemake():
    * --ri v.s. --ii
    * --nolock
    * --unlock
    * -j
    * --cluster
    * -n

Refs:
    - https://snakemake.readthedocs.io/en/stable/api_reference/snakemake.html
    - https://bitbucket.org/snakemake/snakemake/src/e11a57fe1f62f3f56c815d95d82871811dae81b3/snakemake/__init__.py?at=master&fileviewer=file-view-default#__init__.py-580:1127
'''


def get_argument_parser():
    desc = ('CEL-Seq2: A Python Package for Processing CEL-Seq2 RNA-Seq Data.')
    parser = argparse.ArgumentParser(description=desc, add_help=True)

    parser.add_argument(
        "target",
        nargs="*",
        default=None,
        help="Targets to build. May be rules or files.")
    parser.add_argument(
        "--configfile",
        metavar="FILE",
        required=True,
        help=("Specify or overwrite the config file of the workflow."
              "Values specified in JSON or YAML format are available "
              "in the global config dictionary inside the workflow."))

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
        help=("Execute pipeline by submitting jobs to cluster, e.g. "
              "--cluster 'qsub -cwd -j y'"))

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
        "--version", "-v",
        action="version",
        version=__version__)

    return(parser)


def main():
    p = get_argument_parser()
    args = p.parse_args()

    workflow_fpath = get_workflow_file_fpath()

    success = snakemake(snakefile=workflow_fpath,
                        configfile=args.configfile,
                        printshellcmds=True,
                        printreason=True,
                        timestamp=True,
                        latency_wait=1800,

                        targets=args.target,

                        dryrun=args.dryrun,
                        lock=not args.nolock,
                        unlock=args.unlock,

                        cluster=args.cluster,
                        cores=args.cores,
                        nodes=args.cores,

                        force_incomplete=args.rerun_incomplete,
                        ignore_incomplete=args.ignore_incomplete)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
