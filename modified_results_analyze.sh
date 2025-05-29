#!/bin/bash
#Create input files
python generate_inputs_incomplete.py
#Run catmap models, create .dat files
for i in $(seq 0 1 7)
do
python run_models.py $i &
done
wait
#Add blank lines between isolines for plotting
. addblanks.sh
#Plot
cd plots
gnuplot coverage.plot
gnuplot selectivity_new.plot
gnuplot TOF_new.plot
ls -l ../results/*/results.json | awk -F '[/|..]' '{print $6}' > metals.txt
jq '.Hydrogen.energy' ../results/*/results.json > HBEs.txt
#grep "3.40" ../data/heyrovsky/*/barriers.txt | awk '{print $2}' > heyrovskys.txt
#grep "3.40" ../data/volmer/*/barriers.txt | awk '{print $2}' > volmers.txt
#grep "3.40" ../data/tafel/*/barriers.txt | awk '{print $2}' > tafels.txt
jq '.heyrovsky.barrier-1.02*.heyrovsky.barrier_beta' ../results/*/results.json > heyrovskys.txt
jq '.volmer.barrier-1.02*.volmer.barrier_beta' ../results/*/results.json > volmers.txt
jq '.tafel.barrier' ../results/*/results.json > tafels.txt
jq '.heyrovsky.barrier_beta' ../results/*/results.json > heyrovsky_betas.txt
jq '.volmer.barrier_beta' ../results/*/results.json > volmer_betas.txt
jq '.tafel.barrier_beta' ../results/*/results.json > tafel_betas.txt
jq '.heyrovsky.energy' ../results/*/results.json > heyrovsky_energies.txt
jq '.volmer.energy' ../results/*/results.json > volmer_energies.txt
jq '.tafel.energy' ../results/*/results.json > tafel_energies.txt
jq '.heyrovsky.energy-1.02*.heyrovsky.beta' ../results/*/results.json > heyrovsky_energies_at-1V.txt
jq '.volmer.energy-1.02*.volmer.beta' ../results/*/results.json > volmer_energies_at-1V.txt
grep "\-1\.02 1.4" ../results/*/production.dat | awk '{print $4}' > pH14RHE-0.2_activity.txt
grep "\-1\.02 1.4" ../results/*/current.dat | awk '{print $3}' > pH14RHE-0.2_currents.txt
gnuplot lsv.plot
gnuplot polarization.plot
gnuplot betas.plot
grep ".._intercept =" fit_lsv.dat | awk '{print $3}' > i0s.txt
grep ".._slope =" fit_lsv.dat | awk '{print 1000/$3}' > tafel_slopes.txt
gnuplot barriers.plot
gnuplot barrier_volcano.plot
gnuplot activity_volcano.plot
cd ../
display plots/Activity_volcano.png &
#display plots/LSVs.png &
display plots/Polarization_curves.png &
#display plots/Coverage.png &
#Return
