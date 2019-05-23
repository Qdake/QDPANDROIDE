#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:02:53 2019

@author: 3503860
"""
import math
import matplotlib.pyplot as plt
###  genererGrapheEvaluation
def dist(p0,p):
    x0,y0 = p0;
    x,y = p;
    return math.sqrt((x-x0)**2 + (y-y0)**2);
def read(fn,n):
    positions = [];
    f = open(fn,"r");
    for i in range(n):
        line = f.readline();
        line = line.replace('(','');
        line = line.replace(')','');
        x,y = line.split(', ');
        x = int(x);
        y = int(y);
        positions.append([x,y])
    f.close();
    return positions;

def evaluation_performance(positions):
    distances = [];
    for i in range(n):
        d = 0;
        for j in range(len(positions)):
            k = dist(positions[j][i],pe)
            d += k;
        d = d/len(positions);
        distances.append(d);
    
    max_dist = dist(ps,pe);
    evaluation = [0];
    for d in distances:
        if max_dist - d > evaluation[-1]:
            evaluation.append(max_dist-d);
        else:
            evaluation.append(evaluation[-1]);
    return evaluation;

## fitness
#n = 125000 # nb_lignes
#nf = 6  # nb_fichiers
#fpositions = [];
#ps = [40,60]  #position start
#pe = [370,150];   # position goal
#for i in range(nf):
#    fn = "./rf/fitness_{}_run_125000evaluations.txt".format(i);
#    fpositions.append(read(fn,n));
#fit_evaluation_performance = evaluation_performance(fpositions);
#plt.title("Evaluation de performance avec nb_evaluations")
#plt.plot(range(n+1),fit_evaluation_performance);
#
## NS
#npositions = [];
#NS = {1,2,3,4,5}
#n = 102351
#for i in NS:
#    fn = "./rf/fitness_{}_run_125000evaluations.txt".format(i);
#    npositions.append(read(fn,n));
#nov_evaluation_performance = evaluation_performance(npositions);
#plt.plot(range(n+1),nov_evaluation_performance);


# NS+ map ellites
mpositions = [];
MAP = {7,8}
n = 37416
mpositions.append(read("./rf/map_7_run_39629evaluations.txt",n));
map_evaluation_performance = evaluation_performance(mpositions);
plt.plot(range(n+1),map_evaluation_performance);

plt.show();



    
    