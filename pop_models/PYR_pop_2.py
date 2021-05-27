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

# Number of cells
N = 200

# Synaptic parameters
EAMPA = 0
EGABAA = -70                
tauAMPA = 2
tauGABAA = 5

# Firing rate in the absence of recurrent connections
r0 = 10

# Number and weight of the recurrent inpute
K = 50
w = 0.0015

# External input rates and weights
rxe = 5000 * 1e-3        # [1/ms]
rxi = 800 * 1e-3         # [1/ms]
wxe = 0.0015
wxi = 0.005

# Modify the ext rates to compensate for the recurrent connectivity
rxe_ = rxe - r0 * K * w/wxe * 1e-3
rxi_ = rxi

Tsim = 1000
dt = 0.1


# Population
netParams.popParams['pop_PYR'] = {
    "cellType": "PYR",
    "numCells": N
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

# Synaptic mechanisms
netParams.synMechParams['AMPA'] = {'mod': 'ExpSyn', 'tau': tauAMPA, 'e': EAMPA}

# Connections
netParams.connParams['PYR->PYR'] = {
    'preConds': {'pop': 'pop_PYR'}, 
    'postConds': {'pop': 'pop_PYR'},
    'convergence': K,
    'weight': w,
    'synMech': 'AMPA',
    'delay': 'uniform(1,1)'}
                
# Simulation params
simConfig.duration = Tsim
simConfig.dt = dt
simConfig.recordTraces = {
    "V_soma": {'var': 'v', 'sec': 'soma', 'loc': 0.5}
}
simConfig.simLabel = "SIM1"
simConfig.verbose = False  # show detailed messages
simConfig.analysis = {
    "iplotTraces": {'include': ['all'], 'showFig': 'False'}
    }
                
# Create network
(pops, cells, conns, stims, rxd, simData) = sim.create(netParams, simConfig, output=True)

# Create noise input
print('Create external input...')
tt0 = time()
muxe = wxe * rxe_
muxi = wxi * rxi_
sigmaxe = wxe * np.sqrt(rxe_ / dt)
sigmaxi = wxi * np.sqrt(rxi_ / dt)
he_vec = np.ndarray(N, dtype=np.object)
hi_vec = np.ndarray(N, dtype=np.object)
for n in range(N):
    he_vec[n] =\
        add_noise_input_syn(cells[n], 'soma', Tsim, dt, noise_mean=muxe, noise_std=sigmaxe, erev=EAMPA, taus=tauAMPA)
    hi_vec[n] =\
        add_noise_input_syn(cells[n], 'soma', Tsim, dt, noise_mean=muxi, noise_std=sigmaxi, erev=EGABAA, taus=tauGABAA)
print(f'CREATION TIME = {time()-tt0} s')

'''
rxe = 14000 * 1e-3        # [1/ms]
rxi = 1300 * 1e-3         # [1/ms]
wxe = 0.0015
wxi = 0.005
'''


# Run
print('Run...')
tt0 = time()
sim.simulate()
sim.analyze()
print(f'RUN TIME = {time()-tt0} s')


# Visualize the result

'''
t = np.array(sim.simData['t'].to_python())
x = np.array(sim.simData['V_soma']['cell_0'].to_python())
plt.figure()
plt.plot(t,x)
plt.xlabel('Time')
plt.title('Voltage')
'''

sim.analysis.plotRaster();

'''
from neuron import h
hsec = cells[0].secs['soma']['hObj']
hsyn = h.ExpSynD(hsec(0.5))
'''




