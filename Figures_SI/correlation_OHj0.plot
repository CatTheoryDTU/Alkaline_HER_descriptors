set encoding utf8
ticsfont = "Helvetica,14"
titlefont = "Helvetica,22"
set ylabel 'log(|j_0| [mA cm^{-2}])'
set xlabel "OH Binding Energy, eV"
set terminal svg enhanced font titlefont size 600,400
set xtics font ticsfont nomirror
set ytics font ticsfont nomirror
set output "OHBE_vs_j0.svg"
stats "<paste OHBEs.txt i0s.txt" using 1:2 prefix "OHcurrent"
set xrange [0.3:1.5]
set yrange [-10:3]
set label 1 at 1.,-5 sprintf("R^{2} = %1.2f",OHcurrent_correlation**2) rotate by 4 center font "Helvetica,18"
plot \
	"<paste OHBEs.txt i0s.txt metals.txt" using 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 0.5,0.5 notitle, \
	OHcurrent_slope * x + OHcurrent_intercept lc 'black' dt 2 notitle
	
	
	
