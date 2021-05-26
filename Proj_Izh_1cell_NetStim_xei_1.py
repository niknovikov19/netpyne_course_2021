from netpyne import specs, sim
import matplotlib.pyplot as plt
import numpy as np
from time import time


tt0 = time()


netParams = specs.NetParams()
simConfig = specs.SimConfig()


# Populations
netParams.popParams['pop_PYR'] = {
    "cellType": "PYR",
    "numCells": 1
}

# Cell (RS)
netParams.cellParams['PYR'] = {
    "conds": {},
    "secs": {
        "soma": {
            "geom": {
                "L": 10.0,
                "nseg": 1,
                "diam": 10.0,
                "Ra": 35.4,
                "cm": 31.831
            },
            "topol": {},
            "mechs": {},
            "pointps": {
                "Izhi2007b_0": {
                    "mod": "Izhi2007b",
                    "loc": 0.5,
                    "C": 1.0,
                    "k": 0.7,
                    "vr": -60.0,
                    "vt": -40.0,
                    "vpeak": 35.0,
                    "a": 0.03,
                    "b": -2.0,
                    "c": -50.0,
                    "d": 100.0,
                    "Iin": 0.0,
                    "celltype": 1.0,
                    "alive": 1.0,
                    "cellid": -1.0
                }
            }
        }
    },
    "secLists": {},
    "globals": {}
}
                
# Synapse types
netParams.synMechParams['syn_AMPA'] = {
    "mod": "ExpSyn",
    "tau": 2,
    "e": 0
}
netParams.synMechParams['syn_GABAA'] = {
    "mod": "ExpSyn",
    "tau": 5,
    "e": -70
}

# Source of input spikes
netParams.stimSourceParams['EXT_E'] = {
    "type": "NetStim",
    "rate": 40000,
    "noise": 1
}
netParams.stimSourceParams['EXT_I'] = {
    "type": "NetStim",
    "rate": 3500,
    "noise": 1
}

# Input connections
netParams.stimTargetParams['EXT_E->PYR'] = {
    "source": "EXT_E",
    "conds": {'pop':'pop_PYR'},
    "sec": "soma",
    "synMech": "syn_AMPA",
    "weight": 0.0003,
    "delay": "1"
    }
netParams.stimTargetParams['EXT_I->PYR'] = {
    "source": "EXT_I",
    "conds": {'pop':'pop_PYR'},
    "sec": "soma",
    "synMech": "syn_GABAA",
    "weight": 0.0015,
    "delay": "1"
    }

# Simulation parameters
simConfig.duration = 10000
simConfig.dt = 0.1
simConfig.recordTraces = {
    "V_soma": {'var':'v', 'sec':'soma', 'loc':0.5}
}
simConfig.simLabel = "SIM1"
simConfig.verbose = True  # show detailed messages
simConfig.analysis = {
    "iplotTraces": {'include': ['all'], 'showFig': 'False'}
    }


# Run
tt0 = time()
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)


# Visualize the result
plt.figure()
t = np.array(sim.simData['t'].to_python())
V = sim.simData['V_soma']['cell_0']
plt.plot(t,V)
plt.xlabel('Time')
plt.title('Voltage')
plt.show()


print(f'RUN TIME = {time()-tt0} s')

