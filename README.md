# Requirements: 
* ase
* Stefan Ringe's fork of catmap
* bash, grep
* gnuplot
* jq

# Quickstart:
To extract data, run models, and plot select output, run the analyze.sh script
Alternatively, one can modify the results in results/%metal/results.json values and run modified\_results\_analyze.sh to play with the models under different parameters.

## Longer:
analyze.sh runs the python scripts:
* extract\_data.py to extract raw transition state energies from the reaction paths in /data/
* get\_results.py to process that data into catmap input parameters in results/%metal/results.json
* generate\_inputs\_incomplete.py to fill the json data into catmap templates in /template/
* run\_models.py to run the models in parallel
It then makes some data files with jq in /plots/ and runs gnuplot to make and show a few plots of model results

# Directories:
[/data/ contains the final MLNEB paths for each reaction/metal](/data/README.md)
[/Figures/ contains plotting scripts and data for the figures included in the manuscript ](/Figures/README.md)
[/Figures_SI/ contains plotting scripts and data for the figures included in the supporting information ](/Figures_SI/README.md)
[/plots/ contains various plots for use during analysis of MKMs](/plots/README.md)
[/PZCs/ contains ase-db's of neutral calculations of metal surfaces](/PZCs/README.md)
[/results/ contains raw MKM inputs and results](/results/README.md)
[/template/ contains raw MKM inputs and results](/template/README.md)

