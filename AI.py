# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 13:58:31 2019

@author: Christopher Martin
"""

from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import numpy as np
import pandas as pd
from operator import add


class DQNAgent(object):

    def __init__(self):
        self.reward = 0
        self.gamma = 0.9
        self.dataframe = pd.DataFrame()
        self.short_memory = np.array([])
        self.agent_target = 1
        self.agent_predict = 0
        self.learning_rate = 0.0005
        self.model = self.network()
        self.model = self.network("weights.hdf5")
        self.epsilon = 0
        self.actual = []
        self.memory = []

    def get_state(self, game, player, food, direction):
        #evaluates states in bool values for the agent
        '''
        state = [
            (player.x_change == 20 and player.y_change == 0 and ((list(map(add, player.position[-1], [20, 0])) in player.position) or
            player.position[-1][0] + 20 >= (game.game_width - 20))) or (player.x_change == -20 and player.y_change == 0 and ((list(map(add, player.position[-1], [-20, 0])) in player.position) or
            player.position[-1][0] - 20 < 20)) or (player.x_change == 0 and player.y_change == -20 and ((list(map(add, player.position[-1], [0, -20])) in player.position) or
            player.position[-1][-1] - 20 < 20)) or (player.x_change == 0 and player.y_change == 20 and ((list(map(add, player.position[-1], [0, 20])) in player.position) or
            player.position[-1][-1] + 20 >= (game.game_height-20))),  # danger straight

            (player.x_change == 0 and player.y_change == -20 and ((list(map(add,player.position[-1],[20, 0])) in player.position) or
            player.position[ -1][0] + 20 > (game.game_width-20))) or (player.x_change == 0 and player.y_change == 20 and ((list(map(add,player.position[-1],
            [-20,0])) in player.position) or player.position[-1][0] - 20 < 20)) or (player.x_change == -20 and player.y_change == 0 and ((list(map(
            add,player.position[-1],[0,-20])) in player.position) or player.position[-1][-1] - 20 < 20)) or (player.x_change == 20 and player.y_change == 0 and (
            (list(map(add,player.position[-1],[0,20])) in player.position) or player.position[-1][
             -1] + 20 >= (game.game_height-20))),  # danger right

             (player.x_change == 0 and player.y_change == 20 and ((list(map(add,player.position[-1],[20,0])) in player.position) or
             player.position[-1][0] + 20 > (game.game_width-20))) or (player.x_change == 0 and player.y_change == -20 and ((list(map(
             add, player.position[-1],[-20,0])) in player.position) or player.position[-1][0] - 20 < 20)) or (player.x_change == 20 and player.y_change == 0 and (
            (list(map(add,player.position[-1],[0,-20])) in player.position) or player.position[-1][-1] - 20 < 20)) or (
            player.x_change == -20 and player.y_change == 0 and ((list(map(add,player.position[-1],[0,20])) in player.position) or
            player.position[-1][-1] + 20 >= (game.game_height-20))), #danger left


            player.x_change == -20,  # move left
            player.x_change == 20,  # move right
            player.y_change == -20,  # move up
            player.y_change == 20,  # move down
            food.x_food < player.x,  # food left
            food.x_food > player.x,  # food right
            food.y_food < player.y,  # food up
            food.y_food > player.y  # food down
            ]
        '''
        row = int(player[0,-1])
        col = int(player[1,-1])
        if (direction =="north"): # searches the game array relative to the direction facing and updates state as such
            state = [
                #checks the direction
                direction == "north",
                direction == "east",
                direction == "south",
                direction == "west",
                
                
                game[row, col -1] == 1, # checks for danger left
                game[row-1, col] == 1, #checks for danger forward
                game[row, col+1] == 1, # checks for danger right
                
                food[0] < row,  # food left
                food[0] > row,  # food right
                food[1] < col,  # food up
                food[1] > col  # food down         
                ]
        
        if (direction =="east"):
            state = [
                #checks the direction
                direction == "north",
                direction == "east",
                direction == "south",
                direction == "west",
                
                
                game[row - 1, col] == 1, # checks for danger left
                game[row, col + 1] == 1, #checks for danger forward
                game[row + 1, col] == 1, # checks for danger right
                
                food[0] < row,  # food left
                food[0] > row,  # food right
                food[1] < col,  # food up
                food[1] > col  # food down         
                ]

        if (direction =="south"):
            state = [
                #checks the direction
                direction == "north",
                direction == "east",
                direction == "south",
                direction == "west",
                
                
                game[row, col + 1] == 1, # checks for danger left
                game[row + 1, col] == 1, #checks for danger forward
                game[row, col - 1] == 1, # checks for danger right
                
                food[0] < row,  # food left
                food[0] > row,  # food right
                food[1] < col,  # food up
                food[1] > col  # food down         
                ]

        if (direction =="west"):
            state = [
                #checks the direction
                direction == "north",
                direction == "east",
                direction == "south",
                direction == "west",
                
                
                game[row + 1, col] == 1, # checks for danger left
                game[row, col - 1] == 1, #checks for danger forward
                game[row - 1, col] == 1, # checks for danger right
                
                food[0] < row,  # food left
                food[0] > row,  # food right
                food[1] < col,  # food up
                food[1] > col  # food down         
                ]


            
        for i in range(len(state)):
            if state[i]:
                state[i]=1
            else:
                state[i]=0

        return np.asarray(state)

    def set_reward(self, player, crash, closerX, closerY):
        #rewards the agent based on performance 
        self.reward = 0
        if (closerX or closerY):
            self.reward = 1
        elif not (closerX or closerY):
            self.reward = -1.5
        if crash:
            self.reward = -20
            return self.reward
        if player:
            self.reward = 10
        return self.reward

    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=120, activation='relu', input_dim=11))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=120, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=3, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', optimizer=opt)

        if weights:
            model.load_weights(weights)
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay_new(self, memory):
        if len(memory) > 1000:
            minibatch = random.sample(memory, 1000)
        else:
            minibatch = memory
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(np.array([next_state]))[0])
            target_f = self.model.predict(np.array([state]))
            target_f[0][np.argmax(action)] = target
            self.model.fit(np.array([state]), target_f, epochs=1, verbose=0)

    def train_short_memory(self, state, action, reward, next_state, done):
        target = reward
        if not done:
            target = reward + self.gamma * np.amax(self.model.predict(next_state.reshape((1, 11)))[0])
        target_f = self.model.predict(state.reshape((1, 11)))
        target_f[0][np.argmax(action)] = target
        self.model.fit(state.reshape((1, 11)), target_f, epochs=1, verbose=0)




#log loss
#deep lizard

'''
two neural networks, rewrite one every few generations with the other
extra one runs belmonds equation
on all possible actions



take the entire grid
CNN to classification
to use feature extraction

reversing articulated lorry
estimation for truck and trailer systems using deep learning




'''














