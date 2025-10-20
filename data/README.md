# Data

## Files
The final MLNEB paths are organized in terms of reaction directories and metal subdirectories. Each pot_(x).traj corresponds to a run at an applied potential of (x), corresponding to (x)-4.4 V vs SHE.

## Scripts
* plot_bands.py creates a figure of all of the traj files for a specific reaction across potentials and metals.
* analyze_geometries.py extracts the reaction coordinate of each transition state for plotting
* _rc.plot files are used to plot the data from analyze_geometries.py
