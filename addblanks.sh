#!/bin/bash
for file in results/*/production.dat;
do
	[ -e "$file" ] || continue
	gawk '{t=$1;$1=$2;$2=t;print;}' $file | sort -k1,1g -k2,2g | gawk -f addblanks.awk | tac > "tmpaddblanks" &&
		mv "tmpaddblanks" $file.tafel
done

for file in results/*/*dat;
do
	[ -e "$file" ] || continue
	sort -k1,1g -k2,2g $file | gawk -f addblanks.awk > "tmpaddblanks" &&
	#cat $file | gawk -f addblanks.awk > "tmpaddblanks" &&
		mv "tmpaddblanks" $file
done

