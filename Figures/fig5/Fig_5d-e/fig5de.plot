set encoding utf8
set xtics nomirror #offset 0,graph 0.025 nomirror
set ytics nomirror
set terminal epslatex color size 6in,3in "cmss,10" standalone
set output "Figure_5de.tex"
set print '/dev/null'
set multiplot layout 1,2 margins 0.125, 0.875, 0.20, 0.85 spacing 0.05,0.15 # title "Activation Energies at -1 V vs SHE" font titlefont
f2(x,y)=f22*x+f21*y+f23
g2(x,y)=g22*x+g21*y+g23
h2(x,y)=h22*x+h21*y+h23
#set arrow from first 5.5, graph 0 to first 5.5, graph 1 nohead
set pm3d map interpolate 1,1 noborder
#unset surface; 
load '../../turbo.pal'
set pm3d at b;
set view map
set cbrange [0.4:1.5]
set cbtics out nomirror
set cbtics format "%1.1f" #font ticsfont
set cblabel '$\Delta G^\ddagger$ (eV)' #offset graph 0,0.25
# PZC
set xlabel '$\Delta G_H^{fcc}$-0.91e$U_{PZC}$ (eV)'
set ylabel '$\Delta G^{top}_H-\Delta G^{fcc}_H$ (eV)'
set xrange [-0.9:1.4]
set xtics -1.0,.5,1.0
set yrange [-0.3:0.85]
#set yrange [-10:2]
set label 2 at graph -0.15,1.1 '\large{d)}' front
fit f2(x,y) "<paste ../../PZCs.txt data.new" u ($2-0.91*($1-4.44)):($3-$2):4 via f21,f22,f23
fit g2(x,y) "<paste ../../PZCs.txt data.new" u ($2-0.91*($1-4.44)):($3-$2):5 via g21,g22,g23
fit h2(x,y) "<paste ../../PZCs.txt data.new" u ($2-0.91*($1-4.44)):($3-$2):6 via h21,h22,h23
#set arrow 1 from -0.9,(-0.9*(h22-f22)+(h23-f23))/(f21-h21) to 1.3,(1.3*(h22-f22)+(h23-f23))/(f21-h21) front
#set arrow 2 from -0.9,(-0.9*(g22-f22)+(g23-f23))/(f21-g21) to 1.3,(1.3*(g22-f22)+(g23-f23))/(f21-g21) front
#set arrow 3 from -0.9,(-0.9*(g22-h22)+(g23-h23))/(h21-g21) to 1.3,(1.3*(g22-h22)+(g23-h23))/(h21-g21) front
unset colorbox
splot  \
	"heat_1.txt" using 1:2:3 with pm3d notitle, \
	"points_1.txt" using 1:2:(0.):(0.15) with circles linecolor 'black' notitle, \
	"points_1.txt" using 1:2:(0.):(sprintf("%s",stringcolumn(3))) with labels notitle
unset ylabel
#
set xlabel '$\Delta G^{top}_H$ (eV)'# offset 0,screen 0.05
set format y ''
set xrange [-0.28:1.3]
set xtics 0.0,.5,1.0
set label 2 at graph -0.15,1.1 '\large{e)}' front
set colorbox
nf2(x,y)=nf22*x+nf21*y+nf23
ng2(x,y)=ng22*x+ng21*y+ng23
nh2(x,y)=nh22*x+nh21*y+nh23
fit nf2(x,y) "data.new" u 2:($2-$1):3 via nf21,nf22,nf23
fit ng2(x,y) "data.new" u 2:($2-$1):4 via ng21,ng22,ng23
fit nh2(x,y) "data.new" u 2:($2-$1):5 via nh21,nh22,nh23
set arrow 1 from -0.28,(-0.28*(nh22-nf22)+(nh23-nf23))/(nf21-nh21) to .57,(.57*(nh22-nf22)+(nh23-nf23))/(nf21-nh21) front nohead dt 2 lc 'black' #Volmer-Tafel
set arrow 2 from 0.575,(0.575*(ng22-nf22)+(ng23-nf23))/(nf21-ng21) to 0.72,(0.72*(ng22-nf22)+(ng23-nf23))/(nf21-ng21) front nohead dt 2 lc 'black' #Volmer Heyrovsky
set arrow 3 from 0.475,(0.475*(ng22-nh22)+(ng23-nh23))/(nh21-ng21) to .575,(.575*(ng22-nh22)+(ng23-nh23))/(nh21-ng21) front nohead dt 2 lc 'black' #Heyrovsky-Tafel
#set label 3 at graph 0.4,0.2 '\large{Volmer-Limited}' front
#set label 4 at graph 0.02,0.87 '\large{Tafel-Limited}' front
#set label 5 at graph 0.52,0.92 '\large{H}' front
splot  \
	"heat_0.txt" using 1:2:3 with pm3d notitle, \
	"points_0.txt" using 1:2:(0.):(0.1) with circles linecolor 'black' notitle, \
	"points_0.txt" using 1:2:(0.):(sprintf("%s",stringcolumn(3))) with labels notitle
unset multiplot
