set encoding utf8
#tics#font = "Helvetica,10"
#title#font = "Helvetica,14"
set ylabel "pH"
#surfaces= "Au Cu"
#do for [metal in surfaces] {print metal}
#set terminal png enhanced #font titlefont size 1000,1000
#set output "Coverage.png"
#set palette defined ( 1e-9 "blue", 0.1 "red" )
set terminal epslatex color colortext size 7in,3.0in "cmss" standalone
set output "Figure_Selectivity.tex"
load '../moreland.pal'
set xrange [-2.0:0.0]
set yrange [7:14]
set xtics scale 0.5 #font ticsfont
set ytics scale 0.5 nomirror #font ticsfont

set multiplot layout 3,3 margins 0.10, 0.85, 0.05, 0.85 spacing 0.02, 0.03
set pm3d map explicit noborder
unset surface; set pm3d at b; set view map
set cbrange [-10:10]
set cbtics format "%+-0.0f" #font ticsfont
set cblabel '$Log(\frac{R_{Taf}}{R_{Hey}})$' offset graph 0.1,0
#Ag
set title 'Ag' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 dt 2 front 
#set label 1 '0V vs RHE'  at -0.7,13.75 textcolor 'black' rotate by -77.5 front #font ticsfont 
set label 1 '0V vs RHE'  at -0.5195,10.5 textcolor 'black' rotate by atan(3.5*1.75*-0.59)/pi*180+3 center front #font ticsfont 
set ytics 8,2,14 offset graph 0.05,0
unset colorbox
set xlabel "U vs SHE (V)" offset graph 0,1.95
set xtics -1.5,0.5,-0.5 offset graph 0,1.35
set format x "%1.1f"
set label 2 at -1.8,9 '\small \shortstack[l]{{Heyrovsky} \\ {Dominant}}' textcolor 'black' front
splot "../../results/Ag/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
unset label 2
#Au
set title 'Au' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 front
unset colorbox
set format y '';
unset ylabel
splot "../../results/Au/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Cu
set title 'Cu' offset -6.5,-2.5
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'black' lw 5 front
set colorbox front
set format y '';
#set format x '';
splot "../../results/Cu/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle

#Ir
#unset logscale cb
unset xlabel
#set cbtics format "%.1e" #font ticsfont
set format x '';
set ylabel "pH"
set title 'Ir' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set label 1 '0V vs RHE'  at -0.5195,10.5 textcolor 'white' rotate by atan(3.5*1.75*-0.59)/pi*180+3 center front #font ticsfont 
unset colorbox
#set format x "%1.1f"
set format y "%2.0f"
set label 2 at -1.8,9 '\small \shortstack[l]{{           Tafel} \\ {Dominant}}' textcolor 'white' front
splot "../../results/Ir/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
unset label 2
#Ni
unset ylabel
set title 'Ni' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set format y ''; 
splot "../../results/Ni/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Pd
unset ylabel
set title 'Pd' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set colorbox front
set format y ''; 
splot "../../results/Pd/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Pt
set ylabel "pH"
#set xlabel "Potential vs SHE"
set title 'Pt' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
unset colorbox
set format y "%2.0f"
splot "../../results/Pt/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
#Rh
unset ylabel
set title 'Rh' offset -6.5,-2.5 textcolor 'white'
set arrow 1 from -0.413,7 to -0.826,14 nohead lc 'white' lw 5 front
set colorbox front
set format y ''; 
splot "../../results/Rh/rates.dat" using 1:2:(log10($4/$5)) with pm3d notitle
unset multiplot
