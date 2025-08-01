#! gnuplot
set encoding utf8
ticsfont = "Helvetica,14"
titlefont = "Helvetica,14"
ticsfont = "Times,18"
titlefont = "Times,14"
labelfont = 'Times,18'
elementfont = 'Times,28'
elemxoff = -9.1
elemyoff = -3

set terminal png enhanced font titlefont size 1000,1000
set output "Hey_taf_selectivity.png"
load 'bentcoolwarm.pal'
set xrange [-1.99:-0.01]
set xtics -1.8,0.5,0
set cbrange [-10:10]
set cbtics left

set macros
TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.15"
BMARGIN = "set tmargin at screen 0.55; set bmargin at screen 0.15"
LMARGIN = "set lmargin at screen 0.05; set rmargin at screen 0.45"
RMARGIN = "set lmargin at screen 0.50; set rmargin at screen 0.85"

set multiplot layout 3,3 columnsfirst margins 0.10, 0.85, 0.2, 0.925 spacing 0.01,0.01

##First panel only showing colorbar####
CBHeight = 0.20
CBWidth  = 0.05
CBPosX   = 0.2
CBPosY   = 0.70
set origin CBPosX,CBPosY
set size nosquare CBWidth,CBHeight
set lmargin 0; set tmargin 0; set rmargin 0; set bmargin 0
set colorbox user origin graph 0, graph 0 size graph 1, graph 1
unset xtics; unset ytics
set x2label "log(r_{Taf} / r_{Hey})" offset screen 0.0,0.01 font labelfont
set label 2 "Tafel\n dominates" at graph -0.1, graph 0.95 right font labelfont textcolor 'black'
set label 3 "Heyrovsky\n dominates" at graph -0.1, graph 0.15 right font labelfont textcolor 'black'
plot x palette notitle # dummy plot
unset x2label; unset label 2; unset label 3
##############

set pm3d map interpolate 5,5

unset colorbox

# ytics and labels are shown forthe first 3 panels
set xtics font ticsfont; set format x ''
set ytics 8,2,14  font ticsfont; set format y "%2.0f";
set ylabel 'pH' font labelfont offset screen -0.01,0

# Define RHE line
set arrow 1 from -0.413,7 to -0.5605,9.5 nohead lc 'black' lw 2 dt 3 front
set label 1 'RHE'  at -0.73,11.25 textcolor 'black' font ticsfont rotate by -77.5 front
set arrow 2 from -0.693,11.75 to -0.826,14 nohead lc 'black' lw 2 dt 2 front
##

#Rh
set title 'Rh' offset elemxoff, elemyoff textcolor 'white' font elementfont
splot "../../results/Rh/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

#Ir
set format x "%1.1f"
set title 'Ir' offset elemxoff, elemyoff textcolor "white" font elementfont
splot "../../results/Ir/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

#Ni
unset xlabel; set format x ''
set format y '%2.0f';
set title 'Ni' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Ni/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

#Pd
unset ylabel; set format y ''
set title 'Pd' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Pd/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

set xlabel "Potential vs SHE" font elementfont offset 0,-1
#Pt
set title 'Pt' offset elemxoff, elemyoff textcolor "black" font elementfont
set format x "%1.1f"
splot "../../results/Pt/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

#Cu
unset xlabel; set format x ''
set title 'Cu' offset elemxoff, elemyoff textcolor "white" font elementfont
splot "../../results/Cu/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

#Ag
set title 'Ag' offset elemxoff, elemyoff textcolor "white" font elementfont
splot "../../results/Ag/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

#Au
set format x '%1.1f' ;
set title 'Au' offset elemxoff, elemyoff textcolor "white" font elementfont
splot "../../results/Au/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

unset multiplot
