#!/usr/bin/env python

"""
2025 plot overview of metal surfaces: DOS, vacuum, fermi levels.


"""

import numpy as np
import numpy.matlib
import scipy
#import scipy.linalg as SP
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
from scipy import constants
import sys
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.ticker as ticker
import os
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import subprocess
from scipy.constants import golden_ratio, inch

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


import pandas as pd
from sklearn.linear_model import LinearRegression


HtoeV=constants.physical_constants["Hartree energy in eV"][0]
autime=constants.physical_constants["atomic unit of time"][0]*1E15 #in fs

#sept 2022: we want to convert gamma [1/fs] to WDOS [eV] by multiplying by hbar/2.
#the value of hbar, in eV*fs, is (google) 0.658211957
hbar=0.658211957





class xy_plot(object):

    """ simple class to plot a figure """
    def __init__(self,cluster):
        self.cluster=cluster
        self.path = os.getcwd()

    def _set_plotting_env(self,width=None,height=None,lrbt=None,shrinkfactor=None,vfactor=None):
        if (width == None and height == None):
            #width = 3.25 #ACS
            width = 3.37 +0.2
            height = width / golden_ratio *1.5/2  + 0.0
            height = height*vfactor #if no spin down, change aspect ratio.
         #legend mods:
            f=shrinkfactor  #f=0.7
            width = width * (1/f)
            height = height * (1/f)

            #mod for p3x3 ArFe, heatmaps plot:
            #height = height*2

        if (lrbt == None):
            lrbt = [0.135,0.955,0.25,0.78]
        #print width,height
        # set plot geometry
        rcParams['figure.figsize'] = (width, height) # x,y
        #rcParams['font.family'] = 'serif' #'serif', 'sans-serif', 'monospace'
        #rcParams['font.serif'] = 'Computer Modern Roman'#'Times New Roman'  
        #to see options:  import matplotlib.font_manager    
        #for font in matplotlib.font_manager.fontManager.ttflist: print(font.name)       
        #rcParams['font.weight'] = 'medium' #'bold'
        #rcParams['font.style'] = 'normal' #'italic'
        rcParams['font.size'] = 8.0
        #rcParams['mathtext.fontset'] = 'cm'#'stix', 'cm'
        rcParams['figure.subplot.left'] = lrbt[0]  # the left side of the subplots of the figure
        rcParams['figure.subplot.right'] = lrbt[1] #0.965 # the right side of the subplots of the figure
        rcParams['figure.subplot.bottom'] = lrbt[2] # the bottom of the subplots of the figure
        rcParams['figure.subplot.top'] = lrbt[3] # the bottom of the subplots of the figure
        rcParams['figure.subplot.wspace'] = 0.2
        rcParams['figure.subplot.hspace'] = 0.2

        rcParams['axes.linewidth'] = 0.7 #rcParams['axes.linewidth'] *scale
        
        #2022 RAVEN:
        if self.cluster=='raven':
            preamble = [r'\usepackage{physics} \usepackage{amsmath}']
            plt.rcParams.update({"text.usetex": True,
                              "font.family": "sans-serif",           
                              #"font.sans-serif": ["Helvetica"],      #not working
                              "text.latex.preamble": preamble
                              })







    def plot_ref_dos_inner(self,cluster, metals, terminations, df, TM):
                                            


        apply_spin = True
                                    
        #fig1 = plt.figure()
                                                                               
        #ax = fig1.add_subplot(211)
        plt.figure(figsize=(15, 12))
        plt.subplots_adjust(hspace=0.5)
        plt.suptitle("DOS", fontsize=18, y=0.95)
        

        # loop through the length of tickers and keep track of index
        for i, metal in enumerate(metals): #enumerate(tickers):
        #for i in range(len(metals)): #metal in metals:
            metal = metals[i]
            termination = terminations[i]
            surfname = metal+termination
            

            #get vac level and mu for this metal.
            #if xkey == 'WFDFT':   
            #    xlabel=r'WF $\phi_{DFT.}$ [eV]'
            #    #NEW WAY
            #    WFDFT = []
            #    for i in range(len(metals)):
            #        WFDFT.append(  float(df.loc[ df['metal'] == metals[i], 'WF_upper_surf' ])  )
         
            #        #vac_barriers = np.array( [ float(dfB.loc[ dfB['metal'] == metal, 'vacBarrier'].iloc[0])  for metal in metals ] )
            #    WFDFT = np.array(WFDFT)
            #    xvals=WFDFT
            vac = float(df.loc[ df['metal'] == metals[i], 'vac_upper_surf' ])  
            mu = float(df.loc[ df['metal'] == metals[i], 'mu' ])  
           # physics = {
           #        'mu' : mu_surf,
           #        'vac_upper_surf' : vac_upper_surf,
           #        'vac_lower_surf' : vac_lower_surf,
           #        'WF_upper_surf' : WF_upper_surf,
           #        'WF_lower_surf' : WF_lower_surf
           #       }


            if metal in ['Fe','Co','Ni'] and apply_spin: #special case
                surfname+='spin'
        
            method = 'fragS_fragD_2025'

            #show dos of dimer system, which includes one H atom. we don't have dos of surface yet.
            path='/home/scratch3/sangh/HER/reference_wdos/ztest_tight/dimers_z200pm/{}/{}/block_diag_ave/output/dimer_properties/'.format(surfname,method)
            filename = path+'PDOS_DIMER_up_stddev100.txt'
            if not os.path.isfile(filename):
                print('NOT FOUND: metal {}, file {}'.format(surfname,filename))
                continue
            
            pdosup = np.loadtxt(filename)
            print('FOUND: metal {}, file {} '.format(surfname,filename))
  
            
            # add a new subplot iteratively

            ax = plt.subplot(8, 2, i + 1)
            
            # filter df and plot ticker on the new subplot axis
            #df[df["ticker"] == ticker].plot(ax=ax)
            surfalpha = 0.7
            ax.fill_between( pdosup[:,0]-vac, pdosup[:,1],interpolate=True,
                         color='lightgray',label=r'Total DOS',alpha=surfalpha,zorder=0,edgecolor=None)
            
            if True: ax.axvline(x=mu-vac, ymin=0., ymax=1000.,linewidth=0.5,linestyle='--',color='black',zorder=10)
            #ax.set_ylim(ymin,ymax)  #-1*HtoeV,1.5*HtoeV)
            ax.set_xlim(-13,3)  #-1*HtoeV,1.5*HtoeV)
            
            # chart formatting
            ax.set_title(metal) #ticker.upper())
            #ax.get_legend().remove()
            ax.set_xlabel("")



        
        plt.savefig('dos_test.png') 
    
        return None;


 
#        #you could also read dos from the gamma_test files. 
#        found_pdos = False
#        found_pdosup = False
#        found_pdosdn = False
#        found_pgamma = False   #these are updated below if needed.
#
#
#        for use_pgamma_HAB in [False]: #two different projections of the WDOS. These will also be considered in the final results at resonance (later).
#
#
#            #BZ_averaging=True
#            if BZ_averaging:
#                print('bz averaging.') # usepdos is {}'.format(usepdos))
#                
#                
#                if plot_modos: # we can overlay plot modos for max 6 orbitals. 
#                    local_donor_index = local_donor_indices[0]
#                    print('loading modos files')
#                    modosup = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up_stddev{}.txt'.format(local_donor_index,stddev))
#                    modosup[:,0] = modosup[:,0] -mu    #energies shifted, eV
#                    #modosup[:,1:] = modosup[:,1:]   / Nadsatoms    
#                    if show_spin_down:
#                        modosdn = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn_stddev{}.txt'.format(local_donor_index,stddev))
#                        modosdn[:,0] = modosdn[:,0] -mu    #energies shifted, eV
#                        #modosdn[:,1:] = modosdn[:,1:]   / Nadsatoms    
#                    
#                    if len(local_donor_indices) > 1:
#                        local_donor_index = local_donor_indices[1]
#                        modosup1 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up_stddev{}.txt'.format(local_donor_index,stddev))
#                        modosup1[:,0] = modosup1[:,0] -mu    #energies shifted, eV
#                        #modosup1[:,1:] = modosup1[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn1 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn_stddev{}.txt'.format(local_donor_index,stddev))
#                            modosdn1[:,0] = modosdn1[:,0] -mu    #energies shifted, eV
#                            #modosdn1[:,1:] = modosdn1[:,1:]   / Nadsatoms    
#                    if len(local_donor_indices) > 2:
#                        local_donor_index = local_donor_indices[2]
#                        modosup2 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up_stddev{}.txt'.format(local_donor_index,stddev))
#                        modosup2[:,0] = modosup2[:,0] -mu    #energies shifted, eV
#                        #modosup2[:,1:] = modosup2[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn2 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn_stddev{}.txt'.format(local_donor_index,stddev))
#                            modosdn2[:,0] = modosdn2[:,0] -mu    #energies shifted, eV
#                            #modosdn2[:,1:] = modosdn2[:,1:]   / Nadsatoms    
#                    if len(local_donor_indices) > 3:
#                        local_donor_index = local_donor_indices[3]
#                        modosup3 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up_stddev{}.txt'.format(local_donor_index,stddev))
#                        modosup3[:,0] = modosup3[:,0] -mu    #energies shifted, eV
#                        #modosup3[:,1:] = modosup3[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn3 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn_stddev{}.txt'.format(local_donor_index,stddev))
#                            modosdn3[:,0] = modosdn3[:,0] -mu    #energies shifted, eV
#                            #modosdn3[:,1:] = modosdn3[:,1:]   / Nadsatoms    
#                    if len(local_donor_indices) > 4:
#                        local_donor_index = local_donor_indices[4]
#                        modosup4 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up_stddev{}.txt'.format(local_donor_index,stddev))
#                        modosup4[:,0] = modosup4[:,0] -mu    #energies shifted, eV
#                        #modosup4[:,1:] = modosup4[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn4 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn_stddev{}.txt'.format(local_donor_index,stddev))
#                            modosdn4[:,0] = modosdn4[:,0] -mu    #energies shifted, eV
#                            #modosdn4[:,1:] = modosdn4[:,1:]   / Nadsatoms    
#                    
#                    if len(local_donor_indices) > 5:
#                        local_donor_index = local_donor_indices[5]
#                        modosup5 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up_stddev{}.txt'.format(local_donor_index,stddev))
#                        modosup5[:,0] = modosup5[:,0] -mu    #energies shifted, eV
#                        #modosup5[:,1:] = modosup5[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn5 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn_stddev{}.txt'.format(local_donor_index,stddev))
#                            modosdn5[:,0] = modosdn5[:,0] -mu    #energies shifted, eV
#                            #modosdn5[:,1:] = modosdn5[:,1:]   / Nadsatoms    
#                
#                    if show_spin_down: 
#                        print('plotting modos on ax, shape modosup {}, shape modosdn {}'.format(np.shape(modosup),np.shape(modosdn)))
#                    else: 
#                        print('plotting modos on ax, shape modosup {}'.format(np.shape(modosup)))
#
#
#                pdosup = np.loadtxt('dimer_properties/PDOS_DIMER_up_stddev{}.txt'.format(stddev))
#                pdos2up = np.loadtxt('dimer_properties/PDOS2_DIMER_up_stddev{}.txt'.format(stddev))
#                pdos3up = np.loadtxt('dimer_properties/PDOS3_DIMER_up_stddev{}.txt'.format(stddev))
#                pdosAup = np.loadtxt('dimer_properties/PDOS_active_DIMER_up_stddev{}.txt'.format(stddev))
#                
#                if show_spin_down: 
#                    pdosdn = np.loadtxt('dimer_properties/PDOS_DIMER_dn_stddev{}.txt'.format(stddev))
#                    pdos2dn = np.loadtxt('dimer_properties/PDOS2_DIMER_dn_stddev{}.txt'.format(stddev))
#                    pdos3dn = np.loadtxt('dimer_properties/PDOS3_DIMER_dn_stddev{}.txt'.format(stddev))
#                    pdosAdn = np.loadtxt('dimer_properties/PDOS_active_DIMER_dn_stddev{}.txt'.format(stddev))
#                
#            else:
#                '''
#                PDOS header:
#                 'E[raw eV]', 'totnrm','snrm','pnrm','dnrm','fnrm','gnrm','hnrm','sum','surfnrm','bulknrm','surfsnrm','surfpnrm','surfdnrm','ontop_n','ontop_s','ontop_p','ontop_d'))
#                '''
#                pdosup = np.loadtxt('dimer_properties/PDOS_DIMER_up.txt')
#                
#                
#                '''PDOS2 header: 
#                'E[raw eV]', 'ads_norm','ads_snrm','ads_pnrm','ads_dnrm','ads_sum','ads_pxnrm','ads_pynrm','ads_pznrm'))
#                '''
#                pdos2up = np.loadtxt('dimer_properties/PDOS2_DIMER_up.txt')
#                
#                '''PDOS3 header:
#                'E[raw eV]', 'tot','dsum','dxysum','dyzsum', 'dz2sum','dxzsum','dx2y2sum'))
#                '''
#                
#                pdos3up = np.loadtxt('dimer_properties/PDOS3_DIMER_up.txt')
#                pdosAup = np.loadtxt('dimer_properties/PDOS_active_DIMER_up.txt')
#                if show_spin_down: 
#                    pdosdn = np.loadtxt('dimer_properties/PDOS_DIMER_dn.txt')
#                    pdos2dn = np.loadtxt('dimer_properties/PDOS2_DIMER_dn.txt')
#                    pdos3dn = np.loadtxt('dimer_properties/PDOS3_DIMER_dn.txt')
#                    pdosAdn = np.loadtxt('dimer_properties/PDOS_active_DIMER_dn.txt')
#                
#                divide=True #
#                if plot_modos: # we can plot modos for max 4 orbitals. 
#                    local_donor_index = local_donor_indices[0]
#                    print('loading modos files')
#                    modosup = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up.txt'.format(local_donor_index))
#                    modosup[:,0] = modosup[:,0] -mu    #energies shifted, eV
#                    #if divide: modosup[:,1:] = modosup[:,1:]   / Nadsatoms    
#                    if show_spin_down:
#                        modosdn = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn.txt'.format(local_donor_index))
#                        modosdn[:,0] = modosdn[:,0] -mu    #energies shifted, eV
#                     #   if divide: modosdn[:,1:] = modosdn[:,1:]   / Nadsatoms    
#                    if len(local_donor_indices) > 1:
#                        local_donor_index = local_donor_indices[1]
#                        modosup1 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up.txt'.format(local_donor_index))
#                        modosup1[:,0] = modosup1[:,0] -mu    #energies shifted, eV
#                      #  if divide:    modosup1[:,1:] = modosup1[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn1 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn.txt'.format(local_donor_index))
#                            modosdn1[:,0] = modosdn1[:,0] -mu    #energies shifted, eV
#                       #     if divide:   modosdn1[:,1:] = modosdn1[:,1:]   / Nadsatoms    
#                    if len(local_donor_indices) > 2:
#                        local_donor_index = local_donor_indices[2]
#                        modosup2 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up.txt'.format(local_donor_index))
#                        modosup2[:,0] = modosup2[:,0] -mu    #energies shifted, eV
#                       # if divide:  modosup2[:,1:] = modosup2[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn2 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn.txt'.format(local_donor_index))
#                            modosdn2[:,0] = modosdn2[:,0] -mu    #energies shifted, eV
#                        #    if divide:  modosdn2[:,1:] = modosdn2[:,1:]   / Nadsatoms    
#                    if len(local_donor_indices) > 3:
#                        local_donor_index = local_donor_indices[3]
#                        modosup3 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up.txt'.format(local_donor_index))
#                        modosup3[:,0] = modosup3[:,0] -mu    #energies shifted, eV
#                        #if divide:  modosup3[:,1:] = modosup3[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn3 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn.txt'.format(local_donor_index))
#                            modosdn3[:,0] = modosdn3[:,0] -mu    #energies shifted, eV
#                        #    if divide:  modosdn3[:,1:] = modosdn3[:,1:]   / Nadsatoms    
#                    
#                    if len(local_donor_indices) >4:
#                        local_donor_index = local_donor_indices[4]
#                        modosup4 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up.txt'.format(local_donor_index))
#                        modosup4[:,0] = modosup4[:,0] -mu    #energies shifted, eV
#                       # if divide:  modosup4[:,1:] = modosup4[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn4 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn.txt'.format(local_donor_index))
#                            modosdn4[:,0] = modosdn4[:,0] -mu    #energies shifted, eV
#                       #     if divide:  modosdn4[:,1:] = modosdn4[:,1:]   / Nadsatoms    
#                    
#                    if len(local_donor_indices) >5:
#                        local_donor_index = local_donor_indices[5]
#                        modosup5 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_up.txt'.format(local_donor_index))
#                        modosup5[:,0] = modosup5[:,0] -mu    #energies shifted, eV
#                       # if divide:  modosup5[:,1:] = modosup5[:,1:]   / Nadsatoms    
#                        if show_spin_down:
#                            modosdn5 = np.loadtxt('dimer_properties/MODOS_i{}_DIMER_dn.txt'.format(local_donor_index))
#                            modosdn5[:,0] = modosdn5[:,0] -mu    #energies shifted, eV
#                       #     if divide:  modosdn5[:,1:] = modosdn5[:,1:]   / Nadsatoms    
#                
#                            print('plotting modos on ax, shape modosup {}, shape modosdn {}'.format(np.shape(modosup),np.shape(modosdn)))
#                
#            
#
#
#            pdosup[:,0] = pdosup[:,0] -mu    #energies shifted, eV
#            pdos2up[:,0] = pdos2up[:,0] -mu    #energies shifted, eV
#            pdos3up[:,0] = pdos3up[:,0] -mu    #energies shifted, eV
#            pdosAup[:,0] = pdosAup[:,0] -mu    #energies shifted, eV
#            if show_spin_down:
#                pdosdn[:,0] = pdosdn[:,0] -mu    #energies shifted, eV
#                pdos2dn[:,0] = pdos2dn[:,0] -mu    #energies shifted, eV
#                pdos3dn[:,0] = pdos3dn[:,0] -mu    #energies shifted, eV
#                pdosAdn[:,0] = pdosAdn[:,0] -mu    #energies shifted, eV
#            
#            
#          #  #Give DOS Per atom.
#          #  pdos2up[:,1:] = pdos2up[:,1:]   / Nadsatoms   #projection of KS dimer on adsorbate channels
#          #  pdosup[:,1:9] = pdosup[:,1:9]   / Ndimeratoms        #projection of KS dimer on global L channels. columns 1-8 are total dimer properties.
#          #  pdosup[:,9:14] = pdosup[:,9:14]   / Nsurfatoms        #projection of KS dimer on global L channels. columns 1-8 are total dimer properties.
#          #  pdos3up[:,1:] = pdos3up[:,1:]   / Ndimeratoms      #projecion of KS dimer on surface L channels. 
#          #  
#          #  
#          #  if show_spin_down:
#          #      pdos2dn[:,1:] = pdos2dn[:,1:]   / Nadsatoms
#          #      pdosdn[:,1:9] = pdosdn[:,1:9]   / Ndimeratoms   
#          #      pdosdn[:,9:14] = pdosdn[:,9:14]   / Nsurfatoms  
#          #      #pdosdn[:,1:] = pdosdn[:,1:]   / Ndimeratoms               #columns 1-8 are total dimer properties.
#          #      pdos3dn[:,1:] = pdos3dn[:,1:]   / Ndimeratoms               #columns 1-8 are total dimer properties.
#           
#            #MODOS: we can also change that to per atom...originally is per cell.
#
#           # #columns 1-8 are total slab properties.
#           # if False:
#           #     pdosup[:,1:9] = pdosup[:,1:9]   / Ndimeratoms               #columns 1-8 are total slab properties.
#           #     pdosup[:,9]   = pdosup[:,9]     / Nsurfatoms           #column 9 is surfsum
#           #     pdosup[:,10]  = pdosup[:,10]    / (Ndimeratoms-Nsurfatoms)  #column 10 is bulksum  these two should total up to the total dos col1.
#           #     pdosup[:,11:14]  = pdosup[:,11:14] / Nsurfatoms               #column 11-13 are surfsums.  they should total up to surfsum col 9.
#           #    
#           #     if show_spin_down:
#           #         pdosdn[:,1:9] = pdosdn[:,1:9]   / Ndimeratoms               #columns 1-8 are total slab properties.
#           #         pdosdn[:,9]   = pdosdn[:,9]     / Nsurfatoms           #column 9 is surfsum
#           #         pdosdn[:,10]  = pdosdn[:,10]    / (Ndimeratoms-Nsurfatoms)  #column 10 is bulksum  these two should total up to the total dos col1.
#           #         pdosdn[:,11:14]  = pdosdn[:,11:14] / Nsurfatoms               #column 11-13 are surfsums.  they should total up to surfsum col 9.
#                
#
#
#            #if use_resonance:
#            #if experiment:
#            #    #use_resonance_options=[True,False]
#            #    use_resonance_options=[True]
#            #else:
#            use_resonance_options=[False]
#                
#            
#            if True: #else:        # plotdpdos, plotgamma, plotpdos_tot 
#                plot_options = [ 
#                             [ True, True, True, True, True, True, True ],        #presentation basics flagship: only WDOS and total slab DOS.
#                             ] 
#                                        
#            for use_resonance in [False]:
#                for iopt in range(len(plot_options)):
#
#                    for dummy in [True]: #plotsurfdos in plotsurfdos_options:
#                        
#                        plot_inset=False
#                        
#                        show_legend = True
#                        for size in ['LARGE','SMALL']:
#                            for show_modos_unfilled in [True,False]: 
#                                for show_modos_filled_orig in [True,False]:
#                                    if show_modos_filled_orig and show_modos_unfilled:
#                                        continue
#                                    for imodos in local_donor_indices: #[6,7,8]: # [0]: # [6,7,8]:
#                                        print('imodos {}'.format(imodos))
#                                        for show_total_dos in [True]:
#                                            for show_surf_dos in [False,True]: #show_surf_dos = not show_total_dos
#                                                for show_active in [False,True]: #active site channels. 
#                                                    if show_surf_dos or show_modos_unfilled or show_modos_filled:
#                                                        show_active=False
#                                                    if show_active:
#                                                        show_active_options = ['tot','spd','pxyz','dxyz']
#                                                    else:
#                                                        show_active_options = ['dummy']
#                                                    for show_active_option in show_active_options:
#                                                        for plot_ads_channels in [False,True]:
#                                                            for plot_dimer_spdchannels in [False,True]:  #dimer global channels 
#                                                                for plot_dimer_dchannels in [False,True]:  #dimer global channels 
#                                                                    
#                                                                    show_modos_filled=show_modos_filled_orig
#                                                                    if plot_ads_channels: plot_dimer_spdchannels = False
#                                                                    if plot_ads_channels: show_modos_filled=False;show_modos_unfilled=False;plot_dimer_dchannels = False
#                                                                    if plot_ads_channels: 
#                                                                        show_modos_unfilled = False; show_modos_filled = False
#                                                                    
#                                                                    if plot_dimer_spdchannels or plot_dimer_dchannels: 
#                                                                        show_modos_unfilled = False; show_modos_filled = False
#                                                                        
#                                                                    if show_active and show_modos_filled:
#                                                                        continue
#                                                                    if show_active and show_surf_dos:
#                                                                        continue
#                                                                    if show_modos_filled and show_surf_dos:
#                                                                        continue
#                                                                    if show_modos_unfilled and show_surf_dos:
#                                                                        continue
#                                                                    if plot_dimer_dchannels and show_surf_dos:
#                                                                        continue
#                                                                    if plot_dimer_spdchannels and show_surf_dos:
#                                                                        continue
#                                                                    if show_active and show_modos_unfilled:
#                                                                        continue
#                                                                    if show_active and plot_dimer_spdchannels:
#                                                                        continue
#                                                                    if show_active and plot_dimer_dchannels:
#                                                                        continue
#                                                                    if show_active and plot_ads_channels:
#                                                                        continue
#                                                                    if show_surf_dos and plot_ads_channels:
#                                                                        continue
#                 
#                                                                    if plot_dimer_spdchannels and plot_dimer_dchannels: 
#                                                                        continue
#                                                                    else:
#                                                   
#                                                                        if show_legend: shrinkfactor=0.85
#                                                                        #else: shrinkfactor = 1  #paper JCP.
#                                                                        else: shrinkfactor = 0.9  #July 2023: 
#                                                                        shrinkfactor=0.9
#                                                                        #lrbt = list( np.asarray( [0.15,0.87,0.22,0.95])*shrinkfactor )  #paper JCP.
#                                                                        lrbt = list( np.asarray( [0.15,0.87,0.22,0.95])*shrinkfactor )  #July 2023: we want to shrink a bit.
#                                                                        if show_spin_down: 
#                                                                            vfactor=1
#                                                                        else: vfactor=2
#                                                                        
#                                                                        self._set_plotting_env(width=None,height=None,lrbt=lrbt,shrinkfactor=shrinkfactor,vfactor=vfactor) #for eps
#                                                                        
#                                                                    
#                                                                        #if size == 'Large': xmax=10;xmin=-10 #-4.5
#                                                                        if size=='LARGE':
#                                                                            xmin=emin
#                                                                            xmax=emax
#                                                                        elif size == 'SMALL': xmax=2;xmin=-2 #-4.5
#                                                                        
#                                                                        if False:  #deprecate jan 2023.
#                                                                            updos_inrange = [ dosup[i,1] for i in range(len(dosup[:,0])) 
#                                                                                              if (dosup[i,0] <= xmax) and (dosup[i,0] >= xmin) ]
#                                                                            #these are already on shifted scale. 
#                                                                            dndos_inrange = [ dosdn[i,1] for i in range(len(dosdn[:,0])) 
#                                                                                              if (dosdn[i,0] <= xmax) and (dosdn[i,0] >= xmin) ]
#                                                                            print('len(updos_inrange) {}'.format(len(updos_inrange)))
#                                                                        else:
#                                                                            updos_inrange = [ pdosup[i,1] for i in range(len(pdosup[:,0])) 
#                                                                                              if (pdosup[i,0] <= xmax) and (pdosup[i,0] >= xmin) ]
#                                                                            #these are already on shifted scale. 
#                                                                            if show_spin_down:
#                                                                                dndos_inrange = [ pdosdn[i,1] for i in range(len(pdosdn[:,0])) 
#                                                                                              if (pdosdn[i,0] <= xmax) and (pdosdn[i,0] >= xmin) ]
#                                                                            else: dndos_inrange=updos_inrange
#                                                                            print('len(updos_inrange) {}'.format(len(updos_inrange)))
#                                                                    
#                                                                        ymaxup=np.max(updos_inrange)#np.array(DOS[0][1])[:,1])
#                                                                        ymaxdn=np.max(dndos_inrange)#np.array(DOS[1][1])[:,1])
#                                                                        
#                                                                        ymax = np.max((ymaxup,ymaxdn))*1.1
#                                                                        
#                                                                        # test:
#                                                                        #ymax = 5
#                                                                    
#                                                                        if size == 'SMALLF23': #special case, zoom in.
#                                                                            ymax = ymax*0.15
#                                                                            ymax=0.3    #use this everywhere else.
#                                                                            #ymax=0.75  #use this for the exploded bandplot.
#                                                                        ymin=0.0
#                                                                        #find range for couplings**1
#                                                                       
#                                                                        for exponent in [1]:  #2]:
#                                                                       
#                                                                            sigma=1  #show only the second sigma value  #the second value of sigma used is 0.25 eV
#                                                                            
#                                                                       
#                                                                            for uselog in [False]:
#                                                                                fig1 = plt.figure()
#                                                                               
#                                                                                ax = fig1.add_subplot(211)
#                                                                                
#                                                                                #for all plots, we do want the total dos visible. 
#                                                                                #print('ymin and ymax for the dos axis are {} {}'.format(ymin, ymax))
#                                                                                ymin=0
#                                                                                if show_modos_unfilled or show_modos_filled: ymax=1
#                                                                                else: ymax=1
#                                                                                ax.set_ylim(ymin,ymax)  #-1*HtoeV,1.5*HtoeV)
#                                                                                ax.set_xlim(xmin,xmax)  #-1*HtoeV,1.5*HtoeV)
#                                                                                
#                                                                                if show_spin_down:
#                                                                                    if False: ax.annotate(r'$\textbf{maj.}$',
#                                                                                               xy=(0.9,0.75), textcoords='axes fraction',
#                                                                                               va='center',rotation=None,size=8,annotation_clip=False)     #inside
#                                                                    
#                                                                    
#                                                                    
#                                                                                if True: ax.axvline(x=0, ymin=0., ymax=1000.,linewidth=0.5,linestyle='--',color=tumcolors['black'],zorder=10)
#                                                                                
#                                                                    
#                                                                                '''PDOS2 header: 
#                                                                                'E[raw eV]', 'ads_norm','ads_snrm','ads_pnrm','ads_dnrm','ads_sum','ads_pxnrm','ads_pynrm','ads_pznrm'))
#                                                                                '''
#                                                                                
#                                                                                #if plot_totaldos and plot_ads_channels:
#                                                                                surfalpha = 1.0 #0.25 #production.
#                                                                                if show_total_dos: #not show_modos_filled: 
#                                                                                    pdosup = np.loadtxt('dimer_properties/PDOS_DIMER_up.txt')
#                                                                                    ax.fill_between( pdosup[:,0], pdosup[:,1],interpolate=True,
#                                                                                                 #color=tumcolors['lightgray'],label=r'Total DOS',alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                 color=tumcolors['lightgray'],label=r'Total DOS',alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                if show_surf_dos:
#                                                                                    ax.plot( pdosup[:,0], pdosup[:,9],color='black',lw=0.5,label=r'Surf DOS',zorder=2)
#                                                                                
#
#                                                                                if show_active:    #active site channels
#                                                                                    lww=1# .5
#                                                                                   #file header:
#                                                                                   # E[raw eV] actnrm asnrm apnrm apxnrm apynrm apznrm adnrm | adxynrm adyznrm adz2nrm adxznrm adx2y2nrm
# 
#                                                                                    #show_active_options = ['tot','spd','pxyz','dxyz']
#                                                                                    if show_active_option =='tot':
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,1],linewidth=lww,label='active site tot',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                    if show_active_option =='spd':
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,2],linewidth=lww,label='act. s', linestyle='-',  color=tumcolors['tumorange'] ,zorder=2)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,3],linewidth=lww,label='act. p', linestyle='-',  color=tumcolors['tumred']    ,zorder=3)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,7],linewidth=lww, label='act. d',linestyle='-',  color=tumcolors['tumblue'] ,zorder=6)
#                                                                                    if show_active_option =='pxyz':
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,4],linewidth=lww,label='act. px', linestyle='-', color='blue' ,zorder=4)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,5],linewidth=lww,label='act. py', linestyle='-', color='green' ,zorder=4)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,6],linewidth=lww,label='act. pz', linestyle='-', color='red',zorder=5)
#                                                                                                                                                
#                                                                                    if show_active_option =='dxyz':
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,8],linewidth=lww, label='act. dxy',linestyle='-',   color =tumcolors['tumorange']     ,zorder=6)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,9],linewidth=lww, label='act. dyz',linestyle='-',   color =tumcolors['tumred']        ,zorder=6)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,10],linewidth=lww,label='act. dz2',linestyle='-',   color =tumcolors['tumblue']       ,zorder=6)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,11],linewidth=lww,label='act. dxz',linestyle='--',  color=tumcolors['diag_purple_70'] ,zorder=6)
#                                                                                        ax.plot( pdosAup[:,0], pdosAup[:,12],linewidth=lww,label='act. dx2y2',linestyle='--',color=tumcolors['tumgreen']        ,zorder=6)
#                                                                                                                                                 
#                                                                                #elif plot_totaldos :
#                                                                                    #ax.plot( pdosup[:,0], pdosup[:,1],linewidth=0.7,label='Total DOS',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                #if show_modos:
#                                                                                if show_modos_filled:
#                                                                                    lww=1
#                                                                                    mult=1
#
#                                                                                 #   if False: #show filled MODOS plots together overlaid.
#                                                                                 #       if len(local_donor_indices)>0:
#                                                                                 #           local_donor_index=local_donor_indices[0]
#                                                                                 #           ax.fill_between( modosup[:,0], mult*modosup[:,2],interpolate=True,
#                                                                                 #                                color='red',label='mo i{}'.format(local_donor_index),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                 #       if len(local_donor_indices)>1:
#                                                                                 #           local_donor_index=local_donor_indices[1]
#                                                                                 #           ax.fill_between( modosup1[:,0], mult*modosup1[:,2],interpolate=True,
#                                                                                 #                            color='green',label='mo i{}'.format(local_donor_index),alpha=surfalpha,zorder=1,edgecolor=None)
#                                                                                 #       if len(local_donor_indices)>2:
#                                                                                 #           local_donor_index=local_donor_indices[2]
#                                                                                 #           ax.fill_between( modosup2[:,0], mult*modosup2[:,2],interpolate=True,
#                                                                                 #                            color='blue',label='mo i{}'.format(local_donor_index),alpha=surfalpha,zorder=2,edgecolor=None)
#
#                                                                                    if True: #Show each filled MODOS seperate
#                                                                                        if imodos in [0,6]:
#                                                                                            if len(local_donor_indices)>0:
#                                                                                                local_donor_index=local_donor_indices[0]
#                                                                                                ax.fill_between( modosup[:,0], mult*modosup[:,2],interpolate=True,
#                                                                                                                 color='red',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                #ax2.plot( modosdn[:,0],mult* modosdn[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='red',zorder=1)
#                                                                                                norm1 =  scipy.integrate.simps(modosup[:,2],x=modosup[:,0] )  
#                                                                                                if False: ax.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.8),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                        #if imodos==7:
#                                                                                        elif imodos in [1,7]:
#                                                                                            if len(local_donor_indices)>1:
#                                                                                                local_donor_index=local_donor_indices[1]
#                                                                                                ax.fill_between( modosup1[:,0], mult*modosup1[:,2],interpolate=True,
#                                                                                                                 color='green',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                #ax2.plot( modosdn1[:,0], mult*modosdn1[:,2],linewidth=lww,label='mo i{}, x{}'.format(local_donor_index),linestyle='-.',color='green',zorder=1)
#                                                                                                norm1 =  scipy.integrate.simps(modosup1[:,2],x=modosup1[:,0] )  
#                                                                                                if False: ax.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.8),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                        #if imodos==8:
#                                                                                        elif imodos in [2,8]:
#                                                                                            if len(local_donor_indices)>2:
#                                                                                                local_donor_index=local_donor_indices[2]
#                                                                                                ax.fill_between( modosup2[:,0], mult*modosup2[:,2],interpolate=True,
#                                                                                                                 color='blue',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                #ax2.plot( modosdn2[:,0], mult*modosdn2[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='blue',zorder=1)
#                                                                                                norm1 =  scipy.integrate.simps(modosup2[:,2],x=modosup2[:,0] )  
#                                                                                                if False: ax.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.8),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                        
#                                                                                        #if imodos==9:
#                                                                                        elif imodos in [3,9]:
#                                                                                            if len(local_donor_indices)>3:
#                                                                                                local_donor_index=local_donor_indices[3]
#                                                                                                ax.fill_between( modosup3[:,0], mult*modosup3[:,2],interpolate=True,
#                                                                                                                 color='orange',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                #ax2.plot( modosdn2[:,0], mult*modosdn2[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='blue',zorder=1)
#                                                                                                norm1 =  scipy.integrate.simps(modosup3[:,2],x=modosup3[:,0] )  
#                                                                                                if False: ax.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.8),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                        #if imodos==10:
#                                                                                        elif imodos in [4,10]:
#                                                                                            if len(local_donor_indices)>4:
#                                                                                                local_donor_index=local_donor_indices[4]
#                                                                                                ax.fill_between( modosup4[:,0], mult*modosup4[:,2],interpolate=True,
#                                                                                                                 color='brown',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                #ax2.plot( modosdn2[:,0], mult*modosdn2[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='blue',zorder=1)
#                                                                                                norm1 =  scipy.integrate.simps(modosup4[:,2],x=modosup4[:,0] )  
#                                                                                                if False: ax.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.8),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                        elif imodos in [5,11]:
#                                                                                            if len(local_donor_indices)>5:
#                                                                                                local_donor_index=local_donor_indices[5]
#                                                                                                ax.fill_between( modosup5[:,0], mult*modosup5[:,2],interpolate=True,
#                                                                                                                 color='black',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                #ax2.plot( modosdn2[:,0], mult*modosdn2[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='blue',zorder=1)
#                                                                                                norm1 =  scipy.integrate.simps(modosup5[:,2],x=modosup5[:,0] )  
#                                                                                                if False: ax.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.8),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                        
#                                                                                     #   else:  #generic modos
#                                                                                     #       if len(local_donor_indices)>4:
#                                                                                     #           local_donor_index=imodos
#                                                                                     #           ax.fill_between( modosup[:,0], mult*modosup[:,2],interpolate=True,
#                                                                                     #                            color='dimgrey',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                     #           #ax2.plot( modosdn2[:,0], mult*modosdn2[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='blue',zorder=1)
#                                                                                     #           norm1 =  scipy.integrate.simps(modosup4[:,2],x=modosup4[:,0] )  
#                                                                                     #           if False: ax.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.8),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                   
#                                                   
#                                                   
#                                                   
#                                                                                if plot_ads_channels:
#                                                                                    lww=1# .5
#                                                                                    ax.plot( pdos2up[:,0], pdos2up[:,1],linewidth=lww,label='ads tot',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                    if True:
#                                                                                        ax.plot( pdos2up[:,0], pdos2up[:,2],linewidth=lww,label='ads s',linestyle='-',color=tumcolors['tumorange'],zorder=2)
#                                                                                        ax.plot( pdos2up[:,0], pdos2up[:,3],linewidth=lww,label='ads p',linestyle='-',color=tumcolors['tumred'],zorder=3)
#                                                                                        ax.plot( pdos2up[:,0], pdos2up[:,4],linewidth=lww,label='ads d',linestyle='-',color=tumcolors['tumblue'],zorder=4)
#                                                                                        ax.plot( pdos2up[:,0], pdos2up[:,6],linewidth=lww,label='ads px',linestyle='--',color='blue',zorder=5)
#                                                                                        ax.plot( pdos2up[:,0], pdos2up[:,7],linewidth=lww,label='ads py',linestyle='--',color='green',zorder=6)
#                                                                                        ax.plot( pdos2up[:,0], pdos2up[:,8],linewidth=lww,label='ads pz',linestyle='--',color='red',zorder=6)
#                                                                                
#                                                                    
#                                                                                if plot_dimer_spdchannels:
#                                                                                    lww=1
#                                                                                    #ax.plot( pdosup[:,0], pdosup[:,2],linewidth=lww,label='d tot',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                    ax.plot( pdosup[:,0], pdosup[:,2],linewidth=lww, label='total s',linestyle='-',color=tumcolors['tumorange'],zorder=2)
#                                                                                    ax.plot( pdosup[:,0], pdosup[:,3],linewidth=lww, label='total p',linestyle='-',color=tumcolors['tumred'],zorder=3)
#                                                                                    ax.plot( pdosup[:,0], pdosup[:,4],linewidth=lww, label='total d',linestyle='-',color=tumcolors['tumblue'],zorder=4)
#                                                                                    #ax.plot( pdosup[:,0], pdosup[:,6],linewidth=lww,label='dxz',linestyle='--',color=tumcolors['diag_purple_70'],zorder=5)
#                                                                                    #ax.plot( pdosup[:,0], pdosup[:,7],linewidth=lww,label='dx2y2',linestyle='--',color=tumcolors['tumgreen'],zorder=6)
#                                                                                if plot_dimer_dchannels:
#                                                                                    lww=1
#                                                                                    ax.plot( pdos3up[:,0], pdos3up[:,2],linewidth=lww,label='total d',linestyle='-',     color   =tumcolors['black']         ,zorder=1)
#                                                                                    ax.plot( pdos3up[:,0], pdos3up[:,3],linewidth=lww,label='total dxy',linestyle='-',   color =tumcolors['tumorange']     ,zorder=2)
#                                                                                    ax.plot( pdos3up[:,0], pdos3up[:,4],linewidth=lww,label='total dyz',linestyle='-',   color =tumcolors['tumred']        ,zorder=3)
#                                                                                    ax.plot( pdos3up[:,0], pdos3up[:,5],linewidth=lww,label='total dz2',linestyle='-',   color =tumcolors['tumblue']       ,zorder=4)
#                                                                                    ax.plot( pdos3up[:,0], pdos3up[:,6],linewidth=lww,label='total dxz',linestyle='--',  color=tumcolors['diag_purple_70'],zorder=5)
#                                                                                    ax.plot( pdos3up[:,0], pdos3up[:,7],linewidth=lww,label='total dx2y2',linestyle='--',color=tumcolors['tumgreen']    ,zorder=6)
#                                                                                
#                                                                                if show_modos_unfilled: # and not show_modos_filled:  #overlayed
#                                                                                    print('show_modos_unfilled')
#                                                                                    #print('plotting modos on ax, shape modosup {}'.format(np.shape(modosup)))
#                                                                                    lww=1
#                                                                                    mult=1
#                                                                                    if len(local_donor_indices)>0:
#                                                                                        local_donor_index=local_donor_indices[0]
#                                                                                        ax.plot( modosup[:,0], mult*modosup[:,2],linewidth=lww,label='mo i{} (x{})'.format(local_donor_index,mult),linestyle='-',color='red',zorder=1)
#                                                                                    if len(local_donor_indices)>1:
#                                                                                        local_donor_index=local_donor_indices[1]
#                                                                                        ax.plot( modosup1[:,0], mult*modosup1[:,2],linewidth=lww,label='mo i{} (x{})'.format(local_donor_index,mult),linestyle='-',color='green',zorder=1)
#                                                                                    if len(local_donor_indices)>2:
#                                                                                        local_donor_index=local_donor_indices[2]
#                                                                                        ax.plot( modosup2[:,0], mult*modosup2[:,2],linewidth=lww,label='mo i{} (x{})'.format(local_donor_index,mult),linestyle='-',color='blue',zorder=1)
#                                                                                        
#                                                                                    if True:  #i9 Argon
#                                                                                        if len(local_donor_indices)>3:
#                                                                                            local_donor_index=local_donor_indices[3]
#                                                                                            ax.plot( modosup3[:,0], mult*modosup3[:,2],linewidth=lww,label='mo i{} (x{})'.format(local_donor_index,mult),linestyle='-',color='orange',zorder=1)
#                                                                                    if True: #i10
#                                                                                        if len(local_donor_indices)>4:
#                                                                                            local_donor_index=local_donor_indices[4]
#                                                                                            ax.plot( modosup4[:,0], mult*modosup4[:,2],linewidth=lww,label='mo i{} (x{})'.format(local_donor_index,mult),linestyle='-',color='brown',zorder=1)
#                                                                                    if True: #other
#                                                                                        if len(local_donor_indices)>5:
#                                                                                            local_donor_index=local_donor_indices[5]
#                                                                                            ax.plot( modosup5[:,0], mult*modosup5[:,2],linewidth=lww,label='mo i{} (x{})'.format(local_donor_index,mult),linestyle='-',color='black',zorder=1)
#                                                                                    
#                                                                    
#                                                                    
#                                                                                '''
#                                                                                PDOS header:
#                                                                                 'E[raw eV]', 'totnrm','snrm','pnrm','dnrm','fnrm','gnrm','hnrm','sum','surfnrm','bulknrm','surfsnrm','surfpnrm','surfdnrm','ontop_n','ontop_s','ontop_p','ontop_d'))
#                                                                                '''
#                                                                    
#                                                                                
#                                                                    
#                                                                                #d8 productions slabs:
#                                                                                if False:
#                                                                                    dpdosmult=20         #for the production d8 slabs...make this adaptable too...
#                                                                                    dmult=1 #0.02
#                                                                                    surfmult=5       #this value of 5 is for the production slabs d8.
#                                                                                
#                                                                    
#                                                                    
#                                                                                else:  #NEW DEFAULT SETTING, should work for all systems, but made with the He/Ru slabs:
#                                                                                    
#                                                                                    #Jan 2023: 
#                                                                                    #The problem with adapative scaling is that each system will scale differently and have its own legend.  
#                                                                                    #We need to fix axis limits and the scaling to be the same over all systems. Sorry that's just how it is.
#                                                                                    #if you want something special with scaling, make it tied to the size variable.
#                                                                                    
#                                                                                    adaptive_scaling=False
#                                                                                    if adaptive_scaling:
#                                                                                        updpdos_inrange = [ dpdosup[i,1] for i in range(len(dpdosup[:,0])) if (dpdosup[i,0] <= xmax) and (dpdosup[i,0] >= xmin) ]
#                                                                                        dndpdos_inrange = [ dpdosdn[i,1] for i in range(len(dpdosdn[:,0])) if (dpdosdn[i,0] <= xmax) and (dpdosdn[i,0] >= xmin) ]
#                                                                                        
#                                                                                        
#                                                                                        #if not nametail == "allstates":
#                                                                                        #    donor_target = 0.5 # *6 #3 #d4 setting
#                                                                                        #else:
#                                                                                        #    donor_target=0.7
#                                                                                       
#                                                                                        factor = (donor_target * ymax) / max(    max(updpdos_inrange), max(dndpdos_inrange)  ) 
#                                                                                        dpdosmult = round(factor,1 )
#                                                                                        
#                                                                                        
#                                                                                       
#                                                                                        #Jan 2023: we want to normalize DOS to per atom values, but keep contour scheme: Ndimeratoms, Nsurfatoms
#                                                                                        #we will perform that division above at the source.
#                                                                                        #and leave everything else here untouched maybe.
#                                                                                       
#                                                                                  #####  if size == 'SMALLF23':
#                                                                                  #####      surf_target = 0.5
#                                                                                  #####  
#                                                                                  #####  else:
#                                                                                        
#                                                                                        surf_target = 0.5
#                                                                                        
#                                                                                        surffactor = (surf_target * ymax) / max(pdosup[:,9])
#                                                                                        surfmult = round(surffactor,1)
#                                                                                        
#                                                                                        if size == 'SMALLF23': #special case.  we already adjusted the axis limits for the DOS. do not scale the dos (much) therefore.
#                                                                                            surfmult=0.6
#                                                                                       
#                                                                                        print('donor dos multiplied by {}, surfdos multiplied by {}'.format(dpdosmult, surfmult))
#                                                                                        #dmult=1 #0.02
#                                                                                        #surfmult=1       #this value of 5 is for the production slabs d8.
#                                                                                    
#                                                                                    else:
#                                                                                        
#                                                                                        if size == 'SMALLF23':
#                                                                                            dpdosmult=0.1
#                                                                                            surfmult=0.5
#                                                                                        
#                                                                                        else:
#                                                                                            dpdosmult=0.5
#                                                                                            surfmult=0.5
#                                                                                        
#                                                                                        
#                                                                                        #if nametail == 'allstates':
#                                                                                        #    dpdosmult=0.3
#                                                                                        #    surfmult=0.5
#                                                                                    
#                                                                                        if True: 
#                                                                                            surfmult = 1 #presentation. we don't even show the total slab dos anymore.
#                                                                                            
#                                                                    
#                                                                                #print('resonance_predicted {}'.format(resonance_predicted))
#                                                                                #show this only for the flagship d8 results.
#                                                                                #if False: ax.axvline(x=resonance_predicted, ymin=0., ymax=1000,linewidth=1,linestyle='--',color='red',alpha=1,zorder=0)          
#                                                                               # if False: ax.axvline(x=dband_edge_up[sysindex], ymin=0., ymax=1000,linewidth=1,linestyle='-',color=tumcolors['tumblue'],alpha=1,zorder=0)          
#                                                                               # if False: ax.axvline(x=spgap_up[sysindex], ymin=0., ymax=1000,linewidth=1,linestyle='-',color=tumcolors['tumorange'],alpha=1,zorder=0)          
#                                                                                    
#                                                                                #ax and ax1 formatting here:
#                                                                    
#                                                                    
#                                                                                #if size=='LARGE'   or size == 'LARGEP' or size =='LARGEF' or size == 'LARGEF2':
#                                                                                if True:    
#                                                                                    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
#                                                                                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
#                                                                                   # ax2.xaxis.set_major_locator(ticker.MultipleLocator(2))
#                                                                                   # ax2.xaxis.set_minor_locator(ticker.MultipleLocator(1))
#                                                                                
#                                                                                elif size=='SMALL':
#                                                                                    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
#                                                                                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
#                                                                                
#                                                                                elif size=='SMALLF3':
#                                                                                    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.2))
#                                                                                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
#                                                                       
#                                                                                print('ymax is {}'.format(ymax))
#                                                                    
#                                                                                if  ymax <= 10:
#                                                                                    dummy=1
#                                                                                    if False:
#                                                                                        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
#                                                                                        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#                                                                               # elif ymax > 10 and ymax < 100:
#                                                                               #     ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
#                                                                               #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
#                                                                                elif ymax >= 100:
#                                                                                #else:
#                                                                                    dummy=1
#                                                                                 
#                                                                                    ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
#                                                                                    ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))
#                                                                                
#                                                                                if size=='RES':
#                                                                                    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
#                                                                                    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.05))
#                                                                                
#                                                                                
#                                                                                if show_spin_down:
#                                                                                    ax.tick_params(
#                                                                                                axis='x',          # changes apply to the x-axis
#                                                                                                which='both',      # both major and minor ticks are affected
#                                                                                                bottom=False,      # ticks along the bottom edge are off
#                                                                                                top=True,         # ticks along the top edge are off
#                                                                                                direction='in',
#                                                                                                labelbottom=False) # labels along the bottom edge are off
#                                                                                    ax.tick_params(
#                                                                                                axis='y',          # changes apply to the x-axis
#                                                                                                which='both',      # both major and minor ticks are affected
#                                                                                                #bottom=False,      # ticks along the bottom edge are off
#                                                                                                left=True,
#                                                                                                direction='in',
#                                                                                                right=False,
#                                                                                                #top=True,         # ticks along the top edge are off
#                                                                                                labelleft=True) # labels along the bottom edge are off
#                                                                                else:
#                                                                                    if False: #sysindex == 5: 
#                                                                                        direction = 'out'
#                                                                                        labelbottom = True
#                                                                                    else: direction = 'in';labelbottom=False
#                                                                                    
#                                                                                    labelbottom=True
#                                                                    
#                                                                                    ax.tick_params(
#                                                                                                axis='x',          # changes apply to the x-axis
#                                                                                                which='both',      # both major and minor ticks are affected
#                                                                                                bottom=True,      # ticks along the bottom edge are off
#                                                                                                top=True,         # ticks along the top edge are off
#                                                                                                direction='in',
#                                                                                                labelbottom=labelbottom) # labels along the bottom edge are off
#                                                                                    ax.tick_params(
#                                                                                                axis='x',          # changes apply to the x-axis
#                                                                                                which='both',      # both major and minor ticks are affected
#                                                                                                bottom=True,      # ticks along the bottom edge are off
#                                                                                                top=True,         # ticks along the top edge are off
#                                                                                                direction=direction,
#                                                                                                labelbottom=labelbottom) # labels along the bottom edge are off
#                                                                                    ax.tick_params(
#                                                                                                axis='y',          # changes apply to the x-axis
#                                                                                                which='both',      # both major and minor ticks are affected
#                                                                                                #bottom=False,      # ticks along the bottom edge are off
#                                                                                                left=True,
#                                                                                                direction='in',
#                                                                                                right=False,
#                                                                                                #top=True,         # ticks along the top edge are off
#                                                                                                labelleft=True) # labels along the bottom edge are off
#                                                                    
#                                                                    
#                                                                    
#                                                                       
#                                                                       
#                                                                                if not show_spin_down:
#                                                                                    ax.set_xlabel(r'$\epsilon$ - $\epsilon_{\text{F}}$ [eV]')
#                                                                                
#                                                                    
#                                                                                ####
#                                                                                ####
#                                                                                ####OPTIONAL SPIN DOWN AXIS.
#                                                                    
#                                                                                if show_spin_down:   #for non-spin polarized systems....
#                                                                                
#                                                                    
#                                                                    
#                                                                                    ax2 = fig1.add_subplot(212,sharex=ax)
#                                                                                    if True: ax2.axvline(x=0, ymin=0., ymax=1000,linewidth=0.5,linestyle='--',color=tumcolors['black'],zorder=10)
#                                                                                    
#                                                                                    ax2.set_xlim(xmin,xmax)  #-1*HtoeV,1.5*HtoeV)
#                                                                                    ax2.set_ylim(ymin,ymax)  #-1*HtoeV,1.5*HtoeV)
#                                                                                    
#                                                                                    ax2.set_xlabel(r'$\epsilon$ - $\epsilon_{\text{F}}$ [eV]')
#                                                                                    
#                                                                                    if True:
#                                                                                        if False:ax2.annotate(r'\textbf{min.}',
#                                                                                                     xy=(0.9,0.2), textcoords='axes fraction',
#                                                                                                     va='center',rotation=None,size=8,annotation_clip=False)
#                                                                    
#                                                                                   
#                                                                                    #ax2.axvline(x=Ecenter_dn, ymin=0., ymax=1.,linewidth=1,linestyle='-',color=tumcolors['tumred'],zorder=0)          
#                                                                                    #if use_resonance: 
#                                                                                    #    dummy=1
#                                                                                    #    if False: ax2.axvline(x=resonance, ymin=0., ymax=1.,linewidth=1,linestyle='--',color=tumcolors['tumred'],zorder=0)          
#                                                                                        #ax2.annotate('Res.', xy=(resonance+0.1,0.2),textcoords=('data','axes fraction'),size=9,color="k")
#                                                                                        #ax2.errorbar( resonance, etimedn,yerr=errorbar, color='black' , fmt="o",markersize=0.5,capsize=1,elinewidth=0.5 )                                
#                                                                                
#                                                                    
#                                                                                    '''PDOS2 header: 
#                                                                                    'E[raw eV]', 'ads_norm','ads_snrm','ads_pnrm','ads_dnrm','ads_sum','ads_pxnrm','ads_pynrm','ads_pznrm'))
#                                                                                    '''
#                                                                                    if plot_ads_channels:
#                                                                                        lww=1
#                                                                                        ax2.plot( pdos2dn[:,0], pdos2dn[:,1],linewidth=lww,label='ads tot',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                        if True:
#                                                                                            ax2.plot( pdos2dn[:,0], pdos2dn[:,2],linewidth=lww,label='ads s',linestyle='-',color=tumcolors['tumorange'],zorder=2)
#                                                                                            ax2.plot( pdos2dn[:,0], pdos2dn[:,3],linewidth=lww,label='ads p',linestyle='-',color=tumcolors['tumred'],zorder=3)
#                                                                                            ax2.plot( pdos2dn[:,0], pdos2dn[:,4],linewidth=lww,label='ads d',linestyle='-',color=tumcolors['tumblue'],zorder=4)
#                                                                                            ax2.plot( pdos2dn[:,0], pdos2dn[:,6],linewidth=lww,label='ads px',linestyle='--',color='blue',zorder=5)
#                                                                                            ax2.plot( pdos2dn[:,0], pdos2dn[:,7],linewidth=lww,label='ads py',linestyle='--',color='green',zorder=6)
#                                                                                            ax2.plot( pdos2dn[:,0], pdos2dn[:,8],linewidth=lww,label='ads pz',linestyle='--',color='red',zorder=7)
#                                                                                    if plot_dimer_spdchannels:
#                                                                                        lww=1
#                                                                                        #ax.plot( pdosup[:,0], pdosup[:,2],linewidth=lww,label='d tot',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                        ax2.plot( pdosdn[:,0], pdosdn[:,2],linewidth=lww,label='total s',linestyle='-',color=tumcolors['tumorange'],zorder=2)
#                                                                                        ax2.plot( pdosdn[:,0], pdosdn[:,3],linewidth=lww,label='total p',linestyle='-',color=tumcolors['tumred'],zorder=3)
#                                                                                        ax2.plot( pdosdn[:,0], pdosdn[:,4],linewidth=lww,label='total d',linestyle='-',color=tumcolors['tumblue'],zorder=4)
#                                                                                    
#                                                                                    if plot_dimer_dchannels:
#                                                                                        lww=1
#                                                                                        ax2.plot( pdos3dn[:,0], pdos3dn[:,2],linewidth=lww,label='d tot',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                        ax2.plot( pdos3dn[:,0], pdos3dn[:,3],linewidth=lww,label='dxy',linestyle='-',color=tumcolors['tumorange'],zorder=2)
#                                                                                        ax2.plot( pdos3dn[:,0], pdos3dn[:,4],linewidth=lww,label='dyz',linestyle='-',color=tumcolors['tumred'],zorder=3)
#                                                                                        ax2.plot( pdos3dn[:,0], pdos3dn[:,5],linewidth=lww,label='dz2',linestyle='-',color=tumcolors['tumblue'],zorder=4)
#                                                                                        ax2.plot( pdos3dn[:,0], pdos3dn[:,6],linewidth=lww,label='dxz',linestyle='--',color=tumcolors['diag_purple_70'],zorder=5)
#                                                                                        ax2.plot( pdos3dn[:,0], pdos3dn[:,7],linewidth=lww,label='dx2y2',linestyle='--',color=tumcolors['tumgreen'],zorder=6)
#                                                                                
#                                                                                    if show_modos_unfilled: #and not show_modos_filled:   #overlayed.
#                                                                                        print('show_modos_unfilled')
#                                                                                        mult=1 #6
#                                                                                        lww=1
#                                                                                        if len(local_donor_indices)>0:
#                                                                                            local_donor_index=local_donor_indices[0]
#                                                                                            ax2.plot( modosdn[:,0],mult* modosdn[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-',color='red',zorder=1)
#                                                                                        if len(local_donor_indices)>1:
#                                                                                            local_donor_index=local_donor_indices[1]
#                                                                                            ax2.plot( modosdn1[:,0], mult*modosdn1[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-',color='green',zorder=1)
#                                                                                        if len(local_donor_indices)>2:
#                                                                                            local_donor_index=local_donor_indices[2]
#                                                                                            ax2.plot( modosdn2[:,0], mult*modosdn2[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-',color='blue',zorder=1)
#                                                                                      
#                                                   
#                                                                                        if True:  #i9                                                         
#                                                                                            if len(local_donor_indices)>3:
#                                                                                                local_donor_index=local_donor_indices[3]
#                                                                                                ax2.plot( modosdn3[:,0], mult*modosdn3[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-',color='orange',zorder=1)
#                                                                                        if True:  #i10                                                                
#                                                                                            if len(local_donor_indices)>4:
#                                                                                                local_donor_index=local_donor_indices[4]
#                                                                                                ax2.plot( modosdn4[:,0], mult*modosdn4[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-',color='brown',zorder=1)
#                                                                                            
#                                                                                        if True:                 #other                                                
#                                                                                            if len(local_donor_indices)>5:
#                                                                                                local_donor_index=local_donor_indices[5]
#                                                                                                ax2.plot( modosdn5[:,0], mult*modosdn5[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-',color='black',zorder=1)
#                                                                                
#                                                                    
#                                                                                
#                                                                    
#                                                                                    '''
#                                                                                    PDOS header:
#                                                                                     'E[raw eV]', 'totnrm','snrm','pnrm','dnrm','fnrm','gnrm','hnrm','sum','surfnrm','bulknrm','surfsnrm','surfpnrm','surfdnrm','ontop_n','ontop_s','ontop_p','ontop_d'))
#                                                                                    '''
#                                                                                    #if plot_totaldos and plot_ads_channels:
#                                                                                    surfalpha = 1.0 #0.25 #production.
#                                                                                    if show_total_dos: ##not show_modos_filled:
#                                                                                        ax2.fill_between( pdosdn[:,0], pdosdn[:,1],interpolate=True,
#                                                                                                                    #color=tumcolors['lightgray'],label=r'Total DOS',alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                                    color=tumcolors['lightgray'],label=r'Total DOS',alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                    if show_surf_dos: ##not show_modos_filled:
#                                                                                        ax2.plot( pdosdn[:,0], pdosdn[:,9],lw=0.5, color='black',label=r'Surf DOS',zorder=1)
#                                                                                    
#                                                                                    if show_active:    #active site channels
#                                                                                        lww=1# .5
#                                                                                       #file header:
#                                                                                       # E[raw eV] actnrm asnrm apnrm apxnrm apynrm apznrm adnrm | adxynrm adyznrm adz2nrm adxznrm adx2y2nrm
# 
#                                                                                        #show_active_options = ['tot','spd','pxyz','dxyz']
#                                                                                        if show_active_option =='tot':
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,1],linewidth=lww,label='active site tot',linestyle='-',color=tumcolors['black'],zorder=1)
#                                                                                        if show_active_option =='spd':
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,2],linewidth=lww,label='act. s', linestyle='-',  color=tumcolors['tumorange'] ,zorder=2)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,3],linewidth=lww,label='act. p', linestyle='-',  color=tumcolors['tumred']    ,zorder=3)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,7],linewidth=lww, label='act. d',linestyle='-',  color=tumcolors['tumblue'] ,zorder=6)
#                                                                                        if show_active_option =='pxyz':
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,4],linewidth=lww,label='act. px', linestyle='-', color='blue', zorder=4)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,5],linewidth=lww,label='act. py', linestyle='-', color='green', zorder=4)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,6],linewidth=lww,label='act. pz', linestyle='-',color='red', zorder=5)
#                                                                                                                                              
#                                                                                        if show_active_option =='dxyz':
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,8],linewidth=lww, label='act. dxy',linestyle='-',   color =tumcolors['tumorange']     ,zorder=6)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,9],linewidth=lww, label='act. dyz',linestyle='-',   color =tumcolors['tumred']        ,zorder=6)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,10],linewidth=lww,label='act. dz2',linestyle='-',   color =tumcolors['tumblue']       ,zorder=6)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,11],linewidth=lww,label='act. dxz',linestyle='--',  color=tumcolors['diag_purple_70'] ,zorder=6)
#                                                                                            ax2.plot( pdosAdn[:,0], pdosAdn[:,12],linewidth=lww,label='act. dx2y2',linestyle='--',color=tumcolors['tumgreen']        ,zorder=6)
#                                                                                    if show_modos_filled:
#                                                                                        #each modos seperate.
#                                                                                        mult=1 #6
#                                                                                        lww=1
#                                                                                        if True: #Show each filled MODOS seperate
#                                                                                            #if imodos==6:
#                                                                                            if imodos in [0,6]:
#                                                                                                if len(local_donor_indices)>0:
#                                                                                                    local_donor_index=local_donor_indices[0]
#                                                                                                    ax2.fill_between( modosdn[:,0], mult*modosdn[:,2],interpolate=True,
#                                                                                                                     color='red',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                    norm1 =  scipy.integrate.simps(modosdn[:,2],x=modosdn[:,0] )  
#                                                                                                    if False: ax2.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.1),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                            #if imodos==7:
#                                                                                            elif imodos in [1,7]:
#                                                                                                if len(local_donor_indices)>1:
#                                                                                                    local_donor_index=local_donor_indices[1]
#                                                                                                    ax2.fill_between( modosdn1[:,0], mult*modosdn1[:,2],interpolate=True,
#                                                                                                                     color='green',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                    norm1 =  scipy.integrate.simps(modosdn1[:,2],x=modosdn1[:,0] )  
#                                                                                                    if False: ax2.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.1),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                            #if imodos==8:
#                                                                                            elif imodos in [2,8]:
#                                                                                                if len(local_donor_indices)>2:
#                                                                                                    local_donor_index=local_donor_indices[2]
#                                                                                                    ax2.fill_between( modosdn2[:,0], mult*modosdn2[:,2],interpolate=True,
#                                                                                                                     color='blue',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                    norm1 =  scipy.integrate.simps(modosdn2[:,2],x=modosdn2[:,0] )  
#                                                                                                    if False: ax2.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.1),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                            #if imodos==9:
#                                                                                            elif imodos in [3,9]:
#                                                                                                if len(local_donor_indices)>3:
#                                                                                                    local_donor_index=local_donor_indices[3]
#                                                                                                    ax2.fill_between( modosdn3[:,0], mult*modosdn3[:,2],interpolate=True,
#                                                                                                                     color='orange',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                    norm1 =  scipy.integrate.simps(modosdn3[:,2],x=modosdn3[:,0] )  
#                                                                                                    if False: ax2.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.1),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                            #if imodos==10:
#                                                                                            elif imodos in [4,10]:
#                                                                                                if len(local_donor_indices)>4:
#                                                                                                    local_donor_index=local_donor_indices[4]
#                                                                                                    ax2.fill_between( modosdn4[:,0], mult*modosdn4[:,2],interpolate=True,
#                                                                                                                     color='brown',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                    norm1 =  scipy.integrate.simps(modosdn4[:,2],x=modosdn4[:,0] )  
#                                                                                                    if False: ax2.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.1),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                            elif imodos in [5,11]:
#                                                                                                if len(local_donor_indices)>5:
#                                                                                                    local_donor_index=local_donor_indices[5]
#                                                                                                    ax2.fill_between( modosdn5[:,0], mult*modosdn5[:,2],interpolate=True,
#                                                                                                                     color='black',label='mo i{} x{}'.format(local_donor_index,mult),alpha=surfalpha,zorder=0,edgecolor=None)
#                                                                                                    norm1 =  scipy.integrate.simps(modosdn5[:,2],x=modosdn5[:,0] )  
#                                                                                                    if False: ax2.annotate("integral {} ".format(round(norm1,3)) , xy=(0.01,0.1),fontsize=4,textcoords=('axes fraction','axes fraction'),color="black")
#                                                                                      
#                                                                                  #  if False:                                                                
#                                                   
#                                                                                  #      if len(local_donor_indices)>3:
#                                                                                  #          local_donor_index=local_donor_indices[3]
#                                                                                  #          ax2.plot( modosdn3[:,0], mult*modosdn3[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='orange',zorder=1)
#                                                                                  #      if len(local_donor_indices)>4:
#                                                                                  #          local_donor_index=local_donor_indices[4]
#                                                                                  #          ax2.plot( modosdn4[:,0], mult*modosdn4[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='teal',zorder=1)
#                                                                                  #      
#                                                                                  #      if len(local_donor_indices)>5:
#                                                                                  #          local_donor_index=local_donor_indices[5]
#                                                                                  #          ax2.plot( modosdn5[:,0], mult*modosdn5[:,2],linewidth=lww,label='mo i{}'.format(local_donor_index),linestyle='-.',color='magenta',zorder=1)
#                                                   
#                                                                                    #if show_spin_down: 
#                                                                                    #    if False:
#                                                                                    #        ax2.axvline(x=resonance_predicted, ymin=0., ymax=1000,linewidth=1,linestyle='--',color='red',alpha=1,zorder=0)          
#                                                                                    if  ymax <= 10:
#                                                                                        dummy=1
#                                                                                        if False:
#                                                                                            ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
#                                                                                            ax2.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
#                                                                                   
#                                                                                    elif ymax >= 100:
#                                                                                    #else:
#                                                                                        dummy=1
#                                                                                        ax2.yaxis.set_major_locator(ticker.MultipleLocator(100))
#                                                                                        ax2.yaxis.set_minor_locator(ticker.MultipleLocator(50))
#                                                                                   
#                                                                                    
#                                                                                    if size=='RES':
#                                                                                        ax2.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
#                                                                                        ax2.xaxis.set_minor_locator(ticker.MultipleLocator(0.05))
#                                                                                    
#                                                                                    
#                                                                                    
#                                                                                    ax2.tick_params(
#                                                                                                axis='y',          # changes apply to the x-axis
#                                                                                                which='both',      # both major and minor ticks are affected
#                                                                                                left=True,      # ticks along the bottom edge are off
#                                                                                                right=False,         # ticks along the top edge are off
#                                                                                                direction='in',
#                                                                                                labelleft=True,
#                                                                                                labelright=False) # labels along the bottom edge are off
#                                                                                    ax2.tick_params(
#                                                                                                axis='x',          # changes apply to the x-axis
#                                                                                                which='both',      # both major and minor ticks are affected
#                                                                                                bottom=True,      # ticks along the bottom edge are off
#                                                                                                direction='in',
#                                                                                                top=False,         # ticks along the top edge are off
#                                                                                                labelbottom=True,
#                                                                                                labeltop=False) # labels along the bottom edge are off
#                                                                                    
#                                                                                       
#                                                                       
#                                                                       
#                                                                                #UNIT CONVERSION, sept 2022.
#                                                                                if True: #plotgamma_tot: 
#                                                                                    if False: fig1.text(0.97*shrinkfactor,0.6*shrinkfactor, r'$\Delta(\epsilon)$ [eV]',va='center',rotation='vertical') 
#                                                                                #Jan 2023:
#                                                                                if True: #sysindex in [0,1,2,3,5]:  ALL SYSTEMS SCALED. #scaling is only performed for the production systems.
#                                                                                    fig1.text(0.03,0.6*shrinkfactor,'DOS [N/eV/atom]',va='center',rotation='vertical') 
#                                                                                else: 
#                                                                                    fig1.text(0.03,0.6*shrinkfactor,'DOS [N/eV/cell]',va='center',rotation='vertical') 
#                                                                                
#                                                                    
#                                                                    
#                                                                                if show_spin_down:  ax2.invert_yaxis()
#                                                                    
#                                                                            #    if show_spin_down:  
#                                                                            #        if False: ax2.annotate(syslabels[sysindex], xy=(0.02,0.15),
#                                                                            #                 textcoords='axes fraction',size=10,color="k")
#                                                                            #    else:
#                                                                            #        if False: ax.annotate(syslabels[sysindex], xy=(0.02,0.75),
#                                                                            #                 textcoords='axes fraction',size=10,color="k")
#                                                                    
#                                                                       
#                                                                                #tick labels to sans-serif???
#                                                                                ax.xaxis.get_major_formatter()._usetex = False
#                                                                                ax.yaxis.get_major_formatter()._usetex = False
#                                                                                #ax11.xaxis.get_major_formatter()._usetex = False
#                                                                                ax.yaxis.set_tick_params(which='minor', right=False, left=True)
#                                                                                
#                                                                                if show_spin_down:  
#                                                                                    ax2.xaxis.get_major_formatter()._usetex = False
#                                                                                    ax2.yaxis.get_major_formatter()._usetex = False
#                                                                                    ax2.yaxis.set_tick_params(which='minor', right=False, left=True)
#                                                                                
#                                                                                #plt.tight_layout()
#                                                                                                    
#                                                                                if show_legend:
#                                                                                    ax_exists=False
#                                                                                    ax2_exists=False
#                                                                                    ax22_exists=False
#                                                                                    ax11_exists=False
#                                                                                    if True: #plotddos_tot or plotdpdos or  plotados_tot or plotpdos:  
#                                                                                        lines, labels = ax.get_legend_handles_labels();
#                                                                                        ax_exists=True;
#                                                                                        if show_spin_down:    ax2_exists = True
#                                                                                    if False: #plotgamma_tot or plotpgamma     :  
#                                                                                        lines2, labels2 = ax11.get_legend_handles_labels();
#                                                                                        #ax11_exists=True
#                                                                                        if show_spin_down: dummy=1#      ax22_exists=True
#                                                                                    
#                                                                                    #if plotados or plotddos: lines, labels = ax.get_legend_handles_labels()
#                                                                                    #if plotgamma: lines2, labels2 = ax11.get_legend_handles_labels()
#                                                                                    if False: #THIS WORKS.  placed inside. 
#                                                                                        ax.legend(lines + lines2, labels + labels2, loc='upper right',framealpha=0.5,scatterpoints=1,fontsize=4)
#                                                                                    
#                                                                                    if True:  #TEST: place outside.
#                                                                                        #resize axes.
#                                                                                        frac=shrinkfactor #0.6
#                                                                                        box = ax.get_position()
#                                                                                        if ax_exists: 
#                                                                                            ax.set_position([box.x0, box.y0, box.width * frac, box.height*frac])
#                                                                                      #  if ax11_exists: 
#                                                                                      #      ax11.set_position([box.x0, box.y0, box.width * frac, box.height*frac])
#                                                                                        
#                                                                                        
#                                                                                        if ax2_exists: 
#                                                                                            box2 = ax2.get_position()
#                                                                                            ax2.set_position([box2.x0, box2.y0, box2.width * frac,box2.height*frac])
#                                                                                      #  if ax22_exists: 
#                                                                                      #      ax22.set_position([box2.x0, box2.y0, box2.width * frac, box2.height*frac])
#                                                                                        #this one works now:
#                                                                                        
#                                                                                        # Put a legend to the right of the current axis
#                                                                                        #ax.legend(loc='center left', bbox_to_anchor=(1.2, 0.5))
#                                                                                        if True: #placed outside.
#                                                                                            if ax_exists and ax11_exists:
#                                                                                                LINES = lines+lines2; LABELS = labels+labels2
#                                                                                            elif ax_exists and not ax11_exists:
#                                                                                                LINES = lines; LABELS = labels
#                                                                                            elif not ax_exists and  ax11_exists:
#                                                                                                LINES = lines2; LABELS = labels2
#                                                                    
#                                                                                            ax.legend(LINES, LABELS,loc='center left', bbox_to_anchor=(1.02, 0.5),framealpha=0.5,scatterpoints=1,fontsize=4)
#                                                                    
#                                                                       
#                                                                                plt.subplots_adjust(hspace=0.0)
#                                                                                figname = 'dimer_properties/dimer_PDOSX' 
#                                                                                if BZ_averaging:
#                                                                                    figname=figname+'_stddev'  #normalization factor
#                                                                                    figname+='{}'.format(stddev)
#                                                                                #if use_resonance: figname=figname+'_r'
#                                                                                #if plot_totaldos: figname=figname+'_d'
#                                                                                if plot_ads_channels: figname=figname+'_ads'
#                                                                                if plot_dimer_spdchannels: figname=figname+'_dim'   #global channels (dz2 is the target)
#                                                                                if plot_dimer_dchannels: figname=figname+'_dd'   #global channels (dz2 is the target)
#                                                                                figname = figname + '_{}'.format(size)
#                                                                                if show_total_dos: figname = figname+'_tot'
#                                                                                if show_surf_dos: figname = figname+'_surf'
#                                                                                if show_active: figname = figname+'_act_{}'.format(show_active_option)
#                                                                                if show_legend: figname = figname + '_legend'
#                                                                                if show_modos_unfilled: figname = figname + '_modos'
#                                                                                #if show_modos_filled: figname = figname + '_modosi{}filled'.format(imodos)
#                                                                                if show_modos_filled: figname = figname + '_fill_i{}'.format(imodos)
#                                                                                if not show_spin_down:
#                                                                                    figname = figname + '_uponly'
#                                                                                print(figname)
#                                                                                matplotlibhelpers.write(figname,dpi=300,transparent=False,write_info = False,write_png=True,write_pdf=pdf,write_eps=False)
#                                                                                plt.close(fig1)
#            
#            
        
        return None;







 
 

def plot_ref_dos():


    '''
    2025:  reference systems DOS comparison
    '''
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)
    
    
    #LOAD DATA 
    TM = pd.read_csv('CSV/TM_parameters.csv')
    #df = pd.read_csv('CSV/parsed_df.csv')



    df = pd.read_csv(
                 'CSV/parsed_df.csv',
                 converters={
                             "metal": str,
                             "termination": str
                            }
                    )



    #consider all entries in the dictionary.
    metals = df['metal'].tolist()
    terminations = df['termination'].tolist()
    
    print('len metals {}'.format(len(metals)))
    
    cluster='Niflheim'
    #plot DOS of all these metals.    
 
    a = xy_plot(cluster)
    a.plot_ref_dos_inner(cluster, metals, terminations, df, TM)



                        
    
    return None;


if __name__ == "__main__":
    plot_ref_dos()
