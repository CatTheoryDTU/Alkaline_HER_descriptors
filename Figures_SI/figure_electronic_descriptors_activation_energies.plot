set encoding utf8
set ylabel 'Activation Free Energy $\Delta G^\ddag$ (eV)'
#set terminal svg enhanced size 1000,500
#set output "Electronic_Descriptors_Activation_Energies.svg"
set terminal svg enhanced size 1500,500
set terminal epslatex color colortext size 6in,4in "cmss" standalone
set output "Electronic_Descriptors_Activation_Energies.tex"
#set xtics font ticsfont offset 0,graph 0.025 nomirror
set xtics nomirror
set ytics nomirror
set offset 1,1
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste couplings.txt volmers.txt" u 1:2 prefix "coupvol"
stats "<paste couplings.txt heyrovskys.txt" u 1:2 prefix "couphey"
stats "<paste couplings.txt tafels.txt" u 1:2 prefix "couptaf"
stats "<paste dbandcenters.txt volmers.txt" u 1:2 prefix "dbandvol"
stats "<paste dbandcenters.txt heyrovskys.txt" u 1:2 prefix "dbandhey"
stats "<paste dbandcenters.txt tafels.txt" u 1:2 prefix "dbandtaf"
stats "<paste Hdiff.txt volmers.txt" u 1:2 prefix "hdiffvol"
stats "<paste Hdiff.txt heyrovskys.txt" u 1:2 prefix "hdiffhey"
stats "<paste Hdiff.txt tafels.txt" u 1:2 prefix "hdifftaf"
set yrange [0.2:1.5]
set multiplot layout 1,3 margins 0.15, 0.95, 0.25, 0.85 # title "Activation Energies at -1 V vs SHE" font titlefont
set title 
set xrange[-4.5:-1.0]
set xtics -4.,1,-1
set xlabel '$\epsilon_d$'
FILE = "numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
set key at screen 0.8,screen 0.125 maxrows 2
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',dbandvol_correlation**2) at -3.2,0.5 rotate by 0 textcolor 'black' front
set label 2 sprintf('\tiny{Heyrovsky, $R^2 = %1.2f$}',dbandhey_correlation**2) at -3.2,0.4 rotate by 0 textcolor lt 7 front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',dbandtaf_correlation**2) at -3.2,0.3 rotate by 0 textcolor lt 6 front
plot \
	'<paste dbandcenters.txt volmers.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste dbandcenters.txt heyrovskys.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste dbandcenters.txt tafels.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	dbandvol_slope * x + dbandvol_intercept w l lw 7.5 lc 'black' dt 2 notitle , \
	dbandhey_slope * x + dbandhey_intercept w l lw 7.5 lc 7 dt 2 notitle , \
	dbandtaf_slope * x + dbandtaf_intercept w l lw 7.5 lc 6 dt 2 notitle , \
	for [idx=1:8] keyentry with points lc 'black' ps 2 pointtype numbers[idx] title elements[idx] 
unset key
set xrange[0.5:4.5]
set xlabel "$|V_{ad}|^2$"
set xtics 1,1,4
set ylabel ""
set ytics format ""
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',coupvol_correlation**2) at 1.0,0.7 rotate by 0 textcolor 'black' front
set label 2 sprintf('\tiny{Heyrovsky, $R^2 = %1.2f$}',couphey_correlation**2) at 1.0,0.6 rotate by 0 textcolor lt 7 front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',couptaf_correlation**2) at 1.0,0.5 rotate by 0 textcolor lt 6 front
plot \
	'<paste couplings.txt volmers.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste couplings.txt heyrovskys.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste couplings.txt tafels.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	coupvol_slope * x + coupvol_intercept w l lw 7.5 lc 'black' dt 2 notitle, \
	couphey_slope * x + couphey_intercept w l lw 7.5 lc 7 dt 2 notitle, \
	couptaf_slope * x + couptaf_intercept w l lw 7.5 lc 6 dt 2 notitle
set xrange[-0.3:0.9]
set xtics -0.4,0.4,0.8
set xlabel '$\Delta G^{top}_{H} - \Delta G^{fcc}_{H}$'
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',hdiffvol_correlation**2) at -.2,0.45 rotate by 0 textcolor 'black' front
set label 2 sprintf('\tiny{Heyrovsky, $R^2 = %1.2f$}',hdiffhey_correlation**2) at -.2,0.35 rotate by 0 textcolor lt 7 front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',hdifftaf_correlation**2) at -.2,0.25 rotate by 0 textcolor lt 6 front
plot \
	'<paste Hdiff.txt volmers.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste Hdiff.txt heyrovskys.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste Hdiff.txt tafels.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	hdiffvol_slope * x + hdiffvol_intercept w l lw 7.5 lc 'black' dt 2 notitle, \
	hdiffhey_slope * x + hdiffhey_intercept w l lw 7.5 lc 7 dt 2 notitle, \
	hdifftaf_slope * x + hdifftaf_intercept w l lw 7.5 lc 6 dt 2 notitle
unset multiplot
