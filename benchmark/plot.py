for (buildername,symbols), group in sparse:
    pl.rcParams.update({
        'figure.subplot.right': .7 ,
        'figure.subplot.left': .1
    })
    p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'density']).plot()
    ps.set_plot_details(p, buildername)
    pl.ylabel("Extra symbols [" + list(group['unit'])[0] + "]")
    pl.xticks(list(sp.unique(group['symbols'])))

for (buildername,symbols), group in dense:
    pl.rcParams.update({
        'figure.subplot.right': .48 ,
        'figure.subplot.left': .1
    })
    p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'testcase']).plot()
    ps.set_plot_details(p, buildername)
    pl.ylabel("Extra symbols [" + list(group['unit'])[0] + "]")
    pl.xticks(list(sp.unique(group['symbols'])))

for (buildername,symbols), group in sparse:
    pl.rcParams.update({
        'figure.subplot.right': .7 ,
        'figure.subplot.left': .1
    })
    p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'density']).plot()
    ps.set_plot_details(p, buildername)
    pl.ylabel("Overhead [\%]")
    pl.xticks(list(sp.unique(group['symbols'])))
    p.set_yscale('log')

for (buildername,symbols), group in dense:
    pl.rcParams.update({
        'figure.subplot.right': .48 ,
        'figure.subplot.left': .1
    })
    p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'testcase']).plot()
    ps.set_plot_details(p, buildername)
    pl.ylabel("Overhead [\%]")
    pl.xticks(list(sp.unique(group['symbols'])))
    p.set_yscale('log')

for (buildername,symbols), group in sparse:
    pl.rcParams.update({
        'figure.subplot.right': .7 ,
        'figure.subplot.left': .1
    })
    p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'density']).plot()
    ps.set_plot_details(p, buildername)
    pl.ylabel("Throughput [" + list(group['unit'])[0] + "]")
    pl.xticks(list(sp.unique(group['symbols'])))
    p.set_yscale('log')

for (buildername,symbols), group in dense:
    pl.rcParams.update({
        'figure.subplot.right': .48 ,
        'figure.subplot.left': .1
    })
    p = group.pivot_table('mean',  rows='symbols', cols=['benchmark',
        'testcase']).plot()
    ps.set_plot_details(p, buildername)
    pl.ylabel("Throughput [" + list(group['unit'])[0] + "]")
    pl.xticks(list(sp.unique(group['symbols'])))
    p.set_yscale('log')