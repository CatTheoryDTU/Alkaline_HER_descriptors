set encoding utf8
ticsfont = "cmss,12"
titlefont = "cmss,22"
subtitlefont = "cmss,8"
set xlabel '$\Delta G^{fcc}_{H}$ (eV)'
#set ylabel 'Activation Free Energy $\Delta G^\ddag$ (eV)'
set ylabel '$\Delta G^\ddag$ (eV)'
set terminal epslatex color colortext size 6in,6in standalone font 'cmss' #header '\newcommand{\hl}[1]{\setlength{\fboxsep}{0.75pt}\colorbox{white}{#1}}'
set output "2x2_NewVolcano.tex"

set xtics font ticsfont nomirror
set ytics font ticsfont nomirror
set offset 1,1
#set fit quiet
set fit logfile '2x2_newvolcano.log'
set print '/dev/null'
stats "<paste ../vac_HBEs.txt ../volmers.txt" u 1:2 prefix "hbevol"
stats "<paste ../vac_HBEs.txt ../heyrovskys.txt" u 1:2 prefix "hbehey"
stats "<paste ../vac_HBEs.txt ../tafels.txt" u 1:2 prefix "hbetaf"
stats "<paste ../PZCs.txt ../volmers.txt" u ($1-4.44):2 prefix "pzcvol"
stats "<paste ../PZCs.txt ../heyrovskys.txt" u ($1-4.44):2 prefix "pzchey"
stats "<paste ../PZCs.txt ../tafels.txt" u ($1-4.44):2 prefix "pzctaf"
stats "<paste ../vac_Htops.txt ../volmers.txt" u 1:2 prefix "htopvol"
stats "<paste ../vac_Htops.txt ../heyrovskys.txt" u 1:2 prefix "htophey"
stats "<paste ../vac_Htops.txt ../tafels.txt" u 1:2 prefix "htoptaf"
f2(x,y)=f22*(-0.91*(x-4.4)+y)+f23
g2(x,y)=g22*(-0.91*(x-4.4)+y)+g23
h2(x,y)=h22*(-0.91*(x-4.4)+y)+h23
fit f2(x,y) "<paste ../PZCs.txt ../vac_HBEs.txt ../volmers.txt" u 1:2:3 via f22,f23
fit g2(x,y) "<paste ../PZCs.txt ../vac_HBEs.txt ../heyrovskys.txt" u 1:2:3 via g22,g23
fit h2(x,y) "<paste ../PZCs.txt ../vac_HBEs.txt ../tafels.txt" u 1:2:3 via h22,h23
stats "<paste ../PZCs.txt ../vac_HBEs.txt ../volmers.txt" using (f2($1,$2)):3 prefix "VOLM"
stats "<paste ../PZCs.txt ../vac_HBEs.txt ../heyrovskys.txt" using (g2($1,$2)):3 prefix "HEY"
stats "<paste ../PZCs.txt ../vac_HBEs.txt ../tafels.txt" using (h2($1,$2)):3 prefix "TAF"
set xrange [-0.35:0.65]
set xtics -0.25,0.25,0.5
set yrange [0.2:1.5]
set multiplot layout 2,2 margins 0.15, 0.95, 0.15, 0.925 spacing 0.025,0.1 # title "Activation Energies at -1 V vs SHE" font titlefont
set key at screen 0.8,screen 0.05 maxrows 2
set title font subtitlefont
set label 1 sprintf('\small{Volmer $R^2=%1.2f$}',hbevol_correlation**2) at 0.18,0.97 rotate by 25.0 font subtitlefont textcolor 'black' front
set label 2 sprintf('\small{Heyrovsky $R^2=%1.2f$}',hbehey_correlation**2) at 0.15,0.75 rotate by -40.0 font subtitlefont textcolor lt 7 front
set label 3 sprintf('\small{Tafel $R^2=%1.2f$}',hbetaf_correlation**2) at 0.25,0.910 rotate by 0 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.15,1.1 '\large{a)}' front
FILE = "../numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1)
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
plot \
	'<paste ../vac_HBEs.txt ../volmers.txt ../numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste ../vac_HBEs.txt ../heyrovskys.txt ../numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste ../vac_HBEs.txt ../tafels.txt ../numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	hbevol_slope * x + hbevol_intercept w l  lw 5.0 lc 'black' dt 2 notitle, \
	hbehey_slope * x + hbehey_intercept w l  lw 5.0 lc 7 dt 2 notitle, \
	hbetaf_slope * x + hbetaf_intercept w l  lw 5.0 lc 6 dt 2 notitle, \
	for [idx=1:8] keyentry with points lc 'black' ps 2 pointtype numbers[idx] title elements[idx]
#### PZC
set xrange [-1:1]
set xtics -1,0.5,1
set ytics format ""
set ylabel ""
set xlabel '$U_{PZC}$ vs SHE (V)'
set label 1 sprintf('\small{Volmer $R^2=%1.2f$}',pzcvol_correlation**2) at -0.9,1.4 rotate by atan(2*pzcvol_slope/1.3)/pi*180.0 font subtitlefont textcolor 'black' front
set label 2 sprintf('\small{Heyrovsky $R^2=%1.2f$}',pzchey_correlation**2) at 0.1,0.95 rotate by atan(2*pzchey_slope/1.3)/pi*180.0-5 font subtitlefont textcolor lt 7 front
set label 3 sprintf('\small{Tafel $R^2=%1.2f$}',pzctaf_correlation**2) at 0.215,0.855 rotate by atan(2*pzctaf_slope/1.3)/pi*180.0+2 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.1,1.1 '\large{b)}' front
unset key
plot \
	'<paste ../PZCs.txt ../volmers.txt ../numbers.txt' u ($1-4.44):2:3 w points lc 'black' ps 2 pt variable notitle, \
	'<paste ../PZCs.txt ../heyrovskys.txt ../numbers.txt' u ($1-4.44):2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste ../PZCs.txt ../tafels.txt ../numbers.txt' u ($1-4.44):2:3 w points ps 2 pt variable lc 6 notitle, \
	pzcvol_slope * x + pzcvol_intercept w l  lw 5.0 lc 'black' dt 2 title sprintf("R^2=%1.2f",pzcvol_correlation**2), \
	pzchey_slope * x + pzchey_intercept w l  lw 5.0 lc 7 dt 2 title sprintf("R^2=%1.2f",pzchey_correlation**2), \
	pzctaf_slope * x + pzctaf_intercept w l  lw 5.0 lc 6 dt 2 title sprintf("R^2=%1.2f",pzctaf_correlation**2)
#### HBE+PZC
set xrange[-0.8:1.3]
set ytics format "%1.1f"
#set ylabel 'Activation Free Energy $\Delta G^\ddag$ (eV)'
set ylabel '$\Delta G^\ddag$ (eV)'
set xtics -0.5,0.5,1.0
set xlabel '$\Delta G^{fcc}_{H} -\frac{b}{a}(eU_{PZC})$ (eV)'
set style textbox 1 transparent fc rgb 0xffff00 border lc "black" lw 5
set label 1 sprintf('\small{Volmer $R^2=%1.2f$}',VOLM_correlation**2) at 0.35,1.05 rotate by atan(3.6*f22/1.3)/pi*180-15 font subtitlefont textcolor 'black' front
set label 2 sprintf('\small{Heyrovsky $R^2=%1.2f$}',HEY_correlation**2) at 0.32,0.78 rotate by atan(3.6*g22/1.3)/pi*180+12 font subtitlefont textcolor lt 7 front
set label 3 sprintf('\small{Tafel $R^2=%1.2f$}',TAF_correlation**2) at 0.4,0.93 rotate by atan(3.6*h22/1.3)/pi*180-2 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.15,1.1 '\large{c)}' front
plot \
	"<paste ../PZCs.txt ../vac_HBEs.txt ../volmers.txt ../numbers.txt" using (-0.91*($1-4.44)+$2):3:4 w points lc 'black' ps 2 pt variable notitle, \
	"<paste ../PZCs.txt ../vac_HBEs.txt ../heyrovskys.txt ../numbers.txt" using (-0.91*($1-4.44)+$2):3:4 w points ps 2 pt variable lc 7 notitle, \
	"<paste ../PZCs.txt ../vac_HBEs.txt ../tafels.txt ../numbers.txt" using (-0.91*($1-4.44)+$2):3:4 w  points ps 2 pt variable lc 6 notitle, \
	f22 * x + f23 w l lw 5.0 lc 'black' dt 2 title sprintf("R^2=%1.2f",VOLM_correlation**2), \
	g22 * x + g23 w l lw 5.0 lc 7 dt 2 title sprintf("R^2=%1.2f",HEY_correlation**2), \
	h22 * x + h23 w l lw 5.0 lc 6 dt 2 title sprintf("R^2=%1.2f",TAF_correlation**2)
#### Htop
set xrange [-0.4:1.2]
set xtics -0.25,0.25,1
set ytics format ""
set xlabel '$\Delta G^{top}_{H}$ (eV)'
set ylabel ""
set label 1 sprintf('\small{Volmer $R^2=%1.2f$}',htopvol_correlation**2) at 0.525,1.05 rotate by atan(2*htopvol_slope/1.3)/pi*180.0-8 font subtitlefont textcolor 'black' front
set label 2 sprintf('\small{Heyrovsky $R^2=%1.2f$}',htophey_correlation**2) at 0.45,0.75 rotate by atan(2*htophey_slope/1.3)/pi*180.0+10 font subtitlefont textcolor lt 7 front
set label 3 sprintf('\small{Tafel $R^2=%1.2f$}',htoptaf_correlation**2) at -0.35,0.84 rotate by atan(2*htoptaf_slope/1.3)/pi*180.0-10 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.1,1.1 '\large{d)}' front
unset key
plot \
	'<paste ../vac_Htops.txt ../volmers.txt ../numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste ../vac_Htops.txt ../heyrovskys.txt ../numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste ../vac_Htops.txt ../tafels.txt ../numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	htopvol_slope * x + htopvol_intercept w l  lw 5.0 lc 'black' dt 2 title sprintf("R^2=%1.2f",htopvol_correlation**2), \
	htophey_slope * x + htophey_intercept w l  lw 5.0 lc 7 dt 2 title sprintf("R^2=%1.2f",htophey_correlation**2), \
	htoptaf_slope * x + htoptaf_intercept w l  lw 5.0 lc 6 dt 2 title sprintf("R^2=%1.2f",htoptaf_correlation**2)
unset multiplot
