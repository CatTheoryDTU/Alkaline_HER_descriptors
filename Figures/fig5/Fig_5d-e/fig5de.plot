set encoding utf8
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set terminal epslatex color size 6in,3in "cmss,10" standalone
set output "Figure_5de.tex"
set print '/dev/null'
set multiplot layout 1,2 margins 0.125, 0.875, 0.20, 0.85 spacing 0.05,0.15 # title "Activation Energies at -1 V vs SHE" font titlefont
set pm3d map interpolate 2,2 noborder
#unset surface; 
load '../../turbo.pal'
set pm3d at b;
set view map
set cbrange [0.4:1.5]
set cbtics out nomirror
set cbtics format "%1.1f" #font ticsfont
set cblabel '$\Delta G^\ddagger$ (eV)' #offset graph 0,0.25
#
set xlabel '$\Delta G^{top}_H$ (eV)'# offset 0,screen 0.05
set ylabel '$\Delta G^{top}_H-\Delta G^{fcc}_H$ (eV)'
set xrange [-0.28:1.3]
set yrange [-0.3:0.85]
#set yrange [-10:2]
set xtics 0.0,.5,1.0
set label 2 at graph -0.15,1.1 '\large{d)}' front
unset colorbox
splot  \
	"heat_0.txt" using 1:2:3 with pm3d notitle, \
	"points_0.txt" using 1:2:(0.):(0.1) with circles linecolor 'black' notitle, \
	"points_0.txt" using 1:2:(0.):(sprintf("%s",stringcolumn(3))) with labels notitle
unset ylabel
set format y ''
# PZC
set xlabel '$\Delta G_H^{fcc}$-0.91e$U_{PZC}$ (eV)'
set xrange [-1.2:1.2]
set xtics -1.0,.5,1.0
set label 2 at graph -0.15,1.1 '\large{e)}' front
set colorbox
splot  \
	"heat_1.txt" using 1:2:3 with pm3d notitle, \
	"points_1.txt" using 1:2:(0.):(0.15) with circles linecolor 'black' notitle, \
	"points_1.txt" using 1:2:(0.):(sprintf("%s",stringcolumn(3))) with labels notitle
unset multiplot
