set encoding utf8
set ytics nomirror
set y2tics
set logscale y2
set xlabel "Potential vs SHE"
set ylabel "Free Energy"
set y2label "Coverage"
set terminal png enhanced size 500,500
set xrange [-2.0:]
set output "Eff_bar.png"

vol=1.063239
volb=0.485391
taf=0.484060
#taf=0.7000159999994067
plot "pt_coverages.txt" using 1:(vol+volb*$1+0.2*$2) axis x1y1 w l lw 2.0 title "Volmer", \
     "pt_coverages.txt" using 1:(taf-0.2*$2-2*0.188*$2) axis x1y1 w l lw 2.0 title "Tafel", \
     "pt_coverages.txt" using 1:2 axis x1y2 w l dt 2 lc 'black' lw 2.0 notitle
