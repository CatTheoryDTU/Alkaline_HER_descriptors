set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set xlabel "Potential vs SHE"
set ylabel "pH"
#surfaces= "Au Cu"
#do for [metal in surfaces] {print metal}
set terminal png enhanced font titlefont size 1000,1000
#set palette defined ( 1e-9 "blue", 0.1 "red" )
load 'moreland.pal'
#set cbrange [1e-30:1e30]
set cbrange [-10:10]
set xrange [-2.0:]
#set logscale cb
#set cbtics format "%.1e" font ticsfont
set cbtics format "%1.1f" font ticsfont
set cblabel '$Log_{10}(Rate_{Taf}/Rate_{Hey})$'
set xtics font ticsfont
set ytics font ticsfont
set output "Selectivity.png"

set macros
TMARGIN = "set tmargin at screen 0.95; set bmargin at screen 0.15"
BMARGIN = "set tmargin at screen 0.55; set bmargin at screen 0.15"
LMARGIN = "set lmargin at screen 0.05; set rmargin at screen 0.45"
RMARGIN = "set lmargin at screen 0.50; set rmargin at screen 0.85"

set multiplot layout 3,3 margins 0.10, 0.85, 0.2, 0.925 title "Selectivity" font "Helvetica,16"
set pm3d map interpolate 5,5
#Ag
set title 'Ag' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 dt 2 front 
set label 1 'Reversible Hydrogen Electrode'  at -0.7,13.75 textcolor 'black' font ticsfont rotate by -77.5 front 
set ytics 8,2,14
unset colorbox
set format x '';
splot "../results/Ag/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Au
set title 'Au' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
set format y '';
unset ylabel
set format x '';
splot "../results/Au/rates.dat" using 1:2:(log10(abs($4/$5))) with pm3d notitle
#Cu
set title 'Cu' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
unset xlabel
set format y '';
set format x '';
splot "../results/Cu/rates.dat" using 1:2:(log10(abs($4/$5))) with pm3d notitle

#Pd
set ylabel "pH"
set xlabel "Potential vs SHE"
set title 'Pd' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set label 1 'Reversible Hydrogen Electrode'  at -0.7,13.75 textcolor 'black' font ticsfont rotate by -77.5 front 
unset colorbox
#set format x "%1.1f"
set format y "%2.0f"
splot "../results/Pd/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Pt
unset ylabel
unset xlabel
set title 'Pt' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set format y ''; 
splot "../results/Pt/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Rh
unset ylabel
set title 'Rh' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
set format y ''; 
splot "../results/Rh/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Ir
set ylabel "pH"
set xlabel "Potential vs SHE"
set title 'Ir' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
unset colorbox
set format x "%1.1f"
set format y "%2.0f"
splot "../results/Ir/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Ni
unset ylabel
set title 'Ni' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 2 front
set colorbox
set format y ''; 
splot "../results/Ni/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
unset multiplot
