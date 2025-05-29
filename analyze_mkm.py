#! /usr/bin/env python3
import sys, os
import mpmath
from catmap import analyze
import numpy as np
import pickle as pkl
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import cm

plt.rcParams["figure.figsize"] = (10,5)
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.size"] = 16
plt.rc('axes', labelsize=16)    # fontsize of the x and y labels
plt.rcParams['xtick.labelsize'] = 18
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['figure.figsize'] = (12,7)
markersize=10

#from catmaphelpers.catmap_plotter import _make_plots, _plot_model, _plot_CV, post_process_CV, _compute_tafel_prate, plot_tafel_screening, _get_unit_cell_area, _plot_pH, _plot_map, _plot_pH_bar_coverage


home=os.getcwd()

potentialscale='SHE'
dattype='production_rate'
rateunit='TOF'
cov_and_rate={'coverage':['H_a'],'production_rate': ['H2_g']}

def main():
#    for mech in mechanisms:
     fig,ax=plt.subplots(1,3)
     rax,tsax,cax=ax
     model=run_catmap()

     steps=[i for i,label in enumerate(model.output_labels[dattype])
            if label in cov_and_rate[dattype]]
     data,phs,pots=extract_data_from_mkm(model,steps,dattype)

     csteps=[i for i,label in enumerate(model.output_labels['coverage'])
            if label in cov_and_rate['coverage']]
     print(csteps)
     cdata,phs,pots=extract_data_from_mkm(model,csteps,'coverage')

     colors=cm.jet(np.array([0,14])/len(phs))
     for iph,ph in enumerate(phs):
         pdat=[]
         cdat={csteps[0]:[]}
         for pot in pots:
             #pdat.append([pot,np.log10(float(data[pot][ph][steps[0]]))])
             pdat.append([pot,mpmath.log10(data[pot][ph][steps[0]])])
             #pdat.append([pot,data[pot][ph][steps[0]]])
             for s in csteps:
                 cdat[s].append([pot,cdata[pot][ph][s]])
#             cdat[csteps[1]].append([pot,cdata[pot][ph][csteps[1]]])
             #if len(steps) > 1:
             #    pdat.append([pot,data[pot][ph][steps[1]]])
         pdat=np.array(pdat)
         for s in csteps:
             cdat[s]=np.array(cdat[s])
         if potentialscale == 'RHE':
             pdat[:,0]+=0.059*ph
             for s in csteps:
                 cdat[s][:,0]+=0.059*ph
         tsdat=np.diff(pdat[:,0]*1000.)/np.diff(pdat[:,1])

         rax.plot(pdat[:,0],pdat[:,1],color=colors[iph])
         tsax.plot(pdat[:-1,0]+np.diff(pdat[:,0]),tsdat,color=colors[iph])
         tsax.plot(np.nan,np.nan,color=colors[iph],label=f'pH{ph}')
         print(pdat[:,0])
         lines=['-','--','-.']
         cax.set_yscale('log')
         for istep,s in enumerate(csteps):
             cax.plot(cdat[s][:,0],cdat[s][:,1],color=colors[iph],linestyle=lines[istep])
#     rax.set_yscale('log')
     rax.set_ylim([-15,0])
     cax.set_ylim([0,1.5])
     if potentialscale == 'RHE':
         cax.set_xlim([1.3,1.6])
     cax.plot(np.nan,np.nan,'k-',label='*H')
     cax.legend()
     tsax.legend()
#     rax.set_title(facet)
#    plt.savefig(f'../results/{dattype}_{facet}.pdf')
     if 1:
         ax[0].set_xlabel(r'U$_{\mathrm{%s}}$ / V'%potentialscale)
         ax[1].set_xlabel(r'U$_{\mathrm{%s}}$ / V'%potentialscale)
         ax[2].set_xlabel(r'U$_{\mathrm{%s}}$ / V'%potentialscale)
         ax[0].set_ylabel(r'(TOF / s$^{-1}$)')
         ax[1].set_ylabel(r'Tafel Slope / mV/dec')
         ax[2].set_ylabel(r'$\theta$')
     plt.tight_layout()
     plt.show()

def add_annotations(ax,nsteps):
    pass


def run_catmap(runbasedir=home):
    from catmap import ReactionModel
    model = ReactionModel(setup_file = f'input.mkm')
    model.output_variables+=['production_rate', 'free_energy','coverage']
    model.run()
    os.chdir(home)
    return model

def plot_heatplot(data,phs,pots,steps,fig,ax,dattype='coverage'):
    X=np.array(sorted(pots))
    Y=np.array(sorted(phs))
    nsteps=len(steps)

    for col in range(1):
     for istep in steps:
        R,S = get_rate_and_selectivity(col,istep,data,nsteps,X,Y)
        if dattype == 'production_rate':
            if rateunit != 'TOF':
                R*=facet_ratio[facet]*tof2cur['HER']
        plot_it(R,S,fig,ax,col,istep,X,Y,nsteps)
        if 0:
         if istep == nsteps-1:
            for thisax in ax[istep]:
                thisax.set_xlabel('U$_{SHE}$ [V]')
         else:
            for thisax in ax[istep]:
                thisax.set_xticks([])
        if nsteps == 1:
            ax.set_ylabel('pH')
        else:
            ax[istep].set_ylabel('pH')

def get_rate_and_selectivity(col,istep,data,steps,X,Y):
    Selectivity=np.ones((len(X),len(Y)))*0.5
    rate=np.ones((len(X),len(Y)))*0.5
    for ix,x in enumerate(X):
       for iy,y in enumerate(Y):
        try:
            if col == 1:
                Selectivity[ix][iy]=data[x][y][istep]/np.sum(data[x][y][:nsteps])
            else:
                rate[ix][iy]=data[x][y][istep]
        except:
            Selectivity[ix][iy]=np.nan
            rate[ix][iy]=1e-20
    return rate, Selectivity

def plot_it(R,S,fig,ax,col,istep,X,Y,nsteps):
        if dattype=='coverage':
            if facet == '211': vmin=1e-3
            else: vmin=1e-8
            vmax=1
        elif dattype=='production_rate':
            vmin=1e-5
            vmax=1e3

        if nsteps == 1:
            thisax=ax
        else:
            thisax=ax[istep]
        if col == 0:
         b = thisax.imshow(R.T,
                interpolation='bicubic',
                cmap=cm.jet,
                   origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()],norm=LogNorm(#,
                    vmin=vmin,
                    vmax=vmax),#)
                    aspect='auto')

        else:
         a = thisax[1].imshow(S.T,
                interpolation='bicubic',
                cmap=cm.RdYlGn,
                   origin='lower', extent=[X.min(), X.max(), Y.min(), Y.max()],#norm=LogNorm(),#,
                    vmin=0,
                    vmax=1,
                    aspect='auto')

        if istep == 1:
            if dattype == 'coverage':
                label='Coverage'
            elif dattype == 'production_rate':
                if rateunit == 'TOF':
                    label = 'TOF / s$^{-1}$'
                else:
                    label='j$_{\mathrm{HER}}$ / (mA/cm$^2$)'
        if nsteps == 1:
            if dattype == 'coverage':
                label='*H Coverage'
            elif dattype == 'production_rate':
                if rateunit == 'TOF':
                    label = 'TOF / s$^{-1}$'
                else:
                    label='j$_{\mathrm{HER}}$ / (mA/cm$^2$)'

        if istep == 1 or nsteps == 1:
            fig.colorbar(b,ax=ax,shrink=1,label=label)


def extract_data_from_mkm(model,steps,dattype='coverage'):
    data={}
    pots,phs=[],[]

    if dattype=='coverage':
        datin=model.coverage_map
    elif dattype=='production_rate':
        datin=model.production_rate_map

    for dat in datin:
        pot,ph=np.around(dat[0][0],3),np.around(dat[0][1],3)
        if pot not in data:
            data[pot] = {}
        data[pot][ph] = dat[1]
        if pot not in pots:
            pots.append(pot)
        if ph not in phs:
            phs.append(ph)
    return data,phs,pots

def read_data(infile='mkm.pkl'):
    data_in = pkl.load(open(infile,'rb'),encoding='latin1')
    data={}
    pots,phs=[],[]
    for dat in data_in['coverage_map']:
        pot,ph=np.around(dat[0][0],3),np.around(dat[0][1],3)
        if pot not in data:
            data[pot] = {}
        data[pot][ph] = dat[1]
        if pot not in pots:
            pots.append(pot)
        if ph not in phs:
            phs.append(ph)
    return data,phs,pots

def run_catmaps_own_analysis(model):
        if not os.path.exists('output'):
            os.mkdir('output')

        vm = analyze.VectorMap(model)
        vm.plot_variable = 'production_rate'
        vm.log_scale = True
        vm.colorbar = True
        vm.min = 1e-5
        vm.max = 1e+2
        fig = vm.plot(save=False)
        fig.savefig('output/production_rate.pdf')

if __name__ == "__main__":
    main()
