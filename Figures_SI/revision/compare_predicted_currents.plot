set encoding iso_8859_1
set termoption enhanced
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set terminal epslatex color colortext size 4in,3in "cmss,10" standalone
set output "Compare_Currents.tex"
set ylabel 'Descriptor log($|\mathrm{j}|$ [mA cm$^{-2}$])'
set xlabel 'Calculated log($|\mathrm{j}|$ [mA cm$^{-2}$])'
#set key center top
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste real_currents.txt combined_currents.txt " using (log10(-1*$1)):(log10(-1*$2)) prefix "comb"
stats "<paste real_currents.txt htop_currents.txt " using (log10(-1*$1)):(log10(-1*$2)) prefix "htop"
#set yrange [-10:2]
#set xrange [-10:2]
set key top left spacing 2
set label 1 at -4,-5 sprintf('$\mathrm{R^2}$ = %1.2f',comb_correlation**2) rotate by 28 center front 
set label 2 at -4,-3 sprintf('$\mathrm{R^2}$ = %1.2f',htop_correlation**2) textcolor 'red' rotate by 25 center front 
plot \
	'<paste real_currents.txt combined_currents.txt  metals.txt' u (log10(-1*$1)):(log10(-1*$2)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char -2.0,0.5 notitle, \
	comb_slope * x + comb_intercept lc 'black' dt 2  title '$\Delta \methrm{G}^{\mathrm{fcc}}_\mathrm{H}-0.91\mathrm{U}_{\mathrm{PZC}}$', \
	'<paste real_currents.txt htop_currents.txt  metals.txt' u (log10(-1*$1)):(log10(-1*$2)) w points lc 'red' pt 7 notitle, \
	htop_slope * x + htop_intercept lc 'red' dt 4 title '$\Delta \mathrm{G}^{\mathrm{top}}_\mathrm{H}$'
	#'<paste real_currents.txt combined_currents.txt  metals.txt' u (log10(-1*$1)):(log10(-1*2)):(sprintf("%s",stringcolumn(3))) every 2::1 w labels point pt 7 offset char 0.5,-1 notitle, \
