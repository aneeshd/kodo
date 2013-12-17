"""
Copyright Steinwurf ApS 2011-2013.
Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
See accompanying file LICENSE.rst or
http://www.steinwurf.com/licensing
"""
import scipy
from matplotlib import pyplot
from component import Component

markers = [
    ('Binary8'  , 'v'),
    ('Binary16' , '^'),
    ('Binary'   , 'o'),
    ('Prime2325', '*')
]

def get_marker(label):

    for field, marker in markers:
        if field in label:
            return marker
    else:
        assert False, '{} not found'.format(field)

class Plotter(Component):
    """docstring for Plotter"""
    def __init__(self, rows, columns, rc_params, ylabel, yscale = 'linear'):
        super(Plotter, self).__init__()
        self.rows = rows
        self.columns = columns
        self.rc_params = rc_params
        self.yscale = yscale
        self.ylabel = ylabel

    def plot(self, data_point):
        (buildername, symbols), group = data_point
        pyplot.rcParams.update(self._get('rc_params'))
        plot = group.pivot_table('mean',
            rows=self._get('rows'),
            cols=self._get('columns')).plot()
        plot.set_title(buildername,
            ha = 'left',
            position = (.0,1.03),
            fontsize = 'medium')
        for line in plot.lines:
            line.set_marker(get_marker(line.get_label()))

        pyplot.legend(bbox_to_anchor=(1., -0.01), loc=3, ncol=1)

        pyplot.ylabel(self._get('ylabel').format(**self.options))
        plot.set_yscale(
            self._get('yscale'))
        pyplot.xticks(list(scipy.unique(group['symbols'])))
        return buildername

class DependencyPlotter(Component):

    def __init__(self, columns, rc_params, ylabel, xlabel):
        super(DependencyPlotter, self).__init__()
        self.columns = columns
        self.rc_params = rc_params
        self.ylabel = ylabel
        self.xlabel = xlabel

    def plot(self, data):
        (buildername, symbol_size, symbols), group = data

        pyplot.rcParams.update(self._get('rc_params'))
        to_zip = [group[c] for c in self._get('columns')]
        for (dep, field, case) in zip(*to_zip):
            pyplot.plot(
                scipy.arange(symbols),
                dep,
                marker = get_marker(field),
                label = "(" + field +", " + str(case) + ")")

        pyplot.title(
            buildername,
            ha = "left",
            position = (.0,1.03),
            fontsize = "medium")

        pyplot.legend(
            bbox_to_anchor=(1., -0.01),
            loc=3,
            ncol=1)

        pyplot.xlabel(self._get('xlabel'))
        pyplot.ylabel(self._get('ylabel'))

        pyplot.xticks(
            symbols - 2**scipy.arange(scipy.log2(symbols))[::-1] ,
                      2**scipy.arange(scipy.log2(symbols),dtype=int)[::-1])

        pyplot.grid('on')
        return buildername

"""
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
"""
