set encoding utf8
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set terminal epslatex color colortext size 6in,6in "cmss,10" standalone
set output "Volcano_Figure5.tex"
set print '/dev/null'
set multiplot layout 2,2 margins 0.125, 0.85, 0.10, 0.925# spacing 0.0,0.15 
set pm3d map interpolate 1,1 noborder
#unset surface; 
set pm3d at b;
set view map
set cbrange [1e-9:1e2]
set cbtics out nomirror
set logscale cb 
set cbtics format '$10^\mathrm{%T}$' #font ticsfont
set cblabel 'i @ -1 V vs SHE' #offset graph 0,0.25
#
#set xlabel '$\Delta G^{fcc}_H-0.91U_{PZC}$ (eV)'# offset 0,screen 0.05
set ylabel '$\Delta G^{top}_H-\Delta G^{fcc}_H$ (eV)'# offset 0,screen 0.05
set xrange [-0.9:1.3]
set yrange [-0.3:0.8]
set ytics -0.2,.2,1.0
set xtics -0.5,.5,1.0
set xtics format ''
load '../turbo.pal'
unset colorbox
#set label 3 at graph 0.4,0.2 '\large{Volmer-Limited}' front
#set label 4 at graph 0.02,0.87 '\large{Tafel-Limited}' front
#set label 5 at graph 0.52,0.92 '\large{H}' front
set label 1 at graph 0.05,0.95 '\large{a)}' textcolor rgb "white" front
set style line 2 linecolor "white"
splot  \
	"volcano_hbepzc.txt" using 1:2:(-1*$3) with pm3d notitle, \
	"<(paste ../combined_descriptor.txt ../Hdiff.txt)" using 1:2:(0.1):(0.125) with circles linecolor 'black' notitle, \
	"<(paste ../combined_descriptor.txt ../Hdiff.txt| sed -n '4p;7p;' )" using 1:2:(0.1):(0.125):(2) with circles linecolor variable notitle, \
	"<(paste ../combined_descriptor.txt ../Hdiff.txt ../metals.txt)" using 1:2:(0.1):(sprintf("%s",stringcolumn(3))) with labels notitle, \
	"<(paste ../combined_descriptor.txt ../Hdiff.txt ../metals.txt | sed -n '4p;7p;')" using 1:2:(0.1):(sprintf("%s",stringcolumn(3))) with labels textcolor rgb "white" notitle
set label 1 at graph 0.05,0.95 '\large{b)}' textcolor rgb "white" front
set colorbox
#set xlabel '$\Delta G^{top}_H$ (eV)'# offset 0,screen 0.05
set xrange [-0.28:1.3]
set ytics format ''
unset ylabel
set xtics 0.0,.5,1.0
splot  \
	"volcano_htop.txt" using 1:2:(-1*$3) with pm3d notitle, \
	"<(paste ../vac_Htops.txt ../Hdiff.txt)" using 1:2:(0.1):(0.09) with circles linecolor 'black' notitle, \
	"<(paste ../vac_Htops.txt ../Hdiff.txt| sed -n '4p;7p;' )" using 1:2:(0.1):(0.09):(2) with circles linecolor variable notitle, \
	"<(paste ../vac_Htops.txt ../Hdiff.txt ../metals.txt)" using 1:2:(0.1):(sprintf("%s",stringcolumn(3))) with labels notitle, \
	"<(paste ../vac_Htops.txt ../Hdiff.txt ../metals.txt | sed -n '4p;7p;')" using 1:2:(0.1):(sprintf("%s",stringcolumn(3))) with labels textcolor rgb "white" notitle
set label 1 at graph 0.05,0.95 '\large{c)}' textcolor rgb "white" front
load '../bentcoolwarm.pal'
unset colorbox
set xlabel '$\Delta G^{fcc}_H-0.91U_{PZC}$ (eV)'# offset 0,screen 0.05
set ylabel '$\Delta G^{top}_H-\Delta G^{fcc}_H$ (eV)'# offset 0,screen 0.05
set xrange [-0.9:1.3]
set yrange [-0.3:0.8]
set ytics -0.2,.2,1.0
set ytics format '%1.1f'
set xtics format '%1.1f'
set xtics -0.5,.5,1.0
unset logscale cb 
set cbrange [0:1]
splot  \
	"drc_hbepzc.txt" using 1:2:3 with pm3d notitle, \
	"<(paste ../combined_descriptor.txt ../Hdiff.txt)" using 1:2:(0.1):(0.125) with circles linecolor 'black' notitle, \
	"<(paste ../combined_descriptor.txt ../Hdiff.txt ../metals.txt)" using 1:2:(0.1):(sprintf("%s",stringcolumn(3))) with labels notitle
set label 1 at graph 0.05,0.95 '\large{d)}' textcolor rgb "white" front
set cbtics out nomirror
set cbtics format '%1.1f' #font ticsfont
set cblabel 'Volmer Degree of Rate Control' offset graph 0.075,0
set xrange [-0.28:1.3]
set xlabel '$\Delta G^{top}_H$ (eV)'# offset 0,screen 0.05
set colorbox
set ytics format ''
unset ylabel
splot  \
	"drc_htop.txt" using 1:2:3 with pm3d notitle, \
	"<(paste ../vac_Htops.txt ../Hdiff.txt)" using 1:2:(0.1):(0.09) with circles linecolor 'black' notitle, \
	"<(paste ../vac_Htops.txt ../Hdiff.txt ../metals.txt)" using 1:2:(0.08):(sprintf("%s",stringcolumn(3))) with labels notitle
unset multiplot
