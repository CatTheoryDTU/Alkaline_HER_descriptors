set encoding utf8
#ticsfont = "Helvetica,16"
#titlefont = "Helvetica,22"
#labelfont = "Helvetica,32"
#set title "pH = 13"
set xlabel "U vs RHE (V)"
#set ylabel "j mA/cm^2" #font labelfont
#set terminal svg enhanced font titlefont size 1000,500
#set output "Figure_Polarization_curves.svg"
set terminal epslatex color colortext size 4in,3in font "cmss" standalone
set output "Figure_Polarization_curves_standalone.tex"
#set lmargin at screen 0.0
#set rmargin at screen 1.0
#set bmargin at screen 0.0
#set tmargin at screen 1.0
set ylabel "j (mA/cm$^2$)" #font labelfont
set xrange [-1.4:0]
set yrange [-5:0.1]
set yzeroaxis
set xtics nomirror #font ticsfont nomirror #offset 0,graph 0.05 nomirror
set ytics nomirror #font ticsfont nomirror
set xtics -1.5,0.5,0
set ytics 0,-5,-10
#set ytics format ''
#set xtics format ''
pH=13*-0.059
#set key bottom left
set key textcolor variable
plot "<awk '$2==13.0' ../results/Ag/current.dat" using ($1-pH):3 w l lw 5.0 title 'Ag' at beginning, \
	"<awk '$2==13.0' ../results/Au/current.dat" using ($1-pH):3 w l lw 5.0 title 'Au' at beginning, \
	"<awk '$2==13.0' ../results/Cu/current.dat" using ($1-pH):3 w l lw 5.0 title 'Cu' at beginning, \
	"<awk '$2==13.0' ../results/Ir/current.dat" using ($1-pH):3 w l lw 5.0 title 'Ir' at beginning, \
	"<awk '$2==13.0' ../results/Ni/current.dat" using ($1-pH):3 w l lw 5.0 title 'Ni' at beginning, \
	"<awk '$2==13.0' ../results/Pd/current.dat" using ($1-pH):3 w l lw 5.0 title 'Pd' at beginning, \
	"<awk '$2==13.0' ../results/Pt/current.dat" using ($1-pH):3 w l lw 5.0 title 'Pt' at beginning, \
	"<awk '$2==13.0' ../results/Rh/current.dat" using ($1-pH):3 w l lw 5.0 title 'Rh' at beginning
