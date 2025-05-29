set encoding utf8
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set ylabel 'log($|j_0|$/(mA cm$^{-2}$))'
set terminal epslatex color size 6in,4in "cmss" standalone
set output "FeW_Volcano.tex"
f(x,y)=b*(x-4.44)+a*y+c
piecef(x)= x<=-d ? g*(x+d)+h : -g*(x+d)+h
a=2.0
b=-4.4
c=-3.2
d=0.1
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
amps=0 #converts to milliamps
#amps=3 #converts to amps
fit f(x,y) "<paste PZCs.txt vac_HBEs.txt i0s.txt" u 1:2:(1*($3-amps)) via a,b,c
fit piecef(x) "<paste vac_Htops.txt i0s.txt" using 1:(1*($2-amps)) via d,g,h
q=0.1
piecefhmin(x)= x<=-q ? r*(x+q)+n : -r*(x+q)+n
fit piecefhmin(x) "<paste vac_HBEs.txt i0s.txt" using 1:(1*($2-amps)) via r,q,n
stats "<paste PZCs.txt vac_HBEs.txt i0s.txt" using (f($1,$2)):(1*($3-amps)) prefix "DESC"
stats "<paste vac_Htops.txt i0s.txt" using (piecef($1)):(1*($2-amps)) prefix "HTOP"
stats "<paste vac_HBEs.txt i0s.txt" using (piecefhmin($1)):(1*($2-amps)) prefix "HMIN"
stats "<paste PZCs.txt i0s.txt" using ($1-4.44):(1*($2-amps)) prefix "PZC"
#stats "<paste vac_Htops.txt i0s.txt" using 1:(1*($2-amps)) prefix "H"
stats "<paste PZCs.txt vac_Htops.txt" using 1:2 prefix "HPZC"
set xrange [-0.6:0.7]
set yrange [-10:2]
set xtics -0.25,.25,0.5
#set format x '\text{%0.2f}'
set multiplot layout 2,2 margins 0.15, 0.95, 0.15, 0.95 spacing 0.05,0.15 # title "Activation Energies at -1 V vs SHE" font titlefont
#vac_HBEs
set xlabel '$\Delta G^{fcc}_H$ (eV)'# offset 0,screen 0.05
#set title "Thermodynamic" #offset 0,graph -0.05
set label 1 at  -0.2, -8 sprintf('\small \shortstack[l]{{$R^2$=%1.2f} \\ {y=±%1.2f(x+%1.2f)$%1.2f$}}',HMIN_correlation**2,r,q,n) front
set label 2 at graph -0.15,1.1 'a)' front
plot \
	'<paste vac_HBEs.txt i0s.txt metals.txt' u 1:(1*($2-amps)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 0.5,0.5 notitle, \
	piecefhmin(x) lc 'black' dt 2 lw 5 notitle# sprintf("R^2 = %1.2f",HTOP_correlation**2)
unset ylabel
set format y ''
# PZC
#set title "Electrostatic" #offset 0,graph -0.05
set xlabel '$U_{PZC}$ vs SHE (V)'
set xrange [-1.0:1.0]
set xtics -1,0.5,1
set label 1 at  -0.9, -0.1 sprintf('\small \shortstack[l]{{$R^2$=%1.2f} \\ {y=%1.2fx%1.2f}}',PZC_correlation**2,PZC_slope,PZC_intercept) front
set label 2 at graph -0.1,1.1 'b)' front
plot \
	'<paste PZCs.txt i0s.txt metals.txt' u ($1-4.44):(1*($2-amps)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char -1,0.5 notitle, \
	PZC_slope * x + PZC_intercept lc 'black' dt 2 lw 5 notitle# sprintf("R^2 = %1.2f",PZC_correlation**2)
#Combined
set ylabel 'log($|j_0|$/(mA cm$^{-2}$))'
unset format y 
set xrange [-10:2]
set xtics -10,2,2
#set title "Combined" #offset 0,graph -0.05
set xlabel '$a\Delta G^{fcc}_H+b(U_{PZC})+c$'
set label 1 at  -9, -1 sprintf('\small \shortstack[l]{{$R^2$=%1.2f} \\ {a=%1.2f} \\ {b=%1.2f} \\ {c=%1.2f}}',DESC_correlation**2,a,b,c) front
set label 2 at graph -0.15,1.1 'c)' front
plot \
	"<paste PZCs.txt vac_HBEs.txt i0s.txt metals.txt" using (f($1,$2)):(1*($3-amps)):(sprintf("%s",stringcolumn(4))) w  labels point pt 7 offset char 1,0.5 notitle, \
	DESC_slope * x + DESC_intercept lc 'black' dt 2 lw 5 notitle #sprintf("R^2 = %1.2f",DESC_correlation**2)
#vac_Htop
unset ylabel
set format y ''
set xrange [-0.6:1.2]
set xtics -0.5,.5,1.0
set xlabel '$\Delta G^{top}_H$ (eV)'# offset 0,screen 0.05
#set title "Thermodynamic" #offset 0,graph -0.05
set label 1 at  -.2, -8 sprintf('\small \shortstack[l]{{$R^2$=%1.2f} \\ {y=±%1.2f(x+%1.2f)$%1.2f$}}',HTOP_correlation**2,g,d,h) front
set label 2 at graph -0.1,1.1 'd)' front
plot \
	'<paste vac_Htops.txt i0s.txt metals.txt' u 1:(1*($2-amps)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 0.5,0.5 notitle, \
	piecef(x) lc 'black' dt 2 lw 5 notitle# sprintf("R^2 = %1.2f",HTOP_correlation**2)
unset multiplot
