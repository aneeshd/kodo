#!/usr/bin/env python
"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""
import argparse
import sys
sys.path.insert(0, "../")

from runner import Runner
from sources import JsonFile, MongoDbDatabaseQuery, yesterday
from patchers import AddAttribute, AddDependency
from modifiers import Selector, GroupBy
from setters import SetUnit
from writers import FileWriter, PdfWriter
from plotters import Plotter

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Plot the benchmark data')

    decoding_probablity = Runner(
        sources = [
            JsonFile(),
            MongoDbDatabaseQuery(
                collection = 'kodo_decoding_probability',
                query = {
                    "branch" : "master",
                    "scheduler": "kodo-nightly-benchmark",
                    "utc_date" : {"$gte": yesterday}
                })],
        patchers = [
            AddAttribute(attribute = 'buildername', value = 'local'),
            AddDependency(base = 'rank'],
        modifiers = [
            Selector(column = 'testcase',
                     select = "SparseFullRLNC"),
            GroupBy(by = ['buildername', 'symbol_size', 'symbols'])
            ],
        setters = [SetUnit()],
        writers = [FileWriter(), PdfWriter()],
        plotters = [
            Plotter(
                rows=['symbols'],
                columns=['benchmark','density'],
                rc_params = {
                    'figure.subplot.right' : 0.7,
                    'figure.subplot.left'  : 0.1
                },
                ylabel = "Extra symbols [{unit}]")
        ])

    decoding_probablity.add_arguments(parser)

    args = parser.parse_args()

    decoding_probablity.run(
            run_name = 'sparse',
            arguments = args)

    decoding_probablity.run(
        run_name = 'dense',
        arguments = args,
        options = {
            'select_equal' : False,
            'columns'      : ['benchmark','testcase'],
            'rc_params'    : {
                'figure.subplot.right' : 0.48,
                'figure.subplot.left'  : 0.1,
            }
        })


import pandas as pd
import scipy as sp

import sys
sys.path.insert(0, "../")
import processing_shared as ps

def plot_decoding_probablity_dependency(format, jsonfile, **kwargs):

    if jsonfile:
        PATH  = ("figures_local/")
        df = pd.read_json(jsonfile)
        df['buildername'] = "local"

    else:
        PATH  = ("figures_database_detailed/")
        query = {
            "branch" : "master",
            "scheduler": "kodo-nightly-benchmark",
            "utc_date" : {"$gte": ps.yesterday, "$lt": ps.today}
        }

        db = ps.connect_database()
        mc = db.kodo_decoding_probability.find(query)
        df = pd.DataFrame.from_records( list(mc) )

    # Calculate the expected number of extra pacekts depending on the rank
    df['dependency'] = df['rank'].apply(sp.mean, axis=0)-1

    # Group by type of code; dense, sparse
    sparse = df[df['testcase'] == "SparseFullRLNC"].groupby(by= ['buildername',
        'symbol_size','symbols'])
    dense = df[df['testcase'] != "SparseFullRLNC"].groupby(by= ['buildername',
        'symbol_size','symbols'])

    from matplotlib import pyplot as pl
    from matplotlib.backends.backend_pdf import PdfPages as pp
    pl.close('all')

    ps.mkdir_p(PATH + "sparse")
    ps.mkdir_p(PATH + "dense")
    pdf = pp(PATH + "all.pdf")

    for (buildername, symbol_size, symbols), group in sparse:

        #Verbose plotting since due to no pandas support for plotting of vectors
        pl.figure()
        ps.set_sparse_plot()
        for (deps, field,density) in zip(group['dependency'],
            group['benchmark'], group['density']):
            pl.plot(sp.arange(symbols), deps, marker = ps.markers(field),
                label = "(" + field +", " + str(density) + ")")

        pl.title(buildername, ha = "left", position = (.0,1.03),
            fontsize = "medium")
        ps.set_legend()
        pl.xlabel("Rank Defeciency")
        pl.ylabel("Extra Packets")
        pl.xticks( symbols-2**sp.arange(sp.log2(symbols))[::-1] ,
            2**sp.arange(sp.log2(symbols),dtype=int)[::-1])
        pl.grid('on')
        pl.savefig(PATH + "sparse/" + buildername + str(symbols) + "." + format)
        pdf.savefig(transparent=True)

    for (buildername, symbol_size, symbols), group in dense:

        #Verbose plotting since due to no pandas support for plotting of vectors
        pl.figure()
        ps.set_dense_plot()
        for (deps, field,testcase) in zip(group['dependency'],
            group['benchmark'], group['testcase']):
            pl.plot(sp.arange(symbols), deps, marker = ps.markers(field),
                label = "(" + field +", " + testcase + ")")

        pl.title(buildername, ha = "left", position = (.0,1.03),
            fontsize = "medium")
        ps.set_legend()
        pl.xlabel("Rank Defeciency")
        pl.ylabel("Extra Packets")
        pl.xticks( symbols-2**sp.arange(sp.log2(symbols))[::-1],
            2**sp.arange(sp.log2(symbols),dtype=int)[::-1])
        pl.grid('on')
        pl.savefig(PATH + "dense/" + buildername + str(symbols) + "." + format)
        pdf.savefig(transparent=True)

    pdf.close()
