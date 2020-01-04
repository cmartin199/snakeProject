#SETUP
import pygame
import numpy as np
import random
pygame.init()
gameDisplay = pygame.display.set_mode((1000,800))
pygame.display.set_caption('snake')

g = np.zeros(100*80).reshape(80, 100)
s = np.zeros(10).reshape(2, 5)
direction = "east" 
score = 0 

#THE USER DOES SOMETHING TO START THE GAME.

gameRunning = 1

def Food():
    global score
    block = 0
    while (block == 0):
        row = random.randint(0,79)
        column = random.randint(0, 99)
        if (g.item(row, column) == 0):
            g[row, column] = 2
            #print ("test row  ")
            #g.item(row, column)
            block = 1
            score += 1
            

def SnakeInit():
    global g
    g = np.append(g,np.ones[79] , axis = 1)
    g = np.append(g,np.ones[100] , axis = 0)
    for i in range (5):
        #print (i)
        g[20,(20 +i)] = 1
        s[0,i] = 20
        s[1,i] = (20 + i)
        print("s x" + str(s[0, i]))
        print("s y" + str(s[1, i]))
    Food()
    #g[20,(20)] = 1
    #s[0,0] = 20
    #s[1,0] = (20)
       # print("s x" + str(s[0, i]))
       # print("s y" + str(s[1, i]))
        
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
        g[ row, col] = 0 #position of the end of the tail
        
        #s = np.append(s, [[row], [(col + 1)]], axis = 1)
        s = np.delete(s, 0, 1)#deletes the first column in the array
    
    #else:
        #Fail()
        
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
    
    #else:
       # Fail()

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
        
    #else:
    #    Fail()


def Fail():
    global gameRunning
    gameRunning = 0
    print ("failed, you hit the tail")
    




SnakeInit()
#THE GAME LOOP.
while (gameRunning == 1):
    #HANDLE EVENTS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                gameRunning = False
            if event.key == pygame.K_a:
                #cycles counter-clockwise through the directions
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
                    
            if event.key == pygame.K_d:
                #cycles clockwise through the directions
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
    else:
        #continues moving in same direction with no key press
        if (direction == "south"):
            South()
        elif (direction == "west"):
            West()
        elif (direction == "north"):
            North()
        elif (direction == "east"):
            East()



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
    pygame.time.delay(90)
        

#CLEAN UP WHEN FINISHED.
pygame.quit()
quit()



