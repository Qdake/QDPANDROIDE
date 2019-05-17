# -*- coding: utf-8 -*-
"""
Author: Raymundo Cassani
April 2017

This file contains the Multi-Layer Perceptron (MLP) class which creates a
fully-connected-feedforward-artifitial-neural-network object with methods
for its usage

Methods:
    __init__()
    predict(X)
    initialize_theta_weights()
    feedforward(X)
    unroll_weights(rolled_data)
    roll_weights(unrolled_data)
    sigmoid(z)
    relu(z)
    sigmoid_derivative(z)
 """   
import numpy as np
class Mlp():
    '''
    fully-connected Multi-Layer Perceptron (MLP)
    '''

    def __init__(self, size_layers, act_funct='sigmoid', reg_lambda=0, bias_flag=True):
        '''
        Constructor method. Defines the characteristics of the MLP

        Arguments:
            size_layers : List with the number of Units for:
                [Input, Hidden1, Hidden2, ... HiddenN, Output] Layers.
            act_funtc   : Activation function for all the Units in the MLP
                default = 'sigmoid'
            reg_lambda: Value of the regularization parameter Lambda
                default = 0, i.e. no regularization
            bias: Indicates is the bias element is added for each layer, but the output
        '''
        self.size_layers = size_layers
        self.n_layers    = len(size_layers)
        self.act_f       = act_funct
        self.lambda_r    = reg_lambda
        self.bias_flag   = bias_flag
 
        # Ramdomly initialize theta (MLP weights)
        self.initialize_theta_weights()
        
    def predict(self, X):
        '''
        Given X (feature matrix), y_hay is computed
        Arguments:
            X      : Feature matrix [n_examples, n_features]
        Output:
            y_hat  : Computed Vector Class for X
        '''
        A , Z = self.feedforward(X)
        Y_hat = A[-1]
        return Y_hat

    def initialize_theta_weights(self):
        '''
        Initialize theta_weights, initialization method depends
        on the Activation Function and the Number of Units in the current layer
        and the next layer.
        The weights for each layer as of the size [next_layer, current_layer + 1]
        '''
        self.theta_weights = []
        size_next_layers = self.size_layers.copy()
        size_next_layers.pop(0)
        for size_layer, size_next_layer in zip(self.size_layers, size_next_layers):
            if self.act_f == 'sigmoid':
                # Method presented "Understanding the difficulty of training deep feedforward neurla networks"
                # Xavier Glorot and Youshua Bengio, 2010
                epsilon = 4.0 * np.sqrt(6) / np.sqrt(size_layer + size_next_layer)
                # Weigts from a uniform distribution [-epsilon, epsion]
                if self.bias_flag:  
                    theta_tmp = epsilon * ( (np.random.rand(size_next_layer, size_layer + 1) * 2.0 ) - 1)
                else:
                    theta_tmp = epsilon * ( (np.random.rand(size_next_layer, size_layer) * 2.0 ) - 1)
                    theta_tmp = epsilon * ( (np.random.rand(size_next_layer, size_layer) * 2.0 ) - 1)            
            elif self.act_f == 'relu':
                # Method presented in "Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classfication"
                # He et Al. 2015
                epsilon = np.sqrt(2.0 / (size_layer * size_next_layer) )
                # Weigts from Normal distribution mean = 0, std = epsion
                if self.bias_flag:
                    theta_tmp = epsilon * (np.random.randn(size_next_layer, size_layer + 1 ))
                else:
                    theta_tmp = epsilon * (np.random.randn(size_next_layer, size_layer))                    
            self.theta_weights.append(theta_tmp)
        self.theta_weights = self.roll_weights(np.random.uniform(-2.5,2.5,217))
        return self.theta_weights
    
    def feedforward(self, X):
        '''
        Implementation of the Feedforward
        '''

        A = [None] * self.n_layers
        Z = [None] * self.n_layers
        input_layer = X

        for ix_layer in range(self.n_layers - 2):
            n_examples = input_layer.shape[0]
            if self.bias_flag:
                # Add bias element to every example in input_layer
                input_layer = np.concatenate((np.ones([n_examples ,1]) ,input_layer), axis=1)
            A[ix_layer] = input_layer
            # Multiplying input_layer by theta_weights for this layer
            Z[ix_layer + 1] = np.matmul(input_layer,  self.theta_weights[ix_layer].transpose() )
            # Activation Function
            output_layer = self.tanh(Z[ix_layer + 1])
            # Current output_layer will be next input_layer
            input_layer = output_layer

        ix_layer = self.n_layers-2;
        n_examples = input_layer.shape[0]
        if self.bias_flag:
            # Add bias element to every example in input_layer
            input_layer = np.concatenate((np.ones([n_examples ,1]) ,input_layer), axis=1)
        A[ix_layer] = input_layer
        # Multiplying input_layer by theta_weights for this layer
        Z[ix_layer + 1] = np.matmul(input_layer,  self.theta_weights[ix_layer].transpose() )
        # Activation Function
        output_layer = self.sigmoid(Z[ix_layer + 1])
        # Current output_layer will be next input_layer
        input_layer = output_layer

        A[self.n_layers - 1] = output_layer
        return A, Z


    def unroll_weights(self, rolled_data):
        '''
        Unroll a list of matrices to a single vector
        Each matrix represents the Weights (or Gradients) from one layer to the next
        '''
        unrolled_array = np.array([])
        for one_layer in rolled_data:
            unrolled_array = np.concatenate((unrolled_array, one_layer.flatten(1)) )
        return unrolled_array

    def roll_weights(self, unrolled_data):
        '''
        Unrolls a single vector to a list of matrices
        Each matrix represents the Weights (or Gradients) from one layer to the next
        '''
        size_next_layers = self.size_layers.copy()
        size_next_layers.pop(0)
        rolled_list = []
        if self.bias_flag:
            extra_item = 1
        else:
            extra_item = 0
        for size_layer, size_next_layer in zip(self.size_layers, size_next_layers):
            n_weights = (size_next_layer * (size_layer + extra_item))
            data_tmp = unrolled_data[0 : n_weights]
            data_tmp = data_tmp.reshape(size_next_layer, (size_layer + extra_item), order = 'F')
            rolled_list.append(data_tmp)
            unrolled_data = np.delete(unrolled_data, np.s_[0:n_weights])
        return rolled_list

    def sigmoid(self, z):
        '''
        Sigmoid function
        z can be an numpy array or scalar
        '''
        result = 1.0 / (1.0 + np.exp(-z))
        return result
    def tanh(self, z):
        '''
        Sigmoid function
        z is a scalar
        '''
        result = np.tanh(z)       
        return result
    def relu(self, z):
        '''
        Rectified Linear function
        z can be an numpy array or scalar
        '''
        if np.isscalar(z):
            result = np.max((z, 0))
        else:
            zero_aux = np.zeros(z.shape)
            meta_z = np.stack((z , zero_aux), axis = -1)
            result = np.max(meta_z, axis = -1)
        return result


def croissement(nn1,nn2):
    gene1 = nn1.unroll_weights(nn1.theta_weights);
    gene2 = nn2.unroll_weights(nn2.theta_weights);
    print("gene1",len(gene1));
    print("gene2",len(gene2));
    a_gene1 = [];
    b_gene2 = [];
    for i in range(len(gene1)):
        if np.random.randint(1,3) == 1:
            a_gene1.append(gene1[i]);
            b_gene2.append(gene2[i]);
        else:
            a_gene1.append(gene2[i]);
            b_gene2.append(gene1[i]);
    a_nn = Mlp(nn1.size_layers);
    b_nn = Mlp(nn2.size_layers);
    print("len a_gene1 ", len(a_gene1));
    a_nn.theta_weights[0] = a_nn.roll_weights(np.array(a_gene1));
    b_nn.theta_weights[0] = b_nn.roll_weights(np.array(b_gene2));    
    return a_nn,b_nn        

def mutation(nn,probaMutation):
    ''' mutation en changeant quelques valeur des aretes
    '''   
    if np.random.rand()< probaMutation:
        nn.initialize_theta_weights();
    return nn;

# generer une Population initiale de taille N
def genererPopulation(N):
    population = [];
    for i in range(N):
        individu = Mlp([16,12,1])
        population.append(individu);
    return population;

def selection(population,scores,distribution):
    population = [x for x,_ in sorted(zip(population,scores),key=lambda x
                        :x[1])]; # ordoner les individus par distance decroissante
    print("p len",len(distribution)," populationsize ",len(population))
    x,y = np.random.choice(range(len(population)),2,replace=False,p=distribution);
    return population[x],population[y];

# rangement par qualite
def rangementParQualite(p,taille):
    '''generer une distribution pour selectionner des individus
    '''
    distribution = [p*pow((1-p),n) for n in range(taille)];
    distribution[0] = distribution[0]+(1-sum(distribution));
    return distribution;
