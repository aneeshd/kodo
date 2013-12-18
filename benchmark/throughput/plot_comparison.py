#!/usr/bin/env python
"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""
"""
Plot the difference in throughput between all branches where the benchmarks have
been run within the last 72 hours for all supported Kodo platforms

In order for this script to output some comparison figures you should force the
relevant benchmark run on our buildslaves:
http://buildbot.steinwurf.dk/buildslaves
"""


import argparse
import sys
sys.path.insert(0, "../")

from runner import Runner
from sources import JsonFile, MongoDbQuery, MultiMongoDbQuery, yesterday
from patchers import AddAttribute, AddMean
from modifiers import Selector, GroupBy
from setters import SetUnit
from writers import FileWriter, PdfWriter
from plotters import Plotter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Plot the benchmark data')

    parser.add_argument(
        '--days', dest='days', type=int, action='store', default=3,
        help='How many days to look back in time when comparing')

    throughput_comparision = Runner(
        sources = [
            MultiMongoDbQuery([
                MongoDbQuery(
                    collection = 'kodo_throughput',
                    query = None),
                MongoDbQuery(
                    collection = 'kodo_throughput',
                    query = None),
            ])],
        patchers = [
            AddMean(base = 'throughput')],
        modifiers = [
            GroupBy(by = ['buildername'])],
        writers = [FileWriter(), PdfWriter()],
        plotters = [
            ComparisionPlotter(
                rows=['symbols'],
                columns=['benchmark','density'],
                rc_params = {
                    'figure.subplot.right' : 0.7,
                    'figure.subplot.left'  : 0.1
                },
                ylabel = "Throughput [{unit}]",
                yscale = 'log')
        ])

    throughput_comparision.add_arguments(parser)

    args = parser.parse_args()

    for coder in ['decoder', 'encoder']:
        query = {
                    'type'      : coder,
                    'branch'    : 'master',
                    'scheduler' : 'kodo-nightly-benchmark',
                }


        throughput_comparision.run(
            run_name = 'sparse',
            arguments = args,
            options = {
                'query' : query
            })

        throughput_comparision.run(
            run_name = 'dense',
            arguments = args,
            options = {
                'select_equal' : False,
                'columns'      : ['benchmark','testcase'],
                'query'        : query,
                'rc_params'    : {
                    'figure.subplot.right' : 0.48,
                    'figure.subplot.left'  : 0.1,
                }
            })


"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

from datetime import timedelta
import pandas as pd
import scipy as sp

import sys
sys.path.insert(0, "../")
import processing_shared as ps

def plot_throughput_comparison(format, jsonfile, coder, days):
    query_branches = {
        "type": coder,
        "scheduler": "kodo-force-benchmark",
        "utc_date" : {"$gte": ps.now - timedelta(days)}
    }

    query_master = {
        "type": coder,
        "branch" : "master",
        "scheduler": "kodo-nightly-benchmark",
        "utc_date" : {"$gte": ps.yesterday, "$lt": ps.today}
    }

    db = ps.connect_database()
    cursor_master = db.kodo_throughput.find(query_master)
    cursor_branches = db.kodo_throughput.find(query_branches)

    df_all = pd.DataFrame.from_records(sp.hstack( [list(cursor_master),
        list(cursor_branches)] ))

    groups = df_all.groupby(['buildername'])

    from matplotlib import pyplot as pl
    from matplotlib.backends.backend_pdf import PdfPages as pp
    pl.close('all')

    PATH  = ("./figures_database/" + coder + "/")

    branches = list(sp.unique(df_all['branch']))
    if len(branches) == 1:
        print("Only recent benchmarks for the master branch in the database, "
              "no plots will be generated.")

    pdf = {}
    for branch in branches:
        if branch != "master":
            ps.mkdir_p(PATH + branch.replace("-","_") + "/sparse")
            ps.mkdir_p(PATH  + branch.replace("-","_") + "/dense")
            pdf[branch] = pp(PATH + branch.replace("-","_") + "/all.pdf")

    for buildername, group in groups:

        # Group all results from the most recent master build
        master_group = group[sp.array(group['branch'] == "master")]
        group[group['branch'] == "master"]
        if len(master_group) == 0:
            print "Skipping " + buildername + " as no nightly benchmark results \
                exists for the master for this buider yet"
            continue
        master_group = master_group[master_group['buildnumber'] == \
            max(master_group['buildnumber'])]

        # Group all other results by branch
        branches_group = group[group['branch'] != "master"].groupby(by = ['branch'])

        for branch, branch_group in branches_group:
            PATH_BRANCH  = PATH + (branch ).replace("-","_")

            # Calculate the difference compared to master of the latest build
            branch_group = branch_group[branch_group["buildnumber"] \
                == max(branch_group['buildnumber'])]
            branch_group['gain'] = (sp.array(branch_group['mean']) - \
                sp.array(master_group['mean']) ) / sp.array(master_group['mean'])*100

            # Group by type of code; dense, sparse
            dense = branch_group[branch_group['testcase'] != \
                "SparseFullRLNC"].groupby(by= ['symbol_size'])
            sparse = branch_group[branch_group['testcase'] == \
                "SparseFullRLNC"].groupby(by= ['symbol_size'])

            for key, g in sparse:
                ps.set_sparse_plot()
                p = g.pivot_table('gain',  rows='symbols', cols=['benchmark',
                    'density']).plot()
                ps.set_plot_details(p, buildername)
                pl.ylabel("Throughput gain [\%]")
                pl.xticks(list(sp.unique(group['symbols'])))
                pl.savefig(PATH_BRANCH + "/sparse/" + buildername + "." + format)
                pdf[branch].savefig(transparent=True)

            for key, g in dense:
                ps.set_dense_plot()
                p = g.pivot_table('gain',  rows='symbols',
                    cols=['benchmark','testcase']).plot()
                ps.set_plot_details(p, buildername)
                pl.ylabel("Throughput gain [\%]")
                pl.xticks(list(sp.unique(group['symbols'])))
                pl.savefig(PATH_BRANCH + "/dense/" + buildername + "." + format)
                pdf[branch].savefig(transparent=True)

    for p in pdf:
        pdf[p].close()
