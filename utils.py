
import pygame, random, time, math
from datetime import datetime as dt
from external import *
FONT = pygame.font.SysFont('Comic Sans MS', 30)
class Button():
    def __init__(self, pos, size, text):
        self.pos = pos
        self.size = size
        self.text = text
        self.myfont = FONT
        self.color = (148,177,224)
        self.busy = True
        self.lastTime = 0
        self.textS = self.myfont.render(self.text, False, (0, 0, 0))
    def process(self,data):
        print("This button has no process.")
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        screen.blit(self.textS,self.pos)
    def update(self, data):
        self.textS = self.myfont.render(self.text, False, (0, 0, 0))
        mPos, isPressed, screen, c = data[0], data[1], data[2], data[3]
        if data[4] > self.lastTime + 0.5:
            self.busy = False
        if self.busy == False:
            self.color = (148,177,224)
        #Pos[0] is the X
        #Pos[1] is the Y
        if isPressed:
            x,y = mPos
            #print("Mouse X: "+str(x))
            #print("Mouse Y: "+str(y))
            if x >= self.pos[0] and x <= (self.size[0] + self.pos[0]):
                if y >= self.pos[1] and y <= (self.size[1] + self.pos[1]):
                    self.process(data)
    def getType(self):
        return "DefaultButton"


class FeedButton(Button):
    def __init__(self, pos, size, text):
        Button.__init__(self, pos, size, text)
    def getType(self):
        return "FeedButton"
    def update(self,data):
        Button.update(self,data)
    def process(self,data):
        character = data[3][1]
        self.lastTime = data[4]
        if self.busy:
            return
        else:
            self.busy = True
            if data[3][1].actions > 0:
                data[3][1].feed()
                data[3][1].actions -= 1
            else:
                return "No action points"
            self.color = (16,39,145)


class LightButton(Button):
    def __init__(self, pos, size, text):
        Button.__init__(self, pos, size, text)
    def getType(self):
        return "LightButton"
    def update(self,data):
        Button.update(self,data)
    def process(self,data):
        self.lastTime = data[4]
        if self.busy:
            return
        else:
            self.busy = True
            self.color = (16,39,145)
            print(data[3][1].light(data))

class NeedleButton(Button):
    def __init__(self, pos, size, text):
        Button.__init__(self, pos, size, text)
    def getType(self):
        return "NeedleButton"
    def update(self,data):
        Button.update(self,data)
    def process(self,data):
        self.lastTime = data[4]
        if self.busy:
            return
        else:
            self.busy = True
            self.color = (16,39,145)
            data[3][1].changeNeedle()

class Character():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.start = time.time()
        self.cMin = dt.now().minute
        self.oldMin = self.cMin
        self.cSec = time.time()
        self.oldSec = self.cSec
        self.oldSecIn = self.cSec
        self.size = 100 #100x100 cube to start
        self.color = random.randint(0,2)
        self.colorChar = ""
        if self.color == 0:
            self.colorChar = "RED"
        elif self.color == 1:
            self.colorChar = "BLUE"
        elif self.color == 2:
            self.colorChar = "GREEN"
        self.color = (255,255,255)

        self.name = "Nani"
        self.food = 50 #with 0 being starving and 100 being fed
        #if you overfeed it will refuse to eat/do things with you
        self.isSleeping = False
        #dont wake it up with a light
        self.isClean = True
        #it poops.
        self.sick = False #sickness stuff, needle is needed to be healthy
        self.needle = False
        #inject it with something to make it happy?
        self.attention = 50 # with 0 being bad and 100 being good
        #dont spoil it but dont leave it alone
        self.discipline = 50 #too low and it will be a bad boi, too high and it will be sad
        #if you dont do this, it will beep at you
        #and wont eat
        #wont play games either when its sad
        #all of the above being when you dont discipline it

        #stuff for the game/progression
        self.exp = 0
        self.level = 1
        self.message = ""
        self.showMsg = True
        self.actions = 100 #how many times the user can interact with the thing

        #the levels that it will change at
        self.evolutionLevels = [random.randint(5,10),random.randint(15,20),random.randint(25,30),random.randint(50,100),random.randint(100,110)]
        #age in time/total game running
        self.age = 0
        #0-5 years is bad, 10-20 is good, higher is amazing

        self.dead = False
        self.lightOn = False
        self.myfont = FONT
        self.textS = self.myfont.render(self.message, False, (0, 0, 0))
        self.destination = [random.randint(10,1000-self.size), random.randint(10,450-self.size)]
        self.randomMessages = [
                "Whew, nice day out!",
                "This game deserves an E.",
                "owo What's this?"
            ]
        self.levelConstant = 255
        self.interactCooldown = 0
    def getType(self):
        return "Character"
    def changeNeedle(self):
        if self.needle:
            self.needle = False
            self.comment("Guess I don't need that...")
        else:
            self.needle = True
            self.comment("This could be useful...")
        print("Needle: "+str(self.needle))
    def addXp(self,n):
        self.attention += 5
        self.food -= 3
        self.exp += n
    #CORE functions
    def evolve(self):
        if self.color[0] < 60 or self.color[1] < 60:
            #max level for color reached
            self.size += 5
            if self.colorChar == "RED":
                self.color = (self.levelConstant, self.color[1], self.color[2])
            elif self.colorChar == "BLUE":
                self.color = (self.color[0], self.color[1], self.levelConstant)
            elif self.colorChar == "GREEN":
                self.color = (self.color[0], self.levelConstant, self.color[2])
            else:
                self.color = (0,0,0)
            self.levelConstant -= 5
            return
        self.size += 15
        if self.colorChar == "RED":
            self.color = (255, self.color[1]-50, self.color[2]-50)
        elif self.colorChar == "BLUE":
            self.color = (self.color[0]-50, self.color[1]-50, 255)
        elif self.colorChar == "GREEN":
            self.color = (self.color[0]-50, 255, self.color[2]-50)
        else:
            self.color = (0,0,0)
    def move(self):
        tox = self.destination[0]
        toy = self.destination[1]
        if self.x > tox and tox < self.size:
            if self.y > toy and toy < self.size:
                return 
        #print("Coords: "+str([self.x, self.y]))
        #print("Moving to: "+str(self.destination))
        if self.x > tox:
            self.x -= 1
        elif self.x < tox:
            self.x += 1

        if self.y > toy:
            self.y -= 1
        elif self.y < toy:
            self.y += 1


    def feed(self):
        
        if self.discipline < 20:
            self.comment("I refuse!")
            self.food -= 1
            return
        self.food += 5
        self.destination = [self.x, self.y]
        self.attention += 1
        self.exp += 10
        self.actions -= 1
        if self.food > 90:
            self.comment("I'm almost full...")
            return self.name+" is almost completely full!"
        elif self.food < 10:
            self.comment("Yum! More!")
            return self.name+" is still starving!"
        else:
            self.comment(random.choice(["Delicious!","Amazing!","Yum!"]))
            return "You fed "+self.name+"!"
    def light(self,data):
        env = data[3][0]
        if self.lightOn == False:
            self.lightOn = True
            env.light = 10
        else:
            env.light = 0
            self.lightOn = False
        if self.isSleeping and self.lightOn:
            env.light = 10
            self.attention -= 10
            self.isSleeping = False
            self.comment("!")
            return "You woke up "+self.name+" from their nap!"
        elif self.lightOn:
            env.light = 10
            return "The light is on."
        else:
            return "The light is off."
    def clean(self):
        pass
    def medical(self):
        sickMsg = "I don't feel so well..."
        if self.sick == False:
            if random.randint(1,20) == 10:
                print(self.name + " got sick! ------------------")
                self.sick = True
                self.randomMessages.append(sickMsg)
                self.comment(sickMsg)
        else:
            if self.needle and self.sick:
                self.sick = False
                self.randomMessages.remove(sickMsg)
                print("No longer sick.")
            else:
                self.attention -= 10
                print("Hurt from being sick.")
    def reset(self,data):
        print("CHARACTER DIED.")
        data[3][1] = Character(250,250)
    def interact(self):
        if self.isSleeping:
            self.comment("!")
            self.attention -= 5
            self.interactCooldown += 1
            return
        if self.interactCooldown >= 1:
            return
        self.interactCooldown += 1
        self.exp += 2
        self.comment(random.choice(self.randomMessages))
    def discipline(self):
        pass
    def update(self,data):
        #main gotchi boi updates
        self.age = int((self.cSec - self.start) / 3600)
        pos = (self.x, self.y)
        x,y = data[0]
        if x >= pos[0] and x <= (self.size + pos[0]) and data[1]:
            if y >= pos[1] and y <= (self.size + pos[1]):
                self.interact()
        self.cSec = time.time()
        if self.exp > self.level * 20 + 15:
            self.exp = 0
            self.evolve()
            self.level += 1

        if self.actions > 100:
            self.actions = 100
        if self.food < 0 or self.attention < 0:
            self.dead = True
        self.cMin = dt.now().minute
        if self.cMin > self.oldMin:
            self.oldMin = self.cMin
            self.updatePerMin(data)
        if self.cSec >= self.oldSec + 10:
            self.oldSec = self.cSec
            self.update10Seconds(data)
        if self.cSec >= self.oldSecIn + 0.05:
            self.oldSecIn = self.cSec
            self.updateFast(data)
        if self.food > 100:
            self.food = 100
        if self.attention > 100:
            self.attention = 100
        if self.dead:
            self.reset(data)

    def updateFast(self, data):
        if self.isSleeping == False:
            self.move()

    def update10Seconds(self,data):
        self.attention -= 1
        self.food -= 1
        if self.attention > 70:
            self.discipline -= 5
        self.medical()
        self.interactCooldown = 0
        self.exp += 1
        self.destination = [random.randint(20,1000-self.size), random.randint(40,450-self.size)]
        self.showMsg = False
        if self.actions < 5:
            self.comment("Careful, you might overdo yourself out soon...")
        self.actions += 100
        print("Updated once per 10s.\n=================\nName: "+str(self.name)+"\nSleeping: "+str(self.isSleeping)+"\nFood: "+str(self.food)+"\nAction Points: "+str(self.actions))
        print("discipline: "+str(self.discipline)+"\nAge: "+str(self.age))
        print("exp: "+str(self.exp)+"\nlevel: "+str(self.level)+"\nxp needed until next level: "+str((self.level * 20 + 15)-self.exp)+"\nAttention: "+str(self.attention)+"\nDead: "+str(self.dead))

    def updatePerMin(self,data):
        if self.needle == True and self.sick == False:
            self.attention -= 10
            print("Needle is just annoying.")
            self.comment("This needle is kinda bothering me..")
        self.destination = [random.randint(10,1000-self.size), random.randint(10,450-self.size)]
        self.food -= 10
        self.attention -= 5
        self.discipline -= 1
        self.update(data)
        #f = File()
        #f.saveData(self, data[3][0])
        #print("Saving....")
        if self.cMin < 15:
            self.isSleeping = True
            self.comment("ZzZzZz")
        else:
            self.isSleeping = False
        if self.attention > 60 and self.discipline < 30:
            self.comment("Wow, you are boring!")
            self.attention -= 10
        if self.showMsg == False:
            self.comment(random.choice(self.randomMessages))
        

    def draw(self,screen):
        #print("GOTCHI debug\nX: "+str(self.x)+"\nY: "+str(self.y))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        if self.showMsg:
            screen.blit(self.textS,(self.x - (len(self.message)*2.5),self.y-40))
        #if i wanted to make it an image:
        #pygame.Surface.blit(IMAGE, SCREEN, RECT)
    #end of CORE functions


    def comment(self, msg): #message should show for a bit then disappear
        self.message = msg
        print(msg)
        self.showMsg = True
        self.myfont = FONT
        self.textS = self.myfont.render(self.message, False, (20, 255, 10))
    def sleep(self):
        pass


class Environment():
    def __init__(self):
        self.cMin = dt.now().minute
        self.timeStep = 0
        #self.image = pygame.image.load("de.jpg")
        self.light = 0
    def getType(self):
        return "Environment"
    def draw(self,screen):
        screen.fill((self.cMin+self.light, self.cMin+self.light, self.cMin+self.light))

        #screen.blit(self.image,(0,0))
        pygame.draw.rect(screen, (96,82,77), (0, 490, 2000, 2000))
    def update(self,data):
        self.cMin = dt.now().minute


class Gauge():
    def __init__(self,pos,color,n):
        self.pos = pos
        self.color = color
        self.n = n
    def update(self,data):
        c = data[3][1]
        self.change(c)
    def draw(self,screen):
       d = 3
       pygame.draw.circle(screen, (172,172,150), self.pos, int(100/d))
       pygame.draw.circle(screen, self.color, self.pos, int(self.n/d))
       
    def getType(self):
        return "Gauge"
    def change(self, ch):
        print("Nothing made.")

class AttentionGauge(Gauge):
    def __init__(self,pos,color,n):
        Gauge.__init__(self,pos,color,n)
    def change(self,ch):
        self.n = ch.attention

class FoodGauge(Gauge):
    def __init__(self,pos,color,n):
        Gauge.__init__(self,pos,color,n)
    def change(self,ch):
        self.n = ch.food

