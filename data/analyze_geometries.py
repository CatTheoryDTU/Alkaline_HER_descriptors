from ase.io import read, write
import numpy as np
from ase.ga.utilities import get_neighborlist

def extract_ISTS_images(filename):
   try:
       traj=read(filename) 
   except:
       return [None, None]
   energies=[]
   for image in traj:
      energies.append(image.get_potential_energy()) 
   TS_index=energies.index(max(energies))
   return [traj[0],traj[TS_index]]

def extract_RC(image,step):
    element=image.get_chemical_symbols()[0]
    if step == 'volmer':
        H=image.positions[50]
        O=image.positions[48]
        #O is often closer than metal
        metalindex=get_neighborlist(image,dx=0.5)[50][0]
        #print(metalindex)
        Metal=image.positions[metalindex]
        return np.linalg.norm(Metal-H)-np.linalg.norm(H-O)
    if step == 'heyrovsky':
        H1=image.positions[51]
        O=image.positions[49]
        H2=image.positions[36]
        return np.linalg.norm(H2-H1)-np.linalg.norm(H1-O)

#extract data
surfaces=['Au','Cu','Pd','Ag','Ir','Rh','Pt','Ni']
surfaces=['Ni']
steps=['volmer']
#steps=['volmer','tafel','heyrovsky']
for metal in surfaces:
    for step in steps:
        datafile=open('%s_geometry_%s.dat'%(metal,step),'w')
        if step=='heyrovsky':
            potentials=np.linspace(2.40,4.40,5)
        else:
            potentials=[2.40,2.65,2.90,3.15,3.40,3.90,4.40]
        for i,potential in enumerate(potentials):
            [imageIS,imageTS]=extract_ISTS_images('%s/%s/pot_%1.2f.traj@:'%(step,metal,potential))
            #IS_geo=extract_RC(imageIS,step)
            TS_geo=extract_RC(imageTS,step)
            print('%1.2f %1.5f \n'%(potentials[i],TS_geo))
            datafile.write('%1.2f %1.5f \n'%(potentials[i],TS_geo))
        datafile.close()
