#SETUP
import pygame
import numpy as np
from random import randint
from AI import DQNAgent
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import seaborn as sns


pygame.init()
gameDisplay = pygame.display.set_mode((1000,800))
pygame.display.set_caption('snake')

g = np.zeros(100*80).reshape(80, 100)
s = np.zeros(10).reshape(2, 5)
i = np.zeros(6)
foodPos = np.zeros(2)
direction = "east" 
score = 0 
grown = False
crash = False

#THE USER DOES SOMETHING TO START THE GAME.

gameRunning = 1

def Food():
    global score
    global foodPos
    block = 0
    while (block == 0):
        row = randint(0,79)
        column = randint(0, 99)
        if (g.item(row, column) == 0):
            g[row, column] = 2
            #print ("test row  ")
            #g.item(row, column)
            block = 1
            score += 1
    foodPos = [row, column]
            

def SnakeInit(agent):
    global g
    g = np.zeros(100*80).reshape(80, 100)
    global s
    global foodPos
    global direction
    global crash
    crash = False
    global grown
    grown = False
    size = s.size
    global score
    score = 0
    #print(g.shape)
    s = np.zeros(10).reshape(2, 5)
    g[:, -1] = 1
    g[-1, :] = 1
    g[:, 0] = 1
    g[0,:] = 1
    for i in range (5):
        #print (i)
        g[20,(20 +i)] = 1
        s[0,i] = 20
        s[1,i] = (20 + i)
        #print("s x" + str(s[0, i]))
        #print("s y" + str(s[1, i]))
    Food() # generates the food
    
    state_init1 = agent.get_state(g, s, foodPos, direction)  # [0 0 0 0 0 0 0 0 0 1 0 0 0 1 0 0]
    action = [1, 0, 0]
    distX = abs(s[0, -1] - foodPos[0])
    distY = abs(s[1, -1] - foodPos[1])
    Move(action)
    state_init2 = agent.get_state(g, s, foodPos, direction)
    grown = size < (s.size) #finds if the player has eaten
    reward1 = agent.set_reward(grown, crash, (distX> abs(s[0,-1] - foodPos[0])), (distY> abs(s[1,-1] - foodPos[1])))
    grown = False
    agent.remember(state_init1, action, reward1, state_init2, crash)
    agent.replay_new(agent.memory)
    
        
def West():            
    global s
    global g
    row = int(s[0,-1])
    col = int(s[1,-1])
    
    
    if (g[row, (col - 1)] == 1):
        Fail()
    
    elif (g[row, (col - 1)] == 2):
        g[row, (col - 1)] = 1
        s = np.append(s, [[row], [(col - 1)]], axis = 1)
        Food()
        
    elif (g[row, (col - 1)] == 0):
        g[row, (col - 1)] = 1
        s = np.append(s, [[row], [(col - 1)]], axis = 1)
        row = int(s[0,0])
        col = int(s[1,0])
        g[row, col] = 0 #position of the end of the tail
        
        s = np.delete(s, 0, 1)#deletes the first column in the array

def East():
    global s
    global g
    row = int(s[0,-1])
    col = int(s[1,-1])
    
    if (g[row, (col + 1)] == 1):
        Fail()
    
    elif (g[row, (col + 1)] == 2):
        g[row, (col + 1)] = 1
        s = np.append(s, [[row], [(col + 1)]], axis = 1)
        Food()
        
    elif (g[row, (col + 1)] == 0):
        g[row, (col + 1)] = 1
        s = np.append(s, [[row], [(col + 1)]], axis = 1)
        row = int(s[0,0])
        col = int(s[1,0])
        g[row, col] = 0 #position of the end of the tail
        
        #s = np.append(s, [[row], [(col + 1)]], axis = 1)
        s = np.delete(s, 0, 1)#deletes the first column in the array
        
def North():            
    global s
    global g
    row = int(s[0,-1])
    col = int(s[1,-1])
    
    if (g[(row - 1), col] == 1):
        Fail()

    elif (g[(row - 1), col] == 2):
        g[(row - 1), col] = 1
        s = np.append(s, [[(row - 1)], [col]], axis = 1)
        Food()
        
    elif (g[(row - 1), col] == 0):
        g[(row - 1), col] = 1
        s = np.append(s, [[(row - 1)], [col]], axis = 1)
        row = int(s[0,0])
        col = int(s[1,0])
        g[row, col] = 0 #position of the end of the tail
            
        s = np.delete(s, 0, 1)#deletes the first column in the array
    
def South():            
    global s
    global g
    row = int(s[0,-1])
    col = int(s[1,-1])
    
    if (g[(row + 1), col] == 1):
        Fail()
    
    elif (g[(row + 1), col] == 2):
        g[(row + 1), col] = 1
        s = np.append(s, [[(row + 1)], [col]], axis = 1)
        Food()
        
    elif (g[(row + 1), col] == 0):
        g[(row + 1), col] = 1
        s = np.append(s, [[(row + 1)], [col]], axis = 1)
        row = int(s[0,0])
        col = int(s[1,0])
        g[row, col] = 0 #position of the end of the tail
        
        s = np.delete(s, 0, 1) #deletes the first column in the array
        
def Move(action):
    global direction
    if (action[0]==1 and action[1]==0 and action[2]==0): # turns left
        if (direction == "east"):
            direction = "north" 
            North()
        elif (direction == "north"):
            direction = "west"
            West()
        elif (direction == "west"):
            direction = "south"
            South()
        elif (direction == "south"):
            direction = "east"
            East()
    elif (action[0]==0 and action[1]==0 and action[2]==1): # turns right
        if (direction == "east"):
            direction = "south"
            South()
        elif (direction == "south"):
            direction = "west"
            West()
        elif (direction == "west"):
            direction = "north"
            North()
        elif (direction == "north"):
            direction = "east"
            East()
    else: # continues in the same direction
        if (direction == "east"):
            East()
        elif (direction == "north"):
            North()
        elif (direction == "west"):
            West()
        elif (direction == "south"):
            South()
    
        
def Display(g):
    
    gameDisplay.fill((0,0,0))
    for i in range (80):
        for j in range (100):
            if (g[i,j] == 1):
                pygame.draw.rect(gameDisplay,(0,255,0),((j*10), (i*10), 10, 10), True)
            elif (g[i,j] == 0):
                pygame.draw.rect(gameDisplay,(0,0,0),((j*10), (i*10), 10, 10), True)
            elif (g[i,j] == 2):
                pygame.draw.rect(gameDisplay,(255,0,0),((j*10), (i*10), 10, 10), True)    
    pygame.display.update()
    pygame.time.delay(1)
    
def Fail():
    global gameRunning
    global crash
    global score
    #gameRunning = 0
    crash = True
    #print ("failed, you hit the tail")
    #score-=400
    #print (score)



'''
def GraphInit():
    plt.ion()
    
    plt.xlabel("games count")
    plt.ylabel("game score")
    
    
    

def GraphUpdate(x, y):
    
    ax = plt.axes()
    ax.set_xlim(0, np.max(x) + 1)
    ax.set_ylim(0, np.max(y) + 1)
    
    ax.scatter(x, y)

'''
def plot_seaborn(array_counter, array_score):
    sns.set(color_codes=True)
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        color="b",
        x_jitter=.1,
        line_kws={'color': 'green'}
    )
    ax.set(xlabel='games', ylabel='score')
    plt.show()


def run():
    global direction
    global crash
    global g
    global s
    global foodPos
    global grown
    global score
    size = s.size
    pygame.init()
    agent = DQNAgent()
    counter_games = 0
    #GraphInit()
    score_plot = []
    counter_plot =[]
    #record = 0
    display_option = False # selects whether to show the display

    while counter_games < 150:
        # Initialize classes
        SnakeInit(agent)
        # Perform first move
        
        #if display_option:
        #    display(player1, food1, game, record)

        while not crash:
            agent.epsilon = 80 - counter_games #sets the rate at which randomness is reduced
            
            #get old state
            state_old = agent.get_state(g, s, foodPos, direction)
            
            #perform random actions based on agent.epsilon, or choose the action
            if randint(0, 200) < agent.epsilon:
                final_move = to_categorical(randint(0, 2), num_classes=3)
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old.reshape((1,11)))
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=3)
                
            #perform new move and get new state
            distX = abs(s[0, -1] - foodPos[0])
            distY = abs(s[1, -1] - foodPos[1])#check for reward if snake moves closer to food
            Move(final_move)
            state_new = agent.get_state(g, s, foodPos, direction)
            grown = (size > s.size)
            
            #set treward for the new state
            reward = agent.set_reward(grown, crash, (distX> abs(s[0,-1] - foodPos[0])), (distY> abs(s[1,-1] - foodPos[1])))
            grown = False
            #train short memory base on the new action and state
            agent.train_short_memory(state_old, final_move, reward, state_new, crash)
            
            # store the new data into a long term memory
            agent.remember(state_old, final_move, reward, state_new, crash)
            #record = get_record(game.score, record)
            
            if display_option: # shows player screen if display option is set to True
                Display(g)
                        
        agent.replay_new(agent.memory)
        counter_games += 1
        #GraphUpdate(counter_games, score)
        
        #print('Game', counter_games, '      Score:', game.score)
        score_plot.append(score)
        counter_plot.append(counter_games)
        print(score)
    agent.model.save_weights('weights.hdf5')
    plot_seaborn(counter_plot, score_plot)


run()

pygame.quit()
quit()
 


