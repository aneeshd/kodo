"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

class GroupBy(object):
    """docstring for GroupBy"""
    def __init__(self, by):
        super(GroupBy, self).__init__()
        self.by = by

    def add_options(self):
        pass

    def modify(self, options, data):
        return data.groupby(by = self.by)

class Selector(object):
    """docstring for Selector"""
    def __init__(self, column, select, neq = False):
        super(Selector, self).__init__()
        self.column = column
        self.select = select
        self.neq = neq

    def add_options(self):
        pass

    def modify(self, options, data):
        return data[(data[self.column] == self.select) != self.neq]