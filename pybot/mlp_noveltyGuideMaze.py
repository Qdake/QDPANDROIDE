#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
import main as robot
from collide import distc
import time
from Mlp import Mlp,genererPopulation,mutation,croissement,rangementParQualite,selection


def eval_genomes(population,generation,nb_run):
    global solution;
    start_time = time.time()
    f=open("resultat_{}ieme_run.out".format(nb_run),"w");
    taillePopulation =len(population);
    for i in range(generation):
        if i%5 == 0:
            plotmaze(position,"resultat_{}ieme_run_{}_generation_image.rgba".format(nb_run,i))
        print(i,"ieme generation")
        pos = []
        distances = [[0 for i in range(len(population))] for j in range(len(population))]
        ### evaluation des reseaux neurones
        for genome in population:
            #affichage de image
#            positionFinale = robot.simulationNavigation(genome);
            positionFinale = robot.simulationNavigationSansImage(genome);
            if distc(positionFinale, robot.finish_position) < 10 :
                print("***********solution trouveeee****************\n");
                f.write("***********solution trouveeee****************\n");
                f.write("position a'arete:",positionFinale);
                f.write("temps utilise: ",time.time-start_time);
                f.close();
                plotmaze(position,"resultat_{}ieme_run_final_image.png".format(nb_run))
                return
            position.append(positionFinale);
            # evaluation
            pos.append(positionFinale);
        ### calculer des scores avec positions finales des robots
        nouveaute = [0 for i in population];
        for i in range(len(population)):
            for j in range(len(population)):
                if i<=j:
                    distances[i][j] = distc(pos[i],pos[j]);
                    distances[j][i] = distc(pos[j],pos[i]); 
            tb = list(reversed(sorted(distances[i][:])));
            nouveaute[i] = sum(tb[0:15])

            if cases[positionFinale[0]//k][positionFinale[1]//k] == 0:
                nouveaute[i] += 10000;
                cases[positionFinale[0]//k][positionFinale[1]//k] = 1;
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
    
    

# a robot that finishes within five units of the goal counts as a solution
k = 5
cases = [[0 for i in range(200//k)] for j in range(400//k)];
position = [];
N = 250
p = genererPopulation(N,[16,12,1])
probMutation = 0.005
for i in range(1,2):
    eval_genomes(p,3,i);
solution = None;
plotmaze(position,"resultat_{}ieme_run_image.png".format(-1))
#### affichage

from PIL import Image, ImageDraw;
def plotmaze(position,filename):
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
    
    
    for p in position:
        draw.point(p,"red");
    #    draw.ellipse([(p[0],p[1]),(p[0]+2,p[1]+2)],fill = "red");
    img.save(filename);
    img.show()