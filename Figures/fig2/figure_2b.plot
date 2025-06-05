set encoding utf8
set ytics nomirror
set y2tics
#set logscale y2
set xlabel "U vs RHE (V)"
set ylabel r"$\\Delta G^{\\ddag}$ (eV)" offset graph 0,0.2
set y2label r"$\\theta_\\mathrm{H}$" offset graph 0,0.05
set xtics nomirror
set terminal epslatex color colortext size 5in,3in font "ptm,10" standalone
set xrange [-1.0:0.25]
set ytics 0.2,0.2,0.8
set yrange [0.2:1]
set y2range [0:1]
set output "Figure_2B.tex"
pH=13*-0.059
set key textcolor variable
set label 2 at screen 0.05,0.95 '\huge{b)}' front
plot "< paste ../pt_coverages.txt  ../activation_forward.txt" using ($1-pH):3 axis x1y1 w l lw 3.0 lc 'black' title "Volmer" at end, \
     "< paste ../pt_coverages.txt ../activation_forward.txt" using ($1-pH):4 axis x1y1 w l lw 3.0 lc 6 title "Tafel" at end, \
     "../pt_coverages.txt" using ($1-pH):2 axis x1y2 w l dt 3 lc 'black' lw 3.0 notitle
