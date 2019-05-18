#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
import random
import heapq
import main as robot
from collide import distc
import time
from Mlp import Mlp,genererPopulation,mutation,croissement,rangementParQualite,selection
from PIL import Image, ImageDraw;

def butAtteint(positionFinale):
    if distc(positionFinale, robot.finish_position) < 10 :
        return True;
    else:
        return False;
def les_k_plus_petits_elements(k,l):
    t = l[:k];
    for e in l[k:]:
        x = None;
        m = None
        for i in range(len(t)):
            if t[i]>e:
                if x == None:
                    x = i;
                    m = t[i]
                elif t[i]>m:
                    x = i;
                    m = t[i]
        if x != None:
            t[x] = e;
    return t;

def plotmaze(visitedPositions,filename):
    """position:ensemble de toutes les positions atteintes par au moins un robot 
    """
    print("plotmaze, len(visitedPositions) =",len(visitedPositions));
    h = 400;
    l = 200;
    o = (0,0)
    img = Image.new('RGBA', (h, l),(255,255,255))
    draw = ImageDraw.Draw(img);
    draw.line([o,(h-1,0)],fill = 0);
    draw.line([o,(0,l-1)],fill = 0);
    draw.line([(0,l-1),(h-1,l-1)],fill = 0);
    draw.line([(h-1,0),(h-1,l-1)],fill = 0);
    draw.line([(50,80),(340,200)],fill = 0);
    draw.line([(120,0),(70,50)],fill = 0);
    draw.line([(220,0),(170,70)],fill = 0);
    draw.line([(350,0),(300,100)],fill = 0);
    draw.line([(350,140),(380,200)],fill = 0);
    draw.line([(120,60),(150,125)],fill = 0);
    draw.line([(220,85),(250,190)],fill = 0);
    #goal
    draw.ellipse([(370,150),(380,160)],fill = 0);
    #start
    draw.ellipse([(3,20),(13,30)],fill = 0);
    #draw.ellipse([(3,18),(4,23)],fill = 1);
    #img.show()
    
    
    for p in visitedPositions:
        draw.point(p,"red");
    #    draw.ellipse([(p[0],p[1]),(p[0]+2,p[1]+2)],fill = "red");
    img.save(filename);
         
def eval_genomes(nb_run):
    global size_layers;
    
    visitedPosition = set();
    X = [[None for i in range(400)] for j in range(200)]
    P = [[0 for]]
    
    #generate and evaluate B random genomes
    B = [Mlp(size_layers) for i in range(250)];
    pos = [robot.simulationNavigationSansImage(genome) for genome in P];
    for genome,position in zip(P,pos):
        if position not in visitedPosition:
            visitedPosition.add(position);
            X[position[0]][position[1]] = genome;
        else:
            if random.randint(0,1) == 1:
                X[position[0]][position[1]] = genome;
    
    for generation in range(1000):
                
      
    
    
    
    
    global solution;
    global probMutation
    global position
    k = 20; #nombre de voisins les plus proches
    start_time = time.time()
    visitedPosition = set();
    taillePopulation =len(population);
    for j in range(generation):
        print(j,"-ieme generation")
        pos = []
        nouveaute = []
        ### evaluate population and add into archive of past behaviors
        for genome in population:
            #affichage de image
#            positionFinale = robot.simulationNavigation(genome);
            positionFinale = robot.simulationNavigationSansImage(genome);
            # ajouter la positionFinale dans l'ensemble de positions visitees par la population
            pos.append(positionFinale);
            # MAJ de nouveaute
            if (positionFinale[0],positionFinale[1]) not in visitedPosition:
                nouveaute.append(10000)
            else:
                nouveaute.append(0);
            
            # ajouter la positionFinale dans l'ensemble de positions visitees
            visitedPosition.add((positionFinale[0],positionFinale[1]));
            # verifier si le but est atteint
            if butAtteint(positionFinale,start_time,nb_run):
                return;            
            
            
        ### calculer le nouveaute par rapport a ses distances avec les voisins pour chaque genome dans la population
#        print("visitedPosition: ",visitedPosition);
        for i in range(len(population)):
            #calculer les distances entre cette position et toutes les autres positions visitees
            distances = [];
            heapq.heapify(distances);
            for p in visitedPosition:
                heapq.heappush(distances,distc(pos[i],p))
            nouveaute[i] += sum(distances[0:k+1])
#            print("distances: ",distances)
#            print("len(distance) :",len(distances))
#            print("len(visitedPOsitions) :",len(visitedPosition));
#            print("positionFi ", pos[i]);
#            print("pos[i] nouveaute: ",nouveaute[i]);
#        print("nouveaute: ",nouveaute) 
#        print("pos : ",pos);
        
        ### generer prochaine generation
        nextPopulation = [];      
        distribution = rangementParQualite(p = 0.3,taille = taillePopulation);
        for i in range(taillePopulation//2):
            #selection
            individu1,individu2 = selection(population,nouveaute,distribution); 
            #croisement
            individu3,individu4 = croissement(individu1,individu2);
            #mutation
            individu3 = mutation(individu3,probMutation);
            individu4 = mutation(individu4,probMutation);
            #ajouter dans la prochaine population
            nextPopulation.append(individu3);
            nextPopulation.append(individu4);
        population = nextPopulation;
        
        
        #generation de graph
        print("j=", j);
        if j%5 == 0 and j!=0:
#            plotmaze(visitedPosition,"./result/noveltyGuideMaze_{}_run_{}_generation_image.png".format(nb_run,j))
            plotmaze(visitedPosition,"./test_result/NS_mapElite_Maze_{}_run_{}_generation_image.png".format(nb_run,j))

for nb_run in range(1):
    eval_genomes(nb_run);