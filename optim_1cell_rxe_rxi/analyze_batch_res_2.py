from batch_analysis_tools import *
import numpy as np
import matplotlib.pyplot as plt

res = readBatchData(dataFolder='batch_rxe_rxi_50x50', batchLabel='rxe_rxi', loadAll=False, saveAll=True, vars=None, maxCombs=None, listCombs=None)

par1_name = res[0][0]['label']
par2_name = res[0][1]['label']

par1_vals = res[0][0]['values']
par2_vals = res[0][1]['values']

N1 = len(par1_vals)
N2 = len(par1_vals)

R = np.zeros((N1,N2))
CV = np.zeros((N1,N2))

for n1 in range(N1):
    for n2 in range(N2):
        
        key = f'_{n1}_{n2}'
        sd = res[1][key]['simData']
    
        # Firing rate
        R[n1,n2] = sd['avgRate']
        
        # CV
        st = np.array(sd['spkt'])
        ISI = st[2:] - st[1:-1]
        CV[n1,n2] = np.std(ISI) / np.mean(ISI)
        
plt.figure()
plt.subplot(1,2,1)
plt.imshow(R.transpose(), extent=[par1_vals[0], par1_vals[-1], par2_vals[0], par2_vals[-1]],\
           origin='lower', aspect='auto', vmin=0, vmax=30)
plt.xlabel(par1_name)
plt.ylabel(par2_name)
plt.title('Firing rate')
plt.colorbar()
plt.subplot(1,2,2)
plt.imshow(CV.transpose(), extent=[par1_vals[0], par1_vals[-1], par2_vals[0], par2_vals[-1]],\
           origin='lower', aspect='auto', vmin=0, vmax=1.5)
plt.xlabel(par1_name)
plt.ylabel(par2_name)
plt.title('CV')
plt.colorbar()
