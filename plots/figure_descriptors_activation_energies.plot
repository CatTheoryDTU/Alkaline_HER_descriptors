set encoding utf8
ticsfont = "Helvetica,12"
titlefont = "Helvetica,22"
subtitlefont = "Helvetica,8"
set xlabel '$\Delta G_H$ (eV)'
set ylabel 'Activation Free Energy $\Delta G^\ddag$ (eV)'
#set terminal svg enhanced size 1000,500
#set output "Descriptors_Activation_Energies.svg"
#set terminal svg enhanced font titlefont size 1500,500
set terminal epslatex color colortext size 6in,4in "cmss" #header '\newcommand{\hl}[1]{\setlength{\fboxsep}{0.75pt}\colorbox{white}{#1}}'
set output "Descriptors_Activation_Energies.tex"
load 'turbo.pal'

set xtics font ticsfont nomirror
set ytics font ticsfont nomirror
set offset 1,1
#set fit quiet
#set fit logfile '/dev/null'
#set print '/dev/null'
stats "<paste HBEs.txt volmers.txt" u 1:2 prefix "hbevol"
stats "<paste HBEs.txt heyrovskys.txt" u 1:2 prefix "hbehey"
stats "<paste HBEs.txt tafels.txt" u 1:2 prefix "hbetaf"
stats "<paste PZCs.txt volmers.txt" u ($1-4.44):2 prefix "pzcvol"
stats "<paste PZCs.txt heyrovskys.txt" u ($1-4.44):2 prefix "pzchey"
stats "<paste PZCs.txt tafels.txt" u ($1-4.44):2 prefix "pzctaf"
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
set xrange [-0.35:0.65]
set xtics -0.25,0.25,0.5
set yrange [0.2:1.5]
set multiplot layout 1,3 margins 0.05, 0.95, 0.25, 0.85 # title "Activation Energies at -1 V vs SHE" font titlefont
set key at screen 0.8,screen 0.125 maxrows 2
set title font subtitlefont 
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',hbevol_correlation**2) at 0.18,0.98 rotate by 28.9 font subtitlefont textcolor 'black' front
set label 2 sprintf('\tiny{Heyrovsky, $R^2 = %1.2f$}',hbehey_correlation**2) at 0.25,0.75 rotate by -46.5 font subtitlefont textcolor lt 7 front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',hbetaf_correlation**2) at 0.25,0.92 rotate by 5.3 font subtitlefont textcolor lt 6 front
FILE = "numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
plot \
	'<paste HBEs.txt volmers.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste HBEs.txt heyrovskys.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste HBEs.txt tafels.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	hbevol_slope * x + hbevol_intercept w l  lw 5.0 lc 'black' dt 2 notitle, \
	hbehey_slope * x + hbehey_intercept w l  lw 5.0 lc 7 dt 2 notitle, \
	hbetaf_slope * x + hbetaf_intercept w l  lw 5.0 lc 6 dt 2 notitle, \
	for [idx=1:8] keyentry with points lc 'black' ps 2 pointtype numbers[idx] title elements[idx] 
#### PZC
set xrange [-1:1]
set xtics -1,0.5,1
set ytics format ""
set xlabel '$U_{PZC}$ vs SHE (V)'
set ylabel ""
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',pzcvol_correlation**2) at 0.18,0.68 rotate by atan(2*pzcvol_slope/1.3)/pi*180.0-5 font subtitlefont textcolor 'black' front
set label 2 sprintf('\tiny{Heyrovsky, $R^2 = %1.2f$}',pzchey_correlation**2) at 0.1,1.08 rotate by atan(2*pzchey_slope/1.3)/pi*180.0+5 font subtitlefont textcolor lt 7 front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',pzctaf_correlation**2) at 0.25,0.86 rotate by atan(2*pzctaf_slope/1.3)/pi*180.0 font subtitlefont textcolor lt 6 front
unset key
plot \
	'<paste PZCs.txt volmers.txt numbers.txt' u ($1-4.44):2:3 w points lc 'black' ps 2 pt variable notitle, \
	'<paste PZCs.txt heyrovskys.txt numbers.txt' u ($1-4.44):2:3 w points ps 2 pt variable lc 7 notitle, \
	'<paste PZCs.txt tafels.txt numbers.txt' u ($1-4.44):2:3 w points ps 2 pt variable lc 6 notitle, \
	pzcvol_slope * x + pzcvol_intercept w l  lw 5.0 lc 'black' dt 2 title sprintf("R^2 = %1.2f",pzcvol_correlation**2), \
	pzchey_slope * x + pzchey_intercept w l  lw 5.0 lc 7 dt 2 title sprintf("R^2 = %1.2f",pzchey_correlation**2), \
	pzctaf_slope * x + pzctaf_intercept w l  lw 5.0 lc 6 dt 2 title sprintf("R^2 = %1.2f",pzctaf_correlation**2)
#### HBE+PZC
set xrange[-1.8:1.8]
set ytics format ""
set xtics -1.5,1,1.5
set xlabel '$\Delta G_H +\frac{b}{a}(U_{PZC})$'
set ylabel ""
#set key bottom right 
#set key spacing 2.5
#set key top left 
set style textbox 1 transparent fc rgb 0xffff00 border lc "black" lw 5
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',VOLM_correlation**2) at -1.5,0.26 rotate by atan(3.6*f22/1.3)/pi*180+8 font subtitlefont textcolor 'black' front
set label 2 sprintf('\tiny{Heyrovsky, $R^2 = %1.2f$}',HEY_correlation**2) at -0.9,1.48 rotate by atan(3.6*g22/1.3)/pi*180-9 font subtitlefont textcolor lt 7 front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',TAF_correlation**2) at -1.6,0.93 rotate by atan(3.6*h22/1.3)/pi*180-2 font subtitlefont textcolor lt 6 front
plot \
	"<paste PZCs.txt HBEs.txt volmers.txt numbers.txt" using (f21*($1-4.44)/f22+$2):3:4 w points lc 'black' ps 2 pt variable notitle, \
	"<paste PZCs.txt HBEs.txt heyrovskys.txt numbers.txt" using (g21*($1-4.44)/g22+$2):3:4 w points ps 2 pt variable lc 7 notitle, \
	"<paste PZCs.txt HBEs.txt tafels.txt numbers.txt" using (h21*($1-4.44)/h22+$2):3:4 w  points ps 2 pt variable lc 6 notitle, \
	f22 * x + f23 w l lw 5.0 lc 'black' dt 2 title sprintf("R^2 = %1.2f",VOLM_correlation**2), \
	g22 * x + g23 w l lw 5.0 lc 7 dt 2 title sprintf("R^2 = %1.2f",HEY_correlation**2), \
	h22 * x + h23 w l lw 5.0 lc 6 dt 2 title sprintf("R^2 = %1.2f",TAF_correlation**2)
unset multiplot
