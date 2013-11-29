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

        data_frame = None
        for query in self.queries
            data_frame = query.query(options)
            if data_frame:
                break
        else:
            print('No data found.')
            exit()

        map(lambda p: p.patch(options, data_frame), self.patchers)
        map(lambda w: w.init(options), self.writers)
        for plotter in self.plotters:
            for plot in plotter(options):
                map(lambda w: w.save(), self.writers)
        map(lambda w: w.close(), self.writers)
