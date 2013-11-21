#!/usr/bin/env python
"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing

Plot the number of extra symbols needed to decode
"""

import argparse
from decoding_probability.plot import plot_decoding_probablity
from decoding_probability.plot_dependency import \
     plot_dependency_decoding_probablity

from overhead.plot import plot_overhead
from throughput.plot import plot_throughput
from throughput.plot_comparison import plot_comparison_throughput

plots = {
    'plot_decoding_probablity'            : plot_decoding_probablity,
    'plot_dependency_decoding_probablity' : plot_dependency_decoding_probablity,
    'plot_overhead'                       : plot_overhead,
    'plot_throughput'                     : plot_throughput,
    'plot_comparison_throughput'          : plot_comparison_throughput,
}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Plot the benchmark data located at the Steinwurf MongoDB")

    parser.add_argument(
        action  = 'store',
        dest    = 'plot',
        choices = plots.keys(),
        help    = 'Decide which plot you want to generated. '
                  'Write ALL to generated all plots.')
    parser.add_argument('--json',
        action  = 'store',
        default = "",
        dest    = 'jsonfile',
        help    = 'the .json file written by gauge benchmark, if non provided plots from the database')
    parser.add_argument('--days',
        action  = 'store',
        default = 3,
        dest    = 'days',
        help    = 'How many days to look back in time when comparing',
        type    = int)
    parser.add_argument('--coder',
        action  = 'store',
        choices = ['encoder', 'decoder'],
        default = 'decoder',
        dest    = 'coder',
        help    = 'Whether to consider the encoding or decoding performance')
    parser.add_argument('--output-format',
        action  = 'store',
        choices = ['eps', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg',
                   'svgz'],
        default = 'eps',
        dest    = 'format',
        help    = 'The format of the generated figures.')

    args = parser.parse_args()

    plots[args.plot](args)
