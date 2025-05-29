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
set cbrange [0:2e2]
set cbtics format "%.e" font ticsfont
set cblabel "Tafel Slope mV/dec"
set xtics font ticsfont
set ytics font ticsfont
set output "TafelSlope.png"

d2(x,y) = ($0 == 0) ? (x1 = x, y1 = y, 0) : (x2 = x1, x1 = x, y2 = y1, y1 = y, -1*(y1-y2)/(log10(x1)-log10(x2)))


set macros
TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.15"
BMARGIN = "set tmargin at screen 0.55; set bmargin at screen 0.15"
LMARGIN = "set lmargin at screen 0.05; set rmargin at screen 0.45"
RMARGIN = "set lmargin at screen 0.50; set rmargin at screen 0.85"

set multiplot layout 3,3 margins 0.10, 0.85, 0.2, 0.925 title "TOF" font "Helvetica,16"
set pm3d map interpolate 5,5
#Ag
set title 'Ag' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
set format x '';
splot "../results/Ag/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle
#Au
set title 'Au' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
set format y '';
unset ylabel
set format x '';
splot "../results/Au/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle
#Cu
set title 'Cu' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
unset xlabel
set format y '';
set format x '';
splot "../results/Cu/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle

#Pd
set ylabel "pH"
set xlabel "Potential vs SHE"
set title 'Pd' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
#set format x "%1.1f"
set format y "%2.0f"
splot "../results/Pd/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle
#Pt
unset ylabel
unset xlabel
set title 'Pt' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set format y ''; 
splot "../results/Pt/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle
#Rh
unset ylabel
set title 'Rh' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
set format y ''; 
splot "../results/Rh/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle
#Ir
set ylabel "pH"
set xlabel "Potential vs SHE"
set title 'Ir' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
set format x "%1.1f"
set format y "%2.0f"
splot "../results/Ir/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle
#Ni
unset ylabel
set title 'Ni' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
set format y ''; 
splot "../results/Ni/production.dat.tafel" using 2:1:(d2($4,1000*$2)) with pm3d notitle
unset multiplot
