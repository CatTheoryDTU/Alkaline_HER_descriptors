set encoding utf8
set ylabel 'Free Energy $\Delta G$ (eV)'
set terminal svg enhanced size 1000,500
set output "HBE_Electronic_Descriptors.svg"
set terminal epslatex color colortext size 6in,4in "cmss" standalone
set output "HBE_Electronic_Descriptors.tex"
set xtics nomirror
set ytics nomirror
set offset 1,1
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste couplings.txt vac_HBEs.txt" u 1:2 prefix "couphbe"
stats "<paste couplings.txt vac_Htops.txt" u 1:2 prefix "couphtop"
stats "<paste dbandcenters.txt vac_HBEs.txt" u 1:2 prefix "dbandhbe"
stats "<paste dbandcenters.txt vac_Htops.txt" u 1:2 prefix "dbandhtop"
set multiplot layout 1,2 margins 0.15, 0.95, 0.25, 0.85 # title "Activation Energies at -1 V vs SHE" font titlefont
set yrange [-0.4:1.2]
set xrange[-4.5:-1.5]
set xlabel '$\epsilon_d$'
FILE = "numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
set key at screen 0.8,screen 0.125 maxrows 2
set label 1 sprintf('$H_{fcc}$, $R^2 = %1.2f$',dbandhbe_correlation**2) at -3.8,0.2 rotate by -30 textcolor 'black' front
set label 2 sprintf('$H_{top}$, $R^2 = %1.2f$',dbandhtop_correlation**2) at -3.2,0.8 rotate by -30 textcolor lt 7 front
plot \
	'<paste dbandcenters.txt vac_HBEs.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste dbandcenters.txt vac_Htops.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	dbandhbe_slope * x + dbandhbe_intercept w l lw 7.5 lc 'black' dt 2 notitle , \
	dbandhtop_slope * x + dbandhtop_intercept w l lw 7.5 lc 7 dt 2 notitle , \
	for [idx=1:8] keyentry with points lc 'black' ps 2 pointtype numbers[idx] title elements[idx] 
unset key
set xrange[0.5:4.5]
set xlabel "$|V_{ad}|^2$"
set ylabel ""
set ytics format ""
set label 1 sprintf('$H_{fcc}$, $R^2 = %1.2f$',couphbe_correlation**2) at 1.0,0.0 rotate by 0 textcolor 'black' front
set label 2 sprintf('$H_{top}$, $R^2 = %1.2f$',couphtop_correlation**2) at 1.1,0.6 rotate by -30 textcolor lt 7 front
plot \
	'<paste couplings.txt vac_HBEs.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste couplings.txt vac_Htops.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	couphbe_slope * x + couphbe_intercept w l lw 7.5 lc 'black' dt 2 notitle, \
	couphtop_slope * x + couphtop_intercept w l lw 7.5 lc 7 dt 2 notitle
unset multiplot
