"""

d-band upper edge for pure metals:
Xin et al 2014
DOI  https://doi.org/10.1103/PhysRevB.89.115114

"""


import numpy as np
import pandas as pd
import sys


pd.options.display.max_rows = 4000
pd.set_option('display.max_colwidth', None)


#plot digitizer

ud = {
    "Ag": -3.076923,
    "Au":  -1.87912,
    "Cu": -1.505494,
    "Co": -0.65934,
    "Pd": 0.10439,
    "Ni": 0.3186813,
    "Pt": 0.241758,
    "Rh": 0.730769,
    "Ir": 0.96153846
}


df = pd.DataFrame(ud.items(), columns=['metal','dedge'])

df.to_csv('Xin2014_edges.csv',index=False)

