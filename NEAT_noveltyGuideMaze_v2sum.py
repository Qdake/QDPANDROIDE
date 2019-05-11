#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
# recherche avec reseau neurone NEAT et fonction fitness d = distance(positionFinale, goal)
# il reste a ajuster les parametres dans le ficher config

import neat
#import main
from pybot import main as robot
#import pybot.main as robot
from collide import distc
# a robot that finishes within five units of the goal counts as a solution
k = 5
cases = [[0 for i in range(200//k)] for j in range(400//k)];
position = [];
def eval_genomes(genomes, config):
    pos = []
    distances = [[0 for i in range(len(genomes))] for j in range(len(genomes))]
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        #affichage de image
        positionFinale = robot.simulationNavigation(net.activate);
#        positionFinale = robot.simulationNavigationSansImage(net.activate);
        position.append(positionFinale);
        if positionFinale[0] < 0 or positionFinale[1]< 0:
                print("******************position: ",position);
                break;
        # evaluation
        pos.append(positionFinale);
        print("--> la position finale {}".format(positionFinale));
    for i in range(len(genomes)):
        for j in range(len(genomes)):
            if i<=j:
                distances[i][j] = distc(pos[i],pos[j]);
                distances[j][i] = distc(pos[j],pos[i]);
                
        tb = list(reversed(sorted(distances[i][:])));
        genomes[i][1].fitness = sum(tb[0:15])
        
        if cases[positionFinale[0]//k][positionFinale[1]//k] == 0:
            genomes[i][1].fitness += 10000;
            cases[positionFinale[0]//k][positionFinale[1]//k] = 1;
        if distc(positionFinale, robot.finish_position) < 10 :
            print("***********solution trouveeee****************");
            solution = genomes[i];
            break;
        print("--> fitness: ",genomes[i][1].fitness)
# Load configuration.
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'NEAT_fitnessGuideMaze_config')

# Create the population, which is the top-level object for a NEAT run.
p = neat.Population(config)

# Add a stdout reporter to show progress in the terminal.
p.add_reporter(neat.StdOutReporter(False))

# Run until a solution is found.
winner = p.run(eval_genomes,20); 

# Display the winning genome.
print('\nBest genome:\n{!s}'.format(winner))


from PIL import Image, ImageDraw;
h = 400;
l = 200;
o = (0,0)
size = (h,l);
img = Image.new('1',size,1);
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
draw.ellipse([(20,20),(30,30)],fill = 0);
draw.ellipse([(22,22),(28,28)],fill = 1);

img.show();
#img.save('/home/wei/Documents/QDPY/mywork/novelty search/mediumMap.bmp');



for p in position:
    draw.ellipse([(p[0]-1,p[1]-1),(p[0],p[1])],fill = 0);
img.show()