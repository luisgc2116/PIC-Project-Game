#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
pygame.init()


class FlappyBird:
    def __init__(self):
        #Opens images to use as sprites
        self.width = 400
        self.height = 708
        self.screen = pygame.display.set_mode((self.width, self.height)) #width, height

        self.background = pygame.image.load("/Users/ULT19/Downloads/PIC-Project-Game-master/background2.png").convert()
        self.birdSprites = [pygame.image.load("/Users/ULT19/Downloads/PIC-Project-Game-master/1.png").convert_alpha(),
                            pygame.image.load("/Users/ULT19/Downloads/PIC-Project-Game-master/2.png").convert_alpha(),
                            pygame.image.load("/Users/ULT19/Downloads/PIC-Project-Game-master/dead.png")]
        self.wallUp = pygame.image.load("/Users/ULT19/Downloads/PIC-Project-Game-master/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("/Users/ULT19/Downloads/PIC-Project-Game-master/top.png").convert_alpha()

        #Environment/Character characteristics
        self.bird = pygame.Rect(65, 50, 50, 50) #hit-box
        self.pipe_gap = 130
        self.wallx = self.width
        self.bird_y_pos = 350 #start position of bird
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5

        #Sprites
        self.sprite = 0
        self.points_counter = 0
        self.offset = random.randint(-110, 110)
        self.dead = False

        #Colors Referenced
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.green = (255,0,0)

        self.bright_red = (255,0,0)
        self.bright_green = (0,255,0)

        self.block_color = (53,115,255)

        self.clock = pygame.time.Clock()

    def text_objects(self,text, font):
        textSurface = font.render(text, True, self.black)
        return textSurface, textSurface.get_rect()

    def message_display(self,text):
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((self.width/2),(self.height/2))
        self.screen.blit(TextSurf, TextRect)

        pygame.display.update()

        time.sleep(2)
        game_loop()

    def button(self,msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, ic,(x,y,w,h))

        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        self.screen.blit(textSurf, textRect)

    def quitgame(self,):
        pygame.quit()
        quit()

    def game_intro(self,):

        intro = True

        while intro:
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill(self.white)
            largeText = pygame.font.Font('freesansbold.ttf',115)
            TextSurf, TextRect = self.text_objects("A bit Racey", largeText)
            TextRect.center = ((self.width/2),(self.height/2))
            self.screen.blit(TextSurf, TextRect)

            self.button("GO!",150,450,100,50,self.green,self.bright_green,self.run)
            self.button("Quit",550,450,100,50,self.red,self.bright_red,self.quitgame)


            pygame.display.update()
            self.clock.tick(60)

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400 #resets
            self.points_counter += 1
            self.offset = random.randint(-110, 110)

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
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10



            self.screen.fill((255, 255, 255)) #white background
            self.screen.blit(self.background, (0, 0)) #Place background image
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.pipe_gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.pipe_gap - self.offset))
            self.screen.blit(font.render(str(self.points_counter),-1,(255, 255, 255)),(200, 50))


            #Sprites
            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1

            #
            self.screen.blit(self.birdSprites[self.sprite], (70, self.bird_y_pos))
            if not self.dead:
                self.sprite = 0


            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()

FlappyBird().game_intro()
