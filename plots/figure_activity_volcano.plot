set encoding utf8
ticsfont = "Helvetica,18"
titlefont = "Helvetica,22"
subtitlefont = "Helvetica,18"
labelfont = "Helvetica,18"
set ylabel "log(-j$_0$)" font titlefont
load 'turbo.pal'
set xtics font ticsfont nomirror #offset 0,graph 0.025 nomirror
set ytics font ticsfont nomirror
set terminal svg enhanced font labelfont size 1500,500
set ylabel "log(-j_0 A/cm^2)" font titlefont
set output "Figure_Activity_volcano.svg"
#set terminal epslatex color size 6in,4in header "cmss"
#set output "Figure_Activity_volcano.tex"
set offset 1,1
#set key center top
f(x,y)=a*(x-4.44)+b*y+c
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
fit f(x,y) "<paste PZCs.txt HBEs.txt i0s.txt" u 1:2:(1*($3-3)) via a,b,c
stats "<paste PZCs.txt HBEs.txt i0s.txt" using (f($1,$2)):(1*($3-3)) prefix "DESC" # -3 converts to A/cm^2
stats "<paste PZCs.txt i0s.txt" using ($1-4.44):(1*($2-3)) prefix "PZC"
stats "<paste HBEs.txt i0s.txt" using 1:(1*($2-3)) prefix "H"
stats "<paste PZCs.txt HBEs.txt" using 1:2 prefix "HPZC"
#pH14RHE-0.2_currents.txt
#i0s.txt
set xrange [-0.3:0.7]
set yrange [-13:-1]
set multiplot layout 1,3 margins 0.1, 0.95, 0.15, 0.85 #title "Activity Descriptors" font titlefont
set xlabel "Hydrogen Binding Energy, eV" font titlefont #offset 0,screen 0.05
set title font subtitlefont
set title "Thermodynamic" #offset 0,graph -0.05
set key top right
plot \
	'<paste HBEs.txt i0s.txt metals.txt' u 1:(1*($2-3)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 0.5,0.5 notitle, \
	H_slope * x + H_intercept lc 'black' dt 2 title sprintf("r^2 = %1.2f",H_correlation**2)
unset ylabel
set format y ''
set title "Electrostatic" #offset 0,graph -0.05
set xlabel "PZC vs SHE" font titlefont 
set xrange [-1.0:1.0]
#set arrow from -1.03,-8 to -1.03,4 nohead lc 'black' dt 3
#set label "-1.03 V vs SHE" at graph -0.83,3
set key top left
plot \
	'<paste PZCs.txt i0s.txt metals.txt' u ($1-4.44):(1*($2-3)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char -1,0.5 notitle, \
	PZC_slope * x + PZC_intercept lc 'black' dt 2 title sprintf("r^2 = %1.2f",PZC_correlation**2)
set xrange [-14:-2]
#set format x ''
set title "Combined" #offset 0,graph -0.05
#set xlabel "$a*(PZC-4.44)+b*HBE+c$"
set xlabel "a*(PZC-4.44)+b*HBE+c" font titlefont 
set key top left 
#set style textbox 1 transparent fc rgb 0xffffff border lc "black" lw 0
#set obj 1 rect at -2,-8 size 7.5,1
set label 1 sprintf("a=%1.2f b=%1.2f c=%1.2f",a,b,c) at -13,-4 font subtitlefont#boxed bs 1 font subtitlefont
plot \
	"<paste PZCs.txt HBEs.txt i0s.txt metals.txt" using (f($1,$2)):(1*($3-3)):(sprintf("%s",stringcolumn(4))) w  labels point pt 7 offset char 1,0.5 notitle, \
	DESC_slope * x + DESC_intercept lc 'black' dt 2 title sprintf("r^2 = %1.2f",DESC_correlation**2)
unset multiplot

