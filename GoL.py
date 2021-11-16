import numpy as np 
import pygame 
from pygame.locals import * 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from time import sleep

SIZE = 900
RED = (255,0,0)

GRAY  = (150,150,150) 
BLACK = (255,255,255) 
YELLOW = (255,255,0) 
ORANGE = (255,165,0)
GREEN = (0,155,0)
cell_size = 20
rows = 90//2
cols = 90//2 
p = 0.3


class Agent: 
    def __init__(self, loc=(0,0)):
        self.x, self.y = loc[0], loc[1]
        self.score = 0

        self.state =  np.random.choice([1,0],p=[p,1-p]) 
        self.color = GRAY if self.state== 0 else ORANGE 
        self.next_state = None 

    def action(self):
        pass

class Env: 
    def __init__(self, n):
        self.n = n
        self.agents = {}
        self.counter = 0 

        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.font.init()
        self.myfont = pygame.font.Font('freesansbold.ttf',15) 


        self.fig,self.ax = plt.subplots()
        for i in range(rows):
            for j in range(cols):
                agent = Agent(loc=(1+ i*cell_size, 1+ cell_size*j))
                self.agents[(i,j)]  = agent

        print('number of cells : ',len(self.agents))

    def step(self):
        pass 

    def get_ids(self): 
        for i in range(self.n):
            print(i,id(self.agents[i]))

    def drawBackground(self):
        self.screen.fill(GRAY)
        cnt = 0
        for i in range(0,SIZE+1,cell_size):
            color = RED if cnt % 10 == 0 else BLACK
            pygame.draw.line(self.screen,color,(i,0),(i,SIZE))
            pygame.draw.line(self.screen,color,(0,i),(SIZE,i))
            cnt +=1
    def drawAgents(self): 
        pass 
        for agent in self.agents.values():
            rect = Rect(agent.x,agent.y,cell_size-1,cell_size-1) 
            pygame.draw.rect(self.screen,agent.color,rect) 
    
    def draw(self):
        self.drawBackground()
        self.drawAgents()
        text = self.myfont.render('{0} iterations'.format(self.counter),True,(0,0,0))
        textRec = text.get_rect()
        textRec.center = (SIZE-50,20)
 
        self.counter+=1
        self.screen.blit(text,textRec)


        
        pygame.display.flip() 
    def beforeRound(self):
        pass 

    def fullPlayRound(self):
        self.beforeRound()
        self.playRound()
        self.afterRound()

    def getBoundaries(self,i):
        l,r = i-1, i+1 
        return l,r 
    
    def initPlot(self):
        self.xdata, self.ydata = [], []
        self.ln, = plt.plot([], [], 'r')

        self.ax.set_ylim(0, rows*cols*p)
        self.ax.set_xlim(0, 550)
        return self.ln, 

    def update(self,frame):
        for event in pygame.event.get():
            if event.type ==QUIT: 
                running = False 


        #### PLAY one round...
        #self.counter +=1
        self.fullPlayRound()
        

        self.draw()

        self.xdata.append(frame)
        alivecells = np.sum([agent.state for agent in self.agents.values()])
        self.ydata.append(alivecells)
        self.ln.set_data(self.xdata, self.ydata)
        return self.ln,


    def playRound(self):
        for i in range(0,rows):
            for j in range(0,cols):
                agent = self.agents[(i,j)] 
                l,r = self.getBoundaries(i)
                u,d = self.getBoundaries(j)
                r +=1 
                d +=1

                if i == 0:
                    l = i  
                    r = i + 2
                elif i == rows-1: 
                    l = i-1
                    r = i+1
                    
                if j == 0:
                    u = j 
                    d = j + 2
                elif j == cols-1:
                    u = j-1
                    d = j+1
                    
                agent.neighbor_score = np.sum([self.agents[(ii,jj)].state for ii in range(l,r) for jj in range(u,d)]) - agent.state

                if agent.neighbor_score ==3:
                    agent.next_state = 1
                elif agent.state == 1 and agent.neighbor_score == 2: 
                    agent.next_state = 1 
                else:
                    agent.next_state = 0

    def afterRound(self):
       for i in range(0,rows):
           for j in range(0,cols):
               self.agents[(i,j)].state = self.agents[(i,j)].next_state 
               if self.agents[(i,j)].state == 1:
                   self.agents[(i,j)].color = ORANGE  
                   #if self.agents[(i,j)].neighbor_score == 3: 
                        #self.agents[(i,j)].color = GREEN
               else:
                  self.agents[(i,j)].color =  GRAY


    def simulate(self,plot=False):
        self.drawBackground()
        if plot:
            ani = FuncAnimation(env.fig, env.update, init_func=env.initPlot, blit=True)
            plt.show()

        else: 
            running = True 
            while running: 
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False 
                self.fullPlayRound()
                self.draw()
        pygame.quit()


if __name__ == '__main__': 

    pygame.init() 
    env = Env(rows*cols)
    env.simulate(False)
