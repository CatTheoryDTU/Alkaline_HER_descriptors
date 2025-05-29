set encoding utf8
#tics#font = "Helvetica,10"
#title#font = "Helvetica,14"
set ylabel "pH"
#surfaces= "Au Cu"
#do for [metal in surfaces] {print metal}
#set terminal png enhanced #font titlefont size 1000,1000
#set output "Coverage.png"
#set palette defined ( 1e-9 "blue", 0.1 "red" )
set terminal epslatex color colortext size 7in,4.0in "cmss"
set output "Figure_Coverage.tex"
load 'ylgnbu.pal'
set xrange [-2.0:0.0]
set yrange [7:14]
set xtics #font ticsfont
#set ytics #font ticsfont

set multiplot layout 3,3 margins 0.00, 0.85, 0.0, 0.925# title "Coverage" #font "Helvetica,16"
set pm3d map explicit noborder
unset surface; set pm3d at b; set view map
set cbrange [1e-10:1e-4]
set cbtics out nomirror
#set cbtics format "%.1e" #font ticsfont
set cbtics format '$10^{%T}$' #font ticsfont
set logscale cb
set cblabel "H* Coverage"
#Ag
set title 'Ag' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 dt 2 front 
#set label 1 '0V vs RHE'  at -0.7,13.75 textcolor 'black' rotate by -77.5 front #font ticsfont 
set label 1 '0V vs RHE'  at -0.5195,10.5 textcolor 'black' rotate by atan(3.5*1.75*-0.59)/pi*180+3 center front #font ticsfont 
set ytics 8,2,14 offset graph 0.05,0
set cbtics  1e-10,1e2,1e-4
unset colorbox
set xlabel "U vs SHE (V)" offset graph 0,1.65
set xtics -1.5,0.5,0.0 offset graph 0,1.25
set format x "%1.1f"
splot "../results/Ag/coverage.dat" using 1:2:3 with pm3d notitle
#Au
set title 'Au' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 front
unset colorbox
set format y '';
unset ylabel
splot "../results/Au/coverage.dat" using 1:2:3 with pm3d notitle
#Cu
set title 'Cu' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 front
set colorbox front
set format y '';
#set format x '';
splot "../results/Cu/coverage.dat" using 1:2:3 with pm3d notitle

#Ir
#unset logscale cb
unset xlabel
set cbrange [0.01:1]
set cbtics  1e-2,1e1,1e0
load 'turbo.pal'
#set cbtics format "%.1e" #font ticsfont
#set cbtics format "10^{%T}" #font ticsfont
set format x '';
set ylabel "pH"
set title 'Ir' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set label 1 '0V vs RHE'  at -0.5195,10.5 textcolor 'white' rotate by atan(3.5*1.75*-0.59)/pi*180+3 center front #font ticsfont 
unset colorbox
#set format x "%1.1f"
set format y "%2.0f"
splot "../results/Ir/coverage.dat" using 1:2:3 with pm3d notitle
#Ni
unset ylabel
set title 'Ni' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set format y ''; 
splot "../results/Ni/coverage.dat" using 1:2:3 with pm3d notitle
#Pd
unset ylabel
set title 'Pd' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set colorbox front
set format y ''; 
splot "../results/Pd/coverage.dat" using 1:2:3 with pm3d notitle
#Pt
set ylabel "pH"
#set xlabel "Potential vs SHE"
set title 'Pt' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
unset colorbox
set format y "%2.0f"
splot "../results/Pt/coverage.dat" using 1:2:3 with pm3d notitle
#Rh
unset ylabel
set title 'Rh' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set colorbox front
set format y ''; 
splot "../results/Rh/coverage.dat" using 1:2:3 with pm3d notitle
unset multiplot
