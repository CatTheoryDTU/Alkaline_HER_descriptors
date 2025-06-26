
"""

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
        'i0s.txt'
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


def plot_scatter(xvals, yvals,metals,terminations, xlabel, ylabel,xkey,ykey) :

    print(' ')
    print('plotting y {} vs x {} '.format( ykey,xkey))

    lrbt=[0.3,0.9,0.2,0.95]
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


    yvals= yvals.reshape((-1, 1))
    xvals = xvals.reshape((-1, 1))
    
    print('xvals shape {}'.format(xvals.shape))
    
    if True:

        ax.scatter(xvals, yvals,s=5, color='black')
        
        arsize=6
        #dx,dy=(0.1,0.01)
        dx,dy=(0.0,0.03)
        
        for i in range(xvals.shape[0]):
            #ax.annotate('{}{}'.format(metals[i],terminations[i]), xy=(xvals[i]+dx,yvals[i]+dy),
            ax.annotate('{}'.format(metals[i]), xy=(xvals[i]+dx,yvals[i]+dy),
                        fontsize=arsize,ha='center',textcoords='data',
                        color="k",annotation_clip=False)                      
        
        capcoord=(-0.2,-0.3)
        
        #optional CURATE A SUBSET.
        subset  =[]
        excluded_from_regression=[]
        exclude = [] #['Al','Zn']
        for i in range(len(metals)):
            if math.isnan(xvals[i]) or math.isnan(yvals[i]) or metals[i] in exclude: 
                print('dropping NaN at index {} which is metal {}'.format(i,metals[i]))
                excluded_from_regression.append(metals[i])
                continue
            else:
                subset.append(i)
        print('subset of values is {}'.format(subset))
        

        SKregression = True
        if SKregression: 
            LR = LinearRegression().fit(xvals[subset],yvals[subset])
            r_sq = LR.score(xvals[subset],yvals[subset]) 
            print('coefficient of determination:', r_sq)
            print('intercept:', LR.intercept_)
            print('slope:', LR.coef_)
            stringlabel=r'R$^2$:'+' {}'.format(round(r_sq,2))
            #r2duplet=(0.85,0.9)
            r2duplet=(0.5,1.01)
            fsize = 8 #arsize
            ax.annotate('{}'.format(stringlabel), xy=r2duplet,ha='center',
                            xycoords = ('axes fraction'), 
                            textcoords=('axes fraction'),
                            color="blue",fontsize=fsize,annotation_clip=False)     
            #plot the linear fit please:
            sorted_xvals = np.sort( np.array([xvals[i][0] for i in subset])).reshape(-1, 1)
            print('xvals {}'.format(xvals))
            print('sorted_xvals {}'.format(sorted_xvals))

            y_pred = LR.predict(sorted_xvals)
            ax.plot(sorted_xvals,y_pred,lw=1, linestyle='--',color='black',zorder=0 )
                    
            capcoord=(0.40,-0.4)
            if False: 
                ax.annotate('R2 excludes: {}'.format(excluded_from_regression), 
                             xy=capcoord,ha='center', fontsize=arsize,
                             xycoords = ('axes fraction'), textcoords=('axes fraction'),
                             color="k",annotation_clip=False)                      
        
        
        fs=9
        ax.set_xlabel(xlabel,fontsize=fs) 
        ax.set_ylabel(ylabel,fontsize=fs) 
    
   
    figname='{}_vs_{}_reg{}'.format(ykey,xkey,SKregression)

    print(figname)
    plt.savefig('output/'+figname+'.png',dpi=300)
    plt.savefig('output/'+figname+'.pdf',dpi=300)

    return None




if __name__ == "__main__":
    
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)


    #LOAD DATA 
    df = parse_results()
    
    #load elementary descriptors
    TM = pd.read_csv('CSV/TM_parameters.csv')
    
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


    for ykey in ['i0','PZC','vac_Htop','vac_HBE','WF','Htop-Hfcc']: 
        for xkey in ['Htop-Hfcc','vac_HBE','vac_Htop','PZC','vsquaredREL','WF', 'dbandcenter','dbandupperedge']:  
        
            if ykey == 'i0':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'log($|j_0|$/(mA cm$^{-2}$))'
            elif ykey == 'PZC':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'PZC [V]'
            elif ykey == 'vac_Htop':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$ [eV]' #vac
            elif ykey == 'vac_HBE':
                yvals= np.array(  [df.loc[ df['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac
            elif ykey == 'Htop-Hfcc':
                htops= np.array(  [df.loc[ df['metal'] == metal, 'vac_Htop']  for metal in metals ] )
                hfccs= np.array(  [df.loc[ df['metal'] == metal, 'vac_HBE']  for metal in metals ] )
                yvals = htops - hfccs
                ylabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$-$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac
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
                ylabel=r'$\epsilon_d$ upper edge [eV]'
                ylabel=r'd-band upper edge [eV]'
            
            elif ykey == 'vsquaredREL':
                yvals  = np.array(  [TM.loc[ TM['metal'] == metal, ykey]  for metal in metals ] )
                ylabel=r'|V$_{ad}$|$^2$ [Rel. Cu]' 
             



            if xkey == 'WF':   
                xlabel=r'WF $\phi_{Exp.}$ [eV]'
                WF = []
                for i in range(len(metals)):
                    WF.append(  float(TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ])  )
         
                WF = np.array(WF)
                xvals=WF
            elif xkey == 'vac_HBE':
                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac
            elif xkey == 'vac_Htop':
                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$ [eV]' #vac
            elif xkey == 'Htop-Hfcc':
                htops= np.array(  [df.loc[ df['metal'] == metal, 'vac_Htop']  for metal in metals ] )
                hfccs= np.array(  [df.loc[ df['metal'] == metal, 'vac_HBE']  for metal in metals ] )
                xvals = htops - hfccs
                xlabel=r'$\Delta$G$_{\text{H}}^{\text{top}}$-$\Delta$G$_{\text{H}}^{\text{fcc}}$ [eV]' #vac
            
            elif xkey == 'dbandcenter': 
                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'd-band center $\epsilon_d$ [eV]'
        
            elif xkey == 'dbandupperedge':   
                xvals= np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'd-band upper edge [eV]'
            
            elif xkey == 'vsquaredREL':
                xvals  = np.array(  [TM.loc[ TM['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'|V$_{ad}$|$^2$ [Rel. Cu]' 
            elif xkey == 'PZC':
                xvals= np.array(  [df.loc[ df['metal'] == metal, xkey]  for metal in metals ] )
                xlabel=r'PZC [V]'
            
                
            print('metals are {}'.format(metals))
            print('xvals are {} {}'.format(xkey, xvals))
            print('yvals are {} {}'.format(ykey, yvals))
            plot_scatter(xvals, yvals,metals,terminations, xlabel, ylabel,xkey,ykey) 


    

