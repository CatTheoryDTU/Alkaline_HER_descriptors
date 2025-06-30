
"""
subplot array

Y correlate with descriptors X


"""


import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import math        
from matplotlib import rcParams
import matplotlib.ticker as ticker   
from sklearn.linear_model import LinearRegression





def parse_results():
    """
    parse .txt files to dataframe
    """
    filenames=[
        'metals.txt',
        'PZCs.txt', 
        'vac_Htops.txt',
        'vac_HBEs.txt',
        'i0s.txt',
        'volmers.txt',
        'tafels.txt',
        'heyrovskys.txt'
             ]
    
    path='../'
    
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
    volmers = data[5]
    tafels = data[6]
    heyrovskys = data[7]
    
    print('len metals {}'.format(len(metals)))
    
    rlist = [] 
    for j in range(len(metals)):
        attributes = {
                "metal" : metals[j],
                "PZC" : PZCs[j],
                "vac_Htop" : vac_Htops[j],
                "vac_HBE" : vac_HBEs[j],
                "i0" : i0s[j],
                "volmer" : volmers[j],
                "tafel" : tafels[j],
                "heyrovsky" :heyrovskys[j]
                  }
        
        rlist.append(attributes)
        
    df = pd.DataFrame(rlist)
    print(df)

    df.to_csv('CSV/results.csv',index=False)

    return df


def plot_array(dd,labels):

    lrbt=[0.3,0.9,0.2,0.95]
    rcParams['figure.subplot.left'] = lrbt[0]  
    rcParams['figure.subplot.right'] = lrbt[1] 
    rcParams['figure.subplot.bottom'] = lrbt[2]
    rcParams['figure.subplot.top'] = lrbt[3] #


    print('number of columns: {}'.format(len(dd.keys())))

    
    #general parameters 
    fs=9
    arsize=7
    fsize = 8 #arsize
    SKregression = True
    sp=0.5
    #optional CURATE A SUBSET.
    subset  = range(len(dd['metal']))
    excluded_from_regression=[]
    exclude = [] #['Al','Zn']
    show_equation=True 
    


    #dx,dy=(0.1,0.01)
    dx,dy=(0.0,0.03)
    capcoord=(-0.2,-0.3)
    r2duplet=(0.85,1.05)
    r3duplet=(0.2,1.05)

    fig, ax = plt.subplots(1,1, figsize=(2.5,2.5)) 

    for ykey in ['i0']: 
        for xkey in [dd.keys()[1]]:
            print('ykey {}, xkey {}'.format(ykey,xkey))

            ax.set_box_aspect(1)
            ax.tick_params(axis='y',direction='in',which='both',left=True, right=False, labelleft='on')
            ax.tick_params(axis='x',direction='in',which='both',bottom=True, top=False, labelbottom='on')
            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=sp, hspace=sp)
            
            xvals=dd[xkey].to_numpy().reshape((-1, 1))
            yvals=dd[ykey].to_numpy().reshape((-1, 1))
            ax.scatter(xvals, yvals,s=5, color='black')
            for i in range(len(dd['metal'].tolist())): 
                ax.annotate('{}'.format(dd['metal'].tolist()[i]), xy = (xvals[i]+dx, yvals[i]+dy), fontsize=arsize,ha='center',textcoords='data', color="k",annotation_clip=False)                      
            if SKregression: 
                LR = LinearRegression().fit(xvals[subset],yvals[subset])
                r_sq = LR.score(xvals[subset],yvals[subset]) 
                stringlabel=r'R$^2$:'+' {}'.format(round(r_sq,2))
                ax.annotate('{}'.format(stringlabel), xy=r2duplet,ha='center', xycoords = ('axes fraction'), textcoords=('axes fraction'), color="blue",fontsize=fsize,annotation_clip=False)     
                if show_equation:
                    string2label='y={}x+{}'.format(round(LR.coef_[0][0],2), round(LR.intercept_[0],2))
                    ax.annotate('{}'.format(string2label), xy=r3duplet,ha='center', xycoords = ('axes fraction'), textcoords=('axes fraction'), color="blue",annotation_clip=False, fontsize=fsize)
                sorted_xvals = np.sort( np.array([xvals[i][0] for i in subset])).reshape(-1, 1)
                y_pred = LR.predict(sorted_xvals)
                ax.plot(sorted_xvals,y_pred,lw=1, linestyle='--',color='black',zorder=0 )
            
            ax.set_xlabel(labels[xkey],fontsize=fs) 
            ax.set_ylabel(labels[ykey],fontsize=fs) 
    
   
    figname='testarray'

    print(figname)
    plt.savefig('output/'+figname+'.png',dpi=300)
#    plt.savefig('output/'+figname+'.pdf',dpi=300)

    return None




if __name__ == "__main__":
    
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)


    #LOAD DATA 
    df = parse_results()
    
    #load elementary descriptors
    #Hammer_Norskov2000 parameters
    TM = pd.read_csv('CSV/TM_parameters.csv')
   

    #Vojvodic 2013 parameters
    Voj = pd.read_csv('CSV/Vojvodic_parsed_to_excel.csv',converters={"metal": str, 'termination': str})

    metals = df['metal'].tolist()
    terminations = []
    for metal in metals:
        if metal in ['Fe','W']: 
            termination = '110'
        elif metal in [ 'Os','Ru','Re','Zn','Co' ]:
            termination = '0001'
        else: 
            termination='111'
        terminations.append(termination)


    #ake a master df, then simply plot columns.
    

    metals = df['metal'].tolist()
    dcenters  = np.array([float(Voj.loc[ Voj['metal'] == metal, 'ed'].iloc[0])  for metal in metals ] )
    mcns= np.array( [float(Voj.loc[ Voj['metal'] == metal, 'mcn'].iloc[0])  for metal in metals ] )
    dwidths = 4*np.sqrt(mcns)
    dedges = dcenters + dwidths/2
    vads  =  np.array( [float(Voj.loc[ Voj['metal'] == metal, 'vad'].iloc[0])  for metal in metals ] )
    pzcs=np.array([float(df.loc[ df['metal'] == metal, 'PZC'].iloc[0])  for metal in metals ] )
    wfs = []
    for i in range(len(metals)):
        wfs.append(  float( TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ].iloc[0])  )
    wfs = np.array(wfs)
    hfccs = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_HBE'].iloc[0])  for metal in metals ] )
    htops = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_Htop'].iloc[0]) for metal in metals ] )
    hdiffs = htops - hfccs  
    volmers= np.array(  [ float( df.loc[ df['metal'] == metal, 'volmer'].iloc[0])  for metal in metals ] )
    tafels= np.array(  [  float(df.loc[ df['metal'] == metal, 'tafel'].iloc[0])  for metal in metals ] )
    heyrovskys= np.array(  [ float(df.loc[ df['metal'] == metal, 'heyrovsky'].iloc[0])  for metal in metals ] )
    i0s= np.array(  [float(df.loc[ df['metal'] == metal, 'i0'].iloc[0])  for metal in metals ] )

    dd = pd.DataFrame({
                       'metal':metals,
                       'dcenter':dcenters,
                       'dedge':dedges,
                       'dwidth':dwidths,
                       'vad':vads,
                       'pzc':pzcs,
                       'wf':wfs,
                       'htop':htops,
                       'hfcc':hfccs,
                       'hdiff':hdiffs,
                       'volmer':volmers,
                       'heyrovsky':heyrovskys,
                       'tafel':tafels,
                       'i0':i0s
                             })


    labels = {
          'dcenter':  r'd-band center $\epsilon_d$ [eV]',
          'dedge':    r'upper d-band edge [eV]',
          'dwidth':   r'd-band width [eV]',
          'vad':      r'|V$_{ad}$|$^2$ [Rel. Cu]',
          'pzc':      r'PZC [V]',
          'wf' :      r'WF $\phi_{Exp.}$ [eV]',
          'htop':     r'$\Delta$G$_{\text{H}}^{\text{top}}$ [eV]',
          'hfcc':     r'$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]',
          'hdiff':    r'$\Delta$G$_{\text{H}}^{\text{top}}$-$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]',
          'volmer':   r'$\Delta \Omega_{\text{Volmer}} ^{\ddagger}$ [eV]',
          'tafel':    r'$\Delta \Omega_{\text{Tafel}} ^{\ddagger}$ [eV]',
          'heyrovsky':r'$\Delta \Omega_{\text{Heyrovsky}} ^{\ddagger}$ [eV]',
          'i0':       r'log($|j_0|$/(mA cm$^{-2}$))'
         }
    
    #Now plot arrays.
    #first array: exchange current vs descriptors
    #second array: barriers vs descriptors
    #third: HBE vs descriptors
    #fourth: descriptors vs. themselves

    plot_array(dd,labels)








#    for ykey in ['i0','heyrovsky','volmer','tafel','PZC','vac_Htop','vac_HBE','WF','Htop-Hfcc','dbandcenterVoj','dbandupperedgeVoj','dbandwidthVoj']: 
#        for xkey in ['Htop-Hfcc','vac_HBE','vac_Htop','PZC','WF', 'dbandcenterVoj','dbandupperedgeVoj','dbandwidthVoj','vsquaredRELVoj']:
#
#            if ykey == 'volmer':
#                yvals= np.array(  [ float( df.loc[ df['metal'] == metal, 'volmer'].iloc[0])  for metal in metals ] )
#                ylabel=r'$\Delta \Omega_{\text{Volmer}} ^{\ddagger}$ [eV] '
#            
#            elif ykey == 'tafel':
#                yvals= np.array(  [  float(df.loc[ df['metal'] == metal, 'tafel'].iloc[0])  for metal in metals ] )
#                ylabel=r'$\Delta \Omega_{\text{Tafel}} ^{\ddagger}$ [eV] '
#            
#            elif ykey == 'heyrovsky':
#                print('TEST heyrovsky {}'.format(ykey))
#                yvals= np.array(  [ float(df.loc[ df['metal'] == metal, 'heyrovsky'].iloc[0])  for metal in metals ] )
#                ylabel=r'$\Delta\Omega_{\text{Heyrovsky}}^{\ddagger}$ [eV] '
#                print(ykey)
#                print(yvals)
#            
#            elif ykey == 'i0':
#                yvals= np.array(  [float(df.loc[ df['metal'] == metal, ykey].iloc[0])  for metal in metals ] )
#                ylabel=r'log($|j_0|$/(mA cm$^{-2}$))'
#            
#            elif ykey == 'PZC':
#                yvals= np.array(  [float(df.loc[ df['metal'] == metal, ykey].iloc[0])  for metal in metals ] )
#                ylabel=r'PZC [V]'
#            
#            elif ykey == 'vac_Htop':
#                yvals= np.array(  [float(df.loc[ df['metal'] == metal, ykey].iloc[0])  for metal in metals ] )
#                ylabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$ [eV]' #vac, Dipam, free energy.
#            
#            elif ykey == 'vac_HBE':
#                yvals= np.array(  [float(df.loc[ df['metal'] == metal, ykey].iloc[0])  for metal in metals ] )
#                ylabel=r'$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac, Dipam, free energy
#            
#            elif ykey == 'Htop-Hfcc':
#                htops= np.array(  [float(df.loc[ df['metal'] == metal, 'vac_Htop'].iloc[0])  for metal in metals ] )
#                hfccs= np.array(  [float(df.loc[ df['metal'] == metal, 'vac_HBE'].iloc[0])  for metal in metals ] )
#                yvals = htops - hfccs  #vac, Dipam, free energy
#                ylabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$-$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac
#            
#            elif ykey == 'WF':   
#                ylabel=r'WF $\phi_{Exp.}$ [eV]'
#                WF = []
#                for i in range(len(metals)):
#                    WF.append(  float(TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ])  )
#                WF = np.array(WF)
#                yvals=WF
#            
#            elif ykey == 'vsquaredREL':
#                yvals  = np.array(  [float(TM.loc[ TM['metal'] == metal, ykey].iloc[0]) for metal in metals ] )
#                ylabel=r'|V$_{ad}$|$^2$ [Rel. Cu]' 
#            
#
#            elif ykey == 'dbandcenter': 
#                yvals  = np.array(  [float(TM.loc[ TM['metal'] == metal, ykey].iloc[0])  for metal in metals ] )
#                ylabel=r'd-band center $\epsilon_d$ [eV]'
#        
#            elif ykey == 'dbandupperedge':   
#                yvals= np.array(  [ float(TM.loc[ TM['metal'] == metal, ykey].iloc[0])  for metal in metals ] )
#                ylabel=r'd-band upper edge [eV]'
#            
#            elif ykey == 'dbandcenterVoj': 
#                yvals  = np.array(  [Voj.loc[ Voj['metal'] == metal, 'ed']  for metal in metals ] )
#                ylabel=r'd-band center $\epsilon_d$ [eV]'
#        
#            elif ykey == 'dbandupperedgeVoj':   
#                
#                dcenters = np.array(  [Voj.loc[ Voj['metal'] == metal, 'ed']  for metal in metals ] )
#                
#                mcns= np.array(  [Voj.loc[ Voj['metal'] == metal, 'mcn']  for metal in metals ] )
#                
#                dwidths = 4*np.sqrt(mcns)
#                dedges = dcenters + dwidths/2
#                yvals = dedges
#                ylabel=r'd-band upper edge [eV]'
#            
#            elif ykey == 'dbandwidthVoj':   
#                mcns= np.array(  [Voj.loc[ Voj['metal'] == metal, 'mcn']  for metal in metals ] )
#                dwidths = 4*np.sqrt(mcns)
#                yvals = dwidths
#                ylabel=r'd-band width [eV]'
#            
#            elif ykey == 'vsquaredRELVoj':
#                yvals  = np.array(  [Voj.loc[ Voj['metal'] == metal, 'vad']  for metal in metals ] )
#                ylabel=r'|V$_{ad}$|$^2$ [Rel. Cu]' 
#            
#             
#
#
#
#            if xkey == 'WF':   
#                xlabel=r'WF $\phi_{Exp.}$ [eV]'
#                WF = []
#                for i in range(len(metals)):
#                    WF.append(  float(TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ])  )
#         
#                WF = np.array(WF)
#                xvals=WF
#            
#            elif xkey == 'vac_HBE':
#                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
#                xlabel=r'$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac
#            
#            elif xkey == 'vac_Htop':
#                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
#                xlabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$ [eV]' #vac
#            
#            elif xkey == 'Htop-Hfcc':
#                htops= np.array(  [df.loc[ df['metal'] == metal, 'vac_Htop']  for metal in metals ] )
#                hfccs= np.array(  [df.loc[ df['metal'] == metal, 'vac_HBE']  for metal in metals ] )
#                xvals = htops - hfccs
#                xlabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$-$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac
#            
#            elif xkey == 'dbandcenter': 
#                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
#                xlabel=r'd-band center $\epsilon_d$ [eV]'
#        
#            elif xkey == 'dbandupperedge':   
#                xvals= np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
#                xlabel=r'd-band upper edge [eV]'
#            
#
#            elif xkey == 'dbandcenterVoj': 
#                xvals  = np.array(  [Voj.loc[ Voj['metal'] == metal, 'ed']  for metal in metals ] )
#                xlabel=r'd-band center $\epsilon_d$ [eV]'
#        
#            elif xkey == 'dbandupperedgeVoj':   
#                
#                dcenters = np.array(  [Voj.loc[ Voj['metal'] == metal, 'ed']  for metal in metals ] )
#                
#                mcns= np.array(  [Voj.loc[ Voj['metal'] == metal, 'mcn']  for metal in metals ] )
#                
#                dwidths = 4*np.sqrt(mcns)
#                dedges = dcenters + dwidths/2
#                xvals = dedges
#                xlabel=r'd-band upper edge [eV]'
#            
#            elif xkey == 'vsquaredRELVoj':
#                xvals  = np.array(  [Voj.loc[ Voj['metal'] == metal, 'vad']  for metal in metals ] )
#                xlabel=r'|V$_{ad}$|$^2$ [Rel. Cu]' 
#            
#
#            elif xkey == 'vsquaredREL':
#                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
#                xlabel=r'|V$_{ad}$|$^2$ [Rel. Cu]' 
#            
#            
#            elif xkey == 'dbandwidthVoj':   
#                mcns= np.array(  [Voj.loc[ Voj['metal'] == metal, 'mcn']  for metal in metals ] )
#                dwidths = 4*np.sqrt(mcns)
#                xvals = dwidths
#                xlabel=r'd-band width [eV]'
#            
#            elif xkey == 'PZC':
#                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
#                xlabel=r'PZC [V]'
#            
#                
#            print('metals are {}'.format(metals))
#            print('xvals are {} {}'.format(xkey, xvals))
#            print('yvals are {} {}'.format(ykey, yvals))
#         #   plot_scatter(xvals, yvals,metals,terminations, xlabel, ylabel,xkey,ykey) 


    

