"""

PARSING Tafel barriers from vaccuum vs. aqueous trajectories

"""

import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import math        
from matplotlib import rcParams
import matplotlib.ticker as ticker   
from sklearn.linear_model import LinearRegression
import os

import ase.io 
from ase import Atoms, Atom 
from numpy import sqrt 
from ase.visualize import view 
from ase.io import read,write 








if __name__ == "__main__":
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)

                
    #adsorbate='H'      
    metals_all=['Ag','Al','Au','Cu','Fe','Co','Ni','Ir','Os','Pd','Pt','Re','Rh','Ru','W','Zn']
    
    
    terminations = []
    for metal in metals_all:
        if metal in ['Fe','W']:
            terminations.append('bcc') #'110')
        elif metal in ['Co','Ru','Re','Os','Zn']:
            terminations.append('0001')
        else:
            terminations.append('111')

    reaction='tafel'
    


    """
    search for all vacuum or aqueous tafel trajectories and get barrier. 
    """


    cluster = 'Laptop_Simiam'
    #cluster = 'Niflheim'

    metals = metals_all


    if True: #parsing trajectories.
 
        #look for vacuum trajectories
        vac_barriers=[]
        for i in range(len(metals)):  #always parse the full metal list. Deal with missing data later. 
            metal = metals[i]
            termination = terminations[i]
        
            if cluster=='Niflheim':
                trunk='/home/cat/dmapa/gpaw/dissads/tree/endstates/BEEF-{}/H2/doNEB/'.format(metal)
            elif cluster=='Laptop_Simiam':  #traj files are elsewhere.
                trunk='/Users/sangh/software/her-scripts/dissads/tree/endstates/BEEF-{}/H2/doNEB/'.format(metal)
            trajfile = 'final_path.traj'
            fname = trunk+trajfile
            
            if os.path.isfile(fname):
                print('FOUND traj {} {}'.format(metal,fname))
                traj = ase.io.read(fname+'@:')

                energies = np.array([image.get_potential_energy() for image in traj])  #array won't store in df!!!
                vac_barrier = max(energies) - energies[0]
            else:
                print('combined system traj not found {}'.format(fname))
                print('skipping')  #This avoids NaNs.
                vac_barrier = np.nan 
                #continue
            vac_barriers.append(vac_barrier) 
        
        vac_barriers=np.array(vac_barriers)
        
        df_vac = pd.DataFrame([])
        df_vac['metal'] = metals_all
        df_vac['vacBarrier'] = vac_barriers
        
        fname='CSV/parsed_vacuum_tafel_barriers.csv' 
        print('parsed dataframe is {}'.format(fname))
        print(df_vac)
        df_vac.to_csv(fname,index=False)

       

        #look for aqueous trajectories
        pots = [str('{0:.2f}'.format(pot)   ) for pot in np.arange(2.10,4.50, 0.05)]
        for pot in pots: 
            aqu_barriers=[]
            count=0
            for i in range(len(metals)):  #always parse the full metal list. Deal with missing data later. 
                metal = metals[i]
                termination = terminations[i]
               
                
                print('****************')
                print('METAL {} '.format(metal))
               
                if cluster=='Niflheim':
                    trunk='/home/cat/dmapa/gpaw/alkalinebarriers/{}/{}/{}/pot_{}/'.format(reaction,metal,termination, pot)
                elif cluster=='Laptop_Simiam': #traj files are elsewhere.
                    #trunk='../alkalinebarriers/{}/{}/{}/pot_{}/'.format(reaction,metal,termination, pot)
                    trunk='/Users/sangh/software/her-scripts/alkalinebarriers/{}/{}/{}/pot_{}/'.format(reaction,metal,termination, pot)
                
                trajfile = 'final_path.traj'
                fname = trunk+trajfile
                if os.path.isfile(fname):
                    print('FOUND traj {} {}'.format(metal,fname))
                    traj = ase.io.read(fname+'@:')
                    energies = np.array([image.get_potential_energy() for image in traj])  #array won't store in df!!!
                    aqu_barrier= max(energies) - energies[0]
                    count+=1
                else:
                    print('combined system traj not found {}'.format(fname))
                    print('skipping')  #This avoids NaNs.
                    aqu_barrier = np.nan
                    #continue
                aqu_barriers.append(aqu_barrier) 
                
                
            aqu_barriers=np.array(aqu_barriers)
            

            df = pd.DataFrame([])
            df['metal'] = metals_all
            df['termination'] = terminations
            df['aquBarrier'] = aqu_barriers

            if count > 0 :
                fname='CSV/parsed_aqueous_tafel_barriers_pot{}.csv'.format(pot)
                print('parsed dataframe is {}'.format(fname))
                print(df)
                df.to_csv(fname,index=False)
            
   




