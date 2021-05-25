from netpyne import specs, sim
import matplotlib.pyplot as plt
import numpy as np


netParams = specs.NetParams()
simConfig = specs.SimConfig()


# NETWORK ATTRIBUTES -----------------------------------------------------------
netParams.popParams['pop_PYR'] = {
    "cellType": "PYR",
    "numCells": 1
}
netParams.cellParams['PYR'] = {
    "conds": {},
    "secs": {
        "sec": {
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
netParams.synMechParams['exc'] = {
    "mod": "Exp2Syn",
    "tau1": 0.1,
    "tau2": 5,
    "e": 0
}
netParams.stimSourceParams['NS1'] = {
    "type": "NetStim",
    "rate": 50,
    "noise": 0.5
}
netParams.stimTargetParams['NS1->PYR'] = {
    "source": "NS1",
    "conds": {},
    "sec": "PYR",
    "synMech": "exc",
    "weight": "0.005",
    "delay": "5"
}

# NETWORK CONFIGURATION --------------------------------------------------------
simConfig.duration = 1000
simConfig.dt = 0.1
simConfig.recordTraces = {
    "V_soma": {
        "sec": "sec",
        "loc": 0.5,
        "var": "v"
    }
}
simConfig.simLabel = "SIM1"
simConfig.verbose = True  # show detailed messages
simConfig.analysis = {
    "iplotTraces": {
        "include": [
            "all"
        ],
        "showFig": False,
        "theme": "gui"
    }
}

# CREATE SIMULATE ANALYZE  NETWORK ---------------------------------------------
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)


# Visualize the result
t = np.array(sim.simData['t'].to_python())
x = np.array(sim.simData['V_soma']['cell_0'].to_python())
plt.figure()
plt.plot(t,x)
plt.xlabel('Time')
plt.title('Voltage')



