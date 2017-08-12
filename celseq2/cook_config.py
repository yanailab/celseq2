#!/usr/bin/env python3
import argparse
from pkg_resources import resource_string, resource_filename, resource_stream


def get_config_file_fpath(mode='multiple'):
    '''
    Locate config.yaml inside pkg folder
    '''
    fname = 'config.yaml' if mode == 'multiple' else 'config_single_lib.yaml'
    fpath = resource_filename('celseq2', 'template/{}'.format(fname))
    return(fpath)


def get_config_file_string(mode='multiple'):
    fname = 'config.yaml' if mode == 'multiple' else 'config_single_lib.yaml'
    fstring = resource_string('celseq2', 'template/{}'.format(fname))
    return(fstring)


def new_config_file(saveto=None, mode='multiple'):
    '''
    Read config.yaml template and export to end-users

    Parameters:
        - saveto: fpath to save config template
        - mode: multiple(default) or single
    Output:
        saveto: fpath with config template as content
    '''
    with open(saveto, 'wb') as fout:
        # yaml format does not maintain the original order
        fout.write(get_config_file_string(mode=mode))


def main_new_config_file():
    desc = ('New configuration file for user to specify parameters.')
    p = argparse.ArgumentParser(description=desc, add_help=True)
    p.add_argument('-o', '--output-path', type=str, metavar='FILENAME',
                   required=True,
                   help='The output file path.')
    p.add_argument('--mode', type=str, metavar='STRING',
                   default='multiple',
                   help='If one pair of reads, set as single; otherwise \
                         set as multiple.')
    args = p.parse_args()
    new_config_file(saveto=args.output_path, mode=args.mode)


def get_workflow_file_string(mode='multiple'):
    if mode == 'multiple':
        fname = 'celseq2.snakemake'
    else:
        fname = 'celseq2_single_lib.snakemake'
    fstring = resource_string('celseq2', 'workflow/{}'.format(fname))
    return(fstring)


def get_workflow_file_fpath(mode='multiple'):
    if mode == 'multiple':
        fname = 'celseq2.snakemake'
    else:
        fname = 'celseq2_single_lib.snakemake'
    fpath = resource_filename('celseq2', 'workflow/{}'.format(fname))
    return(fpath)


def main_export_snakemake_workflow():
    desc = ('Export the snakemake workflow of entire CEL-Seq2 processing '
            'pipeline')
    p = argparse.ArgumentParser(description=desc, add_help=True)
    p.add_argument('-o', '--output-path', type=str, metavar='FILENAME',
                   required=True,
                   help='The output file path.')
    p.add_argument('--mode', type=str, metavar='STRING',
                   default='multiple',
                   help='If one pair of reads, set as single; otherwise \
                         set as multiple.')
    args = p.parse_args()

    with open(args.output_path, 'wb') as fout:
        fout.write(get_config_file_string(mode=args.mode))


def main():
    '''
    Main function for new configuration file
    '''
    print('This is {}'.format(__file__))


if __name__ == "__main__":
    main()
