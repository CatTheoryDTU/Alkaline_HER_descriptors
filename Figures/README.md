# Figures
Scripts in this directory are used to create the production figures included in the manuscript.

## Scripts
* r2_with_tafel.py generates the data for Figure 5 by fitting barriers as a function of potential
* plot.sh can be helpful in automating the production of the final pdfs.

## Files
* ?.pal palette files for gnuplot
* sansmathfonts.sty and gnuplot.cfg ensure sans fonts throughout the figures
* ?.txt data files contain the eponymous quantity across metals listed in metals.txt
* pt_coverages.txt and activation_forward.txt contain the data coverage and effective barrier data used in fig2b

## Subdirectories

* fig1 - Figure 1
* fig2 - Figure 2
  * figure_coverage_periodictable.plot - Figure 2a
  * figure_2b.plot - Figure 2b
  * figure_2c.plot - Figure 2c
* fig3 - Figure 3
* fig4 - Figure 4
* fig5
  * figure_5.plot - Figure 5
  * fig5_volcano_drc.plot - Figure 6
