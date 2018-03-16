from collections import OrderedDict
import re


def parse_star_report(raw_data):
    """
    Parse the final STAR log file.
    Copied from MultiQC (https://github.com/ewels/MultiQC/blob/b885947a2112be94774a98bc6469026f23f1e36e/multiqc/modules/star/star.py)
    """

    regexes = {
        'total_reads': r"Number of input reads \|\s+(\d+)",
        'avg_input_read_length': r"Average input read length \|\s+([\d\.]+)",
        'uniquely_mapped': r"Uniquely mapped reads number \|\s+(\d+)",
        'uniquely_mapped_percent': r"Uniquely mapped reads % \|\s+([\d\.]+)",
        'avg_mapped_read_length': r"Average mapped length \|\s+([\d\.]+)",
        'num_splices': r"Number of splices: Total \|\s+(\d+)",
        'num_annotated_splices': r"Number of splices: Annotated \(sjdb\) \|\s+(\d+)",
        'num_GTAG_splices': r"Number of splices: GT/AG \|\s+(\d+)",
        'num_GCAG_splices': r"Number of splices: GC/AG \|\s+(\d+)",
        'num_ATAC_splices': r"Number of splices: AT/AC \|\s+(\d+)",
        'num_noncanonical_splices': r"Number of splices: Non-canonical \|\s+(\d+)",
        'mismatch_rate': r"Mismatch rate per base, % \|\s+([\d\.]+)",
        'deletion_rate': r"Deletion rate per base \|\s+([\d\.]+)",
        'deletion_length': r"Deletion average length \|\s+([\d\.]+)",
        'insertion_rate': r"Insertion rate per base \|\s+([\d\.]+)",
        'insertion_length': r"Insertion average length \|\s+([\d\.]+)",
        'multimapped': r"Number of reads mapped to multiple loci \|\s+(\d+)",
        'multimapped_percent': r"% of reads mapped to multiple loci \|\s+([\d\.]+)",
        'multimapped_toomany': r"Number of reads mapped to too many loci \|\s+(\d+)",
        'multimapped_toomany_percent': r"% of reads mapped to too many loci \|\s+([\d\.]+)",
        'unmapped_mismatches_percent': r"% of reads unmapped: too many mismatches \|\s+([\d\.]+)",
        'unmapped_tooshort_percent': r"% of reads unmapped: too short \|\s+([\d\.]+)",
        'unmapped_other_percent': r"% of reads unmapped: other \|\s+([\d\.]+)",
    }
    parsed_data = OrderedDict()
    for k, r in regexes.items():
        r_search = re.search(r, raw_data, re.MULTILINE)
        if r_search:
            parsed_data[k] = float(r_search.group(1))
    # Figure out the numbers for unmapped as for some reason only the percentages are given
    try:
        total_mapped = parsed_data['uniquely_mapped'] + \
            parsed_data['multimapped'] + parsed_data['multimapped_toomany']
        unmapped_count = parsed_data['total_reads'] - total_mapped
        total_unmapped_percent = parsed_data['unmapped_mismatches_percent'] + \
            parsed_data['unmapped_tooshort_percent'] + \
            parsed_data['unmapped_other_percent']
        try:
            parsed_data['unmapped_mismatches'] = int(round(
                unmapped_count * (parsed_data['unmapped_mismatches_percent'] / total_unmapped_percent), 0))
            parsed_data['unmapped_tooshort'] = int(round(
                unmapped_count * (parsed_data['unmapped_tooshort_percent'] / total_unmapped_percent), 0))
            parsed_data['unmapped_other'] = int(round(
                unmapped_count * (parsed_data['unmapped_other_percent'] / total_unmapped_percent), 0))
        except ZeroDivisionError:
            parsed_data['unmapped_mismatches'] = 0
            parsed_data['unmapped_tooshort'] = 0
            parsed_data['unmapped_other'] = 0
    except KeyError:
        pass

    if len(parsed_data) == 0:
        return None
    return parsed_data


def merge_reports(reports, report_names=None, savetocsv='report.csv'):
    """ Merge a list of reports and save as a CSV file """
    if not reports:
        return
    n = len(reports)
    if not report_names:
        report_names = [str(i + 1) for i in range(n)]
    assert len(reports) == len(report_names)
    features = list(reports[0].keys())
    with open(savetocsv, 'w') as fout:
        fout.write('{}\n'.format(','.join(['Item'] + features)))
        for i in range(n):
            i_name = report_names[i]
            i_values = list(reports[i].values())
            fout.write('{}\n'.format(
                ','.join(map(str, [i_name] + i_values))))
    return savetocsv
