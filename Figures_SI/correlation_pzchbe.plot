set encoding utf8
set xlabel "PZC vs SHE, V"
set ylabel "Hydrogen Binding Energy, eV"
set terminal svg enhanced size 600,400
set xtics nomirror
set ytics nomirror
set output "pzc_vs_hbe.svg"
stats "<paste PZCs.txt vac_HBEs.txt" using ($1-4.44):2 prefix "HPZC"
set xrange [-1:1]
set yrange [-1:1]
set label 1 at 0.,0.2 sprintf("R^{2} = %1.2f",HPZC_correlation**2) rotate by -15 center 
plot \
	"<paste PZCs.txt vac_HBEs.txt metals.txt" using ($1-4.44):2:(sprintf("%s",stringcolumn(3))) every 2::0 w labels point pt 7 offset char -1,0.5 notitle, \
	"<paste PZCs.txt vac_HBEs.txt metals.txt" using ($1-4.44):2:(sprintf("%s",stringcolumn(3))) every 2::1 w labels point pt 7 offset char 0.5,-1 notitle, \
	HPZC_slope * x + HPZC_intercept lc 'black' dt 2 notitle
	
	
	
