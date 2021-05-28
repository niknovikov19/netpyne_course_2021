from netpyne import specs, sim
import numpy as np
from neuron import h
from time import time


# Create current noise input to a section
def add_osc_input(cell, sec_name, Tsim, dt, f, A, trange=None):

    hsec = cell.secs[sec_name]['hObj']
    
    tvec = np.linspace(0.0, Tsim, int(Tsim/dt))
    htvec = h.Vector(tvec)
    
    if trange is not None:
        t_idx = (tvec >= trange[0]) & (tvec < trange[1])
        osc_vec = np.zeros(len(tvec))
        osc_vec[t_idx] = A * np.sin(2*np.pi*f*(tvec[t_idx]-trange[0])/1000)
    else:    
        osc_vec = A * np.sin(2*np.pi*f*tvec/1000)
    
    hvec = h.Vector()
    hvec.from_python(osc_vec)
    
    hstim = h.IClamp(hsec(0.5))
    hstim.delay = 0.0
    hstim.dur = 1e9
    
    hvec.play(hstim._ref_amp, htvec, True)
    
    return htvec, hvec, hstim

'''
# Create synaptic noise input to a section
def add_noise_input_syn(cell, sec_name, Tsim, dt, noise_mean, noise_std, erev, taus):

    hsec = cell.secs[sec_name]['hObj']
    
    #tt0 = time()
    tvec = np.linspace(0.0, Tsim, int(Tsim/dt))
    htvec = h.Vector(tvec)
    noise_vec = np.random.normal(noise_mean, noise_std, len(tvec))
    hnoise = h.Vector()
    hnoise.from_python(noise_vec)
    #print(f'PREPARE TIME = {time()-tt0} s')
    
    hsyn = h.ExpSynD(hsec(0.5))
    hsyn.e = erev
    hsyn.tau = taus
    
    hnoise.play(hsyn._ref_w, htvec, True)
    
    return htvec, hnoise, hsyn
'''