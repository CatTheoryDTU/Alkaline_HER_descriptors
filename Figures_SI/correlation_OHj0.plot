set encoding iso_8859_1
set termoption enhanced
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set terminal epslatex color colortext size 4in,3in "cmss,10" standalone
set ylabel 'log(|$j_0$| [mA cm$^{-2}$])'
set xlabel '$\Delta G_{OH}$ [eV]' #offset 0,screen 0.05
#set key center top
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
set output "OHBE_vs_j0.tex"
stats "<paste OHBEs.txt i0s.txt" using 1:2 prefix "OHcurrent"
set xrange [0.3:1.5]
set yrange [-10:3]
set label 1 at 1.,-5 sprintf("$R^{2}$ = %1.2f",OHcurrent_correlation**2) rotate by 4 center
plot \
	"<paste OHBEs.txt i0s.txt metals.txt" using 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 0.5,0.5 notitle, \
	OHcurrent_slope * x + OHcurrent_intercept lc 'black' dt 2 notitle
	
	
	
