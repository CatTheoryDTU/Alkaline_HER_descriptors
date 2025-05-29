set encoding utf8
set ylabel "log(-j$_0$)" 
set xtics nomirror #offset 0,graph 0.025 nomirror
#set format y '\text{%0.f}'
set ytics nomirror
#set terminal svg enhanced size 1500,500
#set output "True_Activity_volcano.svg"
set ylabel 'log($|j_0|$/(mA cm$^{-2}$))'
set terminal epslatex color size 6in,4in "cmss" standalone
set output "Figure_Activity_volcano.tex"
#set key center top
f(x,y)=a*(x-4.44)+b*y+c
piecef(x)= x<=-d ? g*(x+d)+h : -g*(x+d)+h
d=0.1
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
amps=0 #converts to milliamps
#amps=3 #converts to amps
fit f(x,y) "<paste PZCs.txt Htops.txt i0s.txt" u 1:2:(1*($3-amps)) via a,b,c
fit piecef(x) "<paste Htops.txt i0s.txt" using 1:(1*($2-amps)) via d,g,h
stats "<paste PZCs.txt Htops.txt i0s.txt" using (f($1,$2)):(1*($3-amps)) prefix "DESC"
stats "<paste Htops.txt i0s.txt" using (piecef($1)):(1*($2-amps)) prefix "HVOLCANO"
stats "<paste PZCs.txt i0s.txt" using ($1-4.44):(1*($2-amps)) prefix "PZC"
stats "<paste Htops.txt i0s.txt" using 1:(1*($2-amps)) prefix "H"
stats "<paste PZCs.txt Htops.txt" using 1:2 prefix "HPZC"
#pH14RHE-0.2_currents.txt
#i0s.txt
set xrange [-0.3:1.2]
set yrange [-10:2]
set xtics -0.25,.25,0.5
#set format x '\text{%0.2f}'
set multiplot layout 1,3 margins 0.1, 0.95, 0.15, 0.85 #title "Activity Descriptors" font titlefont
set xlabel '$\Delta G_H$ (eV)'# offset 0,screen 0.05
set title 
set title "Thermodynamic" #offset 0,graph -0.05
set key top right
set label 1 at  0.1, 0 sprintf('\small \shortstack[l]{{$r^2$=%1.2f} \\ {y=±%1.2f(x+} \\ {   %1.2f)$%1.2f$}}',HVOLCANO_correlation**2,g,d,h) front
plot \
	'<paste Htops.txt i0s.txt metals.txt' u 1:(1*($2-amps)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 0.5,0.5 notitle, \
	piecef(x) lc 'black' dt 2 lw 5 notitle# sprintf("r^2 = %1.2f",HVOLCANO_correlation**2)
unset ylabel
set format y ''
set title "Electrostatic" #offset 0,graph -0.05
set xlabel '$U_{PZC}$ vs SHE (V)'
set xrange [-1.0:1.0]
set xtics -1,0.5,1
#set arrow from -1.03,-8 to -1.03,4 nohead lc 'black' dt 3
#set label "-1.03 V vs SHE" at graph -0.83,3
set key top left
#set format x '\text{%0.1f}'
set label 1 at  -0.8, 0 sprintf('\small \shortstack[l]{{$r^2$=%1.2f} \\ {y=%1.2fx} \\ {   $%1.2f$}}',PZC_correlation**2,PZC_slope,PZC_intercept) front
plot \
	'<paste PZCs.txt i0s.txt metals.txt' u ($1-4.44):(1*($2-amps)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char -1,0.5 notitle, \
	PZC_slope * x + PZC_intercept lc 'black' dt 2 lw 5 notitle# sprintf("r^2 = %1.2f",PZC_correlation**2)
set xrange [-10:2]
set xtics -10,2,2
#set format x '\text{%0.0f}'
set title "Combined" #offset 0,graph -0.05
#set xlabel "$a*(PZC-4.44)+b*Htop+c$"
set xlabel '$a(U_{PZC})+b\Delta G_H +c$'
set key top left 
#set style textbox 1 transparent fc rgb 0xffffff border lc "black" lw 0
#set obj 1 rect at -2,-8 size 7.5,1
#set label 1 sprintf("a=%1.2f b=%1.2f c=%1.2f",a,b,c) at -13,-4 #boxed bs 1 font subtitlefont
set label 1 at  -9, 0 sprintf('\small \shortstack[l]{{$r^2$=%1.2f} \\ {a=%1.2f} \\ {b=%1.2f} \\ {c=%1.2f}}',DESC_correlation**2,a,b,c) front
plot \
	"<paste PZCs.txt Htops.txt i0s.txt metals.txt" using (f($1,$2)):(1*($3-amps)):(sprintf("%s",stringcolumn(4))) w  labels point pt 7 offset char 1,0.5 notitle, \
	DESC_slope * x + DESC_intercept lc 'black' dt 2 lw 5 notitle #sprintf("r^2 = %1.2f",DESC_correlation**2)
unset multiplot

