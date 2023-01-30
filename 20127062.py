from random import choice
import numpy as np
import pygame
import sys
from pygame.locals import *
#initialize pygame
pygame.init()
black = 0,0,0
red = 255,0,0
blue = 0,0,255
white = 255,255,255
cyan = 0,255,255
screensize = w, h = 700,700
screen = pygame.display.set_mode(screensize)
screen.fill(white)

class Game:
    def __init__(self,size):
        self.size = size
        self.board = np.zeros((size,size),dtype="int")
        players = ['human','AI']
        self.turn = choice(players)
        # self.turn = 'AI'
        self.turn = 'human'
        if self.turn == 'human':
            print('human 1st')
            print('AI 2nd')
            self.order = [1,2]
        else:
            self.order = [2,1]
            print('AI 1st')
            print('human 2nd')
        self.winningPos = []
        if size == 5:
            #horizontal
            for i in range(0,21,5):
                for j in range(2):
                    k = i+j
                    self.winningPos.append([k,k+1,k+2,k+3])
            #vertical
            for i in range(10):
                self.winningPos.append([i,i+5,i+10,i+15])
            #diagonal
            for i in range(0,6,5):
                for j in range(2):
                    k = i+j
                    self.winningPos.append([k,k+6,k+12,k+18])
            for i in range(15,21,5):
                for j in range(2):
                    k = i+j
                    self.winningPos.append([k,k-4,k-8,k-12])

    def isValid(self,x,y):
        if x < 0 or x > self.size-1 or y < 0 or y > self.size-1 or self.board[x][y] != 0:
            return False
        else:
            return True

    def gameOver(self):
        board = self.board
        if self.size == 3:
            if board[0][0] != 0 and board[0][0] == board[0][1] == board[0][2]:
                return board[0][0]
            if board[1][0] != 0 and board[1][0] == board[1][1] == board[1][2]:
                return board[1][0]
            if board[2][0] != 0 and board[2][0] == board[2][1] == board[2][2]:
                return board[2][0]
            if board[0][0] != 0 and board[0][0] == board[1][0] == board[2][0]:
                return board[0][0]
            if board[0][1] != 0 and board[0][1] == board[1][1] == board[2][1]:
                return board[0][1]
            if board[0][2] != 0 and board[0][2] == board[1][2] == board[2][2]:
                return board[0][2]
            if board[0][0] != 0 and board[0][0] == board[1][1] == board[2][2]:
                return board[0][0]
            if board[0][2] != 0 and board[0][2] == board[1][1] == board[2][0]:
                return board[0][2]
            for i in range(0,3):
                for j in range(0,3):
                    if (board[i][j] == 0):
                        return -1
        else: #size = 5
            #horizontal
            for i in range(0,5):
                if board[i][1] != 0 and (board[i][0] == board[i][1] == board[i][2] == board[i][3] or board[i][1] == board[i][2] == board[i][3] == board[i][4]):
                    return board[i][1]
            #vertical
            for i in range(0,5):
                if board[1][i] != 0 and (board[0][i] == board[1][i] == board[2][i] == board[3][i] or board[1][i] == board[2][i] == board[3][i] == board[4][i]):
                    return board[1][i]
            #diagonal 1 00 11 22 33 | 01 12 23 34
            for i in range (0,2):
                if board[0][i] != 0:
                    for j in range (1,4):
                        if board[j][j+i] != board[0][i]:
                            break
                        if j == 3:
                            return board[0][i]
            #diagonal 2  10 21 32 43 | 11 22 33 44
            for i in range (-1,1):
                if board[1][1+i] != 0:
                    for j in range (2,5):
                        if board[j][j+i] != board[1][1+i]:
                            break
                        if j == 4:
                            return board[1][1+i]
            #diagonal 3 30 21 12 03 | 40 31 22 13
            for i in range (3,5):
                if board[i][0] != 0:
                    for j in range(1,4):
                        if board[i-j][j] != board[i][0]:
                            break
                        if j == 3:
                            return board[i][0]
            #diagonal 4 31 22 13 04 | 41 32 23 14
            for i in range(4,6):
                if board[i-1][1] != 0:
                    for j in range(2,5):
                        if board[i-j][j] != board[i-1][1]:
                            break
                        if j == 4:
                            return board[i-1][1]
            #not over
            for i in range(0,5):
                for j in range(0,5):
                    if (board[i][j] == 0):
                        return -1
        return 0
    #alpha-beta-pruning:
    def maxab(self,a,b,depth):
        state = -np.Inf
        board = self.board
        turn = self.order[1]
        end = self.gameOver()
        x = y = None

        if self.size == 3:
            if end == self.order[1]:
                return (1,0,0)
            if end == self.order[0]:
                return (-1,0,0)
        if end == 0:
            return (0,0,0)
        if self.size == 5 and depth == 0:
            return (self.hf(),0,0) 

        for i in range(0,self.size):
            for j in range(0,self.size):
                if board[i][j] == 0:
                    board[i][j] = turn
                    if self.size == 5 and self.gameOver() == self.order[1]:
                        board[i][j] = 0
                        return (100000,i,j)
                    (cur,t1,t2) = self.minab(a,b,depth-1)
                    if cur > state:
                        state = cur
                        x = i
                        y = j
                    board[i][j] = 0
                    a = max(state,a)
                    if a >= b:
                        return (a,x,y)
        return (state,x,y)

    def minab(self,a,b,depth):
        state = np.Inf
        board = self.board
        turn = self.order[0]
        end = self.gameOver()
        x = y = None

        if self.size == 3:
            if end == self.order[1]:
                return (1,0,0)
            if end == self.order[0]:
                return (-1,0,0)
        if end == 0:
            return (0,0,0)

        for i in range(0,self.size):
            for j in range(0,self.size):
                if board[i][j] == 0:
                    board[i][j] = turn
                    if self.size == 5 and self.gameOver() == self.order[0]:
                        board[i][j] = 0
                        return (-100000,i,j)
                    (cur,t1,t2) = self.maxab(a,b,depth-1)
                    if cur < state:
                        state = cur
                        x = i
                        y = j
                    board[i][j] = 0
                    b = min(state,b)
                    if b <= a:
                        return (b,x,y)
        return (state,x,y)
    #heuristic function
    def hf(self):
        #evaluating
        boardcopy = np.copy(self.board.ravel())
        h = 0
        for i in range(0,28):
            maxh = minh = 0
            for j in range(0,4):
                if boardcopy[self.winningPos[i][j]] == self.order[1]:
                    maxh += 1
                elif boardcopy[self.winningPos[i][j]] == self.order[0]:
                    minh += 1
            if (maxh != 0 and minh == 0) or (maxh == 0 and minh != 0):
                h += 10**maxh - 10**minh
        return h
#drawing
def drawshape(turn,x,y,indent):
    if turn == 1:
        pygame.draw.line(screen,red,(indent+x*100+10,indent+y*100+90),(indent+x*100+90,indent+y*100+10),2)
        pygame.draw.line(screen,red,(indent+x*100+10,indent+y*100+10),(indent+x*100+90,indent+y*100+90),2)
    else:
        pygame.draw.circle(screen,blue,(indent+x*100+50,indent+y*100+50),35,2)

def drawboard(size):
    boardsize = size*100
    if size == 3:
        indent = 200
    else:
        indent = 100
    for i in range(size+1):
        #horizontal
        pygame.draw.line(screen,black,(indent,indent+i*100),(indent+boardsize,indent+i*100),1)
        #vertical
        pygame.draw.line(screen,black,(indent+i*100,indent),(indent+i*100,indent+boardsize),1)
    return indent
        
#--main--
while True:
    size = int(input("Input board size (3 or 5): "))
    if size == 3 or size == 5:
        break
indent = drawboard(size)    
font = pygame.font.SysFont("Tahoma",30)
G = Game(size)
done = False
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    result = G.gameOver()

    if not done:
        if result != -1:
            if result == G.order[0]:
                text = font.render("Hooman wins",1,black)
            if result == 0:
                text = font.render("Tie",1,black)
            if result == G.order[1]:
                text = font.render("AI wins",1,black)
            textRect = text.get_rect()
            textRect.center = (350,650)
            screen.blit(text,textRect)
            done = True
            
        else:
            if G.turn == 'human':
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x = int(event.pos[0]/100)-int(indent/100)
                        y = int(event.pos[1]/100)-int(indent/100)
                    
                        if G.isValid(x,y):
                            G.board[x][y] = G.order[0]
                            drawshape(G.order[0],x,y,indent)
                            G.turn = 'AI'
                            break
            else:
                if size == 5 and G.board[2][2] == 0:
                    x = y = 2
                elif size == 5 and G.board[2][2] == G.order[0] and G.board[1][1] == 0:
                    x = y = 1
                else:
                    (value,x,y) = G.maxab(-np.Inf,np.Inf,4)
                G.board[x][y] = G.order[1]
                drawshape(G.order[1],x,y,indent)
                G.turn = 'human' 