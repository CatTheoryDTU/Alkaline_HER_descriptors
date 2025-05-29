set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set xlabel "Hydrogen Binding Energy"
set ylabel "Barrier Energy, eV"
set terminal png enhanced font titlefont size 1800,800
#load 'turbo.pal'
set xtics font ticsfont
set ytics font ticsfont
set output "Barriers.png"
set offset 1,1
stats "<paste HBEs.txt volmer_energies.txt" u 1:2 prefix "hbevol"
stats "<paste HBEs.txt heyrovsky_energies.txt" u 1:2 prefix "hbehey"
stats "<paste HBEs.txt tafel_energies.txt" u 1:2 prefix "hbetaf"
stats "<paste PZCs.txt volmer_energies.txt" u 1:2 prefix "pzcvol"
stats "<paste PZCs.txt heyrovsky_energies.txt" u 1:2 prefix "pzchey"
stats "<paste PZCs.txt tafel_energies.txt" u 1:2 prefix "pzctaf"
f2(x,y)=f21*(x-4.4)+f22*y+f23
g2(x,y)=g21*(x-4.4)+g22*y+g23
h2(x,y)=h21*(x-4.4)+h22*y+h23
set fit quiet
fit f2(x,y) "<paste PZCs.txt HBEs.txt volmer_energies.txt" u 1:2:3 via f21,f22,f23
fit g2(x,y) "<paste PZCs.txt HBEs.txt heyrovsky_energies.txt" u 1:2:3 via g21,g22,g23
fit h2(x,y) "<paste PZCs.txt HBEs.txt tafel_energies.txt" u 1:2:3 via h21,h22,h23
stats "<paste PZCs.txt HBEs.txt volmer_energies.txt" using (f2($1,$2)):3 prefix "VOLM"
stats "<paste PZCs.txt HBEs.txt heyrovsky_energies.txt" using (g2($1,$2)):3 prefix "HEY"
stats "<paste PZCs.txt HBEs.txt tafel_energies.txt" using (h2($1,$2)):3 prefix "TAF"
set xrange [-0.35:0.65]
set yrange [0:2.5]
set multiplot layout 1,3 margins 0.10, 0.85, 0.2, 0.9 title "Barriers Relative to True Initial State"
plot \
	'<paste HBEs.txt volmer_energies.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
	'<paste HBEs.txt heyrovsky_energies.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 7 point pt 7 lc 7 offset char 1,1 notitle, \
	'<paste HBEs.txt tafel_energies.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 6 point pt 7 lc 6 offset char 1,1 notitle, \
	hbevol_slope * x + hbevol_intercept w l lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",hbevol_correlation**2), \
	hbehey_slope * x + hbehey_intercept w l lc 7 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",hbehey_correlation**2), \
	hbetaf_slope * x + hbetaf_intercept w l lc 6 dt 2 title sprintf("Tafel, r^2 = %1.2f",hbetaf_correlation**2)
set xrange [3.4:5.4]
set xlabel "PZC vs SHE"
set ylabel ""
plot \
	'<paste PZCs.txt volmer_energies.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
	'<paste PZCs.txt heyrovsky_energies.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 7 point pt 7 lc 7 offset char 1,1 notitle, \
	'<paste PZCs.txt tafel_energies.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 6 point pt 7 lc 6 offset char 1,1 notitle, \
	pzcvol_slope * x + pzcvol_intercept w l lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",pzcvol_correlation**2), \
	pzchey_slope * x + pzchey_intercept w l lc 7 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",pzchey_correlation**2), \
	pzctaf_slope * x + pzctaf_intercept w l lc 6 dt 2 title sprintf("Tafel, r^2 = %1.2f",pzctaf_correlation**2)
set xrange[0.0:2.0]
set xlabel "PZC, HBE fit"
set ylabel ""
plot \
	"<paste PZCs.txt HBEs.txt volmer_energies.txt metals.txt" using (f2($1,$2)):3:(sprintf("%s",stringcolumn(4))) w labels point pt 7 offset char 1,1 notitle, \
	"<paste PZCs.txt HBEs.txt heyrovsky_energies.txt metals.txt" using (g2($1,$2)):3:(sprintf("%s",stringcolumn(4))) w labels textcolor lt 7 point pt 7 lc 7 offset char 1,1 notitle, \
	"<paste PZCs.txt HBEs.txt tafel_energies.txt metals.txt" using (h2($1,$2)):3:(sprintf("%s",stringcolumn(4))) w  labels textcolor lt 6 point pt 7 lc 6 offset char 1,1 notitle, \
	VOLM_slope * x + VOLM_intercept lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",VOLM_correlation**2), \
	HEY_slope * x + HEY_intercept lc 7 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",HEY_correlation**2), \
	TAF_slope * x + TAF_intercept lc 6 dt 2 title sprintf("Tafel, r^2 = %1.2f",TAF_correlation**2)
unset multiplot

