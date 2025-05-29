set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set xlabel "Hydrogen Binding Energy"
set ylabel "Symmetry Factor β, eV/V"
set terminal png enhanced font titlefont size 1800,800
load 'turbo.pal'
set xtics font ticsfont
set ytics font ticsfont
set output "Betas.png"
set offset 1,1
stats "<paste HBEs.txt volmer_betas.txt" u 1:2 prefix "hbevol"
stats "<paste HBEs.txt heyrovsky_betas.txt" u 1:2 prefix "hbehey"
stats "<paste PZCs.txt volmer_betas.txt" u 1:2 prefix "pzcvol"
stats "<paste PZCs.txt heyrovsky_betas.txt" u 1:2 prefix "pzchey"
f2(x,y)=f21*(x-4.4)+f22*y+f23
g2(x,y)=g21*(x-4.4)+g22*y+g23
h2(x,y)=h21*(x-4.4)+h22*y+h23
fit f2(x,y) "<paste PZCs.txt HBEs.txt volmer_betas.txt" u 1:2:3 via f21,f22,f23
fit g2(x,y) "<paste PZCs.txt HBEs.txt heyrovsky_betas.txt" u 1:2:3 via g21,g22,g23
stats "<paste PZCs.txt HBEs.txt volmer_betas.txt" using (f2($1,$2)):3 prefix "VOLM"
stats "<paste PZCs.txt HBEs.txt heyrovsky_betas.txt" using (g2($1,$2)):3 prefix "HEY"
set xrange [-0.35:0.65]
set yrange [0.20:0.75]
set multiplot layout 1,3 margins 0.10, 0.85, 0.2, 0.9
plot \
	'<paste HBEs.txt volmer_betas.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
	'<paste HBEs.txt heyrovsky_betas.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 2 point pt 7 lc 2 offset char 1,1 notitle, \
	hbevol_slope * x + hbevol_intercept w l lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",hbevol_correlation**2), \
	hbehey_slope * x + hbehey_intercept w l lc 2 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",hbehey_correlation**2)
set xrange [3.4:5.4]
set xlabel "PZC vs SHE"
set ylabel ""
plot \
	'<paste PZCs.txt volmer_betas.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels point pt 7 offset char 1,1 notitle, \
	'<paste PZCs.txt heyrovsky_betas.txt metals.txt' u 1:2:(sprintf("%s",stringcolumn(3))) w labels textcolor lt 2 point pt 7 lc 2 offset char 1,1 notitle, \
	pzcvol_slope * x + pzcvol_intercept w l lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",pzcvol_correlation**2), \
	pzchey_slope * x + pzchey_intercept w l lc 2 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",pzchey_correlation**2)
set xrange[0.25:0.75]
set xlabel "PZC, HBE fit"
set ylabel ""
plot \
	"<paste PZCs.txt HBEs.txt volmer_betas.txt metals.txt" using (f2($1,$2)):3:(sprintf("%s",stringcolumn(4))) w labels point pt 7 offset char 1,1 notitle, \
	"<paste PZCs.txt HBEs.txt heyrovsky_betas.txt metals.txt" using (g2($1,$2)):3:(sprintf("%s",stringcolumn(4))) w labels textcolor lt 2 point pt 7 lc 2 offset char 1,1 notitle, \
	VOLM_slope * x + VOLM_intercept lc 'black' dt 2 title sprintf("Volmer, r^2 = %1.2f",VOLM_correlation**2), \
	HEY_slope * x + HEY_intercept lc 2 dt 2 title sprintf("Heyrovsky, r^2 = %1.2f",HEY_correlation**2)
unset multiplot

