#!/usr/bin/env python3
import argparse
import numpy as np
import pandas as pd
from plotly import tools
import plotly.graph_objs as go
from plotly.offline import plot

from celseq2.helper import print_logger, base_name, is_nonempty_file


def plotly_scatter(x, y, mask_by=None, hover_text=None,
                   xlab='', ylab='', main='',
                   colorscale='Viridis', mask_title=''):
    data = go.Scatter(
        x=x,
        y=y,
        mode='markers')
    if hover_text is not None:
        data['text'] = hover_text
    if mask_by is not None:
        data.marker = go.Marker(
            colorbar=go.ColorBar(
                title=mask_title,
                titleside='right'),
            color=mask_by,
            colorscale=colorscale,
            showscale=True, opacity=0.7)
    trace = [data]
    layout = go.Layout(
        title=main,
        xaxis=dict(title=xlab,
                   autorange=True),
        yaxis=dict(title=ylab, scaleanchor='x',
                   autorange=True),
        height=600,
        width=600)

    fig = go.Figure(data=trace, layout=layout)
    return fig


def plotly_hist(vals, xlab='', ylab='Freq', main=''):
    data = go.Histogram(x=vals)
    trace = [data]
    layout = go.Layout(
        title=main,
        xaxis=dict(title=xlab),
        yaxis=dict(title=ylab),
        height=400,
        width=400)
    fig = go.Figure(data=trace, layout=layout)
    return fig


def plotly_qc(fpath, saveto, sep=',', name=''):
    '''
    Generate a plotly html plot for QC of a scRNA-seq data.

    QC inlucdes:
    - number of total UMIs
    - number of detected genes
    - percent of MT expression

    Input:
    fpath: file path (CSV/TSV) to the expression file with genes/features as rows
    and cells/samples on columns. First column saves gene names.

    saveto: a html file to save the plots using Plot.ly

    sep: file sep. Default: ","
    '''

    bool_success = False
    if not is_nonempty_file(fpath):
        return bool_success

    if not name:
        name = base_name(fpath)

    expr = pd.read_csv(fpath, index_col=0, sep=sep)
    print_logger(('UMI count matrix: '
                  '{} genes x {} cells').format(expr.shape[0], expr.shape[1]))

    total_num_UMIs = expr.sum(axis=0)
    num_detected_genes = (expr > 0).sum(axis=0)
    mt_index = [x for x in expr.index if x.startswith(
        'mt-') or x.startswith('MT-')]
    if not mt_index:
        percent_mt = 0
    else:
        mt_umis = expr.loc[pd.Series(mt_index), :].sum(axis=0)
        percent_mt = mt_umis / total_num_UMIs
        percent_mt = percent_mt.replace(np.inf, 0)

    qc = pd.DataFrame(dict(total_num_UMIs=total_num_UMIs,
                           num_detected_genes=num_detected_genes,
                           percent_mt=percent_mt))

    # 1/5
    plotly_g_vs_umi = plotly_scatter(
        x=qc.total_num_UMIs,
        y=qc.num_detected_genes,
        xlab='#Total UMIs (median={})'.format(qc.total_num_UMIs.median()),
        ylab='#Detected Genes (median={})'.format(
            qc.num_detected_genes.median()),
        main=name,
        hover_text=qc.index.values)
    plotly_g_vs_umi.layout.yaxis.scaleanchor = None

    # 2/5
    plotly_mt_vs_umi = plotly_scatter(
        x=qc.total_num_UMIs,
        y=qc.percent_mt,
        xlab='#Total UMIs (median={})'.format(qc.total_num_UMIs.median()),
        ylab='MT Fraction (median={:6.4f})'.format(qc.percent_mt.median()),
        main=name,
        hover_text=qc.index.values)
    plotly_mt_vs_umi.layout.yaxis.scaleanchor = None

    # 3/5
    plotly_hist_umis = plotly_hist(
        vals=qc.total_num_UMIs,
        xlab='#Total UMIs (median={})'.format(qc.total_num_UMIs.median()))

    # 4/5
    plotly_hist_g = plotly_hist(
        vals=qc.num_detected_genes,
        xlab=('#Detected Genes '
              '(median={})').format(qc.num_detected_genes.median()))
    # 5/5
    plotly_hist_percent_mt = plotly_hist(
        vals=qc.percent_mt,
        xlab='MT Fraction (median={:6.4f})'.format(qc.percent_mt.median()))

    # Merge the 5 figures together
    qc_fig = tools.make_subplots(
        rows=2, cols=3,
        specs=[[{}, {}, None], [{}, {}, {}]])
    qc_fig.append_trace(plotly_g_vs_umi.data[0], 1, 1)
    qc_fig.append_trace(plotly_mt_vs_umi.data[0], 1, 2)
    qc_fig.append_trace(plotly_hist_umis.data[0], 2, 1)
    qc_fig.append_trace(plotly_hist_g.data[0], 2, 2)
    qc_fig.append_trace(plotly_hist_percent_mt.data[0], 2, 3)

    qc_fig.layout.xaxis1 = {**qc_fig.layout.xaxis1,
                            **plotly_g_vs_umi.layout.xaxis}
    qc_fig.layout.yaxis1 = {**qc_fig.layout.yaxis1,
                            **plotly_g_vs_umi.layout.yaxis}

    qc_fig.layout.xaxis2 = {**qc_fig.layout.xaxis2,
                            **plotly_mt_vs_umi.layout.xaxis}
    qc_fig.layout.yaxis2 = {**qc_fig.layout.yaxis2,
                            **plotly_mt_vs_umi.layout.yaxis}

    qc_fig.layout.xaxis3 = {**qc_fig.layout.xaxis3,
                            **plotly_hist_umis.layout.xaxis}
    qc_fig.layout.yaxis3 = {**qc_fig.layout.yaxis3,
                            **plotly_hist_umis.layout.yaxis}

    qc_fig.layout.xaxis4 = {**qc_fig.layout.xaxis4,
                            **plotly_hist_g.layout.xaxis}
    qc_fig.layout.yaxis4 = {**qc_fig.layout.yaxis4,
                            **plotly_hist_g.layout.yaxis}

    qc_fig.layout.xaxis5 = {**qc_fig.layout.xaxis5,
                            **plotly_hist_percent_mt.layout.xaxis}
    qc_fig.layout.yaxis5 = {**qc_fig.layout.yaxis5,
                            **plotly_hist_percent_mt.layout.yaxis}

    qc_fig['layout'].update(height=800, width=1000, title=name,
                            showlegend=False)

    plot(qc_fig, filename=saveto, auto_open=False)

    bool_success = True
    return bool_success


def plotly_qc_st(fpath, saveto, sep='\t', name=''):
    bool_success = False
    if not is_nonempty_file(fpath):
        return bool_success
    if not name:
        name = base_name(fpath)

    ST = pd.read_csv(fpath, sep=sep)
    print_logger(('ST UMI-count matrix has '
                  '{} spots x {} genes').format(ST.shape[0], ST.shape[1]))

    ST_total_UMIs = ST.iloc[:, 2:].sum(axis=1)
    ST_detected_genes = (ST.iloc[:, 2:] > 0).sum(axis=1)
    mt_cols = [x for x in ST.columns if x.startswith(
        'mt-') or x.startswith('MT-')]
    if not mt_cols:
        ST_percent_mt = 0
    else:
        ST_percent_mt = ST[mt_cols].sum(axis=1) / ST_total_UMIs
        ST_percent_mt.replace(np.inf, 0)

    ST_qc = pd.DataFrame(
        dict(Row=ST.Row, Col=ST.Col,
             total_num_UMIs=ST_total_UMIs,
             num_detected_genes=ST_detected_genes,
             percent_mt=ST_percent_mt))

    # 1/3
    plotly_ST_g = plotly_scatter(
        x=ST_qc.Row, y=ST_qc.Col,
        mask_by=ST_qc.num_detected_genes,
        hover_text=ST_qc.num_detected_genes.astype('str'),
        colorscale='Viridis',
        mask_title=('#Detected Genes '
                    '(median={})').format(ST_qc.num_detected_genes.median()))
    # 2/3
    plotly_ST_UMIs = plotly_scatter(
        x=ST_qc.Row, y=ST_qc.Col,
        mask_by=ST_qc.total_num_UMIs,
        hover_text=ST_qc.total_num_UMIs.astype('str'),
        colorscale='Viridis',
        mask_title=('#Total UMIs '
                    '(median={})').format(ST_qc.total_num_UMIs.median()))
    # 3/3
    plotly_ST_mt = plotly_scatter(
        x=ST_qc.Row, y=ST_qc.Col,
        mask_by=ST_qc.percent_mt,
        hover_text=ST_qc.percent_mt.astype('str'),
        colorscale='Viridis',
        mask_title=('MT Fraction '
                    '(median={:6.4f})').format(ST_qc.percent_mt.median()))
    # Merge the 3 figures together
    fig = tools.make_subplots(
        rows=1, cols=3,
        subplot_titles=('#Total UMIs', '#Detected Genes', 'MT Fraction'))

    fig.append_trace(plotly_ST_UMIs.data[0], 1, 1)
    fig.append_trace(plotly_ST_g.data[0], 1, 2)
    fig.append_trace(plotly_ST_mt.data[0], 1, 3)

    fig['layout'].update(height=600, width=1900, title=name)

    fig.layout.showlegend = False
    # Manually change the locations of other two color bars to proper places
    fig.data[0].marker.colorbar.x = 0.28
    fig.data[1].marker.colorbar.x = 0.64

    plot(fig, filename=saveto, auto_open=False)

    bool_success = True
    return bool_success


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        'fpath', type=str, metavar='FILENAME',
        help=('file path (CSV/TSV) to the expression file with genes/features '
              'as rows and cells/samples on columns. '
              'First column saves gene names.'))
    parser.add_argument('saveto', type=str, metavar='FILENAME',
                        help='File path (html) to save the QC plots.')
    parser.add_argument('--name', type=str, metavar='STR', default='')
    parser.add_argument('--sep', type=str, default='\t',
                        help='File sep (default: \'\t\')')
    parser.add_argument('--st', dest='is_st', action='store_true')
    parser.set_defaults(is_st=False)
    args = parser.parse_args()

    if args.is_st:
        plotly_qc_st(args.fpath, args.saveto, args.sep, args.name)
    else:
        plotly_qc(args.fpath, args.saveto, args.sep, args.name)
    print_logger('Generate QC for {}'.format(args.fpath))
    print_logger('See {}'.format(args.saveto))


if __name__ == "__main__":
    main()
