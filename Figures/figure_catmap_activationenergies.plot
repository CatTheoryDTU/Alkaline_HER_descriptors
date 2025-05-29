set encoding utf8
set ytics nomirror
set y2tics
#set logscale y2
set xlabel "U vs RHE (V)"
set ylabel r"$\\Delta G^{\\ddag}$ (eV)" offset graph 0,0.2
set y2label r"$\\theta_H$" offset graph 0,0.05
set xtics nomirror
set terminal epslatex color colortext size 7in,3in "cmss" standalone
set xrange [-1.0:0.25]
set ytics 0.3,0.1,0.8
set output "Figure_Catmap_ActivationEnergies.tex"
pH=13*-0.059
set key top center
plot "< paste pt_coverages.txt  activation_forward.txt" using ($1-pH):3 axis x1y1 w l lw 2.0 lc 'black' title "Volmer", \
     "< paste pt_coverages.txt activation_forward.txt" using ($1-pH):4 axis x1y1 w l lw 2.0 lc 6 title "Tafel", \
     "pt_coverages.txt" using ($1-pH):2 axis x1y2 w l dt 3 lc 'black' lw 3.0 notitle
