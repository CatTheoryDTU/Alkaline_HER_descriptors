set encoding utf8
ticsfont = "Helvetica,10"
titlefont = "Helvetica,14"
set xlabel "PZC vs SHE, V"
set ylabel "Hydrogen Binding Energy, eV"
set cblabel "log10 TOF at pH=14, SHE=-1.03"
set terminal png enhanced font titlefont size 500,500
load 'turbo.pal'
set xtics font ticsfont
set ytics font ticsfont
set output "2D_Descriptorplot.png"
set offset 1,1
set key center top
f(x,y)=a*(x-4.4)+b*y+c
g(x)=d*(x-4.4)+e
fit f(x,y) "<paste PZCs.txt HBEs.txt pH14RHE-0.2_activity.txt" u ($1-4.44):2:(log10($3)) via a,b,c
stats "<paste PZCs.txt HBEs.txt" using ($1-4.44):2 prefix "HPZC"
fit g(x) "<paste PZCs.txt HBEs.txt " u ($1-4.44):2 via d,e
set xrange [-1:1]
set yrange [-1:1]
set cbrange [-10:10]
set pm3d map
splot \
	f(x,y) with pm3d notitle, \
	"<paste PZCs.txt HBEs.txt pH14RHE-0.2_activity.txt metals.txt" using ($1-4.44):2:(log10($3)) w points ls 3 ps 7 notitle, \
	"<paste PZCs.txt HBEs.txt pH14RHE-0.2_activity.txt metals.txt" using ($1-4.44):2:(log10($3)):(sprintf("%s",stringcolumn(4))) w labels offset char 1,1 notitle
	#"" u ($1-4.44):(g($1-4.44)):(f($1-4.44,$2)) w l dt 1 lc palette title sprintf("r^2 = %1.2f",HPZC_correlation**2)
#	HPZC_slope * x + HPZC_intercept lc 'black' dt 2 
