set encoding iso_8859_1
set termoption enhanced
set xlabel "U vs SHE (V)"
set ylabel '$\Delta \Omega^\ddag$ (eV)'
set terminal epslatex color colortext size 4in,3in "cmss,10" standalone
set output "Ni_OHads.tex"
set key top left 
set xtics 
set ytics 
set xzeroaxis
set xrange [-2.5:0.5]
set xtics -2,0.5,0 nomirror
set ytics 0.7,0.2,1.5 nomirror
SHE=4.44
f(x) = a*x + b
g(x) = c*x + d
fit f(x) "111_barriers.txt" u ($1-SHE):2 via a,b
fit g(x) "<tail -n4 OHads_barriers.txt" u ($1-SHE):2 via c,d
set object 1 ellipse center -1.80,0.84  size 0.8,0.13  angle 15 front fs empty bo 3
set label 1 at -1.92,0.92 "Unadsorbed TS" rotate by 30 center front 
plot \
	"111_barriers.txt" u ($1-SHE):2 w p ps 2 title "Normal Volmer", \
	"OHads_barriers.txt" u ($1-SHE):2 w p ps 2 title "OH adsorption", \
	f(x) w l dt '..' lc 1 notitle, \
	g(x) w l dt '..' lc 2 notitle
