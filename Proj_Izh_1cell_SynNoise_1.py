from netpyne import specs, sim
import matplotlib.pyplot as plt
import numpy as np
from time import time

import sys
sys.path.append('E:/WORK/NP_course/Project/useful')
from add_noise_input import *


tt0 = time()


netParams = specs.NetParams()
simConfig = specs.SimConfig()


# Parameters
Tsim = 10000
dt = 0.1


# Population
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
                
# Simulation params
simConfig.duration = Tsim
simConfig.dt = dt
simConfig.recordTraces = {
    "V_soma": {'var':'v', 'sec':'soma', 'loc':0.5}
}
simConfig.simLabel = "SIM1"
simConfig.verbose = True  # show detailed messages
simConfig.analysis = {
    "iplotTraces": {'include': ['all'], 'showFig': 'False'}
    }
                
# Create network
(pops, cells, conns, stims, rxd, simData) = sim.create(netParams, simConfig, output=True)

# Create noise input
rxe = 40000 * 1e-3        # [1/ms]
rxi = 3500 * 1e-3       # [1/ms]
wxe = 0.0003
wxi = 0.0015
muxe = wxe * rxe
muxi = wxi * rxi
sigmaxe = wxe * np.sqrt(rxe / dt)
sigmaxi = wxi * np.sqrt(rxi / dt)
htvec_e, hnoise_e, hsyn_e =\
    add_noise_input_syn(cells[0], 'soma', Tsim, dt, noise_mean=muxe, noise_std=sigmaxe, erev=0, taus=2)
htvec_i, hnoise_i, hsyn_i =\
    add_noise_input_syn(cells[0], 'soma', Tsim, dt, noise_mean=muxi, noise_std=sigmaxi, erev=-70, taus=5)

# Run
tt0 = time()
sim.simulate()
sim.analyze()


# Visualize the result
t = np.array(sim.simData['t'].to_python())
x = np.array(sim.simData['V_soma']['cell_0'].to_python())
plt.figure()
plt.plot(t,x)
plt.xlabel('Time')
plt.title('Voltage')


'''
from neuron import h
hsec = cells[0].secs['soma']['hObj']
hsyn = h.ExpSynD(hsec(0.5))
'''


print(f'RUN TIME = {time()-tt0} s')

