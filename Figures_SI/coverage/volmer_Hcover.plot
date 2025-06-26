set encoding iso_8859_1
set termoption enhanced
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set xlabel "U vs SHE (V)"
set ylabel '$\Delta \Omega^\ddag$ (eV)'
set terminal epslatex color colortext size 4in,3in "cmss,10" standalone
set output "volmer_PtH.tex"
set key top left maxrows 3
set xrange [-2.2:0.2]
set yrange [0.:2.]
SHE=4.44
#set fit nologfile brief errorvariables nocovariancevariables errorscaling prescale nowrap v5
f(x) = a*x + b
g(x) = c*x + d
h(x) = p*x + q
i(x) = r*x + s
j(x) = t*x + u
fit f(x) "Pt_111_barriers.txt" u ($1-SHE):2 via a,b
fit g(x) "Pt_111_quarter_Hcovered_barriers.txt" u ($1-SHE):2 via c,d
fit h(x) "Pt_111_half_Hcovered_barriers.txt" u ($1-SHE):2 via p,q
fit i(x) "Pt_111_threequarter_Hcovered_barriers.txt" u ($1-SHE):2 via r,s
fit j(x) "Pt_111_Hcovered_barriers.txt" u ($1-SHE):2 via t,u
plot \
	"Pt_111_barriers.txt" u ($1-SHE):2 w p ps 2 title '0\%', \
	"Pt_111_quarter_Hcovered_barriers.txt" u ($1-SHE):2 w p ps 2 title '25\%', \
	"Pt_111_half_Hcovered_barriers.txt" u ($1-SHE):2 w p ps 2 title '50\%', \
	"Pt_111_threequarter_Hcovered_barriers.txt" u ($1-SHE):2 w p ps 2 title '75\%', \
	"Pt_111_Hcovered_barriers.txt" u ($1-SHE):2 w p ps 2 title '100\%', \
	f(x) w l dt '..' lc 1 notitle, \
	g(x) w l dt '..' lc 2 notitle, \
	h(x) w l dt '..' lc 3 notitle, \
	i(x) w l dt '..' lc 4 notitle, \
	j(x) w l dt '..' lc 5 notitle
