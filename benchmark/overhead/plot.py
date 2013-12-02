"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

import sys
sys.path.insert(0, "../")

from sources import JsonFile, MongoDbDatabaseQuery
from patchers import AddAttribute, AddRelativeMean
from modifiers import Selector, GroupBy
from writers import FileWriter, PdfWriter
from plotters import Plotter

if __name__ == '__main__':
    sparse_parser = argparse.ArgumentParser(
        description = 'Plot the benchmark data')

    sparse_overhead = Runner(
        name = 'sparse_overhead',
        argsparser = sparse_parser,
        sources = [
            JsonFile(),
            MongoDbDatabaseQuery(collection = 'kodo_overhead')],
        patchers = [
            AddAttribute(attribute = 'buildername', value = 'local'),
            AddRelativeMean(base = 'used', relation = 'coded')],
        modifiers = [
            Selector(column = 'testcase',
                     select = "SparseFullRLNC"),
            GroupBy(by = ['buildername', 'symbol_size'])
            ],
        writers = [FileWriter(), PdfWriter()],
        plotters = [
            Plotter(
                rows=['symbols'],
                cols=['benchmark','density'],
                rc_params = {
                    'figure.subplot.right' : 0.7,
                    'figure.subplot.left'  : 0.1
                },
                ylabel = "Overhead [\%]",
                yscale = 'log')
        ])

    sparse_overhead.run()

    dense_parser = argparse.ArgumentParser(
        description = 'Plot the benchmark data')
    dense_overhead = Runner(
        name = 'dense_overhead',
        argsparser = dense_parser,
        sources = [
            JsonFile(),
            MongoDbDatabaseQuery(collection = 'kodo_overhead')],
        patchers = [
            AddAttribute(attribute = 'buildername', value = 'local'),
            AddRelativeMean(base = 'used', relation = 'coded')],
        modifiers = [
            Selector(column = 'testcase',
                     select = "SparseFullRLNC",
                     equal = False),
            GroupBy(by = ['buildername', 'symbol_size'])
            ],
        writers = [FileWriter(), PdfWriter()],
        plotters = [
            Plotter(
                rows=['symbols'],
                cols=['benchmark','testcase'],
                rc_params = {
                    'figure.subplot.right' : 0.48,
                    'figure.subplot.left'  : 0.1
                },
                ylabel = "Overhead [\%]",
                yscale = 'log')
        ])

    dense_overhead.run()
"""
import pandas as pd
import scipy as sp

def plot_overhead(format, jsonfile):

    if jsonfile:
        PATH  = ("figures_local/")
        df = pd.read_json(jsonfile)
        df['buildername'] = "local"

    else:
        PATH  = ("figures_database/")
        query = {
            "branch" : "master",
            "scheduler": "kodo-nightly-benchmark",
            "utc_date" : {"$gte": ps.yesterday, "$lt": ps.today}
        }

        db = ps.connect_database()
        mc = db.kodo_overhead.find(query)
        df = pd.DataFrame.from_records( list(mc) )

    df['mean'] = (df['used'].apply(sp.mean) - df['coded'].apply(sp.mean) ) \
        / df['coded'].apply(sp.mean)




    from matplotlib import pyplot as pl
    from matplotlib.backends.backend_pdf import PdfPages as pp
    pl.close('all')

    pdf = pp(PATH + "all.pdf")

    ps.mkdir_p(PATH + "sparse")
    ps.mkdir_p(PATH + "dense")
    sparse = df[df['testcase'] == "SparseFullRLNC"]
    sparse.groupby(by= ['buildername', 'symbol_size'])

    dense = df[df['testcase'] != "SparseFullRLNC"]
    dense.groupby(by= ['buildername', 'symbol_size'])

    for (buildername,symbols), group in sparse:
        ps.set_sparse_plot()
        p = group.pivot_table('mean', rows='symbols',
            cols=['benchmark','density']).plot()
        ps.set_plot_details(p, buildername)
        p.set_yscale('log')
        pl.ylabel("Overhead [\%]")
        pl.xticks(list(sp.unique(group['symbols'])))
        pl.savefig(PATH + "sparse/" + buildername + "." + format)
        pdf.savefig(transparent=True)

    for (buildername,symbols), group in dense:
        ps.set_dense_plot()
        p = group.pivot_table('mean',  rows='symbols',
            cols=['benchmark','testcase']).plot()
        ps.set_plot_details(p, buildername)
        p.set_yscale('log')
        pl.ylabel("Overhead [\%]")
        pl.xticks(list(sp.unique(group['symbols'])))
        pl.savefig(PATH + "sparse/" + buildername + "." + format)
        pdf.savefig(transparent=True)

    pdf.close()
"""