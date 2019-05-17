#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 10:50:10 2019

@author: qiu
"""
import main as robot
#import pybot.main as robot
from collide import distc

from Mlp import Mlp,genererPopulation,mutation,croissement,rangementParQualite,selection
import numpy as np
import matplotlib.pyplot as plt
 
# Mathematical function we need to plot
def z_func(x, y):
    return (1 - (x ** 2 + y ** 3)) * np.exp(-(x ** 2 + y ** 2) / 2)
# Setting up input values
x = np.arange(-3.0, 3.0, 0.1)
y = np.arange(-3.0, 3.0, 0.1)
X, Y = np.meshgrid(x, y)
 
# Calculating the output and storing it in the array Z
Z = z_func(X, Y)
 
im = plt.imshow(Z, cmap=plt.cm.RdBu, extent=(-3, 3, 3, -3), interpolation='bilinear')
 
plt.colorbar(im);
 
plt.title('$z=(1-x^2+y^3) e^{-(x^2+y^2)/2}$')
 
plt.show()
def plotmaze(position):
    from PIL import Image, ImageDraw;
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
    
    #img.save('/home/wei/Documents/QDPY/mywork/novelty search/mediumMap.bmp');
    
    for p in position:
        draw.point(p,"red");
    #    draw.ellipse([(p[0],p[1]),(p[0]+2,p[1]+2)],fill = "red");
    img.show()

import random 
position = []
# a robot that finishes within five units of the goal counts as a solution
k = 5;
X = [[None for i in range(200//k)] for j in range(400//k)];
positionsNotNone = [];
P = [[None for i in range(200//k)] for j in range(400//k)];
I = 200;
G = I//2 # nombre de solution radom
size_layers = [16,12,1]
for i in range(I):
    if i < G:
        x = Mlp(size_layers);
    else:
        x = random.choice(positionsNotNone);
        x = mutation(x,2);
        
#   positionFinale = robot.simulationNavigation(genome);
    positionFinale= robot.simulationNavigationSansImage(x);
    a,b = positionFinale
    position.append(positionFinale);
    p = robot.budgetRestant[a//k][b//k]
    if P[a//k][b//k] == None or P[a//k][b//k] < p:
        P[a//k][b//k] = p;
        X[a//k][b//k] = x;

        
#### affichage
plotmaze(position)