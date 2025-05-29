#!/bin/bash
for step in tafel heyrovsky
do
	echo $step
	cd $step
	for element in ./*/
	do 
		cd $element
		pwd
		for traj in *traj
		do
			echo $traj
			python ../../nebplot.py $traj
		done
		cd ../
	done
	cd ../
done
