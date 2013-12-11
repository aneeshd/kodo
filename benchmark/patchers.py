"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

import scipy
from component import Component

class AddAttribute(Component):
    """docstring for AddAttribute"""
    def __init__(self, attribute, value):
        super(AddAttribute, self).__init__()
        self.attribute = attribute
        self.value = value

    def patch(self, data):
        if self.attribute not in data.keys():
            data[self.attribute] = value

class AddMean(Component):
    """docstring for AddMean"""
    def __init__(self, base):
        super(AddMean, self).__init__()
        self.base = base

    def patch(self, data):
        if 'mean' not in data.keys():
            data['mean'] = data[self.base].apply(scipy.mean)

class AddRelativeMean(Component):
    """docstring for AddRelativeMean"""
    def __init__(self, base, relation):
        super(AddRelativeMean, self).__init__()
        self.base = base
        self.relation = relation

    def patch(self, data):
        if 'mean' in data.keys():
            return
        rel_mean = data[self.relation].apply(scipy.mean)
        data['mean'] = (data[self.base].apply(scipy.mean) - rel_mean) / rel_mean

class AddOffsetMean(Component):
    """docstring for AddOffsetMean"""
    def __init__(self, base, offset):
        super(AddOffsetMean, self).__init__()
        self.base = base
        self.offset = offset

    def patch(self, data):
        if 'mean' in data.keys():
            return
        data['mean'] = data[self.base].apply(scipy.mean) - data[self.offset]

class AddDependency(Component):
    """docstring for AddDependency"""
    def __init__(self, base):
        super(AddDependency, self).__init__()
        self.base = base

    def patch(self, data):
        if 'dependency' in data.keys():
            return
        data['dependency'] = data[self.base].apply(scipy.mean, axis = 0) - 1
