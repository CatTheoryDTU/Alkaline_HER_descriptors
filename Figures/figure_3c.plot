set encoding utf8
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
set terminal epslatex color colortext size 2in,5in font "cmss" standalone
set output "Figure_3C.tex"
set xlabel "U vs RHE (V)" offset 0,screen 0 #font labelfont
set ylabel "-j (mA/cm$^2$)" offset graph 0.02,0#font labelfont
set yzeroaxis
set xtics nomirror
set ytics nomirror
set ytics format '$10^{%T}$' #font ticsfont
set rmargin 0.95
pH=13.0*-0.059
stats "<awk '$2==13.0 && $1<-1.000' ../results/Ag/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Ag"
stats "<awk '$2==13.0 && $1<-1.000' ../results/Au/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Au"
stats "<awk '$2==13.0 && $1<-1.000' ../results/Cu/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Cu"
stats "<awk '$2==13.0 && $1<-1.000' ../results/Ir/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Ir"
stats "<awk '$2==13.0 && $1<-1.000' ../results/Ni/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Ni"
stats "<awk '$2==13.0 && $1<-1.000' ../results/Pd/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Pd"
stats "<awk '$2==13.0 && $1<-1.000' ../results/Pt/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Pt"
stats "<awk '$2==13.0 && $1<-1.000' ../results/Rh/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Rh"
save var 'fit_lsv.dat'
a=1.0
set xrange [-1.0:0.25]
set yrange [1e-9:1e9]
set format y ""
set ytics  1e-8,1e2,1e8
set ytics add ('10$^{-8}$' 1e-8, '10$^{-4}$' 1e-4,'10$^{-0}$' 1e-0,'10$^4$' 1e4,'10$^8$' 1e8 )
set ytics offset graph 0.01,-0.01
#set mytics 10
set xtics  -1.0,0.4,0.2
set logscale y
set key textcolor variable 
# from gnuplotting
# get the relation of x- and y-range
dx = 0.25+1.0
dy = log(1e9)-log(1e-9)
s1 = dx/dy
# get ratio of axes
s2 = 5 
# heler function for getting the rotation angle of the labels in degree
deg(x) = x/pi*180.0
r(x) = deg(atan(s1*s2*x))
set label 9 at screen 0.05,0.95 'c)' front
set label 1 sprintf('\scriptsize Ag %3.0f mV/dec',1000/Ag_slope) at -0.35,10**(0.40+(-0.35)*Ag_slope+Ag_intercept) rotate by r(Ag_slope)-15 center textcolor lt 1
set label 2 sprintf('\scriptsize Au %3.0f mV/dec',1000/Au_slope) at -0.45,10**(0.65+(-0.45)*Au_slope+Au_intercept) rotate by r(Au_slope)-12 center textcolor lt 2
set label 3 sprintf('\scriptsize Cu %3.0f mV/dec',1000/Cu_slope) at -0.70,10**(0.45+(-0.55)*Cu_slope+Cu_intercept) rotate by r(Cu_slope)-15. center textcolor lt 3
set label 4 sprintf('\scriptsize Ir %3.0f mV/dec',1000/Ir_slope) at -0.4,10**(0.45+(-0.4)*Ir_slope+Ir_intercept) rotate by r(Ir_slope)-12 center textcolor lt 4
set label 5 sprintf('\scriptsize Ni %3.0f mV/dec',1000/Ni_slope) at -0.55,10**(0.4+(-0.55)*Ni_slope+Ni_intercept) rotate by r(Ni_slope)-7. center textcolor lt 5
set label 6 sprintf('\scriptsize Pd %3.0f mV/dec',1000/Pd_slope) at -0.70,10**(-0.60+(-0.65)*Pd_slope+Pd_intercept) rotate by r(Pd_slope)-13 center textcolor lt 6
set label 7 sprintf('\scriptsize Pt %3.0f mV/dec',1000/Pt_slope) at -0.65,10**(0.45+(-0.7)*Pt_slope+Pt_intercept) rotate by r(Pt_slope)-11 center textcolor lt 7
set label 8 sprintf('\scriptsize Rh %3.0f mV/dec',1000/Rh_slope) at -0.65,10**(0.60+(-0.65)*Rh_slope+Rh_intercept) rotate by r(Rh_slope)-12 center textcolor lt 8
plot "<awk '$2==13.0' ../results/Ag/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Au/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Cu/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Ir/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Ni/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Pd/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Pt/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Rh/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle
