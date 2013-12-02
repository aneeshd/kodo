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
                 writers = [],
                 plotters = []):
        super(Runner, self).__init__()
        self.name = name
        self.argsparser = argsparser
        self.sources = sources
        self.modifiers = modifiers
        self.patchers = patchers
        self.writers = writers
        self.plotters = plotters

    def run(self):
        for item in self.sources + \
                    self.patchers + \
                    self.modifiers + \
                    self.writers + \
                    self.plotters:
            item.add_options(self.argsparser)

        options = self.argsparser.parse_args()

        data = None
        for source in self.sources
            data = source.get_data(options)
            if data:
                break
        else:
            print('No data found.')
            exit()

        map(lambda p: p.patch(options, data), self.patchers)

        for modifier in self.modifiers
            data = modifier.modify(options, data)

        map(lambda w: w.init(options), self.writers)
        for plotter in self.plotters:
            for plotname in plotter.plot(options, data):
                map(lambda w: w.save(plotname), self.writers)
        map(lambda w: w.close(), self.writers)


# runners
parser = argparse.ArgumentParser(description = 'Plot the benchmark data')
decoding_probability = Runner(
    name = 'decoding_probability',
    argsparser = parser,
    sources = [],
    patchers = [],
    writers = [],
    plotters = [])

