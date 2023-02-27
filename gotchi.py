print("Starting Program")
import pygame, time, os.path
pygame.init()
pygame.font.init()
from utils import *
from external import *
from ai import *

def main():
    size = (1000,600)
    screen = pygame.display.set_mode(size)
    fps = 30
    clock = pygame.time.Clock()
    running = True
    isPressed = False
    objects = []
    file = File()
    data = []
    if os.path.isfile(file.dataFile) and 2 == 1:
        print("Loading Save")
        for i in file.loadData():
            objects.append(i)
    else:
        print("Creating new save")
        objects.append(Environment())
        objects.append(Character(250,250))
    objects.append(FeedButton([100,500], [100,40], "Feed"))
    objects.append(LightButton([250,500], [100,40], "Light"))
    objects.append(StartGame([400,500], [100,40], "TTTGame"))
    objects.append(NeedleButton([550,500], [100,40], "Needle"))
    objects.append(AttentionGauge([40,40], (25,50,25), 50))
    objects.append(FoodGauge([40,110], (50,25,25), 50))
    objects.append(BasketBallButton([700,500], [100,40], "BBall"))
    game_increment = time.process_time()
    runtime = 0
    while running:
        runtime = int(time.process_time() - game_increment)
        #logic process
        data = [pygame.mouse.get_pos(), isPressed, screen, objects, runtime, fps]
        pygame.display.set_caption(data[3][1].name)
        for i in objects:
            if objects[8].isGame == True:
                objects[8].update(data)
                break
            else:
                i.update(data)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                isPressed = True
            else:
                isPressed = False
            if e.type == pygame.QUIT:
                running = False
        #draw stuff

        for i in objects:
                i.draw(screen)

        pygame.display.flip()
        clock.tick(fps)
        #end of game loop
    pygame.quit()
