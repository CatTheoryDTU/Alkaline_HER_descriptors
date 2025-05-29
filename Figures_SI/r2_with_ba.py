from scipy.stats import linregress
import numpy as np
import matplotlib.pyplot as plt
fig, ax= plt.subplots(1,1,figsize=(4,3))
volmers=np.loadtxt('volmers.txt')
volmer_betas=np.loadtxt('../volmer_betas.txt')
heyrovskys=np.loadtxt('heyrovskys.txt')
heyrovsky_betas=np.loadtxt('../heyrovsky_betas.txt')
Htops=np.loadtxt('Htops.txt')
HBEs=np.loadtxt('HBEs.txt')
values=np.linspace(-2,2,101)
colors=['k','r']
linestyles=['-','--',':']
potentials=[0.0,-0.5,0.5]
offset=[-0.2,0.1,-0.1]
for idx,potential in enumerate(potentials):
    r2s_volmer=[]
    r2s_heyrovsky=[]
    for ba in values:
        x=Htops-ba*HBEs
        slope, intercept, r_value, p_value, std_err = linregress(x,volmers+potential*volmer_betas)
        r2s_volmer.append(r_value**2)
        slope, intercept, r_value, p_value, std_err = linregress(x,heyrovskys+potential*heyrovsky_betas)
        r2s_heyrovsky.append(r_value**2)
    if idx==0:
        intersect=np.argwhere(np.diff(np.sign(np.array(r2s_volmer)-np.array(r2s_heyrovsky)))).flatten()[0]
        ax.vlines(values[intersect],0.65,r2s_volmer[intersect],ls=linestyles[idx])
        ax.text(values[intersect]+offset[idx],0.635-0.005*idx,f'{values[intersect]:0.2f}')
    ax.plot(values,r2s_volmer,'k'+linestyles[idx],values,r2s_heyrovsky,'r'+linestyles[idx])
dummy_lines = []
for idx in range(0,3):
    dummy_lines.append(ax.plot([],[], c="black", ls = linestyles[idx])[0])
lines = ax.get_lines()
legend1 = plt.legend([lines[i] for i in [0,1]], ["Volmer", "Heyrovsky"], loc=4)
legend2 = plt.legend([dummy_lines[i] for i in [0,1,2]], ["-1.0 V", "-1.5 V", '-0.5 V'], loc=1)
#legend1=plt.legend(['Volmer ','Heyrovsky'])
ax.add_artist(legend1)
ax.set_xlabel(r'$\frac{b}{a}$ constant')
ax.set_ylabel('$R^2$')
#ax.legend(['Volmer','Heyrovsky'])
fig.show()
fig.savefig('R2_b_over_a.svg',bbox_inches="tight")
