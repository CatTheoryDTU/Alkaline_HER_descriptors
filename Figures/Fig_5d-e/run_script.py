from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress
from tools import (
        plot_1_to_1_correlations,
        plot_r2_with_varying_contribution_of_descriptors,
        collect_data,
        plot_volcano,
        correlate_descriptors,
        plot_r2_with_varying_descriptors_in_2D)

rcParams = {
        'font.family': 'serif',
        'font.serif': ['Times New Roman'],
        'font.size': 26,
        }
plt.rcParams.update(rcParams)

metal_order = ['Ni', 'Pd', 'Ir', 'Rh', 'Pt', 'Cu', 'Ag', 'Au']
rxns_long= ['Volmer','Heyrovsky','Tafel']
colors = ['r', 'g', 'b']

if 1:
    data=collect_data()
else:
    import pickle
    data=pickle.load(open('data.pckl', 'rb'))

"""
data is a dictionary that contains all the data
dict_keys: Binding energies: 'hfcc', 'htop',
           Barriers: 'Volmer', 'Heyrovsky', 'Tafel',
           Elements: 'metal',
           Electronic structure: 'vsquaredREL', 'dbandcenter', 'PZC',
           Hybrid descriptors: 'hfcc-pzc' (is actually hfcc-0.58PZC), 'htop-hfcc'])
"""

# Plot correlations between descriptors
if 0:
    correlate_descriptors(data, descriptors=['htop-hfcc','vsquaredREL'])
    correlate_descriptors(data, descriptors=['htop','hfcc-pzc'])

# Plot 1-dimensional correlations
if 0:
 plot_1_to_1_correlations(data, descriptors=['hfcc', 'htop', 'hfcc-pzc','htop-hfcc','vsquaredREL'])

if 0:
    c1s=np.linspace(0.01,1.,100)
    c2s=np.linspace(0.0,1.,101)
    plot_r2_with_varying_contribution_of_descriptors(data,
                                                     rxns_long,
                                                     descriptors=['htop','hfcc'],
                                                     c1s=c1s,
                                                     c2s=c2s)
    plot_r2_with_varying_contribution_of_descriptors(data,
                                                     rxns_long,
                                                     descriptors=['hfcc','PZC'],
                                                     c1s=c1s,
                                                     c2s=c2s)
    plot_r2_with_varying_contribution_of_descriptors(data,
                                                     rxns_long,
                                                     descriptors=['htop-hfcc','vsquaredREL'],
                                                     c1s=c1s,
                                                     c2s=c2s)
# Plot 2-dimensional mixed descriptor quality (possibly fig 5d)
if 1:
    plot_r2_with_varying_descriptors_in_2D(data,
                                                    rxns_long,
                                                    descriptors=['htop','hfcc'],
                                                    cs=np.linspace(-1.3,1.3,500))

#   plot_r2_with_varying_descriptors_in_2D(data,
#                                                    rxns_long,
#                                                    descriptors=['hfcc-pzc','htop'],
#                                                    cs=np.linspace(-20,20,100))

# Plot volcano plots (possibly fig 5e)
if 1:
#    plot_volcano(data,descriptors=['hfcc-pzc','vsquaredREL'])
#    plot_volcano(data,descriptors=['htop','vsquaredREL'])
    plot_volcano(data,descriptors=['hfcc-pzc','htop-hfcc'],only_activity=True)
    plot_volcano(data,descriptors=['htop','htop-hfcc'],only_activity=True)


