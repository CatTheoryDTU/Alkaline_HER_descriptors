set encoding iso_8859_1
set termoption enhanced
set xlabel '$\Delta G_\mathrm{H}$ (eV)'
set ylabel '$\Delta \Omega_\mathrm{Taf}^\ddag$ (eV)'
set terminal epslatex color colortext size 4in,3in "cmss,10" standalone
set output "BEP_Tafel.tex"
set key top left 
set xtics 
set ytics 
set xzeroaxis
set xrange [-0.5:1.0]
set yrange [0.2:2.2]
#set xtics -2,0.5,0 nomirror
#set ytics 0.7,0.2,1.5 nomirror
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<(paste vac_HBEs.txt tafel_energies.txt)" u 1:2 prefix 'BEP'
#set label 1 at 0,0 sprintf('$\mathrm{R^2}$ = %1.2f',BEP_correlation**2) rotate by 28 center front 
#fit g(x) "<tail -n4 OHads_barriers.txt" u ($1-SHE):2 via c,d
#set object 1 ellipse center -1.80,0.84  size 0.8,0.13  angle 15 front fs empty bo 3
#set label 1 at -1.92,0.92 "Unadsorbed TS" rotate by 30 center front 
plot \
	"<(paste vac_HBEs.txt tafel_energies.txt metals.txt)" u 1:2:3 w labels point pt 7 offset char -1.5,0.2 notitle, \
	BEP_slope*x+BEP_intercept w l dt '..' lc 1 notitle
