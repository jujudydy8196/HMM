#!/bin/bash

if [ $1 -eq 1 ] || [ $1 -eq 2]
then
		python count_freqs.py $2 > gene.counts
		python rare.py gene.counts gene.rarecounts
		python p2_$1.py gene.rarecounts $3 > $4
fi

