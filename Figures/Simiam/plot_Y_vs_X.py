
"""

Y correlate with descriptors X

handle missing data!



"""


import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import math        
from matplotlib import rcParams
import matplotlib.ticker as ticker   
from sklearn.linear_model import LinearRegression



def plot_scatter(xvals, yvals,metals, xlabel, ylabel,xkey,ykey) :
#def plot_scatter(xvals, yvals,metals, xlabel, ylabel,spin,mtag,dindex,site,zval,xkey,ykey,adsorbate): 
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



    yvals= yvals.reshape((-1, 1))
    xvals = xvals.reshape((-1, 1))
    
    print('xvals shape {}'.format(xvals.shape))
    
    if True:

        #NEW: plot df columns. do LR in pandas. Doesn't really work though? 

        ax.scatter(xvals, yvals,s=5, color='black')
        
        arsize=4
        #dx,dy=(0.1,0.01)
        dx,dy=(0.0,0.01)
        
        for i in range(xvals.shape[0]):
            ax.annotate('{}{}'.format(metals[i],terminations[i]), xy=(xvals[i]+dx,yvals[i]+dy),
                        fontsize=arsize,ha='center',textcoords='data',
                        color="k",annotation_clip=False)                      
        
        capcoord=(-0.2,-0.3)
        #ax.annotate('a)', xy=capcoord,ha='center',
        #                  xycoords = ('axes fraction'), 
        #                  textcoords=('axes fraction'),
        #                  color="k",annotation_clip=False) 
        
        #exclude W:
        #subset=range(len(metals))#-1)
        #Check for NaN
        #FILTER NANs
        #CURATE A SUBSET.
        subset  =[]
        excluded_from_regression=[]
        exclude = ['Al','Zn']
        for i in range(len(metals)):
            if math.isnan(xvals[i]) or math.isnan(yvals[i]) or metals[i] in exclude: 
                print('dropping NaN at index {} which is metal {}'.format(i,metals[i]))
                excluded_from_regression.append(metals[i])
                continue
            else:
                subset.append(i)
        print('subset of good values is {}'.format(subset))
        

        SKregression = False
        PDregression = False
        if SKregression: 
            LR = LinearRegression().fit(xvals[subset],yvals[subset])
            r_sq = LR.score(xvals[subset],yvals[subset]) 
            print('coefficient of determination:', r_sq)
            print('intercept:', LR.intercept_)
            print('slope:', LR.coef_)
            stringlabel=r'R$^2$:'+' {}'.format(round(r_sq,2))
            r2duplet=(0.4,0.9)
            ax.annotate('{}'.format(stringlabel), xy=r2duplet,ha='center',
                            xycoords = ('axes fraction'), 
                            textcoords=('axes fraction'),
                            color="blue",annotation_clip=False)     
            #plot the linear fit please:
            sorted_xvals = np.sort( np.array([xvals[i][0] for i in subset])).reshape(-1, 1)
            print('xvals {}'.format(xvals))
            print('sorted_xvals {}'.format(sorted_xvals))

            y_pred = LR.predict(sorted_xvals)
            ax.plot(sorted_xvals,y_pred,lw=1, linestyle='--',color='black',zorder=0 )
                    
            capcoord=(0.40,-0.3)
            ax.annotate('R2 Excludes: {}'.format(excluded_from_regression), xy=capcoord,ha='center', fontsize=arsize,
                                xycoords = ('axes fraction'), textcoords=('axes fraction') ,color="k",annotation_clip=False)                      
        
        if PDregression:
            dummy=1





        
        fs=6
        ax.set_xlabel(xlabel,fontsize=fs) 
        ax.set_ylabel(ylabel,fontsize=fs) 
    
   
    figname='{}_vs_{}_reg{}'.format(ykey,xkey,SKregression)

    if xkey == 'wdos':
        figname+='_{}pm_dindex{}{}'.format(zval,dindex,mtag) 
    

    print(figname)
    plt.savefig('output/'+figname+'.png',dpi=300)

    return None




if __name__ == "__main__":
    
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)
    
    
    #LOAD DATA 
    TM = pd.read_csv('CSV/TM_parameters.csv')

    #df_raw = pd.read_csv('../analysis_tafel/CSV/DFT_tafel_Dipam.csv')
   
    """
    #CONFIRM: wdos of H at 2A (4A) top reference geometry correlates well 
    #with some properties: WF and volmer, heyrovsky barriers (less so with Tafel).
    """
    #Simiam FHI-aims calculations at 2,4A.
    #df_wdos = pd.read_csv('../../scripts_packgl/bd_utils/runscripts/STM/reference_wdos/CSV/df_bd_HM111_REF.csv') 
    #dfHBE = pd.read_csv('../../scripts_packgl/bd_utils/runscripts/STM/reference_wdos/CSV/df_HBE_HM111_REF.csv') 

    #I want to see HBE, d-band center, edge, and WF correlated.
    #also with barriers.
    #does HBEtop for example correlate with its own hybridization? 
    #(finding correlation is one thing...deriving a model is something else) 


    #adsorbate='H'      
    #site='top'
    #spin='up';
    #mtag='_m2'
    #zvals = [200,400]  #we do tests at different elevations, [pm].


    #consider all entries in the dictionary.
    metals = TM['metal'].tolist()
            
    terminations = []
    for metal in metals:
        if metal in ['Fe','W']: 
            termination = '110'
        elif metal in [ 'Os','Ru','Re','Zn','Co' ]:
            termination = '0001'
        else: 
            termination='111'
        terminations.append(termination)



    #for ykey in ['WF','dbandcenter','dbandupperedge','vsquaredREL']: 
    for ykey in ['WF']: #,'dbandcenter','dbandupperedge','vsquaredREL']: 
        #, i''HBEdipam','HBEtop_ref_exact','HBEtop_ref_monolayer' ]:    
        #HBEdipam from df_raw (Dipam hollow HBEs which are potential-averaged???) 
        #Simiam DFT  HBEtop at 2A, 4A. 

        #for xkey in ['wdos', 'WF', 'dbandcenter','dbandupperedge','vsquaredREL']:  #VsquaredREL
        for xkey in ['WF','dbandcenter','dbandupperedge','vsquaredREL']:  
        #for xkey in ['dbandupperedge']: #,'vsquaredREL']:  
        
            if ykey == 'WF':   
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
            
            elif ykey == 'vsquaredREL':
                yvals  = np.array(  [TM.loc[ TM['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'V$_{ad}^2$ [Rel. Cu]' #eV$^2$]'
        
        
            if xkey == 'WF':   
                xlabel=r'WF $\phi_{Exp.}$ [eV]'
                #NEW WAY
                WF = []
                for i in range(len(metals)):
                    WF.append(  float(TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ])  )
         
                WF = np.array(WF)
                xvals=WF
            
            elif xkey == 'dbandcenter': 
                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'd-band center $\epsilon_d$ [eV]'
        
            elif xkey == 'dbandupperedge':   
                xvals= np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'd-band upper edge (maj.spin) [eV]'
            
            elif xkey == 'vsquaredREL':
                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'V$_{ad}^2$ [Rel. Cu]' #eV$^2$]'
            

            # arrays contain None. Is that a problem?
            print('metals are {}'.format(metals))
            print('terminations are {}'.format(terminations))
            print('xvals are {} {}'.format(xkey, xvals))
            print('yvals are {} {}'.format(ykey, yvals))
            plot_scatter(xvals, yvals,metals, xlabel, ylabel,xkey,ykey) 

            

            #VsquaredREL
            #all from TM.
            #if xkey=='wdos':
            #    dindices = [0] #,1,2,3,4]
            #else:
            #    dindices = [0]
            #for dindex in dindices:
            #    for zval in zvals:
                    

           #assemble xvals and yvals.

          #  if ykey == 'HBEdipam':
          #      #Dipams HBE hollow. POTENTIAL AVERAGED?
          #      #yvals = np.array(  [df_raw.loc[ df_raw['metal'] == metal, 'HBE']  for metal in metals ] )
          #      
        
          #      
          #      yvals = np.array( df_raw['HBE'] )
          #      metals = df_raw['metal'] # == metal, 'HBE']  for metal in metals ] )
          #      ylabel=r'HBE$_{\text{hollow,Dipam}}$ [eV]'
        
          #      terminations = []
          #      for i in range(metals.shape[0]):
          #          if metals[i] in ['Fe','W']:
          #              terminations.append('110')
          #          else:
          #              terminations.append('111')
        
        
        
          #  elif ykey == 'HBEtop_ref_exact' or ykey == 'HBEtop_ref_monolayer' :
          #      #SIMIAM's DFT calculations.
          #      ######NEW WAY:
          #      criteria=(dfHBE['site'] == site)    &\
          #               (dfHBE['zval'] == zval ) &\
          #               (dfHBE[ykey].notnull())       #removes NaN rows.
          #      
          #      yvals = np.array(   dfHBE.loc[ criteria,  ykey] )  #contains NaN 
          #      
          #      #NaNs have been removed.
          #      
          #      metals = np.array(   dfHBE.loc[ criteria,  'metal'] )
          #      terminations = np.array(  dfHBE.loc[ criteria,  'termination'] )
          #      
          #      if ykey == 'HBEtop_ref_exact': 
          #          ylabel=r'HBE$_{\text{top ref exact}}$ [eV]'+' {}A'.format(int(zval/100))
          #      if ykey == 'HBEtop_ref_monolayer': 
          #          ylabel=r'HBE$_{\text{top ref ML}}$ [eV]'+' {}A'.format(int(zval/100))
          #      
          #  print('yvals {}, metals {}'.format(yvals, metals))
        
          #  
          #  if xkey == 'wdos':
          #      #dindex=0;
          #      
          #      #We look up values of wdos for the metals above, but again check for NaN:
          #      #this is a risky label: perception risk
          #      orbital = np.array(df_wdos.loc[ (df_wdos['dindex'] == dindex) , 'orbital'])[0]
          #      
          #      wdos = []
          #      for i in range(metals.shape[0]):
          #          print('metal {}'.format(metals[i]))
          #          criteria=(df_wdos['dindex'] == dindex) &\
          #                   (df_wdos['site'] == site)    &\
          #                   (df_wdos['metal'] == metals[i])    &\
          #                   (df_wdos['mtag'] == mtag)    &\
          #                   (df_wdos['spin'] == spin ) &\
          #                   (df_wdos['zval'] == zval ) #&\
          #                  # (df_wdos[xkey].notnull())       
          #                  #removes NaN rows.  
          #                  #If you remove NaN here, you compromise the dimension.
          #          res=float(df_wdos.loc[ criteria, xkey  ] )
          #          print('result is {}'.format(res))
          #          wdos.append(res   )
          #      
          #      print('BEFORE NaN filtering:')
          #      print('yvals {}'.format(yvals))
          #      print('wdos {}'.format(wdos))
          #       
          #      #CONTAINS NANs
          #      #If we remove NaNs, we have to update yvals. 
          #      #CURATE A SUBSET.
          #      subset  =[]
          #      for i in range(len(wdos)):
          #          #if wdos[i]=='nan':
          #          if math.isnan(wdos[i]): ##=='nan':
          #              print('dropping NaN at index {} which is metal {}'.format(i,metals[i]))
          #              continue
          #          else:
          #              subset.append(i)
          #      print('subset of good values is {}'.format(subset))
          #      
          #      yvals = np.array([yvals[i] for i in subset])
          #      wdos = np.array([wdos[i] for i in subset])
          #      metals = [metals[i] for i in subset]
          #      terminations = [terminations[i] for i in subset]
        
          #      print('AFTER NaN filtering:')
          #      print('yvals {}'.format(yvals))
          #      print('wdos {}'.format(wdos))
        
          #      print('wdos is {}'.format(wdos))
          #      wdos = np.array(wdos)
          #      xvals=wdos
        
          #      xlabel=r'$\Delta_{\text{H}}(\epsilon_{F})$ [eV] '
