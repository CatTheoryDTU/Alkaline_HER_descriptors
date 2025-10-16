import numpy as np
from scipy.stats import linregress
import json
import ase.db
Hads_db=ase.db.connect('Hads.db')
OHads_db=ase.db.connect('OHads.db')

#surfaces=['Au','Cu','Pd','Ag','Pt','Rh','Ir','Ni'] old order
surfaces=['Ag','Au','Cu','Ir','Ni','Pd','Pt','Rh']
potentials=np.linspace(2.40,4.40,5)
potentials_interp=np.insert(potentials,[1,2],[2.65,3.15])
G_H=-8.028954481677093/2
G_OH=-27.292351322074335-G_H
#new vibrations from Pt
#slab 0.632
#Hads 0.729 
#heyrovsky 0.605 
#tafel 0.918 
#volmer 0.430 
vib_H=0.729-0.632
vib_volmer=0.430-0.632
vib_tafel=0.918-0.632
vib_heyrovsky=0.605-0.632
vib_OH=0.972-0.632
#process and fit
coverage_params=np.loadtxt('33_interactions_diff.txt')
for idx,metal in enumerate(surfaces):
    volmerIS=np.loadtxt('data/volmer/%s/IS.txt'%metal)
    volmerTS=np.loadtxt('data/volmer/%s/TS.txt'%metal)
#
    heyrovskyIS=np.loadtxt('data/heyrovsky/%s/IS.txt'%metal)
    heyrovskyTS=np.loadtxt('data/heyrovsky/%s/TS.txt'%metal)
#
    tafelIS=np.loadtxt('data/tafel/%s/IS.txt'%metal)
    tafelTS=np.loadtxt('data/tafel/%s/TS.txt'%metal)
#
    mask_Hads=np.in1d(np.around(volmerIS[:,0],3),np.around(heyrovskyIS[:,0],3)) #assuming volmer is more complete
    pot_volmer=np.intersect1d(np.around(potentials_interp,3),np.around(volmerTS[:,0],3))-4.40
    pot_tafel=np.intersect1d(np.around(potentials,3),np.around(tafelTS[:,0],3))-4.40
    pot_heyrovsky=np.intersect1d(np.around(potentials,3),np.around(heyrovskyTS[:,0],3))-4.40
#
    clean=Hads_db.get(Element=metal,State='clean').energy
    H_min=Hads_db.get(Element=metal,State='Hfcc').energy
    OH_min=OHads_db.get(Element=metal,State='OHhcp').energy
    if metal == 'Ir':
        H_min=Hads_db.get(Element=metal,State='Htop').energy
        H_min+=0.105 #top site vibration difference
    Hads=H_min-clean-G_H+vib_H
    OHads=OH_min-clean-G_OH+vib_OH
    volmer_barrier=volmerTS[:,1]-volmerIS[:,1]+vib_volmer
    tafel_barrier=tafelTS[:,1]-volmerIS[mask_Hads][:,1]+vib_tafel-2*G_H
    heyrovsky_barrier=heyrovskyTS[:,1]-volmerIS[mask_Hads][:,1]+vib_heyrovsky-G_H
    np.savetxt('data/volmer/%s/free_energy.txt'%metal,np.vstack(
        (pot_volmer,volmer_barrier)).transpose())
    np.savetxt('data/tafel/%s/free_energy.txt'%metal,np.vstack(
        (pot_tafel,tafelTS[:,1]-tafelIS[:,1]+(vib_tafel-2*vib_H))).transpose())
    np.savetxt('data/heyrovsky/%s/free_energy.txt'%metal,np.vstack(
        (pot_heyrovsky,heyrovskyTS[:,1]-heyrovskyIS[:,1]+(vib_heyrovsky-vib_H))).transpose())
#
    volmerfit=linregress(pot_volmer,volmer_barrier)
    tafelfit=linregress(pot_tafel,tafel_barrier)
    tafel_average=np.mean(tafel_barrier)
    heyrovskyfit=linregress(pot_heyrovsky,heyrovsky_barrier)
#
    volmerTSfit=linregress(pot_volmer,volmer_barrier)
    tafelTSfit=linregress(pot_tafel,tafelTS[:,1]-tafelIS[:,1]+(vib_tafel-2*vib_H))
    tafelTS_average=np.mean(tafelTS[:,1]-tafelIS[:,1]+(vib_tafel-2*vib_H))
    heyrovskyTSfit=linregress(pot_heyrovsky,heyrovskyTS[:,1]-heyrovskyIS[:,1]+(vib_heyrovsky-vib_H))
    if metal in ['Au','Pt']:
    #heyrovsky IS for Au,Pt here is in the top site, hollow is lower by around 0.1 eV, making the activation energy greater by 0.1 eV
        heyrovsky_site_correction=0.1
        heyrovskyTSfit=linregress(pot_heyrovsky,heyrovskyTS[:,1]-heyrovskyIS[:,1]+heyrovsky_site_correction+(vib_heyrovsky-vib_H))
        np.savetxt('data/heyrovsky/%s/free_energy.txt'%metal,np.vstack(
            (pot_heyrovsky,heyrovskyTS[:,1]-heyrovskyIS[:,1]+heyrovsky_site_correction+(vib_heyrovsky-vib_H))).transpose())
    if metal in ['Ir']:
    #heyrovsky IS for Ir is top, but we want to compare them all from same state
        heyrovsky_site_correction=0.18 #for Ir
        heyrovskyTSfit=linregress(pot_heyrovsky,heyrovskyTS[:,1]-heyrovskyIS[:,1]+heyrovsky_site_correction+(vib_heyrovsky-vib_H))
        np.savetxt('data/heyrovsky/%s/free_energy.txt'%metal,np.vstack(
            (pot_heyrovsky,heyrovskyTS[:,1]-heyrovskyIS[:,1]+heyrovsky_site_correction+(vib_heyrovsky-vib_H))).transpose())
    #correlation change miniscule with these corrections
    if metal in ['Ni','Au']:
    # exclude too oxidized points from Ni and Au. Does not do much
        volmer_barrier=volmerTS[0:5,1]-volmerIS[0:5,1]+vib_volmer
        volmerfit=linregress(pot_volmer[0:5],volmer_barrier)
        volmerTSfit=linregress(pot_volmer[0:5],volmer_barrier)
        np.savetxt('data/volmer/%s/free_energy.txt'%metal,np.vstack(
            (pot_volmer[0:5],volmer_barrier[0:5])).transpose())
   # cov=coverage_params[idx] # use normal values
    cov=[0.0,0.188] # Katharina
    #confusing, barrier in jsons are actually activation free energies, leaving as is
    results_dictionary= {
            'volmer':{
                'energy':volmerfit.intercept,
                'beta':volmerfit.slope,
                'fit':volmerfit.rvalue**2,
                'barrier':volmerTSfit.intercept,
                'barrier_beta':volmerTSfit.slope,
                'potentials':str(pot_volmer+4.40)
                },
            'tafel':{
                'energy':tafel_average,
                'beta':tafelfit.slope,
                'fit':tafelfit.rvalue**2,
                'barrier':tafelTS_average,
                'barrier_beta':tafelTSfit.slope,
                'potentials':str(pot_tafel+4.40)
                },
            'heyrovsky':{
                'energy':heyrovskyfit.intercept,
                'beta':heyrovskyfit.slope,
                'fit':heyrovskyfit.rvalue**2,
                'barrier':heyrovskyTSfit.intercept,
                'barrier_beta':heyrovskyTSfit.slope,
                'potentials':str(pot_heyrovsky+4.40)
                },
            'Hydrogen':{
                'energy':Hads,
                'cutoff':cov[0],
                'interaction':cov[1],
                },
            }
    json.dump(results_dictionary,open('results/%s/results.json'%metal,'w'),indent=3)
