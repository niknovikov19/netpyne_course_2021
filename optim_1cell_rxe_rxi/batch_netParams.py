from netpyne import specs, sim

print('==========================================')

try:
	from __main__ import cfg
except:
	from simConfig import cfg

# Network parameters
netParams = specs.NetParams()

# Population (1 cell)
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
    "mod": "Exp2Syn",
    "tau1": 0.1,
    "tau2": 2,
    "e": 0
}
netParams.synMechParams['syn_GABAA'] = {
    "mod": "Exp2Syn",
    "tau1": 0.1,
    "tau2": 5,
    "e": -70
}

# Sources of input spikes
netParams.stimSourceParams['EXT_E'] = {
    "type": "NetStim",
    "rate": cfg.ext_e_r,
    "noise": 1
}
netParams.stimSourceParams['EXT_I'] = {
    "type": "NetStim",
    "rate": cfg.ext_i_r,
    "noise": 1
}

# Input connections
netParams.stimTargetParams['EXT_E->PYR'] = {
    "source": "EXT_E",
    "conds": {'pop': 'pop_PYR'},
    "sec": "soma",
    "synMech": "syn_AMPA",
    "weight": cfg.ext_e_w,
    "delay": "1"
}
netParams.stimTargetParams['EXT_I->PYR'] = {
    "source": "EXT_I",
    "conds": {'pop': 'pop_PYR'},
    "sec": "soma",
    "synMech": "syn_GABAA",
    "weight": cfg.ext_i_w,
    "delay": "1"
}


print(f'cfg.ext_e_r = {cfg.ext_e_r:.01f}')
print(f'cfg.ext_i_r = {cfg.ext_i_r:.01f}')


