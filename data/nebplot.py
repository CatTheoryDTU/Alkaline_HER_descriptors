import matplotlib.pyplot as plt
import argparse, os
from ase.io import read
from ase.mep import NEBTools
#from my_neb_tools import *
import re


parser = argparse.ArgumentParser("test")
#parser.add_argument("nimg",help="number of images")
parser.add_argument("trajectory",help="trajectory",nargs='?',default="MLNEB.traj@-15:")
args=parser.parse_args()
#nimg=int(args.nimg)
filename= args.trajectory
pot=re.search(r'\d\.\d+',filename).group()
#images = read(filename+'@-%i:'%nimg)
if '@' in filename:
    images = read(filename)
else:
    images = read(filename+'@:')
nebtools = NEBTools(images)

#CRED = '\033[91m'
#CEND = '\033[0m'
#nimg=len(images)
#print("Number images:"+CRED+"%i"%nimg+CEND)
#print("Barrier:"+CRED+str(nebtools.get_barrier())+CEND)
#print("Max Force:"+CRED+str(nebtools.get_fmax())+CEND)
fig=nebtools.plot_band()
fig.text(x=.2,y=.8,s='U = '+pot+' V',bbox=dict(fill=False),fontsize=14)
out=filename.replace('traj','png')
fig.savefig(out,bbox_inches='tight')
