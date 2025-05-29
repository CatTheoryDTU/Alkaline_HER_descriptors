set encoding utf8
ticsfont = "Helvetica,18"
titlefont = "Helvetica,22"
subtitlefont = "Helvetica,18"
labelfont = "Helvetica,18"
set xtics font ticsfont nomirror #offset 0,graph 0.025 nomirror
set ytics font ticsfont nomirror
set terminal svg enhanced font titlefont size 600,400
set ylabel "log(|j_0| [mA cm^{-2}])" font titlefont
set output "Linear_Activity_HBE.svg"
set offset 1,1
#set key center top
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste vac_HBEs.txt i0s.txt" using 1:(1*($2)) prefix "H"
set xrange [-0.3:0.7]
set yrange [-10:2]
set xlabel "Hydrogen Binding Energy, eV" font titlefont #offset 0,screen 0.05
set key top right
set label 1 at 0.2,-4 sprintf("R^2 = %1.2f",H_correlation**2) rotate by -25 center front font labelfont
plot \
	'<paste vac_HBEs.txt i0s.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) every 2::0 w labels point pt 7 offset char -2.0,0.5 notitle, \
	'<paste vac_HBEs.txt i0s.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) every 2::1 w labels point pt 7 offset char 0.5,-1 notitle, \
	H_slope * x + H_intercept lc 'black' dt 2  notitle
