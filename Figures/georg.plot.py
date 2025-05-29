from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress

rcParams = {
        'font.family': 'sans-serif',
        #'font.serif': ['Times New Roman'],
        'font.size': 12,
        }
plt.rcParams.update(rcParams)
data = np.loadtxt('data.georg')
fig,ax=plt.subplots(1, 3, figsize=(7, 2.5),sharey=True)
# Perform linear regression

c1s=np.linspace(0.01,1.,100)
c2s=np.linspace(0.0,1.,101)

rxns= ['V','H','T']
rxns_long= ['Volmer','Heyrovsky','Tafel']
colors = ['r', 'g', 'b']

all_r2s = []
for ibar, bar in enumerate([2,3,4]):
    hmin_k, hmin_d, hmin_r, p_value, std_err = linregress(data[:, 0], data[:, bar])
    htop_k, htop_d, htop_r, p_value, std_err = linregress(data[:, 1], data[:, bar])
    r2s=[]

    # Perform linear regression for more sophisticated descriptors

    # find r2 for varying coefficients before htop - hfcc
    vec=np.array([data[:, 1], data[:, 0]])
#    c1s=np.linspace(0.02,2.2,110)
#    c2s=np.linspace(0.0,2.2,100)
    hdiff_k1, hdiff_d1 = 0, 0
    for c1 in c1s:
        for c2 in c2s:
            coeffs = (c1,c2)
            hdiff_k, hdiff_d, hdiff_r, p_value, std_err = linregress(
                    coeffs[0]*vec[0]-coeffs[1]*vec[1], data[:, bar])
            if abs(c1-1) < 0.001 and abs(c2-1) < 0.001:
                hdiff_k1,hdiff_d1=hdiff_k,hdiff_d
            #if ibar==2:
            r2s.append([c1,c2,hdiff_r**2])

    r2s = np.array(r2s)
    # Plot 1:1 correlation
    ax[0].plot(data[:, 0], hmin_k*data[:, 0] + hmin_d, '-', color=colors[ibar], label=f'{rxns[ibar]}={hmin_k:.2f}x+{hmin_d:.2f}, R$^2$={hmin_r**2:.2f}')
    ax[0].plot(data[:, 0], data[:, bar], 'o', color=colors[ibar])
    ax[1].plot(data[:, 1], htop_k*data[:, 1] + htop_d, '-', color=colors[ibar], label=f'{rxns[ibar]}={htop_k:.2f}x+{htop_d:.2f}, R$^2$={htop_r**2:.2f}')
    ax[1].plot(data[:, 1], data[:, bar], 'o', color=colors[ibar])

    # Perform linear regression for more sophisticated descriptors
    ax[2].plot(data[:, 1]-data[:, 0], hdiff_k1*(data[:, 1]-data[:, 0]) + hdiff_d1, '-', color=colors[ibar], label=f'{rxns[ibar]}={hdiff_k:.2f}x+{hdiff_d:.2f}, R$^2$={hdiff_r**2:.2f}')
    ax[2].plot(data[:, 1]-data[:, 0], data[:, bar], 'o', color=colors[ibar])
    #ax[2].plot(coeffs[0]*data[:, 1]-coeffs[1]*data[:, 0], hdiff_k*(coeffs[0]*data[:, 1]-coeffs[1]*data[:, 0]) + hdiff_d, '-', color=colors[ibar], label=f'{rxns[ibar]}={hdiff_k:.2f}x+{hdiff_d:.2f}, R$^2$={hdiff_r**2:.2f}')
    #ax[2].plot(coeffs[0]*data[:, 1]-coeffs[1]*data[:, 0], data[:, bar], 'o', color=colors[ibar])
    all_r2s.append(r2s)

ax[0].set_ylabel('Activation energy (eV)')
ax[0].set_xlabel(r'$\Delta G_{H,min}$ (eV)')
ax[1].set_xlabel(r'$\Delta G_{H,top}$ (eV)')
ax[2].set_xlabel(r'$\Delta G_{H,top} - \Delta G_{H,min}$ (eV)')
ax[0].legend(loc='upper left')
ax[1].legend(loc='upper left')
ax[2].legend(loc='upper left')


fig.tight_layout()
#plt.show()
plt.gca()
#print(all_r2s)

fig,ax=plt.subplots(1, 3, figsize=(7, 2.5), sharey=True)
#fig.suptitle(r'Testing correlations of a*$\Delta G_{H,top}$ - b*$\Delta G_{H,fcc}$ based on a and b')
for ibar, bar in enumerate([2,3,4]):
    r2 = all_r2s[ibar]
    bestfit=r2[np.argmax(r2[:, 2])]
    #ax[ibar].set_title(f'{rxns_long[ibar]}')
    im = ax[ibar].imshow(r2[:, 2].reshape(len(c1s), len(c2s)), extent=(min(c1s), max(c1s), min(c2s), max(c2s)), aspect='auto', origin='lower',
               vmin=0.5, vmax=1.0,cmap='RdYlGn', interpolation='bicubic')
    ax[ibar].plot([min(c2s),max(c2s)],[min(c2s),max(c2s)], 'k--')
    ax[ibar].set_xlim(min(c1s), max(c1s))
    #plt.axvline(x=bestfit[0], color='r', linestyle='--')
    #plt.axhline(y=bestfit[1], color='r', linestyle='--')
    ax[ibar].set_xlabel(r'b ($\Delta G^{top}_H$)')
#    if ibar==2:
#        plt.colorbar(label=r'$R^2$', orientation='vertical')

fig.colorbar(im,label=r'Descriptor Strength, $R^2$', orientation='vertical')
ax[0].set_ylabel(r'a ($\Delta G^{fcc}_H$)')
labels=['d)','e)','f)']
from matplotlib.transforms import ScaledTranslation
for label, ax in zip(labels,ax):
    ax.text(
        0.0, 1.0, label, transform=(
            ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
        fontsize='medium', va='bottom', fontfamily='serif')
    ax.set_yticks([0,0.5,1.0])
plt.show()

#print (r2s)
#print(bestfit)
fig.savefig('Georg.pdf',bbox_inches="tight")
