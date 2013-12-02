"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

import scipy

class AddBuilderName(object):
    """docstring for AddBuilderName"""
    def __init__(self):
        super(AddBuilderName, self).__init__()

    def add_option(self, parser):
        pass

    def patch(self, options, data):
        if not data['buildername']:
            data['buildername'] = 'local'

class AddMeanSimple(object):
    """docstring for AddMeanSimple"""
    def __init__(self, base):
        super(AddMeanSimple, self).__init__()
        self.base = base
    def add_option(self, parser):
        pass

    def patch(self, options, data):
        if not data['mean']:
            data['mean'] = data[self.base].apply(scipy.mean)

class AddRelativeMean(object):
    """docstring for AddMeanOverHead"""
    def __init__(self, base, relation):
        super(AddMeanOverHead, self).__init__()
        self.base = base
        self.relation = relation

    def add_option(self, parser):
        pass

    def patch(self, options, data):
        if not data['mean']:
            relation_mean = data[self.relation].apply(scipy.mean)
            data['mean'] = (data[self.base].apply(scipy.mean) - relation_mean) \
                           / relation_mean
