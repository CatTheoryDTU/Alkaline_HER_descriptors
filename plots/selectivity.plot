set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set xlabel "Potential vs SHE"
set ylabel "pH"
#surfaces= "Au Cu"
#do for [metal in surfaces] {print metal}
set terminal png enhanced font titlefont size 1000,1000
#set palette defined ( 1e-9 "blue", 0.1 "red" )
load 'turbo.pal'
set cbrange [1e-9:1e1]
set logscale cb
set cbtics format "%.1e" font ticsfont
set cblabel "Tafel/Heyrovsky Selectivity"
set xtics font ticsfont
set ytics font ticsfont
set output "Selectivity.png"

set macros
TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.15"
BMARGIN = "set tmargin at screen 0.55; set bmargin at screen 0.15"
LMARGIN = "set lmargin at screen 0.05; set rmargin at screen 0.45"
RMARGIN = "set lmargin at screen 0.50; set rmargin at screen 0.85"

set multiplot layout 1,2 #margins 0.10, 0.85, 0.2, 0.9
set pm3d map interpolate 5,5
@LMARGIN
set title 'Au'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
splot "../results/Au/rates.dat" using 1:2:($4/$5) with pm3d notitle
@RMARGIN
set title 'Cu'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
set format y ''; 
#unset ylabel
splot "../results/Cu/rates.dat" using 1:2:($4/$5) with pm3d notitle
unset multiplot
