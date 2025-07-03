
"""
subplot array
Y correlate with descriptors X

sources of electronic parameters used in descriptor analysis:

    D-band centers[all metals] and d-band upper edges[Fe,W only] are from
        Vojvodic et al 2014, DOI https://doi.org/10.1007/s11244-013-0159-2
    
    D-band upper edges [all metal except Fe,W] are from
        Xin et al 2014, DOI https://doi.org/10.1103/PhysRevB.89.115114
    
    Couplings vad [all metals] are from
        Vojvodic et al 2014, DOI https://doi.org/10.1007/s11244-013-0159-2
        which are taken originally from
        Hammer et al 2000, DOI: https://doi.org/10.1016/S0360-0564(02)45013-4

    PZC: this work.

"""



import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import math        
from matplotlib import rcParams
import matplotlib.ticker as ticker   
from sklearn.linear_model import LinearRegression
import string




def parse_results(path):
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

    #df.to_csv('CSV/results.csv',index=False)

    return df


def plot_array(dd,labels,flag):

    lrbt=[0.3,0.9,0.2,0.95]
    lrbt=[0.25,0.95,0.2,0.95]
    rcParams['figure.subplot.left'] = lrbt[0]  
    rcParams['figure.subplot.right'] = lrbt[1] 
    rcParams['figure.subplot.bottom'] = lrbt[2]
    rcParams['figure.subplot.top'] = lrbt[3] #
    rcParams['font.size'] = 8.0                     


    print('number of columns: {}'.format(len(dd.keys())))

    
    #general parameters 
    fs=9
    arsize=9
    fsize = 9 #arsize
    SKregression = True
    sp=0.1
    #optional CURATE A SUBSET.
    subset  = range(len(dd['metal']))
    excluded_from_regression=[]
    exclude = [] #['Al','Zn']
    


    #dx,dy=(0.1,0.01)
    dx,dy=(0.0,0.03)
    capcoord=(-0.3,1.1)
    r2duplet=(0.8,1.1)
    r3duplet=(0.2,1.1)


    Nkeys = len(dd.keys())
    
    for v in [1,2]: 
        
        if v==1:
            #Version 
            Nrows = 2
            Ncols = 2
            figsize = (4,4)
            ykeys = ['hdiff']*4 
            xkeys = ['dcenter','dedge','vad','pzc'] 
            figname='hdiff_vs_descriptors'
            show_equation=False
            hidden_axes = []
            fs=8
            arsize=6
            fsize = 8 #arsize
            rcParams['font.size'] = 8.0                     
            plt.subplots_adjust(hspace=1)
            use_label=True
        elif v==2:
            #Version 
            Nrows = 1
            Ncols = 3
            figsize = (6,2)
            ykeys = ['hfcc']*3
            xkeys = ['pzc']*3
            figname='hfcc_vs_pzc'
            show_equation=False
            hidden_axes = [0,2]
            fs=8
            arsize=6
            fsize = 8 #arsize
            rcParams['font.size'] = 8.0                     
            plt.subplots_adjust(hspace=1)
            use_label=False
    
    
        iss = range(Nrows*Ncols)
    
        fig, axs = plt.subplots(nrows=Nrows, ncols=Ncols, figsize=figsize )

        for ax, ykey,xkey,icap in zip(axs.flat, ykeys,xkeys,iss):
            print(ax)
            print('ykey {}, xkey {}'.format(ykey,xkey))
    
            ax.set_box_aspect(1)
            ax.tick_params(axis='y',direction='in',which='both',left=True, right=False, labelleft='on')
            ax.tick_params(axis='x',direction='in',which='both',bottom=True, top=False, labelbottom='on')
            plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=sp, hspace=sp)
            
            xvals=dd[xkey].to_numpy().reshape((-1, 1))
            yvals=dd[ykey].to_numpy().reshape((-1, 1))
            ax.scatter(xvals, yvals,s=5, color='black')
            for i in range(len(dd['metal'].tolist())): 
                ax.annotate('{}'.format(dd['metal'].tolist()[i]), 
                            xy = (xvals[i]+dx, yvals[i]+dy), fontsize=arsize,
                            ha='center',textcoords='data', color="k",annotation_clip=False)    
            if SKregression: 
                LR = LinearRegression().fit(xvals[subset],yvals[subset])
                r_sq = LR.score(xvals[subset],yvals[subset]) 
                stringlabel=r'R$^2$:'+' {}'.format(round(r_sq,2))
                ax.annotate('{}'.format(stringlabel), xy=r2duplet,ha='center', 
                            xycoords = ('axes fraction'), textcoords=('axes fraction'), 
                            color="blue",fontsize=fsize,annotation_clip=False)     
                if show_equation:
                    if LR.intercept_[0]>=0:  intercept ='+{}'.format(round(LR.intercept_[0],2))
                    elif LR.intercept_[0]<0:  intercept ='{}'.format(round(LR.intercept_[0],2))
                    string2label='y={}x{}'.format(round(LR.coef_[0][0],2), intercept)
                    ax.annotate('{}'.format(string2label), xy=r3duplet,ha='center', 
                                xycoords = ('axes fraction'), textcoords=('axes fraction'), 
                                color="blue",annotation_clip=False, fontsize=fsize)
                sorted_xvals = np.sort( np.array([xvals[i][0] for i in subset])).reshape(-1, 1)
                y_pred = LR.predict(sorted_xvals)
                ax.plot(sorted_xvals,y_pred,lw=1, linestyle='--',color='black',zorder=0 )
                    
            if use_label: ax.annotate('{})'.format(string.ascii_lowercase[icap]), xy=capcoord,
                                     ha='center', xycoords = ('axes fraction'), 
                                     textcoords=('axes fraction'), color="black",
                                     annotation_clip=False, fontsize=fsize)
            
            ax.set_xlabel(labels[xkey],fontsize=fs) 
            ax.set_ylabel(labels[ykey],fontsize=fs) 
       
            if icap in hidden_axes: 
                ax.axis('off') 
                ax.set_axis_off()
                ax.set_visible(False)

       
        if v==9: plt.subplots_adjust(hspace=0.6)
        #else:
        plt.tight_layout()
        #plt.show()
    
        figname +='{}'.format(flag)
        print(figname)
        plt.savefig('output/'+figname+'.png',dpi=300)
        plt.savefig('output/'+figname+'.pdf',dpi=300)

    return None




if __name__ == "__main__":
    
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)


    #Load calculations 
    path='../'
    df = parse_results(path)
    

    #Vojvodic 2014 parameters
    Voj = pd.read_csv('CSV/Vojvodic_parsed_to_excel.csv',converters={"metal": str, 'termination': str})
    
    #Xin 2014 parameters.
    Xin = pd.read_csv('CSV/Xin2014_edges.csv',converters={"metal": str})

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


    #make a master df, then plot columns.

    metals = df['metal'].tolist()
    
    #Vojvodic2014:
    dcenters  = np.array([float(Voj.loc[ Voj['metal'] == metal, 'ed'].iloc[0])  for metal in metals ] )
    
    mcns= np.array( [float(Voj.loc[ Voj['metal'] == metal, 'mcn'].iloc[0])  for metal in metals ] )
    dwidths = 4*np.sqrt(mcns)

    #Vojvodic2014, same as HammerNorskov2000
    vads  =  np.array( [float(Voj.loc[ Voj['metal'] == metal, 'vad'].iloc[0])  for metal in metals ] )
    
    #our calculations
    pzcs=np.array([float(df.loc[ df['metal'] == metal, 'PZC'].iloc[0])  for metal in metals ] )
    hfccs = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_HBE'].iloc[0])  for metal in metals ] )
    htops = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_Htop'].iloc[0]) for metal in metals ] )
    hdiffs = htops - hfccs  
    volmers= np.array(  [ float( df.loc[ df['metal'] == metal, 'volmer'].iloc[0])  for metal in metals ] )
    tafels= np.array(  [  float(df.loc[ df['metal'] == metal, 'tafel'].iloc[0])  for metal in metals ] )
    heyrovskys= np.array(  [ float(df.loc[ df['metal'] == metal, 'heyrovsky'].iloc[0])  for metal in metals ] )
    i0s= np.array(  [float(df.loc[ df['metal'] == metal, 'i0'].iloc[0])  for metal in metals ] )
    

    for edge_flag in ['Xin']: 
        if edge_flag == 'Voj': 
            #Vojvodic2014
            dedges = dcenters + dwidths/2
        elif edge_flag == 'Xin': 
            #Xin2014
            dedges =  np.array( [float(Xin.loc[ Xin['metal'] == metal, 'dedge'].iloc[0])  for metal in metals ] )
            edge_flag=''

        dd = pd.DataFrame({
                           'metal':metals,
                           'dcenter':dcenters,
                           'dedge':dedges,
                           'dwidth':dwidths,
                           'vad':vads,
                           'pzc':pzcs,
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
        

        plot_array(dd,labels,edge_flag)








    

