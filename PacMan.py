import enum
from re import L
from tkinter import VERTICAL, Widget
import pygame,sys,random
from pygame.locals import*


pygame.init()
width = 1280
height = 700
clock = pygame.time.Clock();
FPS = 60;
column = 7;
row = 4;
x_root = 0;
y_root = 0

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

width_wall = 10
radius_wall = 5 
width_rec = 45

class TableGame:
    def __init__(self):
        self.table = [];
    def initTable(self):
        for i in range(0,row):
            temp =[]
            for j in range(0,column):
                temp.append(0);
            self.table.append(temp)

    def UpdateTable(self,posi,posj):
        if(self.table[posi][posj] == 2):
            self.table[posi][posj] = 0

    def checkWin(self):
        for i in range(0,row):
            for j in range(0,column):
                if (self.table[i][j] == 2):
                    return False
        return True



class PacMan:
    def __init__(self):
        self.posi = 1
        self.posj = 0
        self.posx = 0
        self.posy = 0
        self.v = 3
        self.step = width_rec;
        self.pacman_image = pygame.transform.scale(pygame.image.load("pacman.png"),(width_rec/2,width_rec/2))

        #self.map = []
        self.direction_queue =[]
    #def initPacMan(self):
    #    self.direction_queue.append(UP)
    #    

    def drawPacMan(self):
        screen.blit(self.pacman_image,(width_rec*self.posj + width_rec/4 +x_root + self.posx,width_rec*self.posi + width_rec/4+y_root+self.posy))
        self.move()

    def move(self):
        if self.step == width_rec:
            if(len(self.direction_queue) != 0):
                if self.direction_queue[0] == LEFT: self.posj -= 1
                elif self.direction_queue[0] == RIGHT: self.posj += 1
                elif self.direction_queue[0] == UP: self.posi -= 1
                elif self.direction_queue[0] == DOWN: self.posi += 1
                self.direction_queue.pop(0)
            self.UpdateDirectionQueue()
            self.posx = self.posy = 0
            self.step = 0;

        if self.direction_queue[0] == LEFT:
            self.posx -= self.v
        elif self.direction_queue[0] == RIGHT:
            self.posx +=self.v
        elif self.direction_queue[0] == UP:
            self.posy -=self.v
        else:
            self.posy+=self.v

        self.step+=self.v;

    def UpdateDirectionQueue(self):
        direction = DirectionCanGoUp()
        self.direction_queue.append(direction[random.randint(0,len(direction) -1)])
        

class Wall:
    def __init__(self):
        self.horizental_wall = []
        self.vertical_wall = []
    def init_wall(self):
        for i in range(0,row):
            temp = []
            for j in range(0,column-1):
                temp.append(0)
            self.vertical_wall.append(temp)

        for i in range(0,row -1):
            temp = []
            for j in range(0,column):
                temp.append(0)
            self.horizental_wall.append(temp)
    def drawWall(self):
        pygame.draw.rect(screen,(0,38,230),(width/2 - column * width_rec/2,height/2-row*width_rec/2,column*width_rec,row*width_rec),width_wall,radius_wall)
        for i in range(0,row):
            for j in range(0,column-1):
                if self.vertical_wall[i][j] == 1:
                    ystart = width_rec*i + y_root-3
                    yend = width_rec*(i+1) +y_root+3
                    if i == 0: ystart = width_rec*i + y_root
                    if i == row -1: yend = width_rec*(i+1) +y_root -1
                    pygame.draw.line(screen,(0,38,230),(width_rec*(j+1)+x_root,ystart),(width_rec*(j+1) +x_root,yend),width_wall)
    
        for i in range(0,row-1):
            for j in range(0,column):
                if self.horizental_wall[i][j] == 1:
                    xstart = width_rec*j+x_root-3
                    xend = width_rec*(j+1) +x_root+4
                    if j == 0: xstart = width_rec*j+x_root
                    if j == column-1: xend = width_rec*(j+1) +x_root -1
                    pygame.draw.line(screen,(0,38,230),(xstart,width_rec*(i+1) + y_root),(xend,width_rec*(i+1) +y_root),width_wall)

screen = pygame.display.set_mode((width, height),pygame.RESIZABLE)
pygame.display.set_caption("Pacman")

def drawFood():
    for i in range(0,row):
        for j in range(0,column):
            if(Map.table[i][j] == 2):
                pygame.draw.circle(screen,(0,38,230),(width_rec*j +width_rec/2 +x_root,width_rec*i+ width_rec/2 +y_root),10)

def draw(wall):
    screen.fill((0,0,0));
    wall.drawWall()
    drawFood()
    pacman.drawPacMan();

def readFile(filename,wall):
    global row,column
    f = open(filename,'r')
    data = f.read()
    data = data.split("\n\n")

    #reading information for table
    column = int(data[0][data[0].find(" ")+1:])
    row = int(data[0][0:data[0].find(" ")])

    t =data[1].split("\n")
    Map.initTable()
    for i in range(0,row):
        for j in range(0,column):
            Map.table[i][j] = int(t[i][j*2])



    # #reading information for wall
    vertical_wall = data[3]
    horizeltal_wall = data[2]
    wall.init_wall()

    vertical_wall = vertical_wall[vertical_wall.find("\n"):]
    vertical_wall = vertical_wall.replace("\n"," ")
    vertical_wall = vertical_wall.replace(" ","")

    for i in range(0,len(vertical_wall)):
        wall.vertical_wall [i//(column -1)][i% (column -1)] = int(vertical_wall[i]);

    horizeltal_wall = horizeltal_wall[horizeltal_wall.find("\n"):]
    horizeltal_wall = horizeltal_wall.replace("\n"," ")
    horizeltal_wall = horizeltal_wall.replace(" ","")
    for i in range(0,len(horizeltal_wall)):
        wall.horizental_wall [i//column][i% column] = int(horizeltal_wall[i]);

    
    #reading information for pacman
    pacman.posi = int(data[4][0])
    pacman.posj = int(data[4][2])

def DirectionCanGoUp():
    direction =[]
    if pacman.posj != column -1 and wall.vertical_wall[pacman.posi][pacman.posj] == 0: 
        direction.append(RIGHT)
    if pacman.posj != 0 and wall.vertical_wall[pacman.posi][pacman.posj-1] == 0: 
        direction.append(LEFT)
    if pacman.posi != 0 and wall.horizental_wall[pacman.posi -1][pacman.posj] == 0: 
        direction.append(UP)
    if pacman.posi != row -1  and wall.horizental_wall[pacman.posi][pacman.posj] == 0: 
        direction.append(DOWN)

    return direction

isplay = True

while True:
    wall = Wall()
    pacman = PacMan()
    Map = TableGame()
    readFile("map2.txt",wall)
    while isplay:
        Map.UpdateTable(pacman.posi,pacman.posj)
        if (Map.checkWin()):
            isplay =False
        width,height = screen.get_size()
        x_root =  width/2 - column* width_rec/2
        y_root = height/2-row*width_rec/2
        draw(wall)
        #print(DirectionCanGoUp())
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit();
                sys.exit();
        clock.tick(FPS)
        pygame.display.update()

    isplay = True