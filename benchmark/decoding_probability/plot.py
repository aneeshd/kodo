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
from patchers import AddAttribute, AddOffsetMean
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
            AddOffsetMean(base = 'used', offset = 'symbols')],
        modifiers = [
            Selector(column = 'testcase',
                     select = "SparseFullRLNC"),
            GroupBy(by = ['buildername', 'symbol_size'])
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
