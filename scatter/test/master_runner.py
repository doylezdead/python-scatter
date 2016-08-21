import scatter
import time

hostlist = ['localhost',
            '10.100.100.102',
            '10.100.100.103']

m = scatter.Master(hosts=hostlist, kwargs={'val': 300})

m.start(verbose=True)
#time.sleep(3)
m.stop()
