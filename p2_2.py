#! /usr/bin/python

import sys
import operator
from operator import itemgetter
from count_freqs import *
from p2_1 import p2_1emission


def trigram_prob (yi, yi_1, yi_2, hmm):
    if (yi_2,yi_1,yi) in hmm.ngram_counts[2]:
        return hmm.ngram_counts[2][(yi_2,yi_1,yi)]/hmm.ngram_counts[1][(yi_2,yi_1)]
    else:
        print "not"
        return 0

if __name__ == "__main__":
    input = file(sys.argv[1],"r")
    hmm=Hmm(3)
    hmm.read_counts(input)

    testInput = file(sys.argv[2],"r")
    current_sentence=[]
    #node=list(hmm.all_states)
    #node.append('*')
    pairs=[(i,j) for i in hmm.all_states for j in hmm.all_states]
    #pairs=[(i,j) for i in node for j in node]
    
    countTag = dict.fromkeys(hmm.all_states,0)
    #print countTag

    for (word,tag) in hmm.emission_counts:
        countTag[tag] += hmm.emission_counts[(word,tag)]
   
    for line in testInput:
        word=line.strip()
        if word:
            current_sentence.append(word)
        else:
            #print current_sentence
            pi=[dict.fromkeys(pairs,0)]
            bp=[{}]
            pi[0][('*','*')]=1
            for i in range(1,len(current_sentence)+1):
                
                #print w
                pi.append(dict.fromkeys(pairs,0))
                bp.append(dict.fromkeys(pairs))
                emission = dict.fromkeys(hmm.all_states,0)
                w=current_sentence[i-1]
                for tag in hmm.all_states:
                    if (w,tag) in hmm.emission_counts:
                        emission[tag]=p2_1emission(w,tag,hmm,countTag)
                if all(val==0 for val in emission.values()):
                    for tag in hmm.all_states:
                        emission[tag]=p2_1emission("_RARE_",tag,hmm,countTag)
                #print w + " emission: "
                #print emission
                for pair in pairs:
                    y=pair[1]
                    y_1=pair[0]
                    if i==1:
                        #print trigram_prob(y,'*','*',hmm)
                        #print w
                        #print emission[y]
                        pi[i][pair]=pi[i-1][('*','*')]*trigram_prob(y,'*','*',hmm)*emission[y]
                        #print pi[i][pair]
                        continue
                    for y_2 in hmm.all_states:
                        if i==2:
                            prob=pi[i-1][(y_2,y_1)]*trigram_prob(y,y_1,'*',hmm)*emission[y]
                        else:
                            prob=pi[i-1][(y_2,y_1)]*trigram_prob(y,y_1,y_2,hmm)*emission[y]
                        #prob=pi[i-1][(y_2,y_1)]*trigram_prob(y,y_1,y_2,hmm)*p2_1emission(current_sentence[i-1],y,hmm,countTag)
                        if prob > pi[i][pair]:
                            pi[i][pair]=prob
                            bp[i][pair]=y_2 
                    #print pi[i][pair]
                    #print bp[i][pair]
            #print "final"
            path=[None]*len(current_sentence)
            index, element= max(enumerate(pi[len(current_sentence)][pair] * trigram_prob('STOP',pair[0],pair[1],hmm) for pair in pairs),key=itemgetter(1))
            #print pairs[index]
            #print element
            path[len(current_sentence)-1]=pairs[index][1]
            path[len(current_sentence)-2]=pairs[index][0]

            for k in range(len(current_sentence)-2,0,-1):
                path[k-1]=bp[k+2][(path[k],path[k+1])]
                #print path[k-1]
            for k in range(0,len(current_sentence)):
                print current_sentence[k] + " " + path[k]
            current_sentence=[]
            print word
            


            
