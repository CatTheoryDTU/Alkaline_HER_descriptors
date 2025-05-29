from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
rcParams = {
        'font.family': 'sans-serif',
        #'font.serif': ['Times New Roman'],
        'font.size': 12,
        }
plt.rcParams.update(rcParams)
volmers=np.loadtxt('volmers.txt')
tafels=np.loadtxt('tafels.txt')
volmer_betas=np.loadtxt('volmer_betas.txt')
heyrovskys=np.loadtxt('heyrovskys.txt')
heyrovsky_betas=np.loadtxt('heyrovsky_betas.txt')
PZCs=np.loadtxt('PZCs.txt')
HBEs=np.loadtxt('vac_HBEs.txt')
Htops=np.loadtxt('vac_Htops.txt')
couplings=np.loadtxt('couplings.txt')
colors=['g','k','b','g','m','b']
linestyles=['-','-','-','-.','--',':']
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

r2s_htop_volmer=[]
slopes_htop_volmer=[]
r2s_htop_heyrovsky=[]
slopes_htop_heyrovsky=[]

r2s_hbehtop_volmer=[]
slopes_hbehtop_volmer=[]
r2s_hbehtop_heyrovsky=[]
slopes_hbehtop_heyrovsky=[]

r2s_hbepzc_volmer=[]
slopes_hbepzc_volmer=[]
r2s_hbepzc_heyrovsky=[]
slopes_hbepzc_heyrovsky=[]

r2s_pzchtop_volmer=[]
slopes_pzchtop_volmer=[]
r2s_pzchtop_heyrovsky=[]
slopes_pzchtop_heyrovsky=[]

r2s_coup_volmer=[]
slopes_coup_volmer=[]
r2s_coup_heyrovsky=[]
slopes_coup_heyrovsky=[]

r2s_hdiff_volmer=[]
slopes_hdiff_volmer=[]
r2s_hdiff_heyrovsky=[]
slopes_hdiff_heyrovsky=[]

xpzc=PZCs-4.4
xhbe=HBEs
xhtop=Htops
combined_hbepzc=xhbe-0.52*xpzc
xcoup=couplings
xhdiff=HBEs-Htops

for potential in potentials:

    vslope, intercept, r_value, p_value, std_err = linregress(
            xpzc,volmers+potential*volmer_betas)
    r2s_pzc_volmer.append(r_value**2)
    slopes_pzc_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(
            xpzc,heyrovskys+potential*heyrovsky_betas)
    r2s_pzc_heyrovsky.append(r_value**2)
    slopes_pzc_heyrovsky.append(hslope)

    vslope, intercept, r_value, p_value, std_err = linregress(
            xhbe,volmers+potential*volmer_betas)
    r2s_hbe_volmer.append(r_value**2)
    slopes_hbe_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(
            xhbe,heyrovskys+potential*heyrovsky_betas)
    r2s_hbe_heyrovsky.append(r_value**2)
    slopes_hbe_heyrovsky.append(hslope)

    vslope, intercept, r_value, p_value, std_err = linregress(
            xhtop,volmers+potential*volmer_betas)
    r2s_htop_volmer.append(r_value**2)
    slopes_htop_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(
            xhtop,heyrovskys+potential*heyrovsky_betas)
    r2s_htop_heyrovsky.append(r_value**2)
    slopes_htop_heyrovsky.append(hslope)

    vslope, intercept, r_value, p_value, std_err = linregress(
            combined_hbepzc,volmers+potential*volmer_betas)
    r2s_hbepzc_volmer.append(r_value**2)
    slopes_hbepzc_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(
            combined_hbepzc,heyrovskys+potential*heyrovsky_betas)
    r2s_hbepzc_heyrovsky.append(r_value**2)
    slopes_hbepzc_heyrovsky.append(hslope)

    vslope, intercept, r_value, p_value, std_err = linregress(
            xcoup,volmers+potential*volmer_betas)
    r2s_coup_volmer.append(r_value**2)
    slopes_coup_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(
            xcoup,heyrovskys+potential*heyrovsky_betas)
    r2s_coup_heyrovsky.append(r_value**2)
    slopes_coup_heyrovsky.append(hslope)

    vslope, intercept, r_value, p_value, std_err = linregress(
            xhdiff,volmers+potential*volmer_betas)
    r2s_hdiff_volmer.append(r_value**2)
    slopes_hdiff_volmer.append(vslope)
    hslope, intercept, r_value, p_value, std_err = linregress(
            xhdiff,heyrovskys+potential*heyrovsky_betas)
    r2s_hdiff_heyrovsky.append(r_value**2)
    slopes_hdiff_heyrovsky.append(hslope)

potentials=np.linspace(-2,0,101)
fig, (ax1, ax2, ax3)= plt.subplots(1,3,figsize=(7,2.5),sharey=True)
ax1.tick_params(direction='in')
ax2.tick_params(direction='in')
ax3.tick_params(direction='in')
ys=[r2s_pzc_volmer,r2s_hbe_volmer,r2s_htop_volmer,r2s_hbepzc_volmer,r2s_coup_volmer,r2s_hdiff_volmer]
for i,y in enumerate(ys):
    ax1.plot(potentials,y,colors[i]+linestyles[i])
ax1.set_xlabel(r'U vs SHE (V)')
ax1.set_ylabel(r'Descriptor Strength, R$^2$')
ax1.set_title('Volmer')
ys=[r2s_pzc_heyrovsky,r2s_hbe_heyrovsky,r2s_htop_heyrovsky,r2s_hbepzc_heyrovsky,r2s_coup_heyrovsky,r2s_hdiff_heyrovsky]
for i,y in enumerate(ys):
    ax2.plot(potentials,y,colors[i]+linestyles[i])
ax2.set_xlabel(r'U vs SHE (V)')
ax2.legend([r'$U_{PZC}$',r'$\Delta G^{fcc}_H$',r'$\Delta G^{top}_H$',r'$\Delta G^{fcc}_H-0.52U_{PZC}$',r'$|V|^2$',r'$\Delta G^{fcc}_H-\Delta G^{top}_H$',],handlelength=1.0,ncols=1,labelcolor='linecolor',frameon=False,fontsize='x-small')
ax2.set_title('Heyrovsky')
labels=['a)','b)','c)']

ys=[]
for x in [xpzc,xhbe,xhtop,combined_hbepzc,xcoup,xhdiff]:
    slope, intercept, r_value, p_value, std_err = linregress(
            x,tafels)
    ys.append(r_value**2)
    #print(ys[-1])
for i,y in enumerate(ys):
    ax3.plot(potentials,y*np.ones(np.shape(potentials)),colors[i]+linestyles[i])
ax3.set_xlabel(r'U vs SHE (V)')
ax3.set_title('Tafel')
axs=[ax1,ax2,ax3]
from matplotlib.transforms import ScaledTranslation
for label, ax in zip(labels,axs):
    ax.text(
        0.0, 1.0, label, transform=(
            ax.transAxes + ScaledTranslation(-20/72, +7/72, fig.dpi_scale_trans)),
        fontsize='medium', va='bottom', fontfamily='serif')
    ax.set_xticks([-2,-1,0])
#fig.show()
fig.savefig('R2_with_potential.pdf',bbox_inches="tight")
