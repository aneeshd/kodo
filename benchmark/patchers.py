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

    def patch(self, options, data):
        if self.attribute not in data.keys():
            data[self.attribute] = value

class AddMeanSimple(Component):
    """docstring for AddMeanSimple"""
    def __init__(self, base):
        super(AddMeanSimple, self).__init__()
        self.base = base

    def patch(self, options, data):
        if 'mean' not in data.keys():
            data['mean'] = data[self.base].apply(scipy.mean)

class AddRelativeMean(Component):
    """docstring for AddRelativeMean"""
    def __init__(self, base, relation):
        super(AddRelativeMean, self).__init__()
        self.base = base
        self.relation = relation

    def patch(self, options, data):
        if 'mean' not in data.keys():
            relation_mean = data[self.relation].apply(scipy.mean)
            data['mean'] = (data[self.base].apply(scipy.mean) - relation_mean) \
                           / relation_mean
