from netpyne import specs


cfg = specs.SimConfig()


# Variable parameters

# Wights of external exc / inh inputs
cfg.ext_e_w = 0.0003
cfg.ext_i_w = 0.0015

# Rates external exc / inh inputs
cfg.ext_e_r = 1000
cfg.ext_i_r = 1000


# Simulation setup

cfg.duration = 10000         # Duration of the simulation, in ms
cfg.dt = 0.1                # Internal integration timestep to use
cfg.verbose = False         # Show detailed messages
#cfg.recordTraces = {'V_soma': {'sec':'soma', 'loc':0.5, 'var': 'v'}}  
#cfg.recordStep = 0.1        # Step size in ms to save data (eg. V traces, LFP, etc)
cfg.filename = 'rxe_rxi_'  # Set file output name
cfg.saveJson = True
cfg.printPopAvgRates = True
#cfg.analysis['plotRaster'] = {'saveFig': True}                       # Plot a raster
#cfg.analysis['plotTraces'] = {'include': [0], 'saveFig': False}   # Plot traces

cfg.saveDataInclude = ['simData', 'simConfig', 'netParams', 'net']
