"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

import pandas as pd
import scipy as sp

import sys
sys.path.insert(0, "../")
import processing_shared as ps

def plot_decoding_probablity(format, jsonfile):

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
        mc = db.kodo_decoding_probability.find(query)
        df = pd.DataFrame.from_records( list(mc) )

    df['mean'] = df['used'].apply(sp.mean) -df['symbols']
    df['std'] = df['used'].apply(sp.std)

    sparse = df[df['testcase'] == "SparseFullRLNC"].groupby(
        by = ['buildername', 'symbol_size'])
    dense = df[df['testcase'] != "SparseFullRLNC"].groupby(
        by = ['buildername', 'symbol_size'])

    from matplotlib import pyplot as pl
    from matplotlib.backends.backend_pdf import PdfPages as pp
    pl.close('all')

    ps.mkdir_p(PATH + "sparse")
    ps.mkdir_p(PATH + "dense")
    pdf = pp(PATH + "all.pdf")

    for (buildername,symbols), group in sparse:
        ps.set_sparse_plot()
        p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
            'density']).plot()
        ps.set_plot_details(p, buildername)
        pl.ylabel("Extra symbols" + " [" + list(group['unit'])[0] + "]")
        pl.xticks(list(sp.unique(group['symbols'])))
        pl.savefig(PATH + "sparse/" + buildername + "." + format)
        pdf.savefig(transparent=True)

    for (buildername,symbols), group in dense:
        ps.set_dense_plot()
        p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
            'testcase']).plot()
        ps.set_plot_details(p, buildername)
        pl.ylabel("Extra symbols" + " [" + list(group['unit'])[0] + "]")
        pl.xticks(list(sp.unique(group['symbols'])))
        pl.savefig(PATH + "dense/"+ buildername + "." + format)
        pdf.savefig(transparent=True)

    pdf.close()
