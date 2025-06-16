"""

Tafel barriers vac. vs. aqueous trajectories

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




def plot_scatter(xvals, yvals,metals, xlabel, ylabel,xkey,ykey) :
    print(' ')
    #print('{} {} {} {} {} {} {} {}'.format( spin,mtag,dindex,site,zval,xkey,ykey,adsorbate))
    print('plotting y {} vs x{} '.format( ykey,xkey))

    lrbt=[0.3,0.95,0.2,0.95]
    rcParams['figure.subplot.left'] = lrbt[0]  
    rcParams['figure.subplot.right'] = lrbt[1] 
    rcParams['figure.subplot.bottom'] = lrbt[2]
    rcParams['figure.subplot.top'] = lrbt[3] #
    
    fig, ax = plt.subplots(1,1, figsize=(2.5,2.5)) 
    
    ax.set_box_aspect(1)
    ax.tick_params(axis='y',direction='in',which='both',left=True, right=False, labelleft='on')
    ax.tick_params(axis='x',direction='in',which='both',bottom=True, top=False, labelbottom='on')
    
    
    sp=0.5
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=sp, hspace=sp)


    #metal ordering careful!
    #the yvals determine the available metals list.


   

    #exclude W:
    #subset=range(len(metals))#-1)
    #Check for NaN
    #FILTER NANs
    #CURATE A SUBSET.
    subset  =[]
    excluded_from_regression=[] #'Al','Zn']
    exclude = [] #['Al','Zn']
    for i in range(len(metals)):
        if math.isnan(xvals[i]) or math.isnan(yvals[i]) or metals[i] in exclude: 
            print('dropping NaN at index {} which is metal {}'.format(i,metals[i]))
            excluded_from_regression.append(metals[i])
            continue
        else:
            subset.append(i)
    print('subset of good values is {}'.format(subset))


    if True:
        yvals= yvals.reshape((-1, 1))
        xvals = xvals.reshape((-1, 1))
    
    print('xvals shape {}'.format(xvals.shape))



    if True:

        #NEW: plot df columns. do LR in pandas. Doesn't really work though? 

        #ax.scatter(xvals, yvals,s=5, color='black')
        ax.scatter(xvals[subset],yvals[subset],s=5, color='black')
        
        arsize=4
        #dx,dy=(0.1,0.01)
        dx,dy=(0.0,0.01)
        
        for i in subset: #range(xvals.shape[0]):
            ax.annotate('{}{}'.format(metals[i],terminations[i]), xy=(xvals[i]+dx,yvals[i]+dy),
                        fontsize=arsize,ha='center',textcoords='data',
                        color="k",annotation_clip=False)                      
        
        capcoord=(-0.2,-0.3)
        #ax.annotate('a)', xy=capcoord,ha='center',
        #                  xycoords = ('axes fraction'), 
        #                  textcoords=('axes fraction'),
        #                  color="k",annotation_clip=False) 
        
        

        SKregression = True
        PDregression = False
        
        #Another subset for regression.
        subset1 = []
        for i in subset:
            if metals[i] in excluded_from_regression:
                continue
            else: subset1.append(i)
        subset = subset1

        if SKregression: 
            LR = LinearRegression().fit(xvals[subset],yvals[subset])
            r_sq = LR.score(xvals[subset],yvals[subset]) 
            print('coefficient of determination:', r_sq)
            print('intercept:', LR.intercept_)
            print('slope:', LR.coef_)
            stringlabel=r'R$^2$:'+' {}'.format(round(r_sq,2))
            r2duplet=(0.4,0.9)
            afsize=5
            ax.annotate('{}'.format(stringlabel), xy=r2duplet,ha='center',
                            xycoords = ('axes fraction'), 
                            textcoords=('axes fraction'),
                            color="blue",annotation_clip=False,fontsize=afsize)     
            string2label='y={}x+{}'.format(round(LR.coef_[0][0],2), round(LR.intercept_[0],2))
            r2duplet=(0.4,0.85)
            ax.annotate('{}'.format(string2label), xy=r2duplet,ha='center',
                            xycoords = ('axes fraction'), 
                            textcoords=('axes fraction'),
                            color="blue",annotation_clip=False,
                            fontsize=afsize)     
            #plot the linear fit please:
            sorted_xvals = np.sort( np.array([xvals[i][0] for i in subset])).reshape(-1, 1)
            print('xvals {}'.format(xvals))
            print('sorted_xvals {}'.format(sorted_xvals))

            y_pred = LR.predict(sorted_xvals)
            ax.plot(sorted_xvals,y_pred,lw=1, linestyle='--',color='black',zorder=0 )
                    
            capcoord=(0.40,-0.3)
            
            if False:
                ax.annotate('R2 Excludes: {}'.format(excluded_from_regression), xy=capcoord,ha='center', fontsize=arsize,
                                xycoords = ('axes fraction'), textcoords=('axes fraction') ,color="k",annotation_clip=False)                      
            elif True: #if False:
                ax.annotate('Not found: {}'.format(excluded_from_regression), xy=capcoord,ha='center', fontsize=arsize,
                                xycoords = ('axes fraction'), textcoords=('axes fraction') ,color="k",annotation_clip=False)                      
        
        if PDregression:
            dummy=1





        
        fs=6
        ax.set_xlabel(xlabel,fontsize=fs) 
        ax.set_ylabel(ylabel,fontsize=fs) 
    
   
    figname='{}_vs_{}_reg{}'.format(ykey,xkey,SKregression)

    #if xkey == 'wdos':
    #    figname+='_{}pm_dindex{}{}'.format(zval,dindex,mtag) 
    

    print('plotting {}'.format(figname))
    plt.savefig('output/'+figname+'.png',dpi=300)

    return None







if __name__ == "__main__":
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)

    #LOAD INPUTS
    #TM = pd.read_csv('../analysis_general/CSV/TM_parameters.csv')
    TM = pd.read_csv('CSV/TM_parameters.csv')
                
    #adsorbate='H'      
    metals_all=['Ag','Al','Au','Cu','Fe','Co','Ni','Ir','Os','Pd','Pt','Re','Rh','Ru','W','Zn']
    
    #a subset to compare vac vs. aqu tafel runs:
    #metals_all=['Ag','Au','Cu','Ni','Ir','Pt','Rh']  #vacuum tafel: we excluded the wrong trajs and W for now. 
    
    terminations = []
    for metal in metals_all:
        if metal in ['Fe','W']:
            terminations.append('bcc') #'110')
        elif metal in ['Co','Ru','Re','Os','Zn']:
            terminations.append('0001')
        else:
            terminations.append('111')

    #There are different datasets of barriers, containing also different subsets of metals_all.
    
    #bflags = ['aqutraj','vactraj','Hammer'] 
    reaction='tafel'
    
    #if bflag == 'aqutraj':
    pots = [str('{0:.2f}'.format(pot)   ) for pot in np.arange(2.10,4.50, 0.05)]
    #elif bflag == 'vactraj':
    #    pots=['NONE']
    #elif bflag == 'Hammer': #lookup original Hammer DFT barriers.
    #    pots=['NONE']


    """
    search for all vacuum or aqueous tafel trajectories and get barrier. 
    """


    metals = metals_all

    #pots = ['3.40']

    for pot in pots:
        aqu_barriers=[]
        vac_barriers=[]
        count=0
        for i in range(len(metals)):  #always parse the full metal list. Deal with missing data later. 
            metal = metals[i]
            termination = terminations[i]
           
            
            print('****************')
            print('METAL {} '.format(metal))
           
            trunk='../alkalinebarriers/{}/{}/{}/pot_{}/'.format(reaction,metal,termination, pot)
            ylabel=r'$\Delta E^{\ddagger}$ [eV] (aqu.traj)' + ' {}V'.format(pot)
            
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
            


            trunk='../dissads/tree/endstates/BEEF-{}/H2/doNEB/'.format(metal)
            xlabel=r'$\Delta E^{\ddagger}$ [eV] (vac.traj)' #+ ' {}V'.format(pot)
            
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
        aqu_barriers=np.array(aqu_barriers)
        

        df = pd.DataFrame([])
        df['metal'] = metals_all
        df['termination'] = terminations
        df['vacBarrier'] = vac_barriers
        df['aquBarrier'] = aqu_barriers

        
       
        if count > 0 : #len(aqu_barriers) > 0:
            
            filename='CSV/parsed_barriers_vac_aqu_pot{}'.format(pot)
            df.to_csv(filename+'.csv',index=False)
        
            yvals = df['aquBarrier'].to_numpy()
            xvals = df['vacBarrier'].to_numpy()
            xkey = 'vac'
            ykey = 'aqu_pot{}'.format(pot)
            #plot_x_vs_y()
            #plot_model(mp,df,modify,pot,bflag)
            plot_scatter(xvals, yvals,metals, xlabel, ylabel,xkey,ykey) 




