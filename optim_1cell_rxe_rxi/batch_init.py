import matplotlib
from netpyne import sim

#matplotlib.use('Agg')

# read cfg and netParams from command line arguments if available; otherwise use default
simConfig, netParams = sim.readCmdLineArgs(simConfigDefault='batch_cfg.py', netParamsDefault='batch_netParams.py')

# Create network and run simulation
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)
