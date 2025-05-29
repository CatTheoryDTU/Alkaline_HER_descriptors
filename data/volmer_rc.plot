set encoding iso_8859_1
set termoption enhanced
set xlabel "Potential vs SHE, V" font "Times-Roman,22"
set ylabel "dH-M - dH-O" font "Times-Roman,22"
set title "Volmer Reaction Coordinate" font "Times-Roman,22"
set key top left font "Times-Roman,22"
set xtics font "Times-Roman,14"
set ytics font "Times-Roman,14"
set xzeroaxis
#set xrange [2:5]
#set yrange [-5:1]
#set terminal png size 800,800
set terminal svg enhanced size 800,400
#set terminal pngcairo  transparent enhanced fontscale 1.0 size 600, 400 
set output "volmer_rc.svg"
SHE=4.44
#set fit nologfile brief errorvariables nocovariancevariables errorscaling prescale nowrap v5
f(x) = a*x + b
g(x) = c*x + d
h(x) = p*x + q
i(x) = r*x + s
j(x) = t*x + u
k(x) = k1*x + k2
l(x) = l1*x + l2
m(x) = m1*x + m2
fe(x)= fe1*x + fe2
w(x)= w1*x + w2
fit f(x) "Au_geometry_volmer.dat" u ($1-SHE):2 via a,b
fit g(x) "Cu_geometry_volmer.dat" u ($1-SHE):2 via c,d
fit h(x) "Pt_geometry_volmer.dat" u ($1-SHE):2 via p,q
fit i(x) "Ni_geometry_volmer.dat" u ($1-SHE):2 via r,s
fit j(x) "Ag_geometry_volmer.dat" u ($1-SHE):2 via t,u
fit k(x) "Ir_geometry_volmer.dat" u ($1-SHE):2 via k1,k2
fit l(x) "Pd_geometry_volmer.dat" u ($1-SHE):2 via l1,l2
fit m(x) "Rh_geometry_volmer.dat" u ($1-SHE):2 via m1,m2
plot \
	"Au_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Au", \
	"Cu_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Cu", \
	"Pt_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Pt", \
	"Ni_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Ni", \
	"Ag_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Ag", \
	"Ir_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Ir", \
	"Pd_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Pd", \
	"Rh_geometry_volmer.dat" u ($1-SHE):2 w p ps 2 title "Rh", \
	f(x) w l dt '..' lc 1 notitle, \
	g(x) w l dt '..' lc 2 notitle, \
	h(x) w l dt '..' lc 3 notitle, \
	i(x) w l dt '..' lc 4 notitle, \
	j(x) w l dt '..' lc 5 notitle, \
	k(x) w l dt '..' lc 6 notitle, \
	l(x) w l dt '..' lc 7 notitle, \
	m(x) w l dt '..' lc 8 notitle
