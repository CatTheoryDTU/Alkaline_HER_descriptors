set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set xlabel "Hydrogen Binding Energy, eV"
set ylabel "log10(-j) at pH=14, SHE=-1.03"
set terminal png enhanced font titlefont size 1500,500
load 'turbo.pal'
set xtics font ticsfont
set ytics font ticsfont
set output "Activity_volcano.png"
set offset 1,1
set key center top
f(x,y)=a*(x-4.4)+b*y+c
fit f(x,y) "<paste PZCs.txt HBEs.txt pH14RHE-0.2_currents.txt" u 1:2:(log10(-1*$3)) via a,b,c
stats "<paste PZCs.txt HBEs.txt pH14RHE-0.2_currents.txt" using (f($1,$2)):(log10(-1*$3)) prefix "DESC"
stats "<paste PZCs.txt pH14RHE-0.2_currents.txt" using ($1-4.40):(log10(-1*$2)) prefix "PZC"
stats "<paste HBEs.txt pH14RHE-0.2_currents.txt" using 1:(log10(-1*$2)) prefix "H"
stats "<paste PZCs.txt HBEs.txt" using 1:2 prefix "HPZC"
#pH14RHE-0.2_current0s.txt
set xrange [-0.35:0.65]
set yrange [-8:4]
set multiplot layout 1,3 #margins 0.10, 0.85, 0.2, 0.9
plot \
	'<paste HBEs.txt pH14RHE-0.2_currents.txt metals.txt' u 1:(log10(-1*$2)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
	H_slope * x + H_intercept lc 'black' dt 2 title sprintf("r^2 = %1.2f",H_correlation**2)
set xlabel "PZC vs SHE"
set xrange [-1.0:1.0]
#set arrow from -1.03,-8 to -1.03,4 nohead lc 'black' dt 3
#set label "-1.03 V vs SHE" at graph -0.83,3
plot \
	'<paste PZCs.txt pH14RHE-0.2_currents.txt metals.txt' u ($1-4.44):(log10(-1*$2)):(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
	PZC_slope * x + PZC_intercept lc 'black' dt 2 title sprintf("r^2 = %1.2f",PZC_correlation**2)
set xrange [-10:10]
set xlabel "a*HBE+b*(PZC-4.4)+c"
plot \
	"<paste PZCs.txt HBEs.txt pH14RHE-0.2_currents.txt metals.txt" using (f($1,$2)):(log10(-1*$3)):(sprintf("%s",stringcolumn(4))) w  labels point pt 7 offset char 1,1 notitle, \
	DESC_slope * x + DESC_intercept lc 'black' dt 2 title sprintf("r^2 = %1.2f",DESC_correlation**2)
