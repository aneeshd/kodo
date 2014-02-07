#!/usr/bin/env python
"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing

Plot the throughput for all benchmarked Kodo platforms
"""

import pandas as pd
import scipy as sp

import sys
sys.path.insert(0, "../")
import plot_helper as ph

def plot(args):
    plotter = ph.plotter()

    if args.jsonfile:
        plotter.set_base_path("figures_local/" + args.coder + "/")
        df = pd.read_json(args.jsonfile)
        df['buildername'] = "local"
    else:
        plotter.set_base_path("figures_database/" + args.coder + "/")
        query = {
        "type": args.coder,
        "branch" : "master",
        "scheduler": "kodo-nightly-benchmark",
        "utc_date" : {"$gte": ph.yesterday(), "$lt": ph.today()}
        }

        df = ph.get_dataframe_from_database(query)

    df['mean'] = df['throughput'].apply(sp.mean)
    df['std'] = df['throughput'].apply(sp.std)

    # Group by type of code; dense, sparse
    dense = df[df['testcase'] != "SparseFullRLNC"].groupby(by= ['buildername',
        'symbol_size'])
    sparse = df[df['testcase'] == "SparseFullRLNC"].groupby(by= ['buildername',
        'symbol_size'])

    from matplotlib import pyplot as pl

    def set_throughput_details(p):
        pl.ylabel("Throughput" + " [" + list(group['unit'])[0] + "]")
        pl.xticks(list(sp.unique(group['symbols'])))
        p.set_yscale('log')

    plotter.set_extra_path("sparse/")
    ph.set_sparse_params()
    for (buildername,symbols), group in sparse:
        p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'density']).plot()
        set_throughput_details(p)
        ph.set_plot_details(p, buildername)
        plotter.write(p, buildername + "." + args.format)

    plotter.set_extra_path("dense/")
    ph.set_dense_params()
    for (buildername,symbols), group in dense:
        p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'testcase']).plot()
        set_throughput_details(p)
        ph.set_plot_details(p, buildername)
        plotter.write(p, buildername + "." + args.format)


if __name__ == '__main__':

    args = ph.add_arguments(["--json", "--coder", "--output-format"])
    plot(args)
