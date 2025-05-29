set encoding utf8
ticsfont = "Helvetica,14"
titlefont = "Helvetica,22"
set xlabel "Hydrogen Binding Energy"
set ylabel "Barrier Energy, eV"
set terminal png enhanced font titlefont size 800,1000
load 'turbo.pal'
set xtics font ticsfont
set ytics font ticsfont
set output "3D_barrier_volcano.png"
set offset 1,1
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste HBEs.txt volmers.txt" u 1:2 prefix "hbevol"
stats "<paste HBEs.txt heyrovskys.txt" u 1:2 prefix "hbehey"
stats "<paste HBEs.txt tafels.txt" u 1:2 prefix "hbetaf"
stats "<paste PZCs.txt volmers.txt" u 1:2 prefix "pzcvol"
stats "<paste PZCs.txt heyrovskys.txt" u 1:2 prefix "pzchey"
stats "<paste PZCs.txt tafels.txt" u 1:2 prefix "pzctaf"
stats "<paste couplings.txt volmers.txt" u 1:2 prefix "coupvol"
stats "<paste couplings.txt heyrovskys.txt" u 1:2 prefix "couphey"
stats "<paste couplings.txt tafels.txt" u 1:2 prefix "couptaf"
stats "<paste dbandcenters.txt volmers.txt" u 1:2 prefix "dbandvol"
stats "<paste dbandcenters.txt heyrovskys.txt" u 1:2 prefix "dbandhey"
stats "<paste dbandcenters.txt tafels.txt" u 1:2 prefix "dbandtaf"
f2(x,y)=f21*(x-4.4)+f22*y+f23
g2(x,y)=g21*(x-4.4)+g22*y+g23
h2(x,y)=h21*(x-4.4)+h22*y+h23
fit f2(x,y) "<paste PZCs.txt HBEs.txt volmers.txt" u 1:2:3 via f21,f22,f23
fit g2(x,y) "<paste PZCs.txt HBEs.txt heyrovskys.txt" u 1:2:3 via g21,g22,g23
fit h2(x,y) "<paste PZCs.txt HBEs.txt tafels.txt" u 1:2:3 via h21,h22,h23
stats "<paste PZCs.txt HBEs.txt volmers.txt" using (f2($1,$2)):3 prefix "VOLM"
stats "<paste PZCs.txt HBEs.txt heyrovskys.txt" using (g2($1,$2)):3 prefix "HEY"
stats "<paste PZCs.txt HBEs.txt tafels.txt" using (h2($1,$2)):3 prefix "TAF"
#set xrange [-0.35:0.65]
#set yrange [0:1.5]
#set multiplot layout 1,3 margins 0.10, 0.85, 0.2, 0.9 title "Activation Energies at -1 V vs SHE"
#plot \
#	'<paste HBEs.txt volmers.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
#	'<paste HBEs.txt heyrovskys.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 7 point pt 7 lc 7 offset char 1,1 notitle, \
#	'<paste HBEs.txt tafels.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 6 point pt 7 lc 6 offset char 1,1 notitle, \
#	hbevol_slope * x + hbevol_intercept w l lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",hbevol_correlation**2), \
#	hbehey_slope * x + hbehey_intercept w l lc 7 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",hbehey_correlation**2), \
#	hbetaf_slope * x + hbetaf_intercept w l lc 6 dt 2 title sprintf("Tafel, r^2 = %1.2f",hbetaf_correlation**2)
#set xrange [3.4:5.4]
#set xlabel "PZC vs SHE"
#set ylabel ""
#plot \
#	'<paste PZCs.txt volmers.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
#	'<paste PZCs.txt heyrovskys.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 7 point pt 7 lc 7 offset char 1,1 notitle, \
#	'<paste PZCs.txt tafels.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 6 point pt 7 lc 6 offset char 1,1 notitle, \
#	pzcvol_slope * x + pzcvol_intercept w l lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",pzcvol_correlation**2), \
#	pzchey_slope * x + pzchey_intercept w l lc 7 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",pzchey_correlation**2), \
#	pzctaf_slope * x + pzctaf_intercept w l lc 6 dt 2 title sprintf("Tafel, r^2 = %1.2f",pzctaf_correlation**2)
#set xrange[3.4:5.4]
#set yrange[-0.35:-0.65]
#set zrange[0:3]
set xrange[-1:1]
set yrange[-1:1]
set zrange[0:1.5]
set xlabel "PZC, V" rotate parallel font titlefont
set ylabel "HBE, eV" rotate parallel font titlefont
set zlabel "Barrier Energy, eV" rotate parallel font titlefont
#	"<paste PZCs.txt HBEs.txt volmers.txt metals.txt " u 1:2:3:(sprintf("%s",stringcolumn(4))) w labels notitle, \
#	"<paste PZCs.txt HBEs.txt heyrovskys.txt metals.txt" using 1:2:3:(sprintf("%s",stringcolumn(4))) w labels textcolor lt 7 notitle, \
#	"<paste PZCs.txt HBEs.txt tafels.txt metals.txt" using 1:2:3:(sprintf("%s",stringcolumn(4))) w  labels textcolor lt 6 notitle
set key top right font ticsfont offset 0,2
set tmargin at screen 0.9
set lmargin at screen 0.1
set grid x,y,z vertical
set pm3d depthorder
set view 60,45
set isosamples 20
set xyplane 0
set style fill transparent solid 0.25
unset colorbox
splot \
	 f2(x+4.44,y) lc 'black' title sprintf("Volmer, r^2 = %1.2f, %1.2f*PZC+%1.2f*HBE+%1.2f",VOLM_correlation**2,f21,f22,f23) w pm3d fillcolor 'black', \
	 g2(x+4.44,y) lc 7 title sprintf("Heyrovsky, r^2 = %1.2f, %1.2f*PZC+%1.2f*HBE+%1.2f",HEY_correlation**2,g21,g22,g23) w pm3d fillcolor 'red', \
	 h2(x+4.44,y) lc 6 title sprintf("Tafel, r^2 = %1.2f, %1.2f*PZC+%1.2f*HBE+%1.2f",TAF_correlation**2,h21,h22,h23) w pm3d fillcolor 'blue', \
	"<paste PZCs.txt HBEs.txt volmers.txt metals.txt " u ($1-4.44):2:3 w points pt 7 lc 'black' notitle, \
	"<paste PZCs.txt HBEs.txt heyrovskys.txt metals.txt" using ($1-4.44):2:3 w points pt 7 lc 7 notitle, \
	"<paste PZCs.txt HBEs.txt tafels.txt metals.txt" using ($1-4.44):2:3 w points pt 7 lc 6 notitle
#unset multiplot

