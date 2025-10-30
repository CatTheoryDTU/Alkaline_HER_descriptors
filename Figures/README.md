# Figures

Scripts in this directory are used to create the production figures included in the manuscript.

## Subdirectories

* fig1 - Figure 1
* fig2 - Figure 2
  * `figure_coverage_periodictable.plot` - Figure 2a
  * `figure_2b.plot` - Figure 2b
  * `figure_2c.plot` - Figure 2c
* fig3 - Figure 3
* fig4 - Figure 4
* fig5
  * `figure_5.plot` - Figure 5
  * `fig5_volcano_drc.plot` - Figure 6

## Scripts

* `r2_with_tafel.py` generates the data for Figure 5 by fitting barriers as a function of potential
* `plot.sh` can be helpful in automating the production of the final pdfs.

## Other Files

| File | Description |
|-----------|-------------|
| `activation_forward.txt` | effective barrier data used in Figure 2b
| `bentcoolwarm.pal` | blue-red palette for gnuplot
| `combined_descriptor.txt` |  composite (hydrogen binding energy + PZC) descriptor
| `couplings.txt` | squared coupling matrix elements
| `dbandcenters.txt` | d-band centers energy levels
| `dbandedges.txt` | d-band upper-edge energy levels
| `fit_lsv.dat` | fitting data from the log(current) vs potential plot
| `gnuplot.cfg` | config file to make pdflatex use sansmathfonts.sty
| `Hdiff.txt` | hydrogen binding energy difference between fcc and top sites
| `heyrovsky_betas.txt` | symmetry factors for the heyrovsky step
| `heyrovskys.txt` | Heyrovsky barrier heights
| `i0s.txt` | exchange current densities (j0)
| `metals.txt` | metal names
| `numbers.txt` | point indices for gnuplot
| `pt_coverages.txt` | coverage data in Figure 2b
| `PZCs.txt` | Potentials of Zero Charge
| `sheng_i0s.txt` | exchange current densities from Sheng et al
| `tafels.txt` | Tafel barrier heights
| `turbo.pal` | turbo (jet-like) palette for gnuplot
| `vac_Hads.db` | ase db containing H adsorbed structures
| `vac_HBEs.txt` | hydrogen binding free energies in fcc sites
| `vac_Htops.txt` | hydrogen binding free energies in top sites
| `volmer_betas.txt` | Volmer symmetry factors
| `volmers.txt` | Volmer barrier heights
| `ylgnbu.pal` | yellow-green-blue palette for gnuplot