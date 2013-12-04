"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

from component import Component

class SetUnit(Component):
    """docstring for SetUnit"""
    def __init__(self, by):
        super(SetUnit, self).__init__()

    def set(self, options, data):
        result = { 'unit ' : {} }
        for (buildername,_), group in data:
            result['unit'][buildername] = list(group['unit'])[0]
        options.update(result)
