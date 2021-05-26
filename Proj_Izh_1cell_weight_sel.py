from netpyne import specs, sim
import matplotlib.pyplot as plt
import numpy as np


netParams = specs.NetParams()
simConfig = specs.SimConfig()


# Synaptic weights to probe
w_vec = [0.00015, 0.0003, 0.0005, 0.0015, 0.003, 0.005]
Nw = len(w_vec)

# Populations
netParams.popParams['pop_PYR_AMPA'] = {
    "cellType": "PYR",
    "numCells": Nw
}
netParams.popParams['pop_PYR_GABAA'] = {
    "cellType": "PYR",
    "numCells": Nw
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
netParams.stimSourceParams['EXT'] = {
    "type": "NetStim",
    "rate": 3,
    "noise": 0
}

# Input connections
for n in range(Nw):
    netParams.stimTargetParams[f'EXT->PYR_AMPA{n}'] = {
        "source": "EXT",
        "conds": {'pop':'pop_PYR_AMPA', 'cellList': [n]},
        "sec": "soma",
        "synMech": "syn_AMPA",
        "weight": w_vec[n],
        "delay": "1"
        }
    netParams.stimTargetParams[f'EXT->PYR_GABAA{n}'] = {
        "source": "EXT",
        "conds": {'pop':'pop_PYR_GABAA', 'cellList': [n]},
        "sec": "soma",
        "synMech": "syn_GABAA",
        "weight": w_vec[n],
        "delay": "1"
        }

# Simulation parameters
simConfig.duration = 1000
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
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)


# Visualize the result

plt.figure()

t = np.array(sim.simData['t'].to_python())

Vrest = 60
vtrace_lst = list(sim.simData['V_soma'].values())

for n in range(Nw*2):
    x = np.array(vtrace_lst[n].to_python()) + Vrest
    plt.plot(t, x, label=f'w = {w_vec[n%Nw]:.05f}')
    
plt.xlabel('Time')
plt.title('Voltage')
plt.ylim([-1.5, 1.5])
plt.legend()
plt.show()



