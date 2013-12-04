"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

from component import Component

class GroupBy(Component):
    """docstring for GroupBy"""
    def __init__(self, by):
        super(GroupBy, self).__init__()
        self.by = by

    def modify(self, options, data):
        return data.groupby(by = self.by)

class Selector(Component):
    """docstring for Selector"""
    def __init__(self, column, select, equal = True):
        super(Selector, self).__init__()
        self.column = column
        self.select = select
        self.equal = equal

    def modify(self, options, data):
        return data[(data[self.column] == self.select) == self.equal]