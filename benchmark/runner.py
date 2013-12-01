class Runner(object):
    """docstring for Runner"""
    def __init__(self,
                 name,
                 argsparser,
                 queries = [],
                 patchers = [],
                 writers = [],
                 plotters = []):
        super(Runner, self).__init__()
        self.name = name
        self.argsparser = argsparser
        self.queries = queries
        self.patchers = patchers
        self.writers = writers
        self.plotters = plotters

    def run(self):
        for item in self.queries + \
                    self.patchers + \
                    self.writers + \
                    self.plotters:
            item.add_options(self.argsparser)

        options = self.argsparser.parse_args()

        data = None
        for query in self.queries
            data = query.query(options)
            if data:
                break
        else:
            print('No data found.')
            exit()

        map(lambda p: p.patch(options, data), self.patchers)
        map(lambda w: w.init(options), self.writers)
        for plotter in self.plotters:
            for plotname in plotter.plot(options, data):
                map(lambda w: w.save(plotname), self.writers)
        map(lambda w: w.close(), self.writers)
