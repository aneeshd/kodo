"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

class Runner(object):
    """docstring for Runner"""
    def __init__(self,
                 argparser,
                 sources = [],
                 patchers = [],
                 modifiers = [],
                 setters = [],
                 writers = [],
                 plotters = []):
        super(Runner, self).__init__()
        self.argparser = argparser
        self.sources = sources
        self.patchers = patchers
        self.modifiers = modifiers
        self.setters = setters
        self.writers = writers
        self.plotters = plotters

        components = self.sources + \
                     self.patchers + \
                     self.modifiers + \
                     self.setters + \
                     self.plotters + \
                     self.writers

        map(lambda c: c.add_arguments(self.argparser), components)
        o =  {k, v for (k, v) in self.argparser.parse_args()._get_kwargs()}
        print o
        self.options = o
        map(lambda c: c.set_options(self.options), components)

    def run(self, name, options = {}):
        self.options['run_name'] = name
        self.options.update(options)

        data = None
        for source in self.sources:
            data = source.get_data()
            if data:
                break
        else:
            assert False, 'No data found.'

        map(lambda p: p.patch(data), self.patchers)

        for modifier in self.modifiers:
            data = modifier.modify(data)

        map(lambda s: s.set(self.options, data), self.setters)
        map(lambda w: w.init(), self.writers)

        for plotter in self.plotters:
            for plotname in plotter.plot(data):
                map(lambda w: w.save(plotname), self.writers)
        map(lambda w: w.close(), self.writers)
