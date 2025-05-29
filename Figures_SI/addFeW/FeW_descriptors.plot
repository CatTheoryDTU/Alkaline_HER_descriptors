set encoding utf8
ticsfont = "cmss,12"
titlefont = "cmss,22"
subtitlefont = "cmss,8"
set xlabel '$\Delta G^{fcc}_{H}$ (eV)'
set ylabel 'Activation Free Energy $\Delta G^\ddag$ (eV)'
#set terminal svg enhanced size 1000,500
#set output "NewVolcano.svg"
#set terminal svg enhanced font titlefont size 1500,500
set terminal epslatex color colortext size 6in,6in standalone font 'cmss' #header '\newcommand{\hl}[1]{\setlength{\fboxsep}{0.75pt}\colorbox{white}{#1}}'
set output "FeW_Descriptors.tex"

set xtics font ticsfont nomirror
set ytics font ticsfont nomirror
set offset 1,1
#set fit quiet
set fit logfile 'FeW_Descriptors.log'
set print '/dev/null'
stats "<paste Hdiff.txt volmers.txt" u 1:2 prefix "hdiffvol"
stats "<paste Hdiff.txt tafels.txt" u 1:2 prefix "hdifftaf"
stats "<paste couplings.txt volmers.txt" u 1:2 prefix "coupvol"
stats "<paste couplings.txt tafels.txt" u 1:2 prefix "couptaf"
stats "<paste vac_Htops.txt volmers.txt" u 1:2 prefix "htopvol"
stats "<paste vac_Htops.txt tafels.txt" u 1:2 prefix "htoptaf"
f2(x,y)=f22*(-0.52*(x-4.4)+y)+f23
h2(x,y)=h22*(-0.52*(x-4.4)+y)+h23
fit f2(x,y) "<paste PZCs.txt vac_HBEs.txt volmers.txt" u 1:2:3 via f22,f23
fit h2(x,y) "<paste PZCs.txt vac_HBEs.txt tafels.txt" u 1:2:3 via h22,h23
stats "<paste PZCs.txt vac_HBEs.txt volmers.txt" using (f2($1,$2)):3 prefix "VOLM"
stats "<paste PZCs.txt vac_HBEs.txt tafels.txt" using (h2($1,$2)):3 prefix "TAF"
set yrange [0.2:1.6]
set multiplot layout 2,2 margins 0.15, 0.95, 0.15, 0.95 spacing 0.05,0.1 # title "Activation Energies at -1 V vs SHE" font titlefont
set key at screen 0.85,screen 0.05 maxrows 2
set title font subtitlefont 
set label 4 at graph -0.15,1.1 'a)' front
FILE = "numbers.txt"
array numbers[10]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh","Fe","W"]
#### Htop
set xrange [-0.6:1.2]
set xtics -0.5,0.5,1.0
set xlabel '$\Delta G^{top}_{H}$ (eV)'
set ylabel 'Activation Free Energy $\Delta G^\ddag$ (eV)'
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',htopvol_correlation**2) at 0.18,0.68 rotate by atan(2*htopvol_slope/1.3)/pi*180.0-5 font subtitlefont textcolor 'black' front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',htoptaf_correlation**2) at 0.25,0.86 rotate by atan(2*htoptaf_slope/1.3)/pi*180.0 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.1,1.1 'a)' front
plot \
	'<paste vac_Htops.txt volmers.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste vac_Htops.txt tafels.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	htopvol_slope * x + htopvol_intercept w l  lw 5.0 lc 'black' dt 2 notitle,\
	htoptaf_slope * x + htoptaf_intercept w l  lw 5.0 lc 6 dt 2 notitle, \
	for [idx=1:10] keyentry with points lc 'black' ps 2 pointtype numbers[idx] title elements[idx] 
unset key
#### V2
set xrange [0.5:8]
set xtics 1,2,7
set ytics format ""
set ylabel ""
set xlabel '$|V|^2$'
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',coupvol_correlation**2) at 0.18,0.68 rotate by atan(2*coupvol_slope/1.3)/pi*180.0-5 font subtitlefont textcolor 'black' front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',couptaf_correlation**2) at 0.25,0.86 rotate by atan(2*couptaf_slope/1.3)/pi*180.0 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.1,1.1 'b)' front
unset key
plot \
	'<paste couplings.txt volmers.txt numbers.txt' u 1:2:3 w points lc 'black' ps 2 pt variable notitle, \
	'<paste couplings.txt tafels.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	coupvol_slope * x + coupvol_intercept w l  lw 5.0 lc 'black' dt 2 title sprintf("R^2 = %1.2f",coupvol_correlation**2), \
	couptaf_slope * x + couptaf_intercept w l  lw 5.0 lc 6 dt 2 title sprintf("R^2 = %1.2f",couptaf_correlation**2)
#### HBE+PZC
set xrange[-0.8:1.3]
set ytics format "%1.1f"
set ylabel 'Activation Free Energy $\Delta G^\ddag$ (eV)'
set xtics -0.5,0.5,1.0
set xlabel '$\Delta G^{fcc}_{H} -0.52{a}(U_{PZC})$'
set style textbox 1 transparent fc rgb 0xffff00 border lc "black" lw 5
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',VOLM_correlation**2) at -0.5,0.26 rotate by atan(3.6*f22/1.3)/pi*180+8 font subtitlefont textcolor 'black' front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',TAF_correlation**2) at 0.4,0.93 rotate by atan(3.6*h22/1.3)/pi*180-2 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.15,1.1 'c)' front
plot \
	"<paste PZCs.txt vac_HBEs.txt volmers.txt numbers.txt" using (-0.52*($1-4.44)+$2):3:4 w points lc 'black' ps 2 pt variable notitle, \
	"<paste PZCs.txt vac_HBEs.txt tafels.txt numbers.txt" using (-0.52*($1-4.44)+$2):3:4 w  points ps 2 pt variable lc 6 notitle, \
	f22 * x + f23 w l lw 5.0 lc 'black' dt 2 title sprintf("R^2 = %1.2f",VOLM_correlation**2), \
	h22 * x + h23 w l lw 5.0 lc 6 dt 2 title sprintf("R^2 = %1.2f",TAF_correlation**2)
# Hdiff
set ytics format ""
set ylabel ""
set xrange[-0.7:0.7]
set xtics -0.5,0.5,1.0
set xlabel '$\Delta G^{top}_{H} - \Delta G^{fcc}_{H}$'
set label 1 sprintf('\tiny{Volmer, $R^2 = %1.2f$}',hdiffvol_correlation**2) at 0.18,0.98 rotate by 28.9 font subtitlefont textcolor 'black' front
set label 3 sprintf('\tiny{Tafel, $R^2 = %1.2f$}',hdifftaf_correlation**2) at 0.25,0.92 rotate by 5.3 font subtitlefont textcolor lt 6 front
set label 4 at graph -0.15,1.1 'd)' front
plot \
	'<paste Hdiff.txt volmers.txt numbers.txt' u 1:2:3 with points lc 'black' pointtype variable ps 2 notitle, \
	'<paste Hdiff.txt tafels.txt numbers.txt' u 1:2:3 w points ps 2 pt variable lc 6 notitle, \
	hdiffvol_slope * x + hdiffvol_intercept w l  lw 5.0 lc 'black' dt 2 notitle, \
	hdifftaf_slope * x + hdifftaf_intercept w l  lw 5.0 lc 6 dt 2 notitle
unset multiplot
