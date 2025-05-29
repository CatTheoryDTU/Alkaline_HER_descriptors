set encoding utf8
set terminal epslatex color size 6in,4in "cmss" standalone
set output "Reaction_Coordinates.tex"
set xtics -2,1,0 nomirror #offset 0,graph 0.05 nomirror
set ytics nomirror
#set format y ''
set offset 0.5,0.5
#set yrange [-1.0:1.0]
f(x)=a*(x-4.44)+b
set fit quiet
set fit logfile '/dev/null'
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
set multiplot layout 1,2 margins 0.15, 0.95, 0.25, 0.85 spacing 0.08 # title "Activation Energies"
set title 
set title "Volmer" #offset 0,graph -0.1
array coeffs_a[8]
array coeffs_b[8]
do for [i=1:8]{
	ele=elements[i]
	fit f(x) ele."_geometry_volmer.dat" u 1:2 via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
FILE = "../plots/numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
set xlabel "U vs SHE (V)" #offset 0,screen 0.075
set ylabel "TS Reaction Coordinate"
set key at screen 0.8,screen 0.125 maxrows 2
set xrange [-2.5:0.5]
plot for [i=1:8] elements[i]."_geometry_volmer.dat" u ($1-4.44):2 ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:8] coeffs_a[i]*x+coeffs_b[i] lc i lw 2 dt 2 notitle
unset xrange
set ylabel ""
#set xlabel "Potential, V "# offset 0,graph 0.12
set title "Heyrovsky"
array coeffs_a[8]
array coeffs_b[8]
do for [i=1:8]{
	ele=elements[i]
	fit f(x) ele."_geometry_heyrovsky.dat" u 1:2 via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
set xrange [-2.5:0.5]
plot for [i=1:8] elements[i]."_geometry_heyrovsky.dat" u ($1-4.44):2 ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:8] coeffs_a[i]*x+coeffs_b[i] lc i lw 2 dt 2 notitle
unset multiplot
