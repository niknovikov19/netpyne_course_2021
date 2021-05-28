import numpy as np
import matplotlib.pyplot as plt
from netpyne import sim


# Calculate firing rate vector
def calc_rvec(pop_name, bin_sz, t_range):
    plt.ioff()
    fig, sph = sim.analysis.plotSpikeHist(include=[pop_name], binSize=bin_sz, timeRange=t_range, showFig=False)
    plt.close(fig);
    plt.ion()
    rvec = sph['histoData'][0]
    tvec = sph['histoT']
    return rvec, tvec

# Calculate autocorrelation of a firing rate vector
def calc_rvec_autocorr(rvec, bin_sz):
    cc = np.correlate(rvec, rvec, mode='full') / len(rvec)
    nbins = len(rvec)
    lags = np.arange(-nbins+1, nbins) * bin_sz
    return cc, lags

# Smooth data over time
def smooth_data(x, t=None, win_len=0, need_trim=False):
    
    if win_len==0:
        return t.copy(), x.copy()
    
    # Kernel
    w = np.ones(win_len,'d')
    w = w / w.sum()

    if need_trim:
        x1 = np.convolve(w, x, mode='valid')
    else:
        x1 = np.convolve(w, x, mode='same')
    
    if t is None:
        t1 = range(len(x1))    
    elif need_trim:
        t1 = t[win_len-1:]
    else:
        t1 = t.copy()
        
    return x1, t1