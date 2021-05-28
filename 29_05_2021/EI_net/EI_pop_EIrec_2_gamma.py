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
Ne = 200
Ni = 50

# Synaptic parameters
EAMPA = 0
EGABAA = -70                
tauAMPA = 2
tauGABAA = 5

# Firing rate in the absence of recurrent connections
re0 = 10
ri0 = 24

# Number and weight of the recurrent inpute
Kee = 50
Kie = 50
Kei = 15
Kii = 15
wee = 0.0015
wie = 0.006
wei = 0.01
wii = 0.001

# X->E
rxee = 5000 * 1e-3        # [1/ms]
rxei = 800 * 1e-3         # [1/ms]
wxee = 0.0015
wxei = 0.005

# X->I
rxie = 5000 * 1e-3        # [1/ms]
rxii = 800 * 1e-3         # [1/ms]
wxie = 0.003
wxii = 0.01

# Modify the ext rates to compensate for the recurrent connectivity
rxee_ = rxee - re0 * Kee * wee/wxee * 1e-3
rxie_ = rxie - re0 * Kie * wie/wxie * 1e-3
rxei_ = rxei - ri0 * Kei * wei/wxei * 1e-3
rxii_ = rxii - ri0 * Kii * wii/wxii * 1e-3

Tsim = 500
dt = 0.1


# Populations
netParams.popParams['pop_E'] = {
    "cellType": "PYR",
    "numCells": Ne
}
netParams.popParams['pop_I'] = {
    "cellType": "FS",
    "numCells": Ni
}

# Cell (RS)
netParams.cellParams['PYR'] = {
    "conds": {},
    "secs": {
        "soma": {
            "geom": {"L": 10.0, "nseg": 1, "diam": 10.0, "Ra": 35.4, "cm": 31.831},
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
                
# Cell (FS)
netParams.cellParams['FS'] = {
    "conds": {},
    "secs": {
        "soma": {
            "geom": {"L": 10.0, "nseg": 1, "diam": 10.0, "Ra": 35.4, "cm": 31.831},
            "topol": {},
            "mechs": {},
            "pointps": {
                "Izhi2007b_0": {
                    "mod": "Izhi2007b",
                    "loc": 0.5,
                    "C": 0.2,
                    "k": 1.0,
                    "vr": -55.0,
                    "vt": -40.0,
                    "vpeak": 25.0,
                    "a": 0.2,
                    "b": -2.0,
                    "c": -45.0,
                    "d": -55.0,
                    "Iin": 0.0,
                    "celltype": 5.0,
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
netParams.synMechParams['AMPA']  = {'mod': 'ExpSyn', 'tau': tauAMPA,  'e': EAMPA}
netParams.synMechParams['GABAA'] = {'mod': 'ExpSyn', 'tau': tauGABAA, 'e': EGABAA}

# Connections
netParams.connParams['E->E'] = {
    'preConds': {'pop': 'pop_E'}, 
    'postConds': {'pop': 'pop_E'},
    'convergence': Kee,
    'weight': wee,
    'synMech': 'AMPA',
    'delay': 'uniform(1,1)'}
netParams.connParams['E->I'] = {
    'preConds': {'pop': 'pop_E'}, 
    'postConds': {'pop': 'pop_I'},
    'convergence': Kie,
    'weight': wie,
    'synMech': 'AMPA',
    'delay': 'uniform(1,1)'}
netParams.connParams['I->E'] = {
    'preConds': {'pop': 'pop_I'}, 
    'postConds': {'pop': 'pop_E'},
    'convergence': Kei,
    'weight': wei,
    'synMech': 'GABAA',
    'delay': 'uniform(1,1)'}
netParams.connParams['I->I'] = {
    'preConds': {'pop': 'pop_I'}, 
    'postConds': {'pop': 'pop_I'},
    'convergence': Kii,
    'weight': wii,
    'synMech': 'GABAA',
    'delay': 'uniform(1,1)'}
                
# Simulation params
simConfig.duration = Tsim
simConfig.dt = dt
simConfig.recordTraces = {
    #"V_soma": {'var': 'v', 'sec': 'soma', 'loc': 0.5}
}
simConfig.simLabel = "SIM1"
simConfig.verbose = False  # show detailed messages
simConfig.analysis = {
    #"iplotTraces": {'include': ['all'], 'showFig': 'False'}
    }
                
# Create network
(pops, cells, conns, stims, rxd, simData) = sim.create(netParams, simConfig, output=True)


# Create noise inputs

print('Create external input...')
tt0 = time()

# Mean and std: X->E
muxee = wxee * rxee_
muxei = wxei * rxei_
sigmaxee = wxee * np.sqrt(rxee_ / dt)
sigmaxei = wxei * np.sqrt(rxei_ / dt)

# Mean and std: X->I
muxie = wxie * rxie_
muxii = wxii * rxii_
sigmaxie = wxie * np.sqrt(rxie_ / dt)
sigmaxii = wxii * np.sqrt(rxii_ / dt)

hvec = np.ndarray(2*(Ne+Ni), dtype=np.object)
cell_gids = np.array([cell.gid for cell in cells])
m = 0

# Create X->E inputs
for n in range(Ne):
    gid = pops.pop_E.cellGids[n]
    id = np.where(cell_gids == gid)[0][0]
    hvec[m] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxee, noise_std=sigmaxee, erev=EAMPA, taus=tauAMPA)
    hvec[m+1] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxei, noise_std=sigmaxei, erev=EGABAA, taus=tauGABAA)
    m += 2
    
# Create X->I inputs
for n in range(Ni):
    gid = pops.pop_I.cellGids[n]
    id = np.where(cell_gids == gid)[0][0]
    hvec[m] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxie, noise_std=sigmaxie, erev=EAMPA, taus=tauAMPA)
    hvec[m+1] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxii, noise_std=sigmaxii, erev=EGABAA, taus=tauGABAA)
    m += 2

print(f'CREATION TIME = {time()-tt0} s')


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
sim.analysis.plotSpikeStats(include=['pop_E', 'pop_I'])

'''
from neuron import h
hsec = cells[0].secs['soma']['hObj']
hsyn = h.ExpSynD(hsec(0.5))
'''




