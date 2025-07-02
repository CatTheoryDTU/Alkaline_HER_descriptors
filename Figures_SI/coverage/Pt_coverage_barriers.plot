set encoding iso_8859_1
set termoption enhanced
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set xlabel "U vs SHE (V)"
set ylabel '$\Delta \Omega^\ddag$ (eV)'
set terminal epslatex color colortext size 4in,3in "cmss,10" standalone
set output "coverage_barriers.tex"
set xrange [-2.2:0.2]
set yrange [0.:2.5]
SHE=4.44
set fit logfile 'TS_coverage.log' brief errorvariables nocovariancevariables errorscaling prescale nowrap v5
f(x) = a*x + b
g(x) = c*x + d
h(x) = p*x + q
i(x) = r*x + s
j(x) = t*x + u
k(x) = k1*x + k2
fit f(x) "Pt_111_barriers.txt" u ($1-SHE):2 via a,b
fit g(x) "Pt_111_Hcovered_barriers.txt" u ($1-SHE):2 via c,d
fit h(x) "tafel_Pt_111_barriers.txt" u ($1-SHE):2 via p,q
fit i(x) "tafel_Pt_Hcovered_barriers.txt" u ($1-SHE):2 via r,s
fit j(x) "heyrovsky_Pt_111_barriers.txt" u ($1-SHE):2 via t,u
fit k(x) "heyrovsky_Pt_Hcovered_barriers.txt" u ($1-SHE):2 via k1,k2
set label 1 at -1.,1.1 sprintf("Volmer Parameter %1.2f",(g(-1)-f(-1))) rotate by 17 center 
set label 2 at -1.,1.65 sprintf("Heyrovsky Parameter %1.2f",(k(-1)-j(-1))) rotate by 17 center 
set label 3 at -1.,0.5 sprintf("Tafel Parameter %1.2f",(i(-1)-h(-1))) center 
set key top left maxrows 4 spacing 0.75 width -5
plot \
	"Pt_111_barriers.txt" u ($1-SHE):2 w p pt 4 ps 2 title '0\% *H Volmer', \
	"Pt_111_Hcovered_barriers.txt" u ($1-SHE):2 w p pt 5 ps 2 title '100\% *H Volmer', \
	"heyrovsky_Pt_111_barriers.txt" u ($1-SHE):2 w p pt 6 ps 2 title '0\% *H Heyrovsky', \
	"heyrovsky_Pt_Hcovered_barriers.txt" u ($1-SHE):2 w p pt 7 ps 2 title '100\% *H Heyrovsky', \
	"tafel_Pt_111_barriers.txt" u ($1-SHE):2 w p pt 8 ps 2 title '0\% *H Tafel', \
	"tafel_Pt_Hcovered_barriers.txt" u ($1-SHE):2 w p pt 9 ps 2 title '100\% *H Tafel', \
	f(x) w l dt '..' lc 1 notitle, \
	g(x) w l dt '..' lc 2 notitle, \
	j(x) w l dt '..' lc 3 notitle, \
	k(x) w l dt '..' lc 4 notitle, \
	h(x) w l dt '..' lc 5 notitle, \
	i(x) w l dt '..' lc 6 notitle
