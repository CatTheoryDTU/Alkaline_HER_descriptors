set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,13"
set title "pH = 13 "
set xlabel "Potential vs RHE"
set ylabel "Coverage"
set terminal png enhanced font titlefont size 1000,1000
load 'turbo.pal'
#set xrange [:0]
#set yrange [1e-9:1]
set yzeroaxis
set xtics font ticsfont
set ytics font ticsfont
set output "pH13_coverage.png"
pH=13*-0.059

plot "<awk '$2==13.0' ../results/Ag/coverage.dat" using ($1-pH):3 w l title 'Ag', \
	"<awk '$2==13.0' ../results/Au/coverage.dat" using ($1-pH):3 w l title 'Au', \
	"<awk '$2==13.0' ../results/Cu/coverage.dat" using ($1-pH):3 w l title 'Cu', \
	"<awk '$2==13.0' ../results/Ir/coverage.dat" using ($1-pH):3 w l title 'Ir', \
	"<awk '$2==13.0' ../results/Ni/coverage.dat" using ($1-pH):3 w l title 'Ni', \
	"<awk '$2==13.0' ../results/Pd/coverage.dat" using ($1-pH):3 w l title 'Pd', \
	"<awk '$2==13.0' ../results/Pt/coverage.dat" using ($1-pH):3 w l title 'Pt', \
	"<awk '$2==13.0' ../results/Rh/coverage.dat" using ($1-pH):3 w l title 'Rh'
