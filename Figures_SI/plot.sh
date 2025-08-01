#!/bin/bash
#
#
#
#awk '$2==13.0' ../results/Pt/coverage.dat | awk '{print $1, $3}' > pt_coverages.txt
#grep ".._intercept =" fit_lsv.dat | awk '{print $3}' > i0s.txt
#awk '{print $2-$1+4.0144772408+0.097}' vacuum_energies.txt > vac_HBEs.txt
#awk '{print $3-$1+4.0144772408+0.097+0.105}' vacuum_energies.txt > vac_Htops.txt
for plotfile in hbe_electronic_descriptors figure_electronic_descriptors_activation_energies
do 
	gnuplot $plotfile\.plot
	outfile=`grep "^set output" $plotfile\.plot | awk -F '\"' '{print $2}'`
	incfile=`echo $outfile | awk -F '.' '{print $1}'`
	epstopdf $incfile\-inc.eps
	pdflatex -interaction=nonstopmode $outfile > /dev/null
done
