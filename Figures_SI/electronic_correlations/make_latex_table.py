
"""

make latex table for SI

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
        'tafels.txt'
        #'heyrovskys.txt'
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
    #heyrovskys = data[7]
    
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
                "tafel" : tafels[j]
     #           "heyrovsky" :heyrovskys[j]
                  }
        
        rlist.append(attributes)
        
    df = pd.DataFrame(rlist)
    print(df)

    #df.to_csv('CSV/results.csv',index=False)

    return df


def print_table(df,fname):  
    dftable= df.to_latex(index=False,
                      formatters={"name": str.upper},
                      float_format="{:.2f}".format)
    print(dftable)

    with open(fname+'.tex', 'w') as tf:
         tf.write(dftable)


    return None





if __name__ == "__main__":
    
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)


    #Load our calculations 
    path = '../addFeW/'
    df = parse_results(path)

    #Load Vojvodic 2014 parameters
    Voj = pd.read_csv('CSV/Vojvodic_parsed_to_excel.csv',converters={"metal": str, 'termination': str})

    #Load Xin 2014 parameters
    Xin = pd.read_csv('CSV/Xin2014_edges.csv',converters={"metal": str})

    metals = df['metal'].tolist()
    
    dcenters  = np.array([float(Voj.loc[ Voj['metal'] == metal, 'ed'].iloc[0])  for metal in metals ] )

    #Vojvodic2014 d-upper-edge estimates
    #mcns= np.array( [float(Voj.loc[ Voj['metal'] == metal, 'mcn'].iloc[0])  for metal in metals ] )
    #dwidths = 4*np.sqrt(mcns)
    #dedges = dcenters + dwidths/2
    
    #use Xin2014 d-band upper edge (except Fe,W which are from Vojvodic2014). 
    dedges = []
    for metal in metals:
        if any(Xin['metal'] == metal): 
            dedges.append(float(Xin.loc[ Xin['metal'] == metal, 'dedge'].iloc[0]))
        elif any(Voj['metal'] == metal):
            print('using Voj2014 values for {} dedge'.format(metal))
            dcenter =  float(Voj.loc[ Voj['metal'] == metal, 'ed'].iloc[0])
            mcn =      float(Voj.loc[ Voj['metal'] == metal, 'mcn'].iloc[0]) 
            width = 4*np.sqrt( mcn )
            edge = dcenter + width/2
            dedges.append(edge)
        
    dedges = np.array(dedges)



    #use Vojvodic2014 couplings (same as Hammer2000) 
    vads  =  np.array( [float(Voj.loc[ Voj['metal'] == metal, 'vad'].iloc[0])  for metal in metals ] )
    
    #our calculations
    pzcs=np.array([float(df.loc[ df['metal'] == metal, 'PZC'].iloc[0])  for metal in metals ] )
    
    hfccs = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_HBE'].iloc[0])  for metal in metals ] )
    htops = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_Htop'].iloc[0]) for metal in metals ] )
    hdiffs = htops - hfccs  



    

    fname = 'electronic_parameters_table'
    df_table = pd.DataFrame({
                             'metal':metals,'dbandcenter':dcenters,'dupperedge':dedges,
                             'vad':vads,'PZC':pzcs
                             })
    
    print_table(df_table,fname)
    


    fname = 'hbe_table'
    df_table = pd.DataFrame({
                             'metal':metals, 'Hfcc':hfccs,'Htop':htops,'Hdiff':hdiffs 
                             })
            
             
    print_table(df_table,fname)




    

