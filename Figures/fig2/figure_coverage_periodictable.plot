set encoding utf8
#set terminal epslatex color colortext size 5in,3.0in "cmss" standalone font "Times new Roman, 30"
set terminal epslatex color colortext size 5in,3.0in font "cmss, 10" standalone
set output "Figure_Coverage_PeriodicTable.tex"

set multiplot layout 3,3 columnsfirst margins 0.10, 0.85, 0.15, 0.95 spacing 0.02, 0.03
load '../turbo.pal'
#
CBHeight = 0.05
CBWidth  = 0.20
CBPosX   = 0.12
CBPosY   = 0.7
#set colorbox user origin 0.1,0.7 size 0.238,0.04 invert horizontal
set origin CBPosX,CBPosY
set size nosquare CBWidth,CBHeight
set lmargin 0; set tmargin 0; set rmargin 0; set bmargin 0
set x2tics out nomirror scale 1.0,0 offset 0,0
set logscale x2
set colorbox horizontal user origin graph 0, graph 0 size graph 1, graph 1
unset xtics
unset ytics
unset key
set xrange [1e-2:1e0]
set palette negative
unset cbtics
set x2label r"$\\theta_\\mathrm{H}$" offset screen 0.02,0
set x2tics ("0.01" 10, "1" 0.1, "0.1" 1) offset graph 0,-0.03
set label 2 at screen 0.07,0.92 'a)' front font "Times-New_Roman,30" textcolor 'black'
plot x palette notitle # dummy plot
unset x2label
unset x2tics
unset label 2

set xrange [-1.6:0.0]
set yrange [7:14]
set xtics scale 0.5 #font ticsfont
set ytics scale 0.5 nomirror #font ticsfont
set pm3d map explicit noborder interpolate 3,3
set ylabel "pH"
unset surface; set pm3d at b; set view map
#set cbtics nomirror
set cbtics format '$10^{%T}$' #font ticsfont

set palette positive
set logscale cb
unset x2tics

set cbrange [0.01:1]
set cblabel r"$\\theta_\\mathrm{H}$" offset screen 0,0.28
set cbtics  1e-2,1e1,1e0 offset screen 0,0.12
#set multiplot next

#Rh
#set colorbox user origin 0.1,0.7 size 0.238,0.04 invert horizontal
unset colorbox
set format y "%2.0f"
set ytics 8,2,14 offset graph 0.05,0
set title 'Rh' offset -6.6,-2.5 textcolor 'black' left
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 dt 2 front
set format x '';
#set label 1 '0V vs RHE'  at -0.5195,10.5 font ",5" textcolor 'white' rotate by atan(3.5*1.75*-0.59)/pi*180+3 center front #font ticsfont
splot "../../results/Rh/coverage.dat" using 1:2:3 with pm3d notitle
#unset label 1
#Ir
unset colorbox
unset xlabel
set ylabel "pH"
set title 'Ir' offset -6.6,-2.5 textcolor 'white' left
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
unset colorbox
set format x "%1.1f"
set xlabel "U vs SHE (V)"
set xtics -1.5,0.5,-0.5
#set label 1 '0V vs RHE'  at -0.8195,10.5 textcolor 'black' rotate by atan(3.5*1.75*-0.59)/pi*180+3 center front #font ticsfont
splot "../../results/Ir/coverage.dat" using 1:2:3 with pm3d notitle
#Ni
unset ylabel
unset xlabel
set format y '';
set format x '';
set title 'Ni' offset -6.6,-2.5 textcolor 'white' left
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
splot "../../results/Ni/coverage.dat" using 1:2:3 with pm3d notitle
#Pd
set title 'Pd' offset -6.6,-2.5 textcolor 'white' left
splot "../../results/Pd/coverage.dat" using 1:2:3 with pm3d notitle
#Pt
set format x "%1.1f"
set xlabel "U vs SHE (V)"
set title 'Pt' offset -6.6,-2.5 textcolor 'white' left
splot "../../results/Pt/coverage.dat" using 1:2:3 with pm3d notitle
#
set cbrange [1e-10:1e-4]
load '../ylgnbu.pal'
#Ag
unset xlabel
set format x ''
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 dt 2 front
set label 1 '\small{0V vs RHE}'  at -0.5195,10.5 textcolor 'black' rotate by atan(3.5*1.75*-0.42)/pi*180+3 center front #font ticsfont
set title 'Ag' offset -6.6,-2.5 textcolor 'black' left
splot "../../results/Ag/coverage.dat" using 1:2:3 with pm3d notitle
unset label 1
#Au
set title 'Au' offset -6.6,-2.5 textcolor 'black' left
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 front
splot "../../results/Au/coverage.dat" using 1:2:3 with pm3d notitle
#Cu
set xlabel "U vs SHE (V)"
set xtics -1.5,0.5,-0.5
set format x "%1.1f"
set title 'Cu' offset -6.6,-2.5 textcolor 'black' left
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 front
set colorbox front user origin 0.87,0.15 size 0.02,0.80
set cbtics  1e-8,1e2,1e-4 offset screen -0.01,0 nomirror out
unset mcbtics
set cblabel r"$\\theta_{\\mathrm{H}}$" offset screen -0.02,0.04
#set format x '';
splot "../../results/Cu/coverage.dat" using 1:2:3 with pm3d notitle
unset multiplot

#pause -1
