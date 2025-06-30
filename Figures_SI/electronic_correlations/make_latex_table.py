
"""

Y correlate with descriptors X


"""


import numpy as np
import pandas as pd
import sys




def print_table(df,fname):  
    dftable= df.to_latex(index=False,
                      #columns=['m','term1','term2','term3','term4','term5','TotalBarrier'],
                      formatters={"name": str.upper},
                      float_format="{:.2f}".format)
    print(dftable)

    with open(fname+'.tex', 'w') as tf:
         tf.write(dftable)


    return None





if __name__ == "__main__":
    
    
    pd.options.display.max_rows = 4000
    pd.set_option('display.max_colwidth', None)


    #LOAD DATA 
    df = pd.read_csv('CSV/results.csv')
    

    #Vojvodic 2014 parameters
    Voj = pd.read_csv('CSV/Vojvodic_parsed_to_excel.csv',converters={"metal": str, 'termination': str})


    metals = df['metal'].tolist()
    
    dcenters  = np.array([float(Voj.loc[ Voj['metal'] == metal, 'ed'].iloc[0])  for metal in metals ] )
 
    mcns= np.array( [float(Voj.loc[ Voj['metal'] == metal, 'mcn'].iloc[0])  for metal in metals ] )
    dwidths = 4*np.sqrt(mcns)
    dedges = dcenters + dwidths/2
    
    vads  =  np.array( [float(Voj.loc[ Voj['metal'] == metal, 'vad'].iloc[0])  for metal in metals ] )
    
    pzcs=np.array([float(df.loc[ df['metal'] == metal, 'PZC'].iloc[0])  for metal in metals ] )
    
    hfccs = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_HBE'].iloc[0])  for metal in metals ] )
    htops = np.array(  [float(df.loc[ df['metal'] == metal, 'vac_Htop'].iloc[0]) for metal in metals ] )
    hdiffs = htops - hfccs  

    
    #df_table = pd.DataFrame({'metal':metals,'dbandcenter':dcenters,'dupperedge':dedges,
    #                         'dwidth':dwidths,'vad':vads,'PZC':pzcs, 'Hfcc':hfccs,
    #                         'Htop':htops,'Hdiff':hdiffs })

    fname = 'electronic_parameters_table'
    df_table = pd.DataFrame({
                             'metal':metals,'dbandcenter':dcenters,'dupperedge':dedges,
                             'dwidth':dwidths,'vad':vads,'PZC':pzcs
                             })
    
    print_table(df_table,fname)
    


    fname = 'hbe_table'
    df_table = pd.DataFrame({
                             'metal':metals, 'Hfcc':hfccs,'Htop':htops,'Hdiff':hdiffs 
                             })
            
             
    print_table(df_table,fname)




    

