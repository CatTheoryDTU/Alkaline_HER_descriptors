set encoding utf8
load 'turbo.pal'
set xtics nomirror #offset 0,graph 0.025 nomirror
set xtics format ''
set ytics nomirror
unset xtics
set ytics -5,-5,-15
set ytics format ''
#set terminal svg enhanced font labelfont size 1500,500
#set ylabel "$log(-j_0)$" 
set terminal epslatex color size 0.8in,1.2in font "Helvetica,8" standalone
set lmargin at screen 0.0
set rmargin at screen 1.0
set bmargin at screen 0.0
set tmargin at screen 1.0
set output "TOC_activity.tex"
#set key center top
unset key
f(x,y)=a*(x-4.44)+b*y+c
set fit quiet
set fit logfile '/dev/null'
set print '/dev/null'
fit f(x,y) "<paste PZCs.txt HBEs.txt i0s.txt" u 1:2:(1*($3-3)) via a,b,c
stats "<paste PZCs.txt HBEs.txt i0s.txt" using (f($1,$2)):(1*($3-3)) prefix "DESC" # -3 converts to A/cm^2
set xrange [-14:-2]
#set xlabel "Electrochemical Descriptor" 
#set label 1 sprintf("a=%1.2f b=%1.2f c=%1.2f",a,b,c) at -13,-4 
plot \
	"<paste PZCs.txt HBEs.txt i0s.txt metals.txt" using (f($1,$2)):(1*($3-3)):(sprintf("%s",stringcolumn(4))) w  labels point pt 7 offset char 1,0.5 notitle, \
	DESC_slope * x + DESC_intercept lc 'black' dt 2 lw 5.0 title sprintf("$R^2 = %1.2f$",DESC_correlation**2)
