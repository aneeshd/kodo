"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""

class Plotter(object):
    """docstring for Plotter"""
    def __init__(self, rows, cols, rc_params, ylabel, yscale = 'linear'):
        super(Plotter, self).__init__()
        self.rows = rows
        self.cols = cols
        self.rc_params = rc_params
        self.yscale = yscale
        self.ylabel = ylabel

    def add_option(self, parser):
        pass

    def plot(self, options, data):
        for (buildername, symbols), group in data:
            pyplot.rcParams.update(self.rc_params)
            plot = group.pivot_table('mean',
                rows=self.rows,
                cols=self.cols).plot()
            plot.set_title(buildername,
                ha = "left",
                position = (.0,1.03),
                fontsize = "medium")
            for line in plot.lines:
                marker = None
                if "Binary8" in line.get_label():
                    marker = "v"
                elif "Binary16" in line.get_label():
                    marker ="^"
                elif "Binary" in line.get_label():
                    marker = "o"
                elif "Prime2325" in line.get_label():
                    marker = "*"

                if marker:
                    line.set_marker(marker)
                else:
                    print '{} not found'.format(line.get_label())
                    exit()

            pyplot.legend(bbox_to_anchor=(1., -0.01), loc=3, ncol=1)

            pyplot.ylabel(self.ylabel.format(**group))
            pyplot.set_yscale(self.yscale)
            pyplot.xticks(list(sp.unique(group['symbols'])))
            yield buildername


class DependencyPlotter(object):
    """docstring for DependencyPlotter"""
    def __init__(self):
        super(DependencyPlotter, self).__init__()

    def add_option(self, parser):
        pass

    def plot(self, options, data):
        pass

#dependency
#sparse
for (buildername, symbol_size, symbols), group in sparse:

    #Verbose plotting since due to no pandas support for plotting of vectors
    pl.figure()
    ps.set_sparse_plot()
    for (deps, field,density) in zip(group['dependency'],
        group['benchmark'], group['density']):
        pl.plot(sp.arange(symbols), deps, marker = ps.markers(field),
            label = "(" + field +", " + str(density) + ")")

    pl.title(buildername, ha = "left", position = (.0,1.03),
        fontsize = "medium")
    ps.set_legend()
    pl.xlabel("Rank Defeciency")
    pl.ylabel("Extra Packets")
    pl.xticks( symbols-2**sp.arange(sp.log2(symbols))[::-1] ,
        2**sp.arange(sp.log2(symbols),dtype=int)[::-1])
    pl.grid('on')
#dense
for (buildername, symbol_size, symbols), group in dense:

    #Verbose plotting since due to no pandas support for plotting of vectors
    pl.figure()
    ps.set_dense_plot()
    for (deps, field,testcase) in zip(group['dependency'],
        group['benchmark'], group['testcase']):
        pl.plot(sp.arange(symbols), deps, marker = ps.markers(field),
            label = "(" + field +", " + testcase + ")")

    pl.title(buildername, ha = "left", position = (.0,1.03),
        fontsize = "medium")
    ps.set_legend()
    pl.xlabel("Rank Defeciency")
    pl.ylabel("Extra Packets")
    pl.xticks( symbols-2**sp.arange(sp.log2(symbols))[::-1],
        2**sp.arange(sp.log2(symbols),dtype=int)[::-1])
    pl.grid('on')


#comparision
for buildername, group in groups:
    # Group all results from the most recent master build
    master_group = group[sp.array(group['branch'] == "master")]
    group[group['branch'] == "master"]
    if len(master_group) == 0:
        print "Skipping " + buildername + " as no nightly benchmark results \
            exists for the master for this buider yet"
        continue
    master_group = master_group[master_group['buildnumber'] == \
        max(master_group['buildnumber'])]

    # Group all other results by branch
    branches_group = group[group['branch'] != "master"].groupby(by = ['branch'])

    for branch, branch_group in branches_group:
        PATH_BRANCH  = PATH + (branch ).replace("-","_")

        # Calculate the difference compared to master of the latest build
        branch_group = branch_group[branch_group["buildnumber"] \
            == max(branch_group['buildnumber'])]
        branch_group['gain'] = (sp.array(branch_group['mean']) - \
            sp.array(master_group['mean']) ) / sp.array(master_group['mean'])*100

        # Group by type of code; dense, sparse
        dense = branch_group[branch_group['testcase'] != \
            "SparseFullRLNC"].groupby(by= ['symbol_size'])
        sparse = branch_group[branch_group['testcase'] == \
            "SparseFullRLNC"].groupby(by= ['symbol_size'])

        for key, g in sparse:
            ps.set_sparse_plot()
            p = g.pivot_table('gain',  rows='symbols', cols=['benchmark',
                'density']).plot()
            ps.set_plot_details(p, buildername)
            pl.ylabel("Throughput gain [\%]")
            pl.xticks(list(sp.unique(group['symbols'])))
            pl.savefig(PATH_BRANCH + "/sparse/" + buildername + "." + format)
            pdf[branch].savefig(transparent=True)

        for key, g in dense:
            ps.set_dense_plot()
            p = g.pivot_table('gain',  rows='symbols',
                cols=['benchmark','testcase']).plot()
            ps.set_plot_details(p, buildername)
            pl.ylabel("Throughput gain [\%]")
            pl.xticks(list(sp.unique(group['symbols'])))
            pl.savefig(PATH_BRANCH + "/dense/" + buildername + "." + format)
            pdf[branch].savefig(transparent=True)