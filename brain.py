#!/usr/bin/env python
from keras.models import Sequential
from keras.layers import Dense, Activation
import numpy as np

#### input
# sitrep = [( blocked ways: 0 - not blocked, 1 - blocked: ) left, front, right,
#           (nearest food loc_x - x, loc_y - y) x, y, (snake length) len]

#### output:
# moves the last part of the snake in front of it in direction dir
# # 0: up
# # 1: right
# # 2: down
# # 3: left

def softmaxer(inp):
    e = np.exp(inp - np.max(inp))
    return e / np.sum(e)

class Brain():

    def __init__(self, layers = []):
        self.model = Sequential(layers = layers)

    def add_layer(self, dim_out = 1, dim_in = 1, act = 'relu'):
        self.model.add( Dense(dim_out, input_shape=( dim_in, ), activation = act) )

    def think(self, opt = 'adam', loss_fun = 'mean_squared_error', metric = ['accuracy']):
        self.model.compile(loss = loss_fun, optimizer= opt, metrics = metric)

    def step_to(self, situation):
        pred = self.predictor(situation)
        print(pred)
        return np.argmax((softmaxer( pred[[ 0, 3, 4, 5 ]] ),
                          softmaxer( pred[[ 1, 3, 4, 5 ]] ),
                          softmaxer( pred[[ 2, 3, 4, 5 ]] )))

    def predictor(self, situation):
        return self.model.predict(situation)

    def set_genes(self, genes, biases):
        for i in range(len( self.model.layers )):
            self.model.layers[i].set_weights([ genes[i], biases[i] ])

    def genes(self):
        return [layer.get_weights()[0] for layer in self.model.layers]

    def biases(self):
        return [layer.get_weights()[1] for layer in self.model.layers]

    def configs(self):
        return [layer.get_configs() for layer in self.model.layers]


#### just left the testing part here...
# for x in range(10):
#     bran = Brain()
#     bran.add_layer(dim_out = 16)
#     bran.add_layer(dim_in = 16, dim_out = 16)
#     bran.add_layer(dim_in = 16)
#     # print( bran.genes() )
#     # print( bran.biases() )
#     sitrep = [np.random.randint(0, 2),
#               np.random.randint(0, 2),
#               np.random.randint(0, 2),
#               np.random.randint(-10, 11),
#               np.random.randint(-10, 11),
#               np.random.randint(0, 16)]
#     # print( bran.step_to(sitrep) )
#     print("step")
#     print( sitrep )
#     print( bran.step_to(sitrep) )
 
# last_genes = bran.genes()
# last_bias = bran.biases()
# bran.set_genes(last_genes, last_bias)
