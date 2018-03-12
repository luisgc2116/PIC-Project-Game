#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import os
import random
pygame.init()


class FlappyBird(pygame.sprite.Sprite):
    '''


    '''
    def __init__(self):
        #Opens images to use as sprites
        self.width = 470 #640 508
        self.height = 680
        self.screen = pygame.display.set_mode((self.width, self.height)) #width, height
        pygame.sprite.Sprite.__init__(self)

        file_path = "/Users/ULT19/Downloads/PIC-Project-Game-master/"
        self.background = pygame.image.load(file_path + "background2.png").convert()
        self.background1 = pygame.image.load(file_path + "background2_1.png").convert()
        self.background1 = pygame.image.load(file_path + "background2_2.png").convert()
        self.background_homescreen = pygame.image.load(file_path + "Flappy Bird-878531.png").convert()

        self.birdSprites1 = [pygame.image.load(file_path + "1.png").convert_alpha(),
                            pygame.image.load(file_path + "2.png").convert_alpha(),
                            pygame.image.load(file_path + "dead.png")]
        self.birdSprites2 = [pygame.image.load(file_path + "f1.png").convert_alpha(),
                            pygame.image.load(file_path + "f2.png").convert_alpha(),
                            pygame.image.load(file_path + "f3.png")]



        self.size = self.birdSprites2[0].get_size()

        n = 12 #fraction of original sprite
        self.birdSprites_scale = [pygame.transform.scale(self.birdSprites2[0], (int(self.size[0]/n), int(self.size[1]/n))),
            pygame.transform.scale(self.birdSprites2[1], (int(self.size[0]/n), int(self.size[1]/n))),
            pygame.transform.scale(self.birdSprites2[2], (int(self.size[0]/n), int(self.size[1]/n)))]

        self.wallUp = pygame.image.load(file_path + "bottom.png").convert_alpha()
        self.wallDown = pygame.image.load(file_path + "top.png").convert_alpha()

        #Environment/Character characteristics
        self.bird = pygame.Rect(65, 50, 50, 50) #hit-box
        self.pipe_gap = 160
        self.wallx = self.width
        self.bird_y_pos = 350 #start position of bird
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 4

        #Sprites
        self.sprite = 0
        self.points_counter = 0
        self.offset = random.randint(-140, 140)
        self.dead = False

        #Colors Referenced
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.light_red = (220,20,60)

        self.clock = pygame.time.Clock()

    def click_objects(self,text, font):
        '''
        Creates suface where a click follows any action given
        '''
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()


    def button(self,x,y,w,h,ac,action=None):
        '''
        Creates suface where a click follows any action given
        '''
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            if click[0] == 1 and action != None:
                action()

    def button2(self, msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, ic,(x,y,w,h))

        smallText = pygame.font.SysFont("Times New Roman",20)
        textSurf, textRect = self.click_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)

    def quitgame(self):
        pygame.quit()
        quit()

    def restart_program(self):
        """Restarts the current program.
        Note: this function does not return. Any cleanup action (like
        saving data) must be done before calling this function."""
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def bird2(self):
        self.pipe_gap = 180
        self.gravity = 5
        self.birdSprites1 = self.birdSprites_scale
        self.game()

    def game_intro(self):

        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(self.white)
            self.screen.blit(self.background_homescreen, (0, 0))
            self.screen.blit(self.birdSprites_scale[0], (int(self.width/2)+80,280))
            largeText = pygame.font.Font('freesansbold.ttf',40)
            TextSurf, TextRect = self.click_objects("Flappy Bird", largeText)
            TextRect.center = ((self.width/2),(self.height/4))
            #self.screen.blit(TextSurf, TextRect)

            #self.button(95,375,280,50,self.light_red,self.game)
            self.button(95,375,100,50,self.light_red,self.game)
            self.button(270,375,100,50,self.light_red,self.bird2)
            self.button2("Quit",int(self.width/2)+150,620,100,50,self.white,self.light_red,self.quitgame)

            pygame.display.update()
            self.clock.tick(60)

    def updateWalls(self):
        self.wallx -= 2 + self.points_counter//2
        if self.points_counter == 2:
            self.background = self.background1
        if self.points_counter == 4:
            self.background = self.background1


        if self.wallx < -80:
            self.wallx = self.width #resets
            self.points_counter += 1
            self.offset = random.randint(-140, 140)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.bird_y_pos -= self.jumpSpeed
            self.jump -= 1
        else:
            self.bird_y_pos += self.gravity
            self.gravity += 0.2

        self.bird[1] = self.bird_y_pos
        upRect = pygame.Rect(self.wallx,
                             360 + self.pipe_gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.pipe_gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True
        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.bird_y_pos = 50
            self.dead = False
            self.points_counter = 0
            self.wallx = self.width
            self.offset = random.randint(-140, 140)
            self.gravity = 5

    def game(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 9
                    self.gravity = 5
                    self.jumpSpeed = 10



            self.screen.fill(self.white) #white background
            self.screen.blit(self.background, (0, 0)) #Place background image
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.pipe_gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.pipe_gap - self.offset))
            self.screen.blit(font.render(str(self.points_counter),-1,self.white),(self.width/2, 50))
            self.button2("Quit",int(self.width/2)+150,620,100,50,self.white,self.light_red,self.restart_program)


            #Sprites
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites1[self.sprite], (70, self.bird_y_pos))
            if not self.dead:
                self.sprite = 0

            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()


if __name__ == "__main__":
    FlappyBird().game_intro()
