set encoding utf8
ticsfont = "Helvetica,12"
titlefont = "Helvetica,22"
subtitlefont = "Helvetica,18"
set terminal epslatex color colortext size 6in,4in "cmss" standalone
set output "FeW_Activation_Energies.tex"
#set terminal svg enhanced font titlefont size 1000,500
#set output "FeW_Activation_Energies.svg"
set xtics -2,1,0 font ticsfont nomirror #offset 0,graph 0.05 nomirror
set ytics font ticsfont nomirror
set offset 0.5,0.5
set yrange [0.0:2.0]
f(x)=a*(x-4.44)+b
set fit quiet
set fit logfile '/dev/null'
elements="Ag Au Cu Ir Ni Pd Pt Rh"
FILE = "numbers.txt"
array numbers[10]
stats FILE u (numbers[int($0+1)] = $1) 
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh","Fe","W"]
set multiplot layout 1,2 margins 0.15, 0.95, 0.25, 0.85 # title "Activation Energies"
set title font subtitlefont
set title "Volmer" #offset 0,graph -0.1
array coeffs_a[10]
array coeffs_b[10]
do for [i=1:10]{
	ele=elements[i]
	fit f(x) "../../data/volmer/".ele."/barriers.txt" u 1:2 via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
set xlabel "U vs SHE (V)" #offset 0,screen 0.075
set ylabel 'Free Energy $\Delta G$ (eV)'
set key at screen 0.8,screen 0.125 maxrows 2
set xrange [-2.5:0.5]
plot for [i=1:10] "../../data/volmer/".elements[i]."/barriers.txt" u ($1-4.44):2 ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:10] coeffs_a[i]*x+coeffs_b[i] lc i lw 2 dt 2 notitle
unset xrange
#set xlabel "Potential, V "# offset 0,graph 0.12
set ylabel ""
set title "Tafel"
array coeffs_a[10]
array coeffs_b[10]
do for [i=1:10]{
	fit f(x) "../../data/tafel/".elements[i]."/barriers.txt" u 1:2 via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
set xrange [-2.5:0.5]
plot for [i=1:10] "../../data/tafel/".elements[i]."/barriers.txt" u ($1-4.44):2 ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:10] coeffs_a[i]*x+coeffs_b[i] lc i lw 2 dt 2 notitle
unset xrange
unset multiplot
