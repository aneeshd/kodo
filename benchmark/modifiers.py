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

    def modify(self, data):
        return data.groupby(by = self._get('by'))

class Selector(Component):
    """docstring for Selector"""
    def __init__(self, column, select, select_equal = True):
        super(Selector, self).__init__()
        self.column = column
        self.select = select
        self.select_equal = select_equal

    def modify(self, data):
        return data[(data[self._get('column')] == self._get('select')) == \
                    self._get('select_equal')]