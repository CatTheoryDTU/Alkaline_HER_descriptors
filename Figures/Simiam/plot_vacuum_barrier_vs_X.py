"""

Tafel barriers in vacuum vs. descriptors

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



def parse_results():
    """
    parse .txt files to dataframe
    """
    filenames=[
        'metals.txt',
        'PZCs.txt', 
        'vac_Htops.txt',
        'vac_HBEs.txt',
        'i0s.txt'
             ]
    
    path='../'
    #laptop
    #path='/Users/sangh/software/Alkaline_HER_Descriptors/Figures/' 
    data = []
    for i in range(len(filenames)):
        vals=[]
        with open(path+filenames[i],'r') as f:
            for line in f:
                cols = line.split()
                if i !=0:
                    value = float(cols[0])
                else: 
                    value = str(cols[0])
                vals.append(value)
        data.append(vals)
    
    metals = data[0]
    PZCs = data[1]
    vac_Htops = data[2]
    vac_HBEs = data[3]
    i0s = data[4]
    
    print('len metals {}'.format(len(metals)))
    rlist = [] 
    for j in range(len(metals)):
        attributes = {
                "metal" : metals[j],
                "PZC" : PZCs[j],
                "vac_Htop" : vac_Htops[j],
                "vac_HBE" : vac_HBEs[j],
                "i0" : i0s[j]
                  }
        
        rlist.append(attributes)
    
    df = pd.DataFrame(rlist)
    
    df.to_csv('CSV/results_dipam.csv',index=False)

    return df


def plot_scatter(xvals, yvals,metals, xlabel, ylabel,xkey,ykey) :
    print(' ')
    #print('{} {} {} {} {} {} {} {}'.format( spin,mtag,dindex,site,zval,xkey,ykey,adsorbate))
    print('plotting y {} vs x{} '.format( ykey,xkey))

    lrbt=[0.3,0.95,0.2,0.95]
    rcParams['figure.subplot.left'] = lrbt[0]  
    rcParams['figure.subplot.right'] = lrbt[1] 
    rcParams['figure.subplot.bottom'] = lrbt[2]
    rcParams['figure.subplot.top'] = lrbt[3] #
    
    for SKregression in [ True, False]:

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
            
            arsize=6
            #dx,dy=(0.1,0.01)
            dx,dy=(0.0,0.01)
            
            for i in subset: #range(xvals.shape[0]):
                ax.annotate('{}'.format(metals[i]), xy=(xvals[i]+dx,yvals[i]+dy),
                            fontsize=arsize,ha='center',textcoords='data',
                            color="k",annotation_clip=False)                      
            
            capcoord=(-0.2,-0.3)
            #ax.annotate('a)', xy=capcoord,ha='center',
            #                  xycoords = ('axes fraction'), 
            #                  textcoords=('axes fraction'),
            #                  color="k",annotation_clip=False) 
            
            
    
            #SKregression = True
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
                elif False: #if False:
                    ax.annotate('Not found: {}'.format(excluded_from_regression), xy=capcoord,ha='center', fontsize=arsize,
                                    xycoords = ('axes fraction'), textcoords=('axes fraction') ,color="k",annotation_clip=False)                      
            
            if PDregression:
                dummy=1
    
    
    
            fs=6
            ax.set_xlabel(xlabel,fontsize=fs) 
            ax.set_ylabel(ylabel,fontsize=fs) 
        
       
        figname='{}_vs_{}_reg{}'.format(ykey,xkey,SKregression)
        #figname='{}_vs_{}'.format(ykey,xkey)
    
    
        print('plotting {}'.format(figname))
        plt.savefig('output/'+figname+'.png',dpi=300)

    return None







if __name__ == "__main__":
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)
    
    
    #load elementary descriptors
    TM = pd.read_csv('CSV/TM_parameters.csv')

    #LOAD DATA, Dipam's HBEtop:
    df = parse_results()
    
    print('Dipams results in dataframe:')
    print('{}'.format(df))



    metals_all=['Ag','Al','Au','Cu','Fe','Co','Ni','Ir','Os','Pd','Pt','Re','Rh','Ru','W','Zn']
    metals = metals_all

   

    print('metals {}'.format(metals))
    
    
    for ykey in ['vacuum_barrier']:
        for xkey in [ 'HBEtop-HBEfcc',  'vsquaredREL']:
        #for xkey in [ 'vsquaredREL']:

            if ykey == 'vacuum_barrier':
                #load vacuum barriers.
                filename='CSV/parsed_vacuum_tafel_barriers.csv'
                dfB = pd.read_csv(filename)
                print('Vacuum barriers, parsed by Simiam, in dataframe:')
                print('{}'.format(dfB))
                vac_barriers = np.array( [ float(dfB.loc[ dfB['metal'] == metal, 'vacBarrier'].iloc[0])  for metal in metals ] )
                yvals = vac_barriers
                ykey = 'vacuum_barrier'
                ylabel=r'$\Delta E^{\ddagger}$ [eV] (vac.traj)' #+ ' {}V'.format(pot)
            
            if xkey == 'vsquaredREL':
                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'V$_{ad}^2$ [Rel. Cu]' #eV$^2$]'
            
            elif xkey == 'HBEtop-HBEfcc':
                #only few metals available.

                #look up results. return np.nan if not found.
                HBEfccs = []
                HBEtops = []
                for metal in metals:
                    if df.loc[ df['metal'] == metal, 'vac_HBE'].any(): 
                        HBEfccs.append( df.loc[ df['metal'] == metal, 'vac_HBE'].iloc[0] )
                    else:
                        HBEfccs.append( np.nan)
                    
                    if df.loc[ df['metal'] == metal, 'vac_Htop'].any():
                        HBEtops.append( df.loc[ df['metal'] == metal, 'vac_Htop'].iloc[0] )
                    else:
                        HBEtops.append( np.nan)
                        
               
                HBEfccs = np.array(HBEfccs)
                HBEtops = np.array(HBEtops)

                xvals = HBEtops - HBEfccs
                xkey = 'HBEtop-HBEfcc'
                xlabel='HBEtop - HBEfcc [eV]' 

            print('ykey {}'.format(ykey))
            print('yvals {}'.format(yvals))
            print('xkey {}'.format(xkey))
            print('xvals {}'.format(xvals))


            if ykey == 'i0':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'log($|j_0|$/(mA cm$^{-2}$))'#   i0s [TOF]d-band upper edge (maj.spin.) [eV]'
            elif ykey == 'PZC':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'PZC [V]'#   i0s [TOF]d-band upper edge (maj.spin.) [eV]'
            elif ykey == 'vac_Htop':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'vac Htop [eV]'#   i0s [TOF]d-band upper edge (maj.spin.) [eV]'
            elif ykey == 'vac_HBE':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'vac HBE [eV]'#   i0s [TOF]d-band upper edge (maj.spin.) [eV]'
            
            elif ykey == 'WF':   
                ylabel=r'WF $\phi_{Exp.}$ [eV]'
                WF = []
                for i in range(len(metals)):
                    WF.append(  float(TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ])  )
                WF = np.array(WF)
                yvals=WF
            
            elif ykey == 'dbandcenter': 
                yvals  = np.array(  [TM.loc[ TM['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'd-band center $\epsilon_d$ [eV]'
        
            elif ykey == 'dbandupperedge':   
                yvals= np.array(  [TM.loc[ TM['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'd-band upper edge (maj.spin.) [eV]'
            
             



            if xkey == 'WF':   
                xlabel=r'WF $\phi_{Exp.}$ [eV]'
                #NEW WAY
                WF = []
                for i in range(len(metals)):
                    WF.append(  float(TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ])  )
         
                WF = np.array(WF)
                xvals=WF
            elif xkey == 'vac_HBE':
                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'vac HBE [eV]'#   i0s [TOF]d-band upper edge (maj.spin.) [eV]'
            
            elif xkey == 'dbandcenter': 
                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'd-band center $\epsilon_d$ [eV]'
        
            elif xkey == 'dbandupperedge':   
                xvals= np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'd-band upper edge (maj.spin) [eV]'
            
            elif xkey == 'vsquaredREL':
                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'V$_{ad}^2$ [Rel. Cu]' #eV$^2$]'
            elif xkey == 'PZC':
                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'PZC [V]'#   i0s [TOF]d-band upper edge (maj.spin.) [eV]'
    

            plot_scatter(xvals, yvals,metals, xlabel, ylabel,xkey,ykey) 




