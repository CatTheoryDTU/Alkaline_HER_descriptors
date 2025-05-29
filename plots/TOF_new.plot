set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set xlabel "Potential vs SHE"
set ylabel "pH"
#surfaces= "Au Cu"
#do for [metal in surfaces] {print metal}
set terminal png enhanced font titlefont size 1000,1000
#set palette defined ( 1e-30 "blue", 0.1 "red" 
load 'turbo.pal'
set cbrange [-15:5]
set xrange [-2.0:-0.4]
#set logscale cb
set cbtics format "%2.f" font ticsfont
set cblabel "TOF s^{-1}"
set xtics font ticsfont
set ytics font ticsfont
set output "tof.png"

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
splot "../results/Ag/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle
#Au
set title 'Au' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
set format y '';
unset ylabel
set format x '';
splot "../results/Au/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle
#Cu
set title 'Cu' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
unset xlabel
set format y '';
set format x '';
splot "../results/Cu/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle

#Pd
set ylabel "pH"
set xlabel "Potential vs SHE"
set title 'Pd' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
#set format x "%1.1f"
set format y "%2.0f"
splot "../results/Pd/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle
#Pt
unset ylabel
unset xlabel
set title 'Pt' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set format y ''; 
splot "../results/Pt/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle
#Rh
unset ylabel
set title 'Rh' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
set format y ''; 
splot "../results/Rh/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle
#Ir
set ylabel "pH"
set xlabel "Potential vs SHE"
set title 'Ir' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
set format x "%1.1f"
set format y "%2.0f"
splot "../results/Ir/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle
#Ni
unset ylabel
set title 'Ni' offset 0,-1
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
set format y ''; 
splot "../results/Ni/production.dat" using 1:2:(log10($4+1e-30)) with pm3d notitle
unset multiplot
