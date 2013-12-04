"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

class Runner(object):
    """docstring for Runner"""
    def __init__(self,
                 name,
                 argsparser,
                 sources = [],
                 patchers = [],
                 modifiers = [],
                 setters = [],
                 writers = [],
                 plotters = []):
        super(Runner, self).__init__()
        self.name = name
        self.argsparser = argsparser
        self.sources = sources
        self.modifiers = modifiers
        self.patchers = patchers
        self.setters = setters
        self.writers = writers
        self.plotters = plotters

    def run(self, options = {}):
        for item in self.sources + \
                    self.patchers + \
                    self.modifiers + \
                    self.writers + \
                    self.plotters:
            item.add_options(self.argsparser)

        options.update(self.argsparser.parse_args()._get_kwargs())

        data = None
        for source in self.sources:
            data = source.get_data(options)
            if data:
                break
        else:
            print('No data found.')
            exit()

        map(lambda p: p.patch(options, data), self.patchers)

        for modifier in self.modifiers:
            data = modifier.modify(options, data)

        map(lambda s: s.set(options, data), self.setters)
        map(lambda w: w.init(options), self.writers)

        for plotter in self.plotters:
            for plotname in plotter.plot(options, data):
                map(lambda w: w.save(options, plotname), self.writers)
        map(lambda w: w.close(options), self.writers)
