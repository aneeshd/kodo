"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing

Various shared functionality for database query, pandas data processing and
plotting
"""

import os
import scipy as sp

import pandas as pd

def markers(label):
        if "Binary8" in label:
            return "v"
        if "Binary16" in label:
            return"^"
        if "Binary" in label:
            return "o"
        if "Prime2325" in label:
            return "*"

def set_markers(plot):
    """
    Set markers depending on the field
    @param plot a pylab plot
    """
    for l in plot.lines:
        field = l.get_label()
        l.set_marker(markers(field))

def mkdir_p(path):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

from matplotlib import pyplot as pl

pl.rcParams['legend.frameon'] = False
pl.rcParams['legend.loc'] = 'center right'

def set_sparse_plot():

    pl.rcParams.update(
    {'figure.subplot.right': .7 ,
    'figure.subplot.left': .1
    })

def set_dense_plot():

    pl.rcParams.update(
        {'figure.subplot.right': .48 ,
        'figure.subplot.left': .1
        })

def set_legend():
    pl.legend(bbox_to_anchor=(1., -0.01), loc=3, ncol=1)

def set_plot_details(p, title):
    p.set_title(title, ha = "left", position = (.0,1.03), fontsize = "medium")
    set_markers(p)
    set_legend()
