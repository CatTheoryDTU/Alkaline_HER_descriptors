# generate the input files
from string import Template
from collections import namedtuple
import json
surfaces=['Au','Cu','Pd','Ag','Pt','Rh','Ir','Ni']
for metal in surfaces:
    data=json.load(open('results/%s/results.json'%metal,'r'),object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    with open('template/input.mkm','r') as t:
        template = Template(t.read())
    final_output=template.substitute(surf=metal,beta_volmer=data.volmer.beta,beta_heyrovsky=data.heyrovsky.beta,beta_tafel=data.tafel.beta,cutoff=data.Hydrogen.cutoff,interaction=data.Hydrogen.interaction)
    with open('results/%s/input.mkm'%metal,'w') as output:
        output.write(final_output)
    with open('template/energy_input.txt','r') as t:
        template = Template(t.read())
    final_output=template.substitute(surf=metal,Volmer_barrier=data.volmer.energy,Tafel_barrier=data.tafel.energy,
            Heyrovsky_barrier=data.heyrovsky.energy,H_ads_energy=data.Hydrogen.energy)
    with open('results/%s/energy_input.txt'%metal,'w') as output:
        output.write(final_output)

###energy_input.txt
#$surf	111	H	$H_ads_energy	[]	
#$surf	111	H-H	$Tafel_barrier	[]	
#$surf	111	H2O-ele	$Volmer_barrier	[]	
#$surf	111	H2OHele	$Heyrovsky_barrier	[]	
###input.mkm
#'H2O_g + *_a + ele_g <-> H2O-ele_a <-> H_a + OH_g; beta = $beta_volmer',
#'H2O_g + H_a + ele_g <-> H2OHele_a <-> H2_g + OH_g + *_a; beta = $beta_heyrovsky'
## $surf - Alkaline HER input file settings
#surface_names = ['$surf']
#species_definitions['H_a']={'sigma_params':[$sigma_H, 0.0]}
