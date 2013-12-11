"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

class Runner(object):
    """docstring for Runner"""
    def __init__(self,
                 sources = [],
                 patchers = [],
                 modifiers = [],
                 setters = [],
                 writers = [],
                 plotters = []):
        super(Runner, self).__init__()
        self.sources = sources
        self.patchers = patchers
        self.modifiers = modifiers
        self.setters = setters
        self.writers = writers
        self.plotters = plotters

        self.components = self.sources + \
                          self.patchers + \
                          self.modifiers + \
                          self.setters + \
                          self.plotters + \
                          self.writers

    def add_arguments(self, parser):
        map(lambda c: c.add_arguments(parser), self.components)

    def run(self, run_name, arguments, options = {}):
        options.update(arguments.__dict__)
        options['run_name'] = run_name
        map(lambda c: c.set_options(options), self.components)

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

        map(lambda w: w.init(), self.writers)

        for plotter in self.plotters:
            for data_point in data:
                map(lambda s: s.set(data_point), self.setters)
                plotname = plotter.plot(data_point)
                map(lambda w: w.save(plotname), self.writers)
        map(lambda w: w.close(), self.writers)
