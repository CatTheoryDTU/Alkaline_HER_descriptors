set encoding utf8
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics (-9, -6, -3, 0) nomirror
set ylabel 'log($|j_0|$/(mA cm$^{-2}$))'
set terminal epslatex color colortext size 6in,4in "cmss,10" standalone
set output "Sheng_Activity_volcano.tex"
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
fit f(x,y) "<paste ../PZCs.txt ../vac_HBEs.txt ../i0s.txt" u 1:2:(1*($3-amps)) via a,b,c
fit piecef(x) "<paste ../vac_Htops.txt ../i0s.txt" using 1:(1*($2-amps)) via d,g,h
q=0.1
piecefhfcc(x)= x<=-q ? r*(x+q)+n : -r*(x+q)+n
fit piecefhfcc(x) "<paste ../vac_HBEs.txt ../i0s.txt" using 1:(1*($2-amps)) via r,q,n
stats "<paste ../PZCs.txt ../vac_HBEs.txt ../i0s.txt" using (f($1,$2)):(1*($3-amps)) prefix "DESC"
stats "<paste ../vac_Htops.txt ../i0s.txt" using (piecef($1)):(1*($2-amps)) prefix "HTOP"
stats "<paste ../vac_HBEs.txt ../i0s.txt" using (piecefhfcc($1)):(1*($2-amps)) prefix "HMIN"
stats "<paste ../PZCs.txt ../i0s.txt" using ($1-4.44):(1*($2-amps)) prefix "PZC"
#stats "<paste ../vac_Htops.txt ../i0s.txt" using 1:(1*($2-amps)) prefix "H"
stats "<paste ../PZCs.txt ../vac_Htops.txt" using 1:2 prefix "HPZC"

#### Experimental fits
#hfcc
exp_piecefhfcc(x)= x<=-expq ? expr*(x+expq)+expn : -expr*(x+expq)+expn
expq=0.1
fit exp_piecefhfcc(x) "../sheng_i0s.txt" using 1:(1*($5-amps)) via expr,expq,expn
stats "../sheng_i0s.txt" using (exp_piecefhfcc($1)):(1*($5-amps)) prefix "exp_HMIN"
#pzc
stats "../sheng_i0s.txt" using ($2-4.44):(1*($5-amps)) prefix "exp_PZC"
#combined
exp_f(x,y)=expb*(x-4.44)+expa*y+expc
fit exp_f(x,y) "../sheng_i0s.txt" u 2:1:(1*($5-amps)) via expa,expb,expc
stats "../sheng_i0s.txt" using (f($2,$1)):(1*($5-amps)) prefix "exp_DESC"
#Htop
exp_piecef(x)= x<=-expd ? expg*(x+expd)+exph : -expg*(x+expd)+exph
fit exp_piecef(x) "../sheng_i0s.txt" using 3:(1*($5-amps)) via expd,expg,exph
stats "../sheng_i0s.txt" using (exp_piecef($3)):(1*($5-amps)) prefix "exp_HTOP"
#########Line and point styles#######
set style line 1 lc 'black' pt 7 #Theory points
set style line 2 lc 'black' dt 2 lw 5 #Theory line
set style line 3 pt 7 lc 'blue' #Experiment points
set style line 4 lc 'blue' dt 3 lw 1 #Experiment line
set key noautotitle

######## Axes ###########
set xrange [-0.3:0.7]
set yrange [-10:2]
set xtics -0.25,.25,0.5
#set format x '\text{%0.2f}'
set multiplot layout 2,2 margins 0.15, 0.95, 0.15, 0.94 spacing 0.05,0.15 # title "Activation Energies at -1 V vs SHE" font titlefont

#vac_HBEs
set xlabel '$\Delta G^{\mathrm{fcc}}_\mathrm{H}$ (eV)'# offset 0,screen 0.05
#set title "Thermodynamic" #offset 0,graph -0.05
set label 1 at  -0.28, -8 sprintf('\small \shortstack[c]{Theory: {$R^2$=%1.2f} \\ {\tiny y=±%1.2f|x+%1.2f|$%1.2f$}}',HMIN_correlation**2,r,q,n) front
set label 3 at  0.28, -0 sprintf('\small \shortstack[c]{Exp: {$R^2$=%1.2f} \\ {\tiny y=±%1.2f|x+%1.2f|$%1.2f$}}',exp_HMIN_correlation**2,expr,expq,expn) textcolor 'blue' front
set label 2 at graph -0.15,1.1 '\large{a)}' front

set label 4 at -0.09,0.8 'Pt' center front
set label 5 at 0.03,-0.6 'Ir' center front
set label 6 at -0.01,-4.4 'Rh' center front
set label 7 at -0.2,-4.7 'Ni' center front
set label 8 at -0.11,-4.1 'Pd' center front
set label 9 at 0.25,-7.8 'Cu' center front
set label 10 at 0.61,-6.8 'Au' center front
set label 11 at 0.54,-9.3 'Ag' center front

plot \
	'<paste ../vac_HBEs.txt ../i0s.txt ../metals.txt' u 1:(1*($2-amps)):(sprintf("%s",stringcolumn(3))) \
        ls 1, \
	'../sheng_i0s.txt' u 1:(1*($5-amps)):6 w errorbars ls 3, \
	piecefhfcc(x) ls 2, \
	exp_piecefhfcc(x) ls 4 #,\
#	'<paste ../vac_HBEs.txt ../i0s.txt ../metals.txt' u 1:(1*($2-amps)):(sprintf("%s",stringcolumn(3))) \
#        w labels point ls 1 offset char 0.5,0.5
unset ylabel
set format y ''

# PZC
set label 2 at graph -0.1,1.1 '\large{b)}' front
#set title "Electrostatic" #offset 0,graph -0.05
set xlabel '$U_{\mathrm{PZC}}$ vs SHE (V)'
set xrange [-1.0:1.0]
set xtics -1,0.5,1
set label 1 at  0.08, -8 sprintf('\small \shortstack[c]{{Theory: $R^2$=%1.2f} \\ {\tiny y=%1.2fx%1.2f}}',PZC_correlation**2,PZC_slope,PZC_intercept) front
set label 3 at  -0.92, 0 \
    sprintf('\small \shortstack[c]{{Exp: $R^2$=%1.2f} \\ {\tiny y=%1.2fx%1.2f}}',exp_PZC_correlation**2,exp_PZC_slope,exp_PZC_intercept) \
    textcolor 'blue' front

set label 4 at 0.6,0.8 'Pt' center front
set label 5 at 0.25,-0.6 'Ir' center front
set label 6 at -0.34,-4.3 'Rh' center front
set label 7 at 0.0,-4.8 'Ni' center front
set label 8 at 0.11,-4.1 'Pd' center front
set label 9 at -0.7,-6.5 'Cu' center front
set label 10 at -0.1,-6.8 'Au' center front
set label 11 at -0.7,-9.3 'Ag' center front

plot \
	'<paste ../PZCs.txt ../i0s.txt ../metals.txt' u ($1-4.44):(1*($2-amps)):(sprintf("%s",stringcolumn(3))) ls 1,\
	'../sheng_i0s.txt' u ($2-4.44):(1*($5-amps)):6 w errorbars ls 3, \
	PZC_slope * x + PZC_intercept ls 2, \
	exp_PZC_slope * x + exp_PZC_intercept ls 4

#Combined
set label 2 at graph -0.15,1.1 '\large{c)}' front
set ylabel 'log($|j_0|$/(mA cm$^{-2}$))'
unset format y
set xrange [-10:2]
set xrange [-2:10]
set xtics -10,2,2
set xtics -2,2,10
#set title "Combined" #offset 0,graph -0.05
set xlabel '$a\Delta G^{\mathrm{fcc}}_\mathrm{H}+b(\mathrm{e}U_{\mathrm{PZC}})+c$  (eV)'
set label 1 at  -0.4, -8.3 sprintf('\small \shortstack[c]{{Theory: $R^2$=%1.2f} \\ {\tiny a=%1.2f, b=%1.2f, c=%1.2f}}',DESC_correlation**2,-1*a,-1*b,-1*c) front
set label 3 at  4.6, 0 \
    sprintf('\small \shortstack[c]{{Exp: $R^2$=%1.2f } \\ {\tiny a=%1.2f, b=%1.2f, c=%1.2f}}',exp_DESC_correlation**2,-1*expa,-1*expb,-1*expc)  textcolor 'blue' front

set label 4 at 0.,0.8 'Pt' center front
set label 5 at 2.3,-0.6 'Ir' center front
set label 6 at 4.9,-4.1 'Rh' center front
set label 7 at 3.3,-4.9 'Ni' center front
set label 8 at 2.2,-4. 'Pd' center front
set label 9 at 7.3,-6.5 'Cu' center front
set label 10 at 6.5,-8.4 'Au' center front
set label 11 at 9.2,-7.7 'Ag' center front

plot \
	"<paste ../PZCs.txt ../vac_HBEs.txt ../i0s.txt ../metals.txt" using (-1*f($1,$2)):(1*($3-amps)):(sprintf("%s",stringcolumn(4))) \
        ls 1,\
	'../sheng_i0s.txt' u (-1*f($2,$1)):(1*($5-amps)):6 w errorbars ls 3, \
	DESC_slope * -x + DESC_intercept ls 2, \
	exp_DESC_slope * -x + exp_DESC_intercept ls 4

#vac_Htop
set label 2 at graph -0.1,1.1 '\large{d)}' front
unset ylabel
set format y ''
set xrange [-0.3:1.2]
set xtics 0,.25,1.0
set xlabel '$\Delta G^{\mathrm{top}}_\mathrm{H}$ (eV)'# offset 0,screen 0.05
#set title "Thermodynamic" #offset 0,graph -0.05
set label 1 at  -.25, -8 sprintf('\small \shortstack[c]{{Theory: $R^2$=%1.2f} \\ {\tiny y=±%1.2f|x+%1.2f|$%1.2f$}}',HTOP_correlation**2,g,d,h) front
set label 3 at  .55, -0 sprintf('\small \shortstack[c]{{Exp: $R^2$=%1.2f} \\ {\tiny y=±%1.2f|x+%1.2f|+$%1.2f$}}',exp_HTOP_correlation**2,expg,expd,exph) textcolor 'blue' front

set label 4 at -0.1,0.8 'Pt' center front
set label 5 at -0.1,-2.4 'Ir' center front
set label 6 at 0.15,-4.1 'Rh' center front
set label 7 at 0.37,-5.1 'Ni' center front
set label 8 at 0.33,-2.8 'Pd' center front
set label 9 at 0.92,-6.5 'Cu' center front
set label 10 at 0.78,-8.4 'Au' center front
set label 11 at 1.15,-7.8 'Ag' center front

plot \
	'<paste ../vac_Htops.txt ../i0s.txt ../metals.txt' u 1:(1*($2-amps)):(sprintf("%s",stringcolumn(3))) ls 1,\
	'../sheng_i0s.txt' u 3:(1*($5-amps)):6 w errorbars ls 3, \
	piecef(x) ls 2, \
	exp_piecef(x) ls 4
unset multiplot
