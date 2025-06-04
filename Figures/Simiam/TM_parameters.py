"""

Transition Metal parameters from literature, compiled by Simiam Ghan.

SOURCES

    d-band fillings, centers, couplings from
    Page 86, Fig 10. Theoretical Surface Science and Catalysis - Calculations and Concepts, 
    by B.Hammer, J.K.Norskov, in ADVANCES IN CATALYSIS, VOLUME 45, Elsevier (2000) 
    DOI: https://doi.org/10.1016/S0360-0564(02)45013-4
   
    d-band edges estimated visually (Simiam Ghan) from Materials Project bulk systems.

    Workfunctions are experimental, various sources. 

    To get absolute couplings squared, multiply relative values by:
    VsqCu=2.42 [eV^2] 
    Table 1, B.Hammer and J.K. Norskov 1995: DOI https://doi.org/10.1016/0039-6028(96)80007-0

"""


import numpy as np
import pandas as pd
import sys




rlist = [ 
         {
         'metal': "PtCu3Pt",  #Hammer1995
         "Z" : 78 ,
         "WF111": None,  
         "vsquaredREL" : 3.90, 
         "dbandcenter" : -2.55, 
         "dbandfilling" : 0.95,  #this is a guess. calculate from Hammer1995!!!!
         "dbandupperedge": None
         },
         {
         'metal': "CuCu3Pt",  #Hammer1995
         "Z" : 29 ,
         "WF111": None,  
         "vsquaredREL" : 1, 
         "dbandcenter" : -2.35, 
         "dbandfilling" : 0.95, #my guess, calculate!
         "dbandupperedge": None
         },
         {
         'metal': "NiNiAl",  #Hammer1995
         "Z" : 28 ,
         "WF111": None,  
         "vsquaredREL" : 1.34, 
         "dbandcenter" : -1.91, 
         "dbandfilling" : 0.9,  #my guess...calculate!
         "dbandupperedge": None
         },
         {
         'metal': "Ag", 
         "Z" : 47 ,
         "WF111": 4.46,  
         "vsquaredREL" : 2.26, 
         "dbandcenter" : -4.3, 
         "dbandfilling" : 1,
         "dbandupperedge": -2.82 #https://next-gen.materialsproject.org/materials/mp-124?chemsys=Ag 
         },
         { 
         "metal": "Au"  ,
         "Z" : 79  , 
         "WF111": 5.29,  
         "vsquaredREL" : 3.35, 
         "dbandcenter" : -3.56, 
         "dbandfilling" : 1,
         "dbandupperedge": -1.7 #https://next-gen.materialsproject.org/materials/mp-81?chemsys=Au
         },
         { 
         "metal": "Cu",
         "Z" : 29,
         "WF111": 4.94,  
         "vsquaredREL" : 1.0, 
         "dbandcenter" : -2.67, 
         "dbandfilling" : 1,
         "dbandupperedge": -1.44 #https://next-gen.materialsproject.org/materials/mp-30?formula=Cu
         },
         {
         "metal": "Fe",
         "Z": 26,
         "WF111": None,  
         "WF110": 5.07,  
         "vsquaredREL" : 1.59, 
         "dbandcenter" : -0.92, 
         "dbandfilling" : 0.7,
         "dbandupperedge": 0.21 #majority spin, https://next-gen.materialsproject.org/materials/mp-13?formula=Fe
         },
         { 
         "metal": "Co",
         "Z" : 27,
         "WF0001": 5.55,
         "WF111": None,
         "WF110": None,
         "vsquaredREL" : 1.34, 
         "dbandcenter" : -1.17, 
         "dbandfilling" : 0.8,
         "dbandupperedge": -0.48  #majority spin, https://next-gen.materialsproject.org/materials/mp-102?chemsys=Co   
         },
         {
         "metal": "Ni",
         "Z": 28,
         "WF111": 5.24,
         "vsquaredREL" : 1.34, 
         "dbandcenter" : -1.29, 
         "dbandfilling" : 0.9,
         "dbandupperedge": -0.36 #majority spin https://next-gen.materialsproject.org/materials/mp-23?formula=Ni
         },
         { 
         "metal": "Ir",
         "Z":77,
         "WF111": 5.7,          #online experiments.  
         "vsquaredREL" : 4.45, 
         "dbandcenter" : -2.11, 
         "dbandfilling" : 0.8,
         "dbandupperedge": 1.41 #https://next-gen.materialsproject.org/materials/mp-101?chemsys=Ir
         },
         {
         "metal": "Pd",
         "Z":46,
         "WF100": 5.48  ,
         "WF110": 5.07 ,    #
         "WF111": 5.67,
         "vsquaredREL" : 2.78, 
         "dbandcenter" : -1.83, 
         "dbandfilling" : 0.9,
         "dbandupperedge": 0.11 #majority spin. https://next-gen.materialsproject.org/materials/mp-2?formula=Pd
         },
         { 
         "metal":"Pt",
         "Z":78,
         "WF111": 5.91,  
         "vsquaredREL" : 3.9, 
         "dbandcenter" : -2.25, 
         "dbandfilling" : 0.9,
         "dbandupperedge": 0.55  #https://next-gen.materialsproject.org/materials/mp-126?formula=Pt
         },
         { 
         "metal" : "Rh",
         "Z" : 45, 
         "WF111":5.46,
         "vsquaredREL" : 3.32, 
         "dbandcenter" : -1.73, 
         "dbandfilling" : 0.8,
         "dbandupperedge": 0.94  #https://next-gen.materialsproject.org/materials/mp-74?formula=Rh 
         },
         { 
         "metal": "W",
         "Z" : 74,
         "WF111": None,
         "WF110": 5.44,
         "vsquaredREL" : 7.27, 
         "dbandcenter" : 0.77, 
         "dbandfilling" : 0.5,
         "dbandupperedge": 3.5  #https://next-gen.materialsproject.org/materials/mp-91?formula=W
         },
         { 
         "metal": "Re",
         "Z" : 75,
         "WF111": None,
         "WF110": None,
         "WF0001": 5.71,     #polycrystalline estimate...
         "vsquaredREL" : 6.04, 
         "dbandcenter" : -0.51, 
         "dbandfilling" : 0.6,
         "dbandupperedge": 4.33   #https://next-gen.materialsproject.org/materials/mp-1186901?formula=Re   
         },
         { 
         "metal": "Ru",
         "Z" : 44,
         "WF111": None,
         "WF110": None,
         "WF0001": 5.52,   #ESTIMATE
         "vsquaredREL" : 3.87, 
         "dbandcenter" : -1.41, 
         "dbandfilling" : 0.7,
         "dbandupperedge": 1.83 #https://next-gen.materialsproject.org/materials/mp-33?formula=Ru  
         },
         { 
         "metal": "Os",
         "Z" : 76,
         "WF111": None,
         "WF110": None,
         "WF0001": 5.7,   #ESTIMATE
         "vsquaredREL" : 5.13, 
         "dbandcenter" : -1.41, #Find value!  #"similar to Ru (-1.41)":  https://doi.org/10.1016/j.enrev.2023.100053 
         "dbandfilling" : 0.7,
         "dbandupperedge": 2.61 #https://next-gen.materialsproject.org/materials/mp-49?formula=Os   
         },
         { 
         "metal": "Zn",
         "Z" : 30,
         "WF111": None,
         "WF110": None,
         "WF0001": 4.15,
         "vsquaredREL" : 0.46, 
         "dbandcenter" : -5.1,    #dummy guess  
         "dbandfilling" : 1,
         "dbandupperedge": -4 #dummy guess   
         },
         { 
         "metal": "Al",
         "Z" : 13,
         "WF111": 4.32,
         "WF110": None,
         "vsquaredREL" : None, #0.1 would be my guess #dummy 
         "dbandcenter" : +5,  #dummy 
         "dbandfilling" : 0,
         "dbandupperedge": 6 #dummy
         }

        ]




df = pd.DataFrame(rlist)


df.to_csv('CSV/TM_parameters.csv',index=False)

df.to_json('CSV/TM_parameters.json',index=False)

sys.exit()

#df = pd.read_json()
#df = pd.read_csv()




