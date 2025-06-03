import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import json


def collect_data(metal_order=['Ni', 'Pd', 'Ir', 'Rh', 'Pt', 'Cu', 'Ag', 'Au']):
    """
    Collect the data from the files and return it as a dictionary.
    The data is collected from the files 'data' and 'TM_parameters.json'.
    The data is stored in a dictionary with the following keys:
    'hfcc', 'htop', 'Volmer', 'Heyrovsky', 'Tafel', 'metal', 'vsquaredREL', 'dbandcenter'.
    The values are the corresponding values for each metal in the order given in
    the metal_order list.

    """
    # Read in the data
    data = np.loadtxt('data')
    dat_dict = {'hfcc': data[:, 0], 'htop': data[:, 1], 'Volmer': data[:, 2],
                'Heyrovsky': data[:, 3], 'Tafel': data[:, 4],
                'metal': metal_order
                }

    simi=json.load(open('TM_parameters.json'))

    for quant in ['vsquaredREL','dbandcenter']:
      quants=[]

      for metal in metal_order:
       for key, value in simi['metal'].items():
         if value not in metal_order: continue
         val=np.nan
         if value == metal:
#            print(f'Found {value} in {key}')
            val = simi[quant][key]
            break

#       print(f'{quant} for {value}: {val}')
       quants.append(val)
      dat_dict[quant] = np.array(quants)

    dat_dict['PZC'] = np.array([
        5.02015, 4.81861, 5.12015, 4.57793, 5.45706,
        4.29556, 3.95333, 4.69770])
    dat_dict['hfcc-pzc'] = dat_dict['hfcc'] - 0.58*dat_dict['PZC']
    dat_dict['htop-hfcc'] = dat_dict['htop'] - dat_dict['hfcc']


    import pickle
    pickle.dump(dat_dict, open('data.pckl', 'wb'))
    return dat_dict

def plot_volcano(data, rxns_long=['Volmer','Heyrovsky','Tafel','Activity'],
                descriptors=['htop', 'hfcc'],
                 metal_order=['Ni', 'Pd', 'Ir', 'Rh', 'Pt', 'Cu', 'Ag', 'Au'],
                 extend_axes=(0.2, 0.2, 0.2, 0.2),
                 only_activity=False
                 ):
    """
    Plot the volcano plot for the different reactions.
    The volcano plot is a plot of the activation energy vs the
    descriptor values. The activation energy is the energy barrier
    for the reaction to occur. The descriptor values are the
    values of the descriptors for each metal.
    """

    # Make a heatplot showing the barrier heights
    transform = {'htop': '$\Delta G^{top}_\mathrm{H}$',
                 'hfcc': '$\Delta G^{fcc}_\mathrm{H}$',
                 'htop-hfcc': '$\Delta G^{top}_\mathrm{H} - \Delta G^{fcc}_\mathrm{H}$',
                 'vsquaredREL': '$V^2_{rel}$',
                 'hfcc-pzc': '$\Delta G^{fcc}_\mathrm{H} - PZC$'}

    ranges= (np.linspace(min(data[descriptors[0]])-extend_axes[0],max(data[descriptors[0]]+extend_axes[1]),50),
             np.linspace(min(data[descriptors[1]])-extend_axes[2],max(data[descriptors[1]]+extend_axes[3]),50))
    dats=[]
    rxns_long_changed = ['Volmer', 'Heyrovsky', 'Tafel', 'Activity']
    for ibar, bar in enumerate(rxns_long[:-1]):
        if rxns_long[ibar]!='Tafel':
            index=0
#            descriptor = data[descriptors[0]]     #data['htop']
#            d_range=ranges[0]
        else:
            index=1
        descriptor = data[descriptors[index]]
        d_range=ranges[index]
        k, d, r, p_value, std_err = linregress(descriptor, data[bar])
        print(f'{rxns_long[ibar]}, {descriptor[0]}: k={k:.2f}, d={d:.2f}, R^2={r**2:.2f}')
        dat = k*d_range + d
        dat = dat*np.ones((len(ranges[1-index]), len(ranges[1-index])))
        if rxns_long[ibar]=='Tafel':
            dat= dat.T
        rxns_long_changed[ibar] = f'{rxns_long[ibar]}:\n k={k:.2f}, d={d:.2f}, R$^2$={r**2:.2f}'
        dats.append(dat)

    # Compare the magnitude in all three dat matrices: Take the lower one between
    # Tafel and Heyrovsky and compare it to the Volmer and take the higher one.
    diffs = np.zeros((len(ranges[0]), len(ranges[1])))
    print(dats[0].shape)
    for i in range(dats[0].shape[0]):
     for j in range(dats[0].shape[1]):
#        for j in range(len(dats[1])):
            diffs[i][j] = min(dats[1][i][j],dats[2][i][j])
            diffs[i][j] = max(dats[0][i][j],diffs[i][j])
    dats.append(diffs)

    # Plotting the heatmaps
    x=data[descriptors[0]]
    y=data[descriptors[1]]
    if not only_activity:
        fig,ax=plt.subplots(1, len(dats), figsize=(20, 6), dpi=80, sharey=True,sharex=True)
        for idat,dat in enumerate(dats):
            thisax = ax[idat]
            if not idat:
                thisax.set_ylabel(f'{transform[descriptors[1]]}')
            thisax.set_xlabel(f'{transform[descriptors[0]]}')
            thisax.set_title(f'{rxns_long_changed[idat]}')
    #        x=data[descriptors[0]]
    #        y=data[descriptors[1]]
            #print(min(ranges[0]), max(ranges[0]), min(ranges[1]),max(ranges[1]))
            im=thisax.imshow(dats[idat],
                                 extent=(min(ranges[0]), max(ranges[0]),
                                         min(ranges[1]),max(ranges[1])),
                             aspect='auto', origin='lower',
                       vmin=0.4, vmax=1.3,cmap='RdYlGn_r', interpolation='nearest')

            for i in range(len(x)):
                thisax.annotate(metal_order[i],
                                xy=(x[i],y[i]),
                                fontsize=15,ha='center', va='center')
            thisax.plot(x,y, 'ko', markeredgecolor='k', markersize=20, markerfacecolor='none')
        thisax.set_xlim(min(ranges[0]), max(ranges[0]))
        thisax.set_ylim(min(ranges[1]), max(ranges[1]))
        fig.colorbar(im,label=r'Effective barrier', orientation='vertical')
        plt.show()

    # Making a large heatplot only containing the activity
    fig,ax=plt.subplots(1, 1, figsize=(6, 6), dpi=80)
    ax.set_ylabel(f'{transform[descriptors[1]]}')
    ax.set_xlabel(f'{transform[descriptors[0]]}')
    ax.set_title(f'Activity')

    im=ax.imshow(dats[3],
                             extent=(min(ranges[0]), max(ranges[0]),
                                     min(ranges[1]),max(ranges[1])),
                         aspect='auto', origin='lower',
                   vmin=0.4, vmax=1.3,cmap='RdYlGn_r', interpolation='nearest')

    for i in range(len(data[descriptors[0]])):
        ax.annotate(metal_order[i],
                    xy=(x[i],y[i]),
                    fontsize=15,ha='center', va='center')

    ax.plot(x,y, 'ko', markeredgecolor='k', markersize=20, markerfacecolor='none')
    ax.set_xlim(min(ranges[0]), max(ranges[0]))
    ax.set_ylim(min(ranges[1]), max(ranges[1]))
    fig.colorbar(im,label=r'Effective barrier', orientation='vertical')
    plt.tight_layout()
    plt.show()
    return

def plot_r2_with_varying_descriptors_in_2D(
        data, rxns_long=['Volmer','Heyrovsky','Tafel'],
        descriptors=['htop', 'hfcc'],
        cs=np.linspace(-2, 2, 500)):
    """
    Plot the R^2 value of the linear regression of the sum of two descriptors
    with the varying coefficient c. c is the ratio of coefficients
    to be varied.
    """
    all_r2s = []
    colors= ['r', 'g', 'b']
    for ibar, bar in enumerate(rxns_long):
        r2s=[]
        # Perform linear regression for more sophisticated descriptors
        print(bar,len(descriptors))
        vec=np.array([data[descriptors[0]], data[descriptors[1]]])
        hdiff_k1, hdiff_d1 = 0, 0
        for c in cs:
            hdiff_k, hdiff_d, hdiff_r, p_value, std_err = linregress(
                    vec[0]+c*vec[1], data[bar])
            r2s.append([c,hdiff_r**2])

        r2s = np.array(r2s)
        all_r2s.append(r2s)
    fig,ax=plt.subplots(1, 1, figsize=(10, 6), dpi=80, sharey=True)

    for ibar, bar in enumerate([2,3,4]):
        r2 = all_r2s[ibar]
        bestfit=r2[np.argmax(r2[:, 1])]
        print(bestfit)
        ax.plot(r2[:, 0], r2[:, 1], color=colors[ibar], label=f'{rxns_long[ibar]}: R$^2_{{best}}$={bestfit[1]:.2f}')
#        ax.plot(bestfit[0], bestfit[1], 'o', color='k', markersize=10,)
        ax.plot([bestfit[0],bestfit[0]], [0,bestfit[1]], '--', color=colors[ibar], markersize=10,)
#        im = ax[ibar].imshow(r2[:, 2].reshape(len(c1s), len(c2s)),
#                             extent=(min(c1s), max(c1s), min(c2s),
#                             max(c2s)), aspect='auto', origin='lower',
#                   vmin=0.5, vmax=1.0,cmap='RdYlGn', interpolation='bicubic')
#        ax.plot([min(c2s),max(c2s)],[min(c2s),max(c2s)], 'k--')
        ax.set_xlim(min(cs), max(cs))
        ax.set_xlabel(f'b/a in {descriptors[0]} + b/a * {descriptors[1]}')

    ax.set_ylabel(r'$R^2$')
    ax.set_ylim([0,1])
    plt.tight_layout()
    plt.legend()
    plt.show()



def plot_r2_with_varying_contribution_of_descriptors(
        data, rxns_long=['Volmer','Heyrovsky','Tafel'],
        descriptors=['htop', 'hfcc'],
        c1s=np.linspace(0.5, 1.5, 20),
        c2s=np.linspace(0.5, 1.5, 20)):
    """
    Plot the R^2 value of the linear regression of combined descriptors
    with the varying coefficients a and b. c1 and c2 are the coefficients
    that are tried out.
    The difference of the descriptors are used to calculate the
    linear regression.
    """

    all_r2s = []
    for ibar, bar in enumerate(rxns_long):
        r2s=[]
        # Perform linear regression for more sophisticated descriptors
        print(bar,len(descriptors))
        print(bar,descriptors[0])
        print(bar,descriptors[1])
        vec=np.array([data[descriptors[0]], data[descriptors[1]]])
        hdiff_k1, hdiff_d1 = 0, 0
        for c1 in c1s:
            for c2 in c2s:
                coeffs = (c1,c2)
                hdiff_k, hdiff_d, hdiff_r, p_value, std_err = linregress(
                        coeffs[0]*vec[0]-coeffs[1]*vec[1], data[bar])
                if abs(c1-1) < 0.001 and abs(c2-1) < 0.001:
                    hdiff_k1,hdiff_d1=hdiff_k,hdiff_d
                r2s.append([c1,c2,hdiff_r**2])

        r2s = np.array(r2s)
        all_r2s.append(r2s)

    fig,ax=plt.subplots(1, 3, figsize=(18, 6), dpi=80, sharey=True)
    fig.suptitle(r'Testing correlations of'+'\n'+'a*%s - b*%s\n based on a and b'%(descriptors[0],descriptors[1]))
    for ibar, bar in enumerate([2,3,4]):
        r2 = all_r2s[ibar]
        bestfit=r2[np.argmax(r2[:, 2])]
        ax[ibar].set_title(f'{rxns_long[ibar]}')
        im = ax[ibar].imshow(r2[:, 2].reshape(len(c1s), len(c2s)),
                             extent=(min(c1s), max(c1s), min(c2s),
                             max(c2s)), aspect='auto', origin='lower',
                   vmin=0.5, vmax=1.0,cmap='RdYlGn', interpolation='bicubic')
        ax[ibar].plot([min(c2s),max(c2s)],[min(c2s),max(c2s)], 'k--')
        ax[ibar].set_xlim(min(c1s), max(c1s))
        ax[ibar].set_xlabel(r'b')

    fig.colorbar(im,label=r'$R^2$', orientation='vertical')
    ax[0].set_ylabel(r'a')
    plt.tight_layout()
    plt.show()

def correlate_descriptors(data,descriptors=['htop','hfcc'],metal_order=['Ni', 'Pd', 'Ir', 'Rh', 'Pt', 'Cu', 'Ag', 'Au']):
    x,y=data[descriptors[0]],data[descriptors[1]]
    k,d,r,p,stderr = linregress(x, y)
    plt.plot(x, k*x+d, '-', color='k')
    plt.plot(x,y, 'o', color='k', label='htop-hfcc vs vsquaredREL')
    plt.annotate(f'R$^2$={r**2:.2f}', xy=(0.8, 0.9), xycoords='axes fraction', fontsize=12)
    for imet, met in enumerate(metal_order):
        plt.annotate(met, xy=(x[imet], y[imet]), xytext=(5, 5), textcoords='offset points', fontsize=12)
    plt.xlabel(descriptors[0])
    plt.ylabel(descriptors[1])
    plt.tight_layout()
    plt.show()

def plot_1_to_1_correlations(data, rxns_long=['Volmer','Heyrovsky','Tafel','Activity'],
                             colors=['r', 'g', 'b'], descriptors=['htop', 'hfcc','htop-hfcc']):
    """
    Plot the 1 to 1 correlations of the different reactions.
    The reactions are plotted in different colors.
    The descriptors are plotted on the x-axis and the activation energy
    is plotted on the y-axis. The activation energy is the energy barrier
    for the reaction to occur. The descriptor values are the values of the
    descriptors for each metal.
    """

    rxns= [i[0] for i in rxns_long]
    fig,ax=plt.subplots(1, len(descriptors), figsize=(5*len(descriptors),6), dpi=80,sharey=True)
    for idesc,descr in enumerate(descriptors):
     for ibar, bar in enumerate(rxns_long[:-1]):
        thisdesc = data[descr]
        k, d, r, p_value, std_err = linregress(thisdesc, data[bar])
        ax[idesc].plot(thisdesc, k*thisdesc + d, '-', color=colors[ibar], label=f'{rxns[ibar]}={k:.2f}x+{d:.2f}, R$^2$={r**2:.2f}')
        ax[idesc].plot(thisdesc, data[bar], 'o', color=colors[ibar])
     ax[idesc].set_xlabel(f'{descr}')
     ax[idesc].legend(loc='upper left') #set_xlabel(f'{descr}')]
    ax[0].set_ylabel('Activation energy (eV)')

    fig.tight_layout()
    plt.show()


