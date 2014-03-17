"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing

Various helper functions for database query, pandas data processing and
plotting
"""

import os
import scipy as sp
import argparse

import pymongo
assert pymongo.version_tuple[:2] >= (2,5), "You need a newer version of pymongo"
from pymongo import MongoClient

from matplotlib import pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages as pp

import pandas as pd
assert sp.any(sp.array(pd.version.version.split(".")) >= ['1','12',sp.inf]), \
    "You need a newer version of pandas"

import datetime

def now():
    return datetime.datetime.utcnow()

def today():
    today = now().date()
    return datetime.datetime(today.year, today.month, today.day)

def timedelta(arg):
    return datetime.timedelta(arg)

marker = {
    "$2^8$" : "v",
    "$2^{16}$" : "^",
    "$2$" : "o",
    "$2^{32}-5$" : "*",
    }

def markers(string):
    if marker.has_key(string):
        return marker[string]

field = {
    "Binary8" : "$2^8$",
    "Binary16" : "$2^{16}$",
    "Binary" : "$2$",
    "Prime2325" : "$2^{32}-5$",
    }

def fields(string):
    if field.has_key(string):
        return field[string]

algorithm = {
    "BackwardFullRLNC" : "Backwards",
    "FullDelayedRLNC" : "Delayed",
    "FullRLNC" : "Standard",
    }

def algorithms(string):
    if algorithm.has_key(string):
        return algorithm[string]

slaves = {
    "debian0" : {"OS": "", "CPU" : ""},
    "debian1" : {"OS": "", "CPU" : ""},
    "debian2" : {"OS": "Debian testing x86-64", "CPU" : "i7-3770S CPU @ 3.10GHz"},
    "debian3" : {"OS": "Debian testing x86-64", "CPU" : "i7-3770S CPU @ 3.10GHz"},
    "debian4" : {"OS": "Debian testing x86-64", "CPU" : "i7-3770S CPU @ 3.10GHz"},
    "debian5" : {"OS": "", "CPU" : ""},
    "arch1" : {"OS": "ArchLinux x86-64", "CPU" : "i7-3770S CPU @ 3.10GHz"},
    "arch2" : {"OS": "ArchLinux x86-64", "CPU" : "i7-3770S CPU @ 3.10GHz"},
    "windows1" : {"OS": "Windows 7 Enterprise x86-64", "CPU" : "Athlon 64 Processor 3200+ @ 2.00GHz, "},
    "windows2" : {"OS": "Windows 7 Enterprise x86-64", "CPU" : "Core2 Duo E6550 @ 2.33 GHz"},
    "windows3" : {"OS": "Windows 7 Enterprise x86-64", "CPU" : "i7-2600 CPU @ 3.40GHz"},
    "mac1" : {"OS": "MacOS, 10.8.5, x86-64", "CPU" : "i5-2400 CPU @ 3.10GHz"},
    "mac2" : {"OS": "MacOS, 10.9.1, x86-64", "CPU" : "i5-3210M CPU @ 2.50GHz"},
    "mac3" : {"OS": "MacOS, 10.8.5, x86-64", "CPU" : "i5-3210M CPU @ 2.50GHz"},
    }

def specifications(slavename):
    if slaves.has_key(slavename):
        return "ID: " + slavename + "\n" + "OS: " + slaves[slavename]['OS'] + \
        "\n" + "CPU: " + slaves[slavename]['CPU']
    else:
        return "ID: " + slavename.replace("_","-")

def set_common_params():
        pl.rcParams.update(
            {'figure.autolayout' : True,
            'text.usetex' : True,
            'loc' : "upper left",
            'fontsize' : "x-small",
            })

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        pass

def connect_database():
    """
    Connect to the benchmark database
    """

    address = "176.28.49.184"
    username = "guest"
    password = "none"

    client = MongoClient(address)
    db = client["benchmark"]
    db.authenticate(username, password)
    return db

class plotter:
    """
    for convenient plotting
    """

    def __init__(self, args):
        self.args = args
        if hasattr(self.args, "json"):
            self.from_json = bool(self.args.json)
        else:
            self.from_json = False
        self.legend_title = False
        self.branch = False
        pl.close('all')
        self.pdf = False

        set_common_params()

    def __del__(self):
        self.pdf.close()

    def get_dataframe(self, query, collection="none"):
        if self.from_json:
            df = pd.read_json(self.args.json)
            df['slavename'] = "local"
        else:
            db = connect_database()
            if collection == "kodo_throughput":
                mc = db.kodo_throughput.find(query)
            elif collection == "kodo_decoding_probability":
                mc = db.kodo_decoding_probability.find(query)
            elif collection == "kodo_overhead":
                mc = db.kodo_overhead.find(query)
            df = pd.DataFrame.from_records( list(mc) )

        return df

    def get_base_path(self):
        if self.from_json:
            path = os.path.basename("local")
        else:
            path = os.path.basename("database")

        if hasattr(self.args, "coder"):
            path = os.path.join(path, self.args.coder)

        if self.branch:
            path = os.path.join(path, self.branch)

        mkdir_p(path)
        return path

    def get_full_path(self, subdirectory, filename):
        path = os.path.join(self.get_base_path(), subdirectory)
        mkdir_p(path)
        return os.path.join(path, filename + "." + self.args.output_format)

    def set_branch(self, branch):
        self.branch = branch.replace("-","_")

    def set_title(self, title):
        pl.title(title.replace("-","_"), ha = "left", position = (.0,1.03), fontsize = "medium")

    def set_info_box(self, text):
        pl.figtext(0.11,0.2, "\underline{Specs} \n" + str(text),
        backgroundcolor = "lightgrey", verticalalignment = "top",
        horizontalalignment = "left", fontsize ="x-small")

    def set_slave_info(self, slavename):
        self.set_info_box(specifications(slavename))

    def set_markers(self, plot):
        """
        Set markers depending on the field
        @param plot a pylab plot
        """
        for l in plot.lines:
            field = l.get_label()
            l.set_marker(markers(field))

    def set_legend_title(self, title):
        self.legend_title = title

    def write(self, subdirectory, filename):
        pl.legend(fontsize = "x-small", ncol=4, mode="expand", title = self.legend_title)
        if not self.pdf:
            self.pdf = pp(os.path.join(self.get_base_path(), "all.pdf"))
        self.pdf.savefig(transparent=True)

        pl.savefig(self.get_full_path(subdirectory, filename))
        pl.close('all')

def add_arguments(argument_list):
    """
    add arguments to the runtime
    """

    parser = argparse.ArgumentParser()
    arguments = {
        "json" : add_argument_json,
        "coder" : add_argument_coder,
        "output-format" : add_argument_output_format,
        "date" : add_argument_date,
        "days" : add_argument_days,
        }

    for argument in argument_list:
        arguments[argument](parser)

    args = parser.parse_args()
    return args

def add_argument_json(parser):
    parser.add_argument(
    '--json', dest='json', action='store',
    help='the .json file written by gauge benchmark, if non provided\
    plots from the database', default=False)

def add_argument_coder(parser):
    parser.add_argument(
    '--coder', dest='coder', action='store', choices=['encoder','decoder'],
    default='decoder',
    help='Whether to consider the encoding or decoding performance')

def add_argument_output_format(parser):
    parser.add_argument(
    '--output-format', dest='output_format', action='store', default='eps',
    help='The format of the generated figures, e.g. eps, pdf')

def add_argument_date(parser):
    parser.add_argument(
    '--date', dest='date', type=datetime.datetime, action='store', default=today(),
    help='What data to use when accessing the database, must be of type datetime.datetime')

def add_argument_days(parser):
    parser.add_argument(
    '--days', dest='days', type=int, action='store', default=1,
    help='How many days to look back in time when comparing')