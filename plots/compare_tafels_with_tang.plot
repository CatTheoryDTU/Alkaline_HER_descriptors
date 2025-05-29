set encoding utf8
set title "Comparison with Michael Tang 2020"
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set terminal png enhanced font titlefont size 600,600
#load 'turbo.pal'
set xtics font ticsfont
set ytics font ticsfont
set output "Compare_MichaelTang2020.png"
set offset 1,1
set xlabel "Coupling elements"
set ylabel "Tafel Activation Energy, eV"
set xrange [0.5:5]
set yrange [0.5:1.2]
stats "<(paste tang_couplings.txt tang_hbes.txt tang_tafels.txt )" u 1:($3-2*$2) prefix "tang"
plot "<(paste tang_couplings.txt tang_hbes.txt tang_tafels.txt tang_metals.txt )" u 1:($3-2*$2):(sprintf("%s",stringcolumn(4))) w labels point pt 7 ps 2 offset char 1,1 title "Tang Data", \
	tang_slope*x+tang_intercept w l lc 'black' dt 2 title sprintf("Coupling Fit, r^2 = %1.2f",tang_correlation**2)
