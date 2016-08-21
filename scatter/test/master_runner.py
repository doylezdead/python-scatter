import scatter

hostlist = ['localhost',
            '10.100.100.102',
            '10.100.100.103']

m = scatter.Master(hosts=hostlist)

m.start(verbose=True)
