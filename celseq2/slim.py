#!/usr/bin/env python3
import argparse
import glob
from celseq2.helper import popen_communicate, print_logger
from celseq2.helper import join_path, base_name, dir_name
from celseq2.helper import is_nonempty_file, rmfile
from multiprocessing import Pool


def get_argument_parser():
    desc = ('celseq2-slim: make project directory slim'
            ' by gzip fastq and sam2bam')

    parser = argparse.ArgumentParser(description=desc, add_help=True)
    parser.add_argument(
        "--project-dir",
        metavar="DIRECTORY",
        required=True,
        help=("All results are saved with here as root directory."))
    parser.add_argument(
        "--cores", "--jobs", "-j",
        action="store",
        nargs="?",
        metavar="N",
        type=int,
        default=1,
        help=("Use at most N cores in parallel (default: 1). "))
    parser.add_argument("--dryrun", "-n",
                        action="store_true",
                        help="Do not execute anything.")
    return(parser)


def run_gzip_fastq(x):
    _ = popen_communicate('gzip -f {}'.format(x))
    print_logger('Finished: gzip -f {}'.format(x))


def run_sam2bam(x):
    x_dirname, x_basename = dir_name(x), base_name(x)
    y = join_path(x_dirname, x_basename + '.bam')
    _ = popen_communicate('samtools view -bS {} > {}'.format(x, y))
    if is_nonempty_file(y):
        print_logger('Finished: sam to bam {} to {}'.format(x, y))
        rmfile(x)
    else:
        print_logger('Failed: sam to bam {} to {}'.format(x, y))


def run_gunzip_fastq(x):
    _ = popen_communicate('gzip -f -d {}'.format(x))
    print_logger('Finished: gzip -f -d {}'.format(x))


def run_bam2sam(x):
    x_dirname, x_basename = dir_name(x), base_name(x)
    y = join_path(x_dirname, x_basename + '.sam')
    _ = popen_communicate('samtools view -h {} -o {}'.format(x, y))
    if is_nonempty_file(y):
        print_logger('Finished: bam to sam {} to {}'.format(x, y))
        rmfile(x)
    else:
        print_logger('Failed: bam to sam {} to {}'.format(x, y))


def dirsize_str(x):
    xsize, _ = popen_communicate('du -sh {}'.format(x)).split()
    return(str(xsize, 'utf-8'))


def main():
    p = get_argument_parser()
    args = p.parse_args()

    SUBDIR_FASTQ = 'small_fq'
    SUBDIR_ALIGN = 'small_sam'
    fqs = glob.glob(join_path(args.project_dir, SUBDIR_FASTQ, '*', '*.fastq'),
                    recursive=True)
    fqs_unknown = glob.glob(join_path(args.project_dir, SUBDIR_FASTQ, '*',
                                      'UNKNOWN', '*.fq'), recursive=True)
    sams = glob.glob(join_path(args.project_dir, SUBDIR_ALIGN, '*', '*.sam'),
                     recursive=True)

    if args.dryrun:
        print_logger(('{} fastqs are '
                      'to be gzipped. ').format(len(fqs + fqs_unknown)))
        print_logger('{} sams are to be converted to bam'.format(len(sams)))
        return 0

    subdir_fastq_size0 = dirsize_str(join_path(args.project_dir, SUBDIR_FASTQ))
    subdir_align_size0 = dirsize_str(join_path(args.project_dir, SUBDIR_ALIGN))

    p = Pool(args.cores)
    for fq in fqs + fqs_unknown:
        p.apply_async(run_gzip_fastq, args=(fq,))
    for sam in sams:
        p.apply_async(run_sam2bam, args=(sam,))
    p.close()
    p.join()

    subdir_fastq_size1 = dirsize_str(join_path(args.project_dir, SUBDIR_FASTQ))
    subdir_align_size1 = dirsize_str(join_path(args.project_dir, SUBDIR_ALIGN))

    print_logger('Storage of FASTQs: {} => {}'.format(subdir_fastq_size0,
                                                      subdir_fastq_size1))
    print_logger('Storage of Alignments: {} => {}'.format(subdir_align_size0,
                                                          subdir_align_size1))

    return 0


if __name__ == "__main__":
    main()
