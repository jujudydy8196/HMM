#! /usr/bin/python

import sys
import operator
from collections import defaultdict
from count_freqs import Hmm

def p2_1emission (word,tag,hmm,countTag):

    #print "p2_1 " + word + " " + tag + " %i" %hmm.emission_counts[(word,tag)]
    if (word,tag) in hmm.emission_counts:
        return hmm.emission_counts[(word,tag)]/countTag[tag]
    else:
        return 0

if __name__ == "__main__":
    input = file(sys.argv[1],"r")
    model = Hmm(3)
    #print len(model.emission_counts)
    model.read_counts(input)
    #print len(model.emission_counts
    #if ("BACKGROUND","O") in model.emission_counts:
        #print "yes"
    #print model.all_states 
    testFile = file(sys.argv[2],"r")

    tagsNum = len(model.all_states)
    countTag = dict.fromkeys(model.all_states,0)
    #print countTag

    for (word,tag) in model.emission_counts:
        countTag[tag] += model.emission_counts[(word,tag)]
    #print countTag
    for line in testFile:
        word = line.strip()
        if word:
            emission = dict.fromkeys(model.all_states,0)
            for tag in model.all_states:
                if (word,tag) in model.emission_counts:
                    emission[tag]=p2_1emission(word,tag,model,countTag)
                    #print word + " " + tag + ": %f" % emission[tag]
                #else:
                    #emission[tag]=p2_1emission("_RARE_",tag,model,countTag)
                    #print tag + ": %f" % emission[tag]
            if all(val==0 for val in emission.values()):
                for tag in model.all_states:
                    emission[tag]=p2_1emission("_RARE_",tag,model,countTag)
                #print word + " _RARE_"
            #else:
            print word + " " + max(emission.iteritems(), key=operator.itemgetter(1))[0]
        else:
            print word
        

    #for (word,tag) in model.emission_counts:
        #p2_1emission(word,tag,model)
