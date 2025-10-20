Improved hydrogen evolution activity descriptors from first-principles electrochemical kinetics
=====================================
This repo contains the data and scripts associated with the paper: 
[Improved hydrogen evolution activity descriptors from first-principles electrochemical kinetics](https://www.sciencedirect.com/science/article/pii/S001346862501833X)

# Requirements
* ase
* Stefan Ringe's fork of catmap
* bash, grep
* gnuplot
* jq

# Quickstart
To extract data, run models, and plot select output, run the analyze.sh script.

Alternatively, one can modify the results in results/{metal}/results.json values and run modified\_results\_analyze.sh to play with the models under different parameters.

### Details
analyze.sh runs the python scripts:
* extract\_data.py to extract raw transition state energies from the reaction paths in /data/
* get\_results.py to process that data into catmap input parameters in results/{metal}/results.json
* generate\_inputs\_incomplete.py to fill the json data into catmap templates in /template/
* run\_models.py to run the models in parallel
It then makes some data files with jq in /plots/ and runs gnuplot to make and show a few plots of model results

# Directories
[/data/](/data/README.md) contains the final MLNEB paths for each {reaction}/{metal}

[/Figures/](/Figures/README.md) contains plotting scripts and data for the figures included in the manuscript

[/Figures_SI/](/Figures_SI/README.md) contains plotting scripts and data for the figures included in the supporting information

[/plots/](/plots/README.md) contains various plots for use during analysis of MKMs

[/PZCs/](/PZCs/README.md) contains ase-db's of neutral calculations of metal surfaces

[/results/](/results/README.md) contains raw MKM inputs and results

[/template/](/template/README.md) contains raw MKM inputs and results

