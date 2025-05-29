set encoding utf8
ticsfont = "Helvetica,12"
titlefont = "Helvetica,22"
subtitlefont = "Helvetica,12"
set ylabel 'Free Energy $\Delta G$ (eV) Relative to Cu'
#set terminal svg enhanced size 1000,500
#set output "Figure_Coupling_Tafel.svg"
#set terminal svg enhanced font titlefont size 1000,500
set terminal epslatex color colortext size 4in,3in "cmss"
set output "Figure_Coupling_Tafel.tex"
load 'turbo.pal'
#set xtics font ticsfont offset 0,graph 0.025 nomirror
set xtics font ticsfont nomirror
set ytics font ticsfont nomirror
#set offset 1,1
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
stats "<paste couplings.txt tafels.txt" u 1:($2-1.033) prefix "couptaf"
stats "<paste couplings.txt HBEs.txt" u 1:($2-0.181) prefix "couphbe"
#set yrange [0.2:1.5]
#set multiplot layout 1,2 margins 0.05, 0.95, 0.25, 0.85 # title "Activation Energies at -1 V vs SHE" font titlefont
set title font subtitlefont
FILE = "numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
#set key at screen 0.8,screen 0.125 maxrows 2
set xrange[0.5:4.5]
set yrange[-0.5:0.5]
set xlabel "$|V_{ad}|^2$"
set label 1 sprintf('\tiny{Tafel Activation Energy, $R^2 = %1.2f$}',couptaf_correlation**2) at 1.5,0.2 rotate by 0 font subtitlefont textcolor lt 6 front
set label 2 sprintf('\tiny{Hydrogen Binding Energy, $R^2 = %1.2f$}',couphbe_correlation**2) at 1.5,0.1 rotate by 0 font subtitlefont textcolor lt 7 front
plot \
	'<paste couplings.txt tafels.txt numbers.txt' u 1:($2-1.033):3 w points ps 2 pt variable lc 6 notitle, \
	'<paste couplings.txt HBEs.txt numbers.txt' u 1:($2-0.181):3 w points ps 2 pt variable lc 7 notitle, \
	couptaf_slope * x + couptaf_intercept w l lw 7.5 lc 6 dt 2 notitle, \
	couphbe_slope * x + couphbe_intercept w l lw 7.5 lc 7 dt 2 notitle
#	for [idx=1:8] keyentry with points lc 'black' ps 2 pointtype numbers[idx] title elements[idx] 
unset multiplot
