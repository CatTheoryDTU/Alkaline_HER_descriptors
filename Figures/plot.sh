#!/bin/bash
#
#
#
#awk '$2==13.0' ../results/Pt/coverage.dat | awk '{print $1, $3}' > pt_coverages.txt
#grep ".._intercept =" fit_lsv.dat | awk '{print $3}' > i0s.txt
#awk '{print $2-$1+4.0144772408+0.097}' vacuum_energies.txt > vac_HBEs.txt
#awk '{print $3-$1+4.0144772408+0.097+0.105}' vacuum_energies.txt > vac_Htops.txt
# 3c and 3b are actually for figure 2, not updating
for dir in fig*
do
	cd $dir
	for plotfile in *plot
	do 
		gnuplot $plotfile
		outfile=`grep "^set output" $plotfile | awk -F '\"' '{print $2}'`
		incfile=`echo $outfile | awk -F '.' '{print $1}'`
		epstopdf $incfile\-inc.eps
		pdflatex $outfile > /dev/null
	done
	cd ../
done
#python r2_with_tafel.py
#python georg.plot.py
