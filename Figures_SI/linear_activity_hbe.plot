set encoding iso_8859_1
set termoption enhanced
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set terminal epslatex color colortext size 4in,3in "cmss,10" standalone
set output "Linear_Activity_HBE.tex"
set ylabel 'log(|$j_0$| [mA cm$^{-2}$])'
#set key center top
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste vac_HBEs.txt i0s.txt" using 1:(1*($2)) prefix "H"
set xrange [-0.3:0.7]
set yrange [-10:2]
set xlabel '$\Delta G_H^{fcc}$ [eV]' #offset 0,screen 0.05
set key top right
set label 1 at 0.2,-4 sprintf("$R^2$ = %1.2f",H_correlation**2) rotate by -25 center front 
plot \
	'<paste vac_HBEs.txt i0s.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) every 2::0 w labels point pt 7 offset char -2.0,0.5 notitle, \
	'<paste vac_HBEs.txt i0s.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) every 2::1 w labels point pt 7 offset char 0.5,-1 notitle, \
	H_slope * x + H_intercept lc 'black' dt 2  notitle
