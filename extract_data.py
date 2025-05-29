from ase.io import read, write
import numpy as np

def extract_ISTS(filename):
   try:
       traj=read(filename) 
   except:
       return [None, None]
   energies=[]
   for image in traj:
      energies.append(image.get_potential_energy()) 
   ISenergy=energies[0]
   TSenergy=max(energies)
   return [ISenergy,TSenergy]

def write_datatxt(filename,potentials,energies):
    f=open(filename,"w")
    for i in range(0,len(potentials)):
        if energies[i] is not None:
            f.write('%1.2f %.5f \n'%(potentials[i],energies[i]))
    f.close()

def write_datatxt_barriers(filename,potentials,TS,IS):
    #same as above
    f=open(filename,"w")
    for i in range(0,len(potentials)):
        if IS[i] is not None:
            f.write('%1.2f %.5f \n'%(potentials[i],TS[i]-IS[i]))
    f.close()
#extract data
surfaces=['Au','Cu','Pd','Ag','Pt','Rh','Ir','Ni']
steps=['volmer','tafel','heyrovsky']
potentials=np.linspace(2.40,4.40,5)
potentials_interp=np.insert(potentials,[1,2],[2.65,3.15])
for metal in surfaces:
    potentials=np.linspace(2.40,4.40,5)
    for step in steps:
        if step=='volmer':
            potentials=potentials_interp
        ISenergies=[]
        TSenergies=[]
        for potential in potentials:
            [G_IS,G_TS]=extract_ISTS('data/%s/%s/pot_%1.2f.traj@:'%(step,metal,potential))
            ISenergies.append(G_IS)
            TSenergies.append(G_TS)
        write_datatxt('data/%s/%s/IS.txt'%(step,metal),potentials,ISenergies)
        write_datatxt('data/%s/%s/TS.txt'%(step,metal),potentials,TSenergies)
        write_datatxt_barriers('data/%s/%s/barriers.txt'%(step,metal),potentials,TSenergies,ISenergies)
