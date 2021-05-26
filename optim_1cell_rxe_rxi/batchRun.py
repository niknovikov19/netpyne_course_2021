from netpyne import specs
from netpyne.batch import Batch
from time import time
import numpy as np


# Create variable of type ordered dictionary (NetPyNE's customized version)
params = specs.ODict()

# Param range to explore
#params['ext_e_r'] = [25000, 50000, 75000, 100000]
#params['ext_i_r'] = [1000, 2000, 3000, 4000, 5000]
#params['ext_e_r'] = [75000, 100000]
#params['ext_i_r'] = [3000, 3500, 4000, 4500, 5000]
#params['ext_e_r'] = [100000]
#params['ext_i_r'] = [3500]
params['ext_e_r'] = np.linspace(5*1e4, 10*1e4, 51).tolist()
params['ext_i_r'] = np.linspace(2*1e3, 5*1e3, 51).tolist()

# create Batch object with parameters to modify, and specifying files to use
b = Batch(params=params, cfgFile='batch_cfg.py', netParamsFile='batch_netParams.py')

# Set output folder, grid method (all param combinations), and run configuration
b.batchLabel = 'rxe_rxi'
b.saveFolder = 'batch_rxe_rxi'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'batch_init.py', 'skip': False}

# Run batch simulations
t = time()
b.run()
dt = time() - t
print(f'Time: {dt} s')
