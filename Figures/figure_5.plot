#
#
#
set encoding utf8
set ylabel 'Descriptor Strength, $R^2$ '
set terminal epslatex color colortext size 6in,3in "cmss" standalone
set output "Figure_5.tex"
set xtics nomirror
set ytics nomirror
set ytics 0,0.25,0.75
set xtics -2,1,0
set offset 1,1
#set yrange [0:1.2]
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
set multiplot layout 1,3 margins 0.12, 0.95, 0.15, 0.90 # title "Activation Energies at -1 V vs SHE" font titlefont
set xrange[-2.1:0.1]
set yrange[-0.05:1.05]
set ytics format "%1.2f"
set xlabel 'U vs SHE (V)'
set label 1 '$U_{PZC}$' at -1.5, 0.75 textcolor 'dark-green' front
set label 2 '$\Delta G^{fcc}_H$' at -1,0.62 textcolor 'black' front
set label 3 at graph -0.15,1.05 'a)' front
#'$|V|^2$','$\Delta G^{fcc}_H-\Delta G^{top}_H$'
plot \
	"<paste fig5x.txt fig5a.txt" u 1:3 w l lc 'black' lw 3.0 notitle, \
	"<paste fig5x.txt fig5a.txt" u 1:2 w l lc 'dark-green' lw 3.0 notitle, \
	"<paste fig5x.txt fig5a.txt" u 1:5 w l lc 'dark-red' lw 3.0 dashtype '-.' notitle, \
	"<paste fig5x.txt fig5a.txt" u 1:4 w l lc 'blue' lw 3.0 notitle, \
	"<paste fig5x.txt fig5a.txt" u 1:6 w l lc 'purple' lw 3.0 notitle, \
	"<paste fig5x.txt fig5a.txt" u 1:7 w l lc 'dark-goldenrod' lw 3.0 dashtype '.' notitle
set ylabel ""
set ytics format ""
set label 1 '$\Delta G^{fcc}_H-0.52U_{PZC}$' at -1.9, 1.0 textcolor 'dark-red' front
set label 2 '$\Delta G^{top}_H$' at -1,0.83 textcolor 'blue' front
set label 3 at graph -0.15,1.05 'b)' front
plot \
	"<paste fig5x.txt fig5b.txt" u 1:3 w l lc 'black' lw 3.0 notitle, \
	"<paste fig5x.txt fig5b.txt" u 1:2 w l lc 'dark-green' lw 3.0 notitle, \
	"<paste fig5x.txt fig5b.txt" u 1:5 w l lc 'dark-red' lw 3.0 dashtype '-.' notitle, \
	"<paste fig5x.txt fig5b.txt" u 1:4 w l lc 'blue' lw 3.0 notitle, \
	"<paste fig5x.txt fig5b.txt" u 1:6 w l lc 'purple' lw 3.0 notitle, \
	"<paste fig5x.txt fig5b.txt" u 1:7 w l lc 'dark-goldenrod' lw 3.0 dashtype '.' notitle
set label 1 '$|V_{ad}|^2$' at -1, 0.88 textcolor 'purple' front
set label 2 '$\Delta G^{fcc}_H-\Delta G^{top}_H$' at -1.5,0.75 textcolor 'dark-goldenrod' front
set label 3 at graph -0.15,1.05 'c)' front
plot \
	"<paste fig5x.txt fig5c.txt" u 1:3 w l lc 'black' lw 3.0 notitle, \
	"<paste fig5x.txt fig5c.txt" u 1:2 w l lc 'dark-green' lw 3.0 notitle, \
	"<paste fig5x.txt fig5c.txt" u 1:5 w l lc 'dark-red' lw 3.0 dashtype '-.' notitle, \
	"<paste fig5x.txt fig5c.txt" u 1:4 w l lc 'blue' lw 3.0 notitle, \
	"<paste fig5x.txt fig5c.txt" u 1:6 w l lc 'purple' lw 3.0 notitle, \
	"<paste fig5x.txt fig5c.txt" u 1:7 w l lc 'dark-goldenrod' lw 3.0 dashtype '.' notitle
unset multiplot
