from audioop import reverse
import enum
import math
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

#class Position():
#    def __init__(self,i,j):
#        self.posi = i 
#        self.posj = j 


def getDistance(x1,y1,x2,y2):
    return round(math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)) *100) /100

class TableGame:
    def __init__(self):
        self.table = [];
        self.heuristic = [];
    def initTable(self):
        for i in range(0,row):
            temp =[]
            for j in range(0,column):
                temp.append(0);
            self.table.append(temp)

        for i in range(0,row):
            temp =[]
            for j in range(0,column):
                temp.append(0);
            self.heuristic.append(temp)

    def UpdateTable(self,posi,posj):
        if(self.table[posi][posj] == 2):
            self.table[posi][posj] = 0

    def checkWin(self):
        for i in range(0,row):
            for j in range(0,column):
                if (self.table[i][j] == 2):
                    return False
        return True
    def UpdateHeuristicTable(self,posi,posj):
        for i in range(0,row):
            for j in range(0,column):
                self.heuristic[i][j] = getDistance(i,j,posi,posj);

    def findFoodNearest(self,posi,posj):
        nearestFood = 100000
        ifood=0
        jfood=0
        for i in range(0,row):
            for j in range (0,column):
                if self.table[i][j] == 2 and nearestFood  > getDistance(posi,posj,i,j):
                    ifood = i
                    jfood = j
                    nearestFood = getDistance(posi,posj,i,j)

        return [ifood,jfood]
        
    def A_star_Lv1(self):
        result = []
        Queue = []
        pfood = self.findFoodNearest(pacman.posi,pacman.posj)
        self.UpdateHeuristicTable(pfood[0],pfood[1])
        visited =[]
        for i in range(0,row):
            temp = []
            for j in range (0,column):
                temp.append(0)
            visited.append(temp)
        pacmanpos = [pacman.posi,pacman.posj]
        visited[pacman.posi][pacman.posj] =1
        print(pfood," ")
        result.append(pacmanpos)
        while True:
            if(len(Queue)!=0):
                pos = Queue[0]
                pos.pop(2) #delete weight
                pacmanpos = pos
                result.append(pacmanpos)
                Queue.pop(0)
                if pacmanpos[0] == pfood[0] and pacmanpos[1] == pfood[1]:
                    break
            connectdirection = PositionCanGoUp(pacmanpos[0],pacmanpos[1])
            #add weight for sort
            for i in range (0,len(connectdirection)):
                if(visited[connectdirection[i][0]][connectdirection[i][1]] == 0):
                    connectdirection[i].append(self.heuristic[connectdirection[i][0]][connectdirection[i][1]])
                    Queue.append(connectdirection[i])
                    visited[connectdirection[i][0]][connectdirection[i][1]] =1 
            Queue = sorted(Queue,key = lambda item: item[2],reverse = False)
        #result.append(DirectionCanGoUp(pacman.posi,pacman.posj)[random.randint(0,len(DirectionCanGoUp(pacman.posi,pacman.posj)) -1)])
        print(result)


        return ConvertDirection(result)


def ConvertDirection(pos):
    direction =[]
    i = len(pos) - 1
    while(i!=0):
        j = 1
        t = -1
        while(t == -1):
            t= DirectionFromTo(pos[i-j],pos[i])
            if (t!=-1 and t in DirectionCanGoUp(pos[i-j][0],pos[i-j][1])):
                i = i-j
                direction.insert(0,t)
            else: t=-1
            j+=1

    return direction


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
            if len(self.direction_queue) == 0:
                if(Map.table[self.posi][self.posj] == 2):
                    Map.table[self.posi][self.posj] =0
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

        #A* here. the path is insert to the direction_queue
        self.direction_queue = Map.A_star_Lv1();
        

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

def DirectionFromTo(pos1,pos2):
    if(pos1[0] - pos2[0]) == 1 and pos1[1] == pos2[1]:
        return UP
    if(pos1[0] - pos2[0]) == -1 and pos1[1] == pos2[1]:
        return DOWN
    if(pos1[1] - pos2[1]) == 1 and pos1[0] == pos2[0]:
        return LEFT
    if(pos1[1] - pos2[1]) == -1 and pos1[0] == pos2[0]:
        return RIGHT
    else: 
        return -1

def DirectionCanGoUp(posi,posj):
    direction =[]
    if posj != column -1 and wall.vertical_wall[posi][posj] == 0: 
        direction.append(RIGHT)
    if posj != 0 and wall.vertical_wall[posi][posj-1] == 0: 
        direction.append(LEFT)
    if posi != 0 and wall.horizental_wall[posi -1][posj] == 0: 
        direction.append(UP)
    if posi != row -1  and wall.horizental_wall[posi][posj] == 0: 
        direction.append(DOWN)

    return direction

def PositionCanGoUp(posi,posj):
    result =[]
    direction = DirectionCanGoUp(posi,posj);
    for i in range(0,len(direction)):
        if direction[i] == LEFT:
            result.append([posi,posj - 1])
        elif direction[i] == RIGHT:
            result.append([posi,posj+1])
        elif direction[i] == UP:
            result.append([posi -1,posj])
        elif direction[i] == DOWN:
            result.append([posi +1,posj])
    return result

isplay = True

while True:
    wall = Wall()
    pacman = PacMan()
    Map = TableGame()
    readFile("map2.txt",wall)
    Map.UpdateHeuristicTable(3,4)
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