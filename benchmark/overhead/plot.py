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
from sources import JsonFile, MongoDbQuery, yesterday
from patchers import AddAttribute, AddRelativeMean
from modifiers import Selector, GroupBy
from writers import FileWriter, PdfWriter
from plotters import Plotter

if __name__ == '__main__':


    overhead = Runner(
        sources = [
            JsonFile(),
            MongoDbQuery(
                collection = 'kodo_overhead',
                query = {
                    'branch'    : 'master',
                    'scheduler' : 'kodo-nightly-benchmark',
                    'utc_date'  : { '$gte': yesterday }
            })],
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
                columns=['benchmark','density'],
                rc_params = {
                    'figure.subplot.right' : 0.7,
                    'figure.subplot.left'  : 0.1
                },
                ylabel = "Overhead [%]",
                yscale = 'log')
        ])

    parser = argparse.ArgumentParser(description = 'Plot the benchmark data')
    overhead.add_arguments(parser)

    args = parser.parse_args()

    overhead.run(
        run_name = 'sparse',
        arguments = args)

    overhead.run(
        run_name = 'dense',
        arguments = args,
        options = {
            'select_equal' : False,
            'columns'      : ['benchmark','testcase'],
            'rc_params'    : {
                'figure.subplot.right' : 0.48,
                'figure.subplot.left'  : 0.1
            }
        })
