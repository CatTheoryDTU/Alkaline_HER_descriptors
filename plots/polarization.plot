set encoding utf8
ticsfont = "Helvetica,32"
titlefont = "Helvetica,48"
#set title "pH = 13 "
set xlabel "Potential vs RHE" font titlefont
set ylabel "j mA/cm^2" font titlefont
set terminal png enhanced font titlefont size 1200,900
load 'turbo.pal'
set xrange [:0]
set yrange [-7:0.75]
set yzeroaxis
set xtics font ticsfont nomirror offset 0,graph 0.05
set ytics font ticsfont nomirror
#set key top center vertical maxrows 2 font titlefont offset 0,-0.5
set output "Polarization_curves.png"
set label "pH = 13" at -1.0, 0.4 font ticsfont
pH=13*-0.059
set key textcolor variable font ticsfont
plot "<awk '$2==13.0' ../results/Ag/current.dat" using ($1-pH):3 w l lw 5 title 'Ag' at beginning, \
	"<awk '$2==13.0' ../results/Au/current.dat" using ($1-pH):3 w l lw 5 title 'Au   ' at beginning, \
	"<awk '$2==13.0' ../results/Cu/current.dat" using ($1-pH):3 w l lw 5 title 'Cu' at beginning, \
	"<awk '$2==13.0' ../results/Ir/current.dat" using ($1-pH):3 w l lw 5 title 'Ir' at beginning, \
	"<awk '$2==13.0' ../results/Ni/current.dat" using ($1-pH):3 w l lw 5 title 'Ni' at beginning, \
	"<awk '$2==13.0' ../results/Pd/current.dat" using ($1-pH):3 w l lw 5 title 'Pd' at beginning, \
	"<awk '$2==13.0' ../results/Pt/current.dat" using ($1-pH):3 w l lw 5 title 'Pt' at beginning, \
	"<awk '$2==13.0' ../results/Rh/current.dat" using ($1-pH):3 w l lw 5 title 'Rh' at beginning
