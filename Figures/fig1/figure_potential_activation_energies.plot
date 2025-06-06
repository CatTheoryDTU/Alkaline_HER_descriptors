set encoding utf8
set terminal epslatex color colortext size 3in,8in "cmss, 10" standalone
set output "All_Activation_Energies.tex"
set xtics -2,1,0 nomirror #offset 0,graph 0.05 nomirror
set ytics nomirror
set offset 0.5,0.5
set yrange [0.0:2.0]
f(x)=a*(x-0)+b
set fit quiet
set fit logfile '/dev/null'
elements="Ag Au Cu Ir Ni Pd Pt Rh"
FILE = "numbers.txt"
array numbers[8]
stats FILE u (numbers[int($0+1)] = $1)
array elements = ["Ag","Au","Cu","Ir","Ni","Pd","Pt","Rh"]
set multiplot layout 4,1 margins 0.20, 0.95, 0.125, 0.975 spacing 0.0,0.05 # title "Activation Energies at -1 V vs SHE" font titlefont
set key at screen 1.0,screen 0.05 maxrows 2
set title '\large{ a) Volmer}' offset -13,graph -0.25 left
array coeffs_a[8]
array coeffs_b[8]
do for [i=1:8]{
	ele=elements[i]
	fit f(x) "../../data/volmer/".ele."/free_energy.txt" u 1:2 via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
set ylabel '$\Delta G^\ddag$ (eV)'
set xrange [-2.5:0.5]
set ytics format '%1.1f'
plot for [i=1:8] "../../data/volmer/".elements[i]."/free_energy.txt" u ($1-0):2 ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:8] coeffs_a[i]*x+coeffs_b[i] lc i lw 2 dt 2 notitle
unset xrange
set title "\\large b) Heyrovsky"
array coeffs_a[8]
array coeffs_b[8]
do for [i=1:8]{
	fit f(x) "../../data/heyrovsky/".elements[i]."/free_energy.txt" u 1:2 via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
set xrange [-2.5:0.5]
plot for [i=1:8] "../../data/heyrovsky/".elements[i]."/free_energy.txt" u ($1-0):2 ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:8] coeffs_a[i]*x+coeffs_b[i] lc i lw 2 dt 2 notitle
unset xrange
set title "\\large c) Tafel"
array coeffs_a[8]
array coeffs_b[8]
do for [i=1:8]{
	fit f(x) "../../data/tafel/".elements[i]."/free_energy.txt" u 1:2 via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
set xrange [-2.5:0.5]
plot for [i=1:8] "../../data/tafel/".elements[i]."/free_energy.txt" u ($1-0):2 ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:8] coeffs_a[i]*-1+coeffs_b[i] lc i lw 2 dt 2 notitle
set yrange [-1:1]
set ytics 
set title "\\large d) Hydrogen Adsorption"
array coeffs_a[8]
array coeffs_b[8]
array free_energy_corrections[8]=[-3.8144772408,-3.8144772408,-3.8144772408,-3.7144772408,-3.8144772408,-3.8144772408,-3.8144772408,-3.8144772408] #Ir top site, vib +0.1 eV
do for [i=1:8]{
	fit f(x) "../../data/hydrogen/".elements[i]."_diff.txt" u ($1-4.4):($2-free_energy_corrections[i]) via a,b
	coeffs_a[i]=a
	coeffs_b[i]=b
}
set xrange [-2.5:0.5]
set ylabel '$\Delta G_H$ (eV)' offset char 1,0
set xlabel "U vs SHE (V)" #offset 0,screen 0.075
plot for [i=1:8] "../../data/hydrogen/".elements[i]."_diff.txt" u ($1-4.4):($2-free_energy_corrections[i]) ps 2 pointtype numbers[i] title elements[i], \
     for [i=1:8] coeffs_a[i]*x+coeffs_b[i] lc i lw 2 dt 2 notitle
unset xrange
unset multiplot
