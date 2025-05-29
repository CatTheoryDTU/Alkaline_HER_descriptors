from catmap import ReactionModel, analyze
from copy import copy
import numpy as np
import matplotlib.pyplot as plt
from analyze_mkm import *
import argparse, os
parser = argparse.ArgumentParser("test")
parser.add_argument("division",help="")
args=parser.parse_args()
division=int(args.division)
surfaces=['Au','Cu','Pd','Ag','Pt','Rh','Ir','Ni']
lat_consts={'Ag': 4.31,
           'Au': 4.27,
           'Cu':3.74,
           'Ir': 3.90,
           'Ni':3.58,
           'Pd': 4.02,
           'Pt': 4.03,
           'Rh':3.89}
#surfaces=['Pt']
#for metal in surfaces[division*2:(division+1)*2]:
for metal in [surfaces[division]]:
    model = ReactionModel(setup_file = f'results/{metal}/input.mkm')
    model.output_variables+=['production_rate', 'free_energy','coverage','rate_control']
    model.run()
    if True:
        mm=analyze.MatrixMap(model)
        mm.plot_variable = 'rate_control' #tell the model which output to plot
        mm.include_indices=list(range(50000))
        mm.log_scale = False #rates should be plotted on a log-scale
        mm.min = -2 #minimum rate to plot
        mm.max = 2 #maximum rate to plot
        mm.plot(save='%s_rate_control.png'%metal)
    if True:
        ma = analyze.MechanismAnalysis(model)
        ma.energy_type = 'free_energy' #can also be free_energy/potential_energy
        ma.pressure_correction = False #assume all pressures are 1 bar (so that energies are the same as from DFT)
        ma.include_labels = False
        fig = ma.plot(plot_variants=[(-1.5),(-1.0),(-0.5)], save='%s_FED.svg'%metal)
        #print(ma.data_dict)  # contains [energies, barriers] for each rxn_mechanism defined
    coverage=model.coverage_map
    data=[]
    for dat in coverage:
        data.append([dat[0][0],dat[0][1],np.float64(dat[1][0])])
    np.savetxt('results/%s/coverage.dat'%metal,np.array(data),fmt=' '.join(['%1.2f'] + ['%e']*(len(data[0])-1)))
    data=[]
    production=model.production_rate_map
    for dat in production:
        tmp=[dat[0][0],dat[0][1]]
        tmp.extend(np.float64(dat[1]))
        data.append(tmp)
    np.savetxt('results/%s/production.dat'%metal,np.array(data),fmt=' '.join(['%1.2f'] + ['%2.12e']*(len(data[0])-1)))
    # current density
    currentdata=np.array(data)[:,[0,1,3]]
    conversionfactor=1.602 # e/A^2 to mC/cm^2
    area=(3*np.sqrt(0.5))*(4*np.sqrt(0.375))*(lat_consts[metal]**2)
    sites=12
    currentdata[:,2]*=-2*conversionfactor*sites/area
    np.savetxt('results/%s/current.dat'%metal,np.array(currentdata),fmt=' '.join(['%1.2f'] + ['%2.12e']*(len(currentdata[0])-1)))
   # data2=np.array(data)
   # tafel=data2[np.lexsort((data2[:,0],data2[:,1]))]
   # np.savetxt('results/%s/tafel.txt'%metal,np.array(tafel[::-1]),fmt=' '.join(['%1.2f'] +['%e']*(len(tafel[0])-1)))
    data=[]
    production=model.rate_map
    for dat in production:
        tmp=[dat[0][0],dat[0][1]]
        tmp.extend(np.float64(dat[1]))
        data.append(tmp)
    np.savetxt('results/%s/rates.dat'%metal,np.array(data),fmt=' '.join(['%1.2f'] + ['%e']*(len(data[0])-1)))
    #rate control map
    data=[]
    rate_control=model.rate_control_map
    for dat in rate_control:
        tmp=[dat[0][0],dat[0][1]]
        tmp.extend(np.float64(dat[1][0][0:4]))
        tmp.extend(np.float64(dat[1][1][0:4]))
        #tmp.extend(np.float64(dat[1][2][0:4]))
        #tmp.extend(np.float64(dat[1][3][0:4]))
        data.append(tmp)
    np.savetxt('results/%s/rate_control.dat'%metal,np.array(data),fmt=' '.join(['%1.2f'] + ['%2.12e']*(len(data[0])-1)))


