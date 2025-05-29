import numpy as np
#barx: value for the barrier so the maximum is located at its x and y value
#(x_IS,En_IS): x and y values of the initial state
#(x_FS,En_FS): x and y value of the final state
#Eddag: y-value of the barrier
import json
from collections import namedtuple
metal='Pt'
data=json.load(open('results/%s/results.json'%metal,'r'),object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
H_ads=data.Hydrogen.energy
vol_bar=data.volmer.energy
hey_bar=data.heyrovsky.energy
vol_beta=data.volmer.beta
hey_beta=data.heyrovsky.beta
taf_bar=data.tafel.energy
pot=0.0
ground_states_tafel=[0,H_ads+pot,H_ads*2+pot*2,pot*2]
ground_states_heyrovsky=[0,H_ads+pot,pot*2]
def get_parabola(En_IS,En_FS,x_IS,x_FS,Eddag):
    bar_x=np.sqrt((En_IS-Eddag)*(En_FS-Eddag)*(x_IS-x_FS)**2)+En_IS*x_FS-En_FS*x_IS+Eddag*(x_IS-x_FS)
    bar_x/=En_IS-En_FS
    return bar_x
vol_x=get_parabola(0,ground_states_tafel[1],1,2,vol_bar+pot*vol_beta)
hey_x=get_parabola(ground_states_heyrovsky[1],ground_states_heyrovsky[2],3,4,hey_bar+pot*hey_beta)
vol_x2=get_parabola(ground_states_tafel[1],ground_states_tafel[2],3,4,vol_bar+pot*vol_beta)
taf_x=get_parabola(ground_states_tafel[2],ground_states_heyrovsky[2],5,6,taf_bar)
import mpl as
