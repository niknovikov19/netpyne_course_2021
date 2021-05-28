from netpyne import specs, sim
import matplotlib.pyplot as plt
import numpy as np
from time import time

import sys
sys.path.append('E:/WORK/NP_course/Project/useful')
from add_noise_input import *
from add_osc_input import *

tt0 = time()


netParams = specs.NetParams()
simConfig = specs.SimConfig()


# Parameters

#!nrnivmodl

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

# Numbers of the recurrent inputs
Kee = 50
Kie = 50
Kei = 15
Kii = 15

# Weight of the recurrent inputs
wee = 0.0015
wie = 0.0055
wei = 0.0055
wii = 0.001

'''
# No osc
wee = 0.0015
wie = 0.003
wei = 0.005
wii = 0.001

# Weak osc
wee = 0.0015
wie = 0.0055
wei = 0.0055
wii = 0.001
'''


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

Tsim = 2000
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

# Square pulse input
pulse_t = [1000, 2000]
pulse_amp_e = -0.18
pulse_amp_i = -0.3
netParams.stimSourceParams['SQE'] =  {'type': 'IClamp', 'del': pulse_t[0], 'dur': pulse_t[1]-pulse_t[0], 'amp': pulse_amp_e}
netParams.stimTargetParams['SQE->E'] = {'source': 'SQE', 'sec': 'soma', 'loc': 0.5, 'conds': {'pop':'pop_E'}}
netParams.stimSourceParams['SQI'] =  {'type': 'IClamp', 'del': pulse_t[0], 'dur': pulse_t[1]-pulse_t[0], 'amp': pulse_amp_i}
netParams.stimTargetParams['SQI->I'] = {'source': 'SQI', 'sec': 'soma', 'loc': 0.5, 'conds': {'pop':'pop_I'}}
                
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

hvec = np.ndarray(3*(Ne+Ni), dtype=np.object)
cell_gids = np.array([cell.gid for cell in cells])
m = 0

# Get index of a cell by ist position in a population
def get_cell_id(pop_name, cell_num):
    gid = pops[pop_name].cellGids[cell_num]
    id = np.where(cell_gids == gid)[0][0] 
    return id

# Create X->E inputs
for n in range(Ne):
    id = get_cell_id('pop_E', n)
    hvec[m] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxee, noise_std=sigmaxee, erev=EAMPA, taus=tauAMPA)
    hvec[m+1] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxei, noise_std=sigmaxei, erev=EGABAA, taus=tauGABAA)
    m += 2
    
# Create X->I inputs
for n in range(Ni):
    id = get_cell_id('pop_I', n)
    hvec[m] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxie, noise_std=sigmaxie, erev=EAMPA, taus=tauAMPA)
    hvec[m+1] = add_noise_input_syn(cells[id], 'soma', Tsim, dt, noise_mean=muxii, noise_std=sigmaxii, erev=EGABAA, taus=tauGABAA)
    m += 2

print(f'CREATION TIME = {time()-tt0} s')


# Create oscillatory input
osc_f = 40
osc_A = 0.1
for n in range(Ne):
    id = get_cell_id('pop_E', n)
    hvec[m] = add_osc_input(cells[id], 'soma', Tsim, dt, osc_f, osc_A)
    m += 1


# Run
print('Run...')
tt0 = time()
sim.simulate()
sim.analyze()
print(f'RUN TIME = {time()-tt0} s')


# Visualize the result

sim.analysis.plotRaster(include=['pop_E','pop_I'], spikeHist='None', spikeHistBin=2, popRates=False)
fig, sph = sim.analysis.plotSpikeHist(include=['pop_E','pop_I'], binSize=20, timeRange=[0,Tsim], showFig=True)
#sim.analysis.plotSpikeStats(include=['pop_E', 'pop_I'])


bin_sz = 2

sph = [None]*2
rvec = [None]*2
cc = [None]*2
lags = [None]*2

plt.ioff()
fig0, sph[0] = sim.analysis.plotSpikeHist(include=['pop_E'], binSize=bin_sz, timeRange=[0, pulse_t[0]], showFig=False)
fig1, sph[1] = sim.analysis.plotSpikeHist(include=['pop_E'], binSize=bin_sz, timeRange=[pulse_t[0], pulse_t[1]], showFig=False)
plt.close(fig0); plt.close(fig1)
plt.ion()

for n in range(2):
    rvec[n] = sph[n]['histoData'][0]
    cc[n] = np.correlate(rvec[n], rvec[n], mode='full') / len(rvec[n])
    nbins = len(rvec[n])
    lags[n] = np.arange(-nbins+1, nbins) * bin_sz

plt.figure()
plt.plot(lags[0], cc[0])
plt.plot(lags[1], cc[1])
plt.xlim([-150,150])



