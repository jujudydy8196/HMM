#!/usr/bin/python

import sys
from count_freqs import Hmm

countInput = file(sys.argv[1],"r")
hmm = Hmm(3)
hmm.read_counts(countInput)

for tag in hmm.all_states:
    hmm.emission_counts[("_RARE_",tag)]=0

for key,value in hmm.emission_counts.items():
    #print value
    if key[0] == "_RARE_":
        continue
    if value < 5:
        hmm.emission_counts[("_RARE_",key[1])] += value
        #print "%s delete %i to RARE %i" %(key,value,hmm.emission_counts[("_RARE_",key[1])])
        del hmm.emission_counts[key]

#print len(hmm.emission_counts)
rareOutput = file(sys.argv[2],"w")
hmm.write_counts(rareOutput)


