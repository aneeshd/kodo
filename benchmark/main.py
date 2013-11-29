#!/usr/bin/env python
"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing

Plot the number of extra symbols needed to decode
"""
import argparse
import sys

from decoding_probability.plot import plot_decoding_probablity
from decoding_probability.plot_dependency import \
     plot_decoding_probablity_dependency

from overhead.plot import plot_overhead
from throughput.plot import plot_throughput
from throughput.plot_comparison import plot_throughput_comparison

FUNCTION_KEY = 'function'
ARGUMENT_KEY = 'arguments'

benchmarks = {
    'decoding_probablity'            : {
        FUNCTION_KEY  : plot_decoding_probablity,
        ARGUMENT_KEY : ['output-format', 'json',]},
    'decoding_probablity_dependency' : {
         FUNCTION_KEY : plot_decoding_probablity_dependency,
         ARGUMENT_KEY : ['output-format', 'json',]},
    'overhead' : {
         FUNCTION_KEY : plot_overhead,
         ARGUMENT_KEY : ['output-format', 'json',]},
    'throughput' : {
         FUNCTION_KEY : plot_throughput,
         ARGUMENT_KEY : ['output-format', 'json', 'coder']},
    'throughput_comparison' : {
         FUNCTION_KEY : plot_throughput_comparison,
         ARGUMENT_KEY : ['output-format', 'coder', 'days']},
}

arguments = {
    'output-format' : {
        'action'  : 'store',
        'choices' : ['eps', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg',
                     'svgz'],
        'default' : 'eps',
        'dest'    : 'format',
        'help'    : 'The format of the generated figures.'
    },
    'json' : {
        'action'  : 'store',
        'default' : '',
        'dest'    : 'jsonfile',
        'help'    : 'the .json file written by gauge benchmark, if non provided'
                    'plots from the database'
    },
    'days' : {
        'action'  : 'store',
        'default' : 3,
        'dest'    : 'days',
        'help'    : 'How many days to look back in time when comparing',
        'type'    : int
    },
    'coder' : {
        'action'  : 'store',
        'choices' : ['encoder', 'decoder'],
        'default' : 'decoder',
        'dest'    : 'coder',
        'help'    : 'Whether to consider the encoding or decoding performance'
    }
}

def add_argument(parser, argument):
    parser.add_argument(
        '--{}'.format(argument),
        **arguments[argument])

def main():
    if len(sys.argv) < 2:
        print 'Please specify which benchmark to plot:\n{}'.format('\n'.join(
            ['{}. {}'.format(i+1, name) \
                for i, name in enumerate(benchmarks.keys())]))
        return

    index = None
    try:
        index = int(sys.argv[1])-1
    except ValueError:
        pass

    key = None
    if index is not None:
        if index in range(len(benchmarks)):
            key = benchmarks.keys()[index]
        else:
            print('index out of range')
            return
    else:
        key = sys.argv[1]

    benchmark = None
    if key in benchmarks.keys():
        benchmark = benchmarks[key]
        print "Creating plots for the {} benchmark".format(key)
    else:
        print('{} is not a valid plot.'.format(key))
        return

    parser = argparse.ArgumentParser(
        description = 'Plot the benchmark data',
        usage       = '%(prog)s [plot|plot-index] {options}')

    #for argument in benchmark[ARGUMENT_KEY]:
    #    add_argument(parser, argument)

    from plot import Plot

    p1 = Plot("test", parser, ['coder', 'days', 'json', 'output-dir'])
    p1.plot()
    p2.plot()
    #print sys.argv[2:]
    #args = parser.parse_args(sys.argv[2:])
    #benchmark[FUNCTION_KEY](
    #    **{ key: value for (key, value) in args._get_kwargs() })
    #print args

if __name__ == '__main__':
    main()
