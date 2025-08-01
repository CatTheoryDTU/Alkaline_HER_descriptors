#! gnuplot
set output "rate_control_taf.png"
load "rate_control_template.gnu"

#Rh
set title 'Rh' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Rh/rate_control.dat" using 1:2:8 with pm3d notitle

#Ir
set format x "%1.1f"
set title 'Ir' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Ir/rate_control.dat" using 1:2:8 with pm3d notitle

#Ni
unset xlabel; set format x ''
set format y '%2.0f';
set title 'Ni' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Ni/rate_control.dat" using 1:2:8 with pm3d notitle

#Pd
unset ylabel; set format y ''
set title 'Pd' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Pd/rate_control.dat" using 1:2:8 with pm3d notitle

set xlabel "Potential vs SHE" font elementfont offset 0,-1
#Pt
set title 'Pt' offset elemxoff, elemyoff textcolor "black" font elementfont
set format x "%1.1f"
splot "../../results/Pt/rate_control.dat" using 1:2:8 with pm3d notitle

#Cu
unset xlabel; set format x ''
set title 'Cu' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Cu/rate_control.dat" using 1:2:8 with pm3d notitle

#Ag
set title 'Ag' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Ag/rate_control.dat" using 1:2:8 with pm3d notitle

#Au
set format x '%1.1f' ;
set title 'Au' offset elemxoff, elemyoff textcolor "black" font elementfont
splot "../../results/Au/rate_control.dat" using 1:2:8 with pm3d notitle

unset multiplot
