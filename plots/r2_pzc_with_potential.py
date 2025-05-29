from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
fig, ax= plt.subplots(1,1,figsize=(4,3))
volmers=np.loadtxt('volmers.txt')
volmer_betas=np.loadtxt('volmer_betas.txt')
heyrovskys=np.loadtxt('heyrovskys.txt')
heyrovsky_betas=np.loadtxt('heyrovsky_betas.txt')
PZCs=np.loadtxt('PZCs.txt')
HBEs=np.loadtxt('HBEs.txt')
colors=['k','r']
potentials=np.linspace(-1,1,101)
offset=[-0.2,0.1,-0.1]
r2s_pzc_volmer=[]
slopes_pzc_volmer=[]
r2s_pzc_heyrovsky=[]
slopes_pzc_heyrovsky=[]
r2s_hbe_volmer=[]
slopes_hbe_volmer=[]
r2s_hbe_heyrovsky=[]
slopes_hbe_heyrovsky=[]
for potential in potentials:
    xpzc=PZCs-4.4
    xhbe=HBEs
    vslope, intercept, r_value, p_value, std_err = linregress(xpzc,volmers+potential*volmer_betas)
    r2s_pzc_volmer.append(r_value**2)
    slopes_pzc_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(xpzc,heyrovskys+potential*heyrovsky_betas)
    r2s_pzc_heyrovsky.append(r_value**2)
    slopes_pzc_heyrovsky.append(hslope)
    vslope, intercept, r_value, p_value, std_err = linregress(xhbe,volmers+potential*volmer_betas)
    r2s_hbe_volmer.append(r_value**2)
    slopes_hbe_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(xhbe,heyrovskys+potential*heyrovsky_betas)
    r2s_hbe_heyrovsky.append(r_value**2)
    slopes_hbe_heyrovsky.append(hslope)
potentials=np.linspace(-2,0,101)
ax.plot(potentials,r2s_hbe_volmer,'k',potentials,r2s_hbe_heyrovsky,'r',potentials,r2s_pzc_volmer,'k--',potentials,r2s_pzc_heyrovsky,'r--')
ax.set_xlabel(r'Potential vs SHE')
ax.set_ylabel('$R^2$')
ax.legend(['Volmer','Heyrovsky'])
#fig.show()
fig.savefig('R2_both_with_potential.svg',bbox_inches="tight")
fig, ax= plt.subplots(1,1,figsize=(4,3))
ax.plot(potentials,slopes_hbe_volmer,'k',potentials,slopes_hbe_heyrovsky,'r',potentials,slopes_pzc_volmer,'k--',potentials,slopes_pzc_heyrovsky,'r--')
ax.set_xlabel(r'Potential vs SHE')
ax.set_ylabel('Slope')
ax.legend(['Volmer','Heyrovsky'])
#fig.show()
fig.savefig('Slopes_both_with_potential.svg',bbox_inches="tight")
