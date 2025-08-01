from ase.io import read,write
from matplotlib.pyplot import cm
import numpy as np
from ase.mep import NEBTools
import matplotlib.pyplot as plt
import sys,os
import matplotlib

#plt.rcParams["figure.figsize"] = (7,5)
plt.rcParams["font.family"] = "sans-serif"
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

reference_to_FS=False
s_all={}
E_all={}
colors=cm.jet(np.linspace(0,1,7))
potentials=[2.40,2.90,3.40,3.90,4.40]
fig, axes = plt.subplots(4,2,figsize=(7,6),sharex=True,sharey=True)
fig.subplots_adjust(hspace=0)
fig.subplots_adjust(wspace=0)
axes = axes.flatten()
elements=['Ag','Au','Cu','Ir','Ni','Pd','Pt','Rh']
for idx,element in enumerate(elements):
    ax=axes[idx]
    for i,pot in enumerate(potentials):
        if element=='Ni' and pot==4.40:
            continue
        infile=f'tafel/{element}/pot_{pot:1.2f}.traj'
        readfile=infile+'@:'
        atoms = read(readfile)
        s_all[infile],E_all[infile],Sfit,Efit,lines = NEBTools(atoms).get_fit()
        if reference_to_FS:
            E_all[infile]-=E_all[infile][0]
            Efit-=Efit[0]
        ax.plot(Sfit/s_all[infile][-1], Efit, '-', color=colors[i])
        ax.plot(np.array(s_all[infile])/s_all[infile][-1], E_all[infile], 'o', color=colors[i],markeredgecolor='k')
        if idx==7:
            ax.plot(np.nan,np.nan,'o-',color=colors[i],label='Pot=%1.2f V'%pot)
    #if idx%2==0:
        #ax.set_ylabel('Energy [eV]')
    if idx>5:
        ax.set_xlabel('Relative reaction path')
    ax.set_ylim([-1.0,1.5])
    ax.set_yticks([0,1])
    ax.set_xlim([0,1])
    ax.set_xticks([0.2,0.4,0.6,0.8])
    ax.text(0.15, 0.8, element,transform=ax.transAxes,fontsize=12)
    #plt.tight_layout()
ax.legend(bbox_to_anchor=(0.75,4.5),ncols=3)
fig.text(0.04, 0.5, 'Energy [eV]', va='center', rotation='vertical',fontsize=12)
fig.savefig('tafel_bands.pdf')
#fig.close()
