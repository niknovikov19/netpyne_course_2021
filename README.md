# netpyne_course_2021

## Project

*Proj_Izh_1cell_test_1.py*  
Test a single Izhikevich neuron

*Proj_Izh_1cell_weight_sel.py*  
Probe various synaptic weights and plot PSP's

*Proj_Izh_1cell_NetStim_xei_1.py*  
Single neuron with two NetStim inputs acting via AMPA and GABAA respectively

*Proj_Izh_1cell_ICnoise_1.py*  
Single neuron with white-noise input acting via IClamp

*Proj_Izh_1cell_SynNoise_1.py*  
Single neuron with white-noise input acting via ExpSynD (a modification of ExpSyn)
Two noise inputs are delivered via AMPA and GABAA respectively
Noise parameters are derived in such a way that the result matches the one of Proj_Izh_1cell_NetStim_xei_1.py

*useful/add_noise_input.py*  
Functions to add white-noise input to a cell compartment (via IClamp or ExpSynD)

*ExpSynD.mod*  
Modified version of ExpSyn with a constant w added to g at each time step
Vector.play() could be used to dynamically control w (thus producing a conductance-based custom input)

*optim_1cell_rxe_rxi*  
Scripts for probing various combinations of two external firing rates  
(external spikes go to a single neuronn via AMPA and GABAA synapses respectively)  
*optim_1cell_rxe_rxi/analyze_batch_res_2.py*  
Plot the result of the batch simulations (firing rate and CV of a neuron)  
*optim_1cell_rxe_rxi/batch_result.png*  
Results of the batch simulation (firing rate and CV)
