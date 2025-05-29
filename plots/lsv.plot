set encoding utf8
ticsfont = "Helvetica,18"
titlefont = "Helvetica,18"
labelfont = "Helvetica,32"
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
#set title "pH = 13 "
#set terminal png enhanced font titlefont size 1200,900
#set output "LSVs.png"
#set terminal epslatex color colortext size 4in,3in "cmss"
#set output "Figure_Log_current.tex"
set terminal svg enhanced font titlefont size 1000,500
set output "LSVs.svg"
load 'turbo.pal'
set xlabel "Potential vs RHE" offset 0,screen 0 font labelfont
#set ylabel "log10(-j)" font labelfont
set ylabel "-j mA/cm^2" font labelfont
set yzeroaxis
set xtics font ticsfont nomirror
set ytics font ticsfont nomirror
set ytics format "10^{%T}" font ticsfont
pH=13*-0.059
stats "<awk '$2==13.0 && $1<-0.767' ../results/Ag/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Ag"
stats "<awk '$2==13.0 && $1<-0.767' ../results/Au/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Au"
stats "<awk '$2==13.0 && $1<-0.767' ../results/Cu/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Cu"
stats "<awk '$2==13.0 && $1<-0.767' ../results/Ir/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Ir"
stats "<awk '$2==13.0 && $1<-0.767' ../results/Ni/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Ni"
stats "<awk '$2==13.0 && $1<-0.767' ../results/Pd/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Pd"
stats "<awk '$2==13.0 && $1<-0.767' ../results/Pt/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Pt"
stats "<awk '$2==13.0 && $1<-0.767' ../results/Rh/current.dat" using ($1-pH):(log10(-1*$3)) prefix "Rh"
save var 'fit_lsv.dat'
a=1.0
set xrange [-1.2:0.25]
set yrange [1e-9:1e9]
set logscale y
#set rmargin 50
#set key right center outside reverse box lw 1 samplen 2 width -4 offset 0,0
#plot "<awk '$2==13.0' ../results/Ag/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Ag slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Ag_slope,Ag_intercept), \
#	"<awk '$2==13.0' ../results/Au/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Au slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Au_slope,Au_intercept), \
#	"<awk '$2==13.0' ../results/Cu/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Cu slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Cu_slope,Cu_intercept), \
#	"<awk '$2==13.0' ../results/Ir/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Ir slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Ir_slope,Ir_intercept), \
#	"<awk '$2==13.0' ../results/Ni/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Ni slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Ni_slope,Ni_intercept), \
#	"<awk '$2==13.0' ../results/Pd/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Pd slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Pd_slope,Pd_intercept), \
#	"<awk '$2==13.0' ../results/Pt/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Pt slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Pt_slope,Pt_intercept), \
#	"<awk '$2==13.0' ../results/Rh/current.dat" using ($1-pH):(a*(-1*$3)) w l lw 2.0 title sprintf('Rh slope=%3.0f mV/dec, i0=%1.2f mA/cm2 ', 1000/Rh_slope,Rh_intercept)
set key textcolor variable 
# from gnuplotting
# get the relation of x- and y-range
dx = 0.25+1.2
dy = log(1e9)-log(1e-9)
s1 = dx/dy
# get ratio of axes
s2 = 0.75
# heler function for getting the rotation angle of the labels in degree
deg(x) = x/pi*180.0
r(x) = deg(atan(s1*s2*x))
set label 1 sprintf('Ag %3.0f mV/dec',1000/Ag_slope) at -0.8,10**(0.3+(-0.8)*Ag_slope+Ag_intercept) rotate by r(Ag_slope)-12 center textcolor lt 1
set label 2 sprintf('Au %3.0f mV/dec',1000/Au_slope) at -0.8,10**(0.35+(-0.8)*Au_slope+Au_intercept) rotate by r(Au_slope)-13 center textcolor lt 2
set label 3 sprintf('Cu %3.0f mV/dec',1000/Cu_slope) at -0.8,10**(0.3+(-0.8)*Cu_slope+Cu_intercept) rotate by r(Cu_slope)-12 center textcolor lt 3
set label 4 sprintf('Ir %3.0f mV/dec',1000/Ir_slope) at -0.8,10**(0.3+(-0.8)*Ir_slope+Ir_intercept) rotate by r(Ir_slope)-11 center textcolor lt 4
set label 5 sprintf('Ni %3.0f mV/dec',1000/Ni_slope) at -0.8,10**(0.3+(-0.8)*Ni_slope+Ni_intercept) rotate by r(Ni_slope)-9 center textcolor lt 5
set label 6 sprintf('Pd %3.0f mV/dec',1000/Pd_slope) at -0.8,10**(-0.55+(-0.8)*Pd_slope+Pd_intercept) rotate by r(Pd_slope)-12 center textcolor lt 6
set label 7 sprintf('Pt %3.0f mV/dec',1000/Pt_slope) at -0.8,10**(0.3+(-0.8)*Pt_slope+Pt_intercept) rotate by r(Pt_slope)-11 center textcolor lt 7
set label 8 sprintf('Rh %3.0f mV/dec',1000/Rh_slope) at -0.8,10**(0.45+(-0.8)*Rh_slope+Rh_intercept) rotate by r(Rh_slope)-12 center textcolor lt 8
#set arrow from -1.5,1 to 0.2,1
plot "<awk '$2==13.0' ../results/Ag/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Au/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Cu/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Ir/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Ni/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Pd/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Pt/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle, \
	"<awk '$2==13.0' ../results/Rh/current.dat" using ($1-pH):(a*(-1.0*$3)) w l lw 2.0 notitle
