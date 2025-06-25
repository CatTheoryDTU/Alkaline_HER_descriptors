set encoding utf8
set terminal epslatex color colortext size 6in,4in "cmss,10" standalone
set output "PZC_Htop_Relation.tex"
set xtics nomirror
set ytics nomirror
set offset 1,1
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste PZCs.txt vac_Htops.txt" u ($1-4.44):2 prefix "pzchtop"
stats "<paste vac_Htops.txt heyrovskys.txt" u 1:2 prefix "htophey"
stats "<paste predicted_htop_pzc.txt heyrovskys.txt" u 1:2 prefix "htoppzchey"
set multiplot layout 1,2 margins 0.15, 0.95, 0.25, 0.85 spacing 0.125,0# title "Activation Energies at -1 V vs SHE" font titlefont
set yrange [-0.4:1.6]
set xlabel '$U_{PZC}$'
set ylabel '$\Delta G_H^{top}$ (eV)'
FILE = "numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
set key at screen 0.8,screen 0.125 maxrows 2
set label 4 at graph -0.15,1.1 'a)' front
set label 1 sprintf('$R^2 = %1.2f$',pzchtop_correlation**2) at -0.8,0.2 rotate by -40 textcolor 'black' front
set xrange [-1:1]
plot \
	'<paste PZCs.txt vac_Htops.txt numbers.txt' u ($1-4.44):2:3 w points ps 2 pt variable lc 'black' notitle, \
	pzchtop_slope * x + pzchtop_intercept w l lw 7.5 lc 'black' dt 2 notitle , \
	for [idx=1:8] keyentry with points lc 'black' ps 2 pointtype numbers[idx] title elements[idx] 
unset key
set xlabel '$\Delta G_H^{top}$'
set ylabel '$\Delta \Omega^{\ddag}$ (eV)'
set yrange [0.1:1.9]
#set ytics format ""
set xrange [-0.5:1.5]
set label 1 sprintf('Real $R^2 = %1.2f$',htophey_correlation**2) at -0.3,0.8 rotate by -42 textcolor 'black' front
set label 2 sprintf('Predicted($U_{PZC}$) $R^2 = %1.2f$',htoppzchey_correlation**2) at 0.,1.8 rotate by -42 textcolor 'red' front
set label 4 at graph -0.15,1.1 'b)' front
plot \
	'<paste vac_Htops.txt heyrovskys.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste predicted_htop_pzc.txt heyrovskys.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	htophey_slope * x + htophey_intercept w l lw 7.5 lc 'black' dt 2 notitle, \
	htoppzchey_slope * x + htoppzchey_intercept w l lw 7.5 lc 7 dt 2 notitle
unset multiplot
