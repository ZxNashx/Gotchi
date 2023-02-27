
import numpy, sys, pymunk, random
from utils import *
import pygame
from pygame.locals import *
import pymunk.pygame_util


class StartGame(Button):
    def __init__(self, pos, size, text):
        Button.__init__(self, pos, size, text)
        self.game = False
        self.gameObj = 0
    def update(self,data):
        Button.update(self,data)
        if not self.gameObj == 0:
            if self.gameObj.done:
                self.game = False
                for i in data[3]:
                    if i.getType() == "GameButton":
                        data[3].remove(i)

    def process(self,data):
        self.lastTime = data[4]
        if self.busy:
            return
        else:
            self.busy = True
            self.color = (16,39,145)
            if self.game == False:
                self.game = True
                self.gameObj = ttt_game(data)

class GameButton(Button):
    def __init__(self, pos,id, size=[300,100], state="-"):
        Button.__init__(self, pos, size, text=state)
        self.state = state
        self.id = id
        self.game = 0

    def update(self, data):
        self.game = data[3][4].gameObj
        Button.update(self,data)
        self.text = self.state
        if (self.game.checkWinner() == "-1" or self.game.checkWinner() == "-2" or self.game.checkWinner() == "-3") and self.game.done == False:
            self.game.done = True
            print("Game Over.")
            if data[3][4].gameObj.checkWinner() == "-1":
                print("Player Won")
                data[3][1].comment("Awe, I was so close!")
                data[3][1].addXp(5)
            elif data[3][4].gameObj.checkWinner() == "-2":
                data[3][1].addXp(8)
                data[3][1].comment("Aha, I win!")
                print("AI won")
            else:
                data[3][1].addXp(10)
                data[3][1].comment("Close match!")
                print("Tie")
    def changeState(self,m):
        self.state = m
    def process(self,data):
        self.lastTime = data[4]
        if self.busy:
            return
        else:
            self.busy = True
            self.color = (16,39,145)
            self.game.buttonPressed(self,data)
    def getType(self):
        return "GameButton"


class ttt_game():
    def __init__(self,data):
        self.turn = 0
        self.done = False
        self.moves = []
        self.board = ["1","2","3",
                      "4","5","6",
                      "7","8","9"
                      ]
        col1x, col2x, col3x = 10,320,630
        row1y, row2y, row3y = 10,120,230
        self.buttons = [GameButton([col1x,row1y],1), GameButton([col2x,row1y],2), GameButton([col3x,row1y],3),
                        GameButton([col1x,row2y],4), GameButton([col2x,row2y],5), GameButton([col3x,row2y],6),
                        GameButton([col1x,row3y],7), GameButton([col2x,row3y],8), GameButton([col3x,row3y],9)
                        ]
        for i in self.buttons:
            data[3].append(i)
        #-1 for PLAYER taken and -2 for AI taken
    def replace(self, n, rep):
        #finds n on the board and replaces it with rep, which should be -1 or -2 based on the players info
        for i in self.board:
            if i == n:
                self.board[self.board.index(i)] = rep
    def checkPlace(self,pos):
        #pos is the place on the board, 1-9
        if int(self.board[pos-1]) > 0:
            return True
        return False
    def buttonPressed(self,button,data):
        if self.checkPlace(button.id):
            pass
        else:
            return
        self.replace(str(button.id), "-1")
        button.changeState("X")

        #AI code should go here.
        if int(self.checkWinner()) > 0:
            pass
        else:
            return
        choice = random.randint(1,9)
        while self.checkPlace(choice) == False:
            choice = random.randint(1,9)
        for i in data[3]:
            if i.getType() == "GameButton":
                if i.id == choice:
                    self.replace(str(choice), "-2")
                    i.changeState("O")
                    return
                


    def checkWinner(self):
        #see if someone has won the game
        #first check is -1
        run = True
        while run:
            if self.board[0] == "-1":
                if self.board[3] == "-1":
                    if self.board[6] == "-1":
                        return "-1"
                if self.board[1] == "-1":
                    if self.board[2] == "-1":
                        return "-1"

            if self.board[1] == "-1":
                if self.board[4] == "-1":
                    if self.board[7] == "-1":
                        return "-1"
            if self.board[2] == "-1":
                if self.board[5] == "-1":
                    if self.board[8] == "-1":
                        return "-1"

            if self.board[3] == "-1":
                if self.board[4] == "-1":
                    if self.board[5] == "-1":
                        return "-1"
            if self.board[6] == "-1":
                if self.board[7] == "-1":
                    if self.board[8] == "-1":
                        return "-1"

            if self.board[2] == "-1":
                if self.board[4] == "-1":
                    if self.board[6] == "-1":
                        return "-1"
            if self.board[0] == "-1":
                if self.board[4] == "-1":
                    if self.board[8] == "-1":
                        return "-1"
            #end of player -1 and start of player -2
            if self.board[0] == "-2":
                if self.board[3] == "-2":
                    if self.board[6] == "-2":
                        return "-2"
                if self.board[1] == "-2":
                    if self.board[2] == "-2":
                        return "-2"

            if self.board[1] == "-2":
                if self.board[4] == "-2":
                    if self.board[7] == "-2":
                        return "-2"
            if self.board[2] == "-2":
                if self.board[5] == "-2":
                    if self.board[8] == "-2":
                        return "-2"

            if self.board[3] == "-2":
                if self.board[4] == "-2":
                    if self.board[5] == "-2":
                        return "-2"
            if self.board[6] == "-2":
                if self.board[7] == "-2":
                    if self.board[8] == "-2":
                        return "-2"

            if self.board[2] == "-2":
                if self.board[4] == "-2":
                    if self.board[6] == "-2":
                        return "-2"
            if self.board[0] == "-2":
                if self.board[4] == "-2":
                    if self.board[8] == "-2":
                        return "-2"
            highest = -10
            for i in self.board:
                i = int(i)
                if i > highest:
                    highest = i
            if highest < 0:
                return "-3" # tie
            run = False
        return "1"


#start of basketball code...

class BasketBallButton(Button):
    def __init__(self, pos, size, text):
        Button.__init__(self, pos, size, text)
        self.isGame = False
        self.game = 0

        
    def draw(self,screen):
        Button.draw(screen)
    def getType(self):
        return "BasketBallButton"
    def draw(self,screen):
        if self.isGame:
            self.game.draw(screen)
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        screen.blit(self.textS,self.pos)


    def endGame(self):
        self.isGame = False
    def update(self,data):
        Button.update(self,data)
        if self.isGame:
            self.game.update(data)
            self.text = "Back"
        else:
            self.text = "BBall"
    def process(self,data):
        character = data[3][1]
        self.lastTime = data[4]
        if self.busy:
            return
        else:
            self.busy = True
            self.color = (16,39,145)
            if self.isGame == False:
                self.game = BasketBallGame(data)
                self.isGame = True
            else:
                self.endGame()
            


#physics setup for basketball game thing
class Physics():
    def __init__(self,screen):
        #physics pymunk stuff
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.objects = []
        self.ground()
    def applyForce(self,force=(0,0)):
        for obj in self.objects:
            y = 600 - obj.body.position.y
            force = (force[0] - obj.body.position.x, (force[1] - y) * -2)
            print("Force Applied: "+str(force))
            obj.body.apply_impulse_at_local_point(force)

    def add_ball(self,space,x,y):
        mass = 1
        radius = 14
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0,0))

        space.add(body, shape)
        return shape

    #creating a ball thing
    def ball(self,x,y):
        #THE BALL POSITION STARTS FROM THE BOTTOM NOT THE TOP
        print("Ball Made")
        self.objects.append(self.add_ball(self.space,x,y))
    def ground(self):
        ### walls
        static_body = self.space.static_body
        static_lines = [pymunk.Segment(static_body, (-5.0, 100.0), (2000.0, 100.0), 10.0)]
        for line in static_lines:
            line.elasticity = 2
            line.friction = 1
        self.space.add(static_lines)
    def remove(self):
        objects_to_remove = []
        for obj in self.objects:
            if obj.body.position.y < -100:
                objects_to_remove.append(obj)

        for obj in objects_to_remove:
            self.space.remove(obj, obj.body)
            self.objects.remove(obj)
            print("Ball removed")
            self.ball(600,400)
    def updatePhysics(self,fps):
        self.remove()
        self.space.step(1/fps)
    def getType(self):
        return "PhysicsEngine"
    def update(self,data):

       # for i in self.objects:
         #   print(i)
         #   print("OBJ x: "+str(i.body.position.x))
         #   print("OBJ y: "+str(i.body.position.y))
        self.updatePhysics(data[5])
    def draw(self,screen):
        screen.fill((25,25,25))
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(screen))

  

class BasketBallGame(Physics):
    def __init__(self,data):
        Physics.__init__(self,data[2])
        self.score = 0
        self.ball(600,400)
        self.mouseTicks = 30
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
    def update(self,data):
        self.checkPress(data)
        self.updatePhysics(data[5])
    def checkPress(self,data):
        if self.mouseTicks < 90:
            self.mouseTicks += 1
        else:
            if pygame.mouse.get_pressed()[0] == 1:
                self.mouseTicks = 0
                self.shoot(data)
    def shoot(self,data):
        mPos = data[0]
        self.applyForce((mPos[0], mPos[1]))
        data[3][1].addXp(10)
    def draw(self,screen):
        screen.fill((25,25,25))
        self.space.debug_draw(pymunk.pygame_util.DrawOptions(screen))
        textS = self.myfont.render("Tick till next throw: "+str((self.mouseTicks-90)*-1), False, (0, 0, 0))
        screen.blit(textS,(10,450))