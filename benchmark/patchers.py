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

class AddSimpleMean(object):
    """docstring for AddSimpleMean"""
    def __init__(self, base):
        super(AddSimpleMean, self).__init__()
        self.base = base
    def add_option(self, parser):
        pass

    def patch(self, options, data):
        if not data['mean']:
            data['mean'] = data[self.base].apply(scipy.mean)