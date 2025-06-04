
"""

PCA of exchange currents versus descriptors


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


    i0s = np.array( [ float(df.loc[ df['metal'] == metal, 'i0'].iloc[0])  for metal in metals ] )
            
    WFs = []
    for i in range(len(metals)):
        WFs.append(  float(TM.loc[ TM['metal'] == metals[i], 'WF{}'.format(terminations[i] ) ].iloc[0])  )

    
    rdict = {
             'PZC': [ float(df.loc[ df['metal'] == metal, 'PZC'].iloc[0]) for metal in metals ] ,
             'vac_Htop': [ float(df.loc[ df['metal'] == metal, 'vac_Htop'].iloc[0]) for metal in metals ] ,
             'vac_HBE': [ float(df.loc[ df['metal'] == metal, 'vac_HBE'].iloc[0]) for metal in metals ] 
             'dbandcenter': [ float(TM.loc[ TM['metal'] == metal, 'dbandcenter'].iloc[0])  for metal in metals ] ,
             'dbandupperedge': [ float(TM.loc[ TM['metal'] == metal, 'dbandupperedge'].iloc[0])  for metal in metals ] ,
             'vsquaredREL': [ float(TM.loc[ TM['metal'] == metal, 'vsquaredREL'].iloc[0]) for metal in metals ],
             'WF': WFs
             }
                 
    
    df_pca = pd.DataFrame(rdict)
            
    #PCA analysis
    #if True:
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    print('pca analysis')
    #TUTORIAL: https://stackoverflow.com/questions/47370795/pca-on-sklearn-how-to-interpret-pca-components
    #from sklearn import datasets
    #iris = datasets.load_iris()
    #X = iris.data
    #y = iris.target
    
    X=df_pca
    y=i0s

    #In general it is a good idea to scale the data
    if True:
        scaler = StandardScaler()
        scaler.fit(X)
        X=scaler.transform(X)
        
        pca = PCA()
        pca.fit(X,y)
        x_new = pca.transform(X)   
    
    def myplot(score,coeff,labels=None):
        xs = score[:,0]
        ys = score[:,1]
        n = coeff.shape[0]
    
        sc=plt.scatter(xs ,ys, c = y,cmap='viridis') #without scaling
        
        for i in range(n):
            plt.arrow(0, 0, coeff[i,0], coeff[i,1],color = 'r',alpha = 0.5)
            if labels is None:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, "Var"+str(i+1), color = 'g', ha = 'center', va = 'center')
            else:
                plt.text(coeff[i,0]* 1.15, coeff[i,1] * 1.15, labels[i], color = 'g', ha = 'center', va = 'center')
        cbar = plt.colorbar(sc)
        ylabel=r'log($|j_0|$/(mA cm$^{-2}$))'#   i0s [TOF]d-band upper edge (maj.spin.) [eV]'
        cbar.set_label(ylabel, rotation=270,fontsize=10,labelpad=20)

    plt.xlabel("PC{}".format(1))
    plt.ylabel("PC{}".format(2))
    plt.grid()
    
    ddf2 = pd.DataFrame(pca.components_, columns=list(df_pca.columns))
    print('pca.components_ :')
    print(format(ddf2))
    print('pca.explained_variance_ratio_ :')
    print( pca.explained_variance_ratio_)
    
    #Call the function. 
    myplot(x_new[:,0:2], pca.components_) 
    #plt.show()
    plt.savefig('output/pca.png')
    plt.close()






