# -*- coding: utf-8 -*-
#https://github.com/adamkdean/Python.Snowfall
# Revision by: Ahmet aksoy - https://github.com/ahmetax/Python.Snowfall
import random
import sys
import pygame
import snowflake
from pygame.locals import * #@UnusedWildImport
from snowflake import Snowflake


class Game:
    first_time=True
    def __init__(self, width, height, caption="Game"):
        # plethora of fields
        self.width = width
        self.height = height
        self.caption = caption
        self.framerate = 90 # FPS
        self.foreground_color = (255, 255, 255)
        self.background_color = (21, 26, 79)
        self.snowflakes = []
        self.snowflake_counter = 0
        self.snowflake_frequency = 3
        self.snowflake_size = 1
        self.snowflake_line = [height] * width # for collision detection
        self.wind_chance = 5
        self.wind_strength = 50
        self.show_text = False
        # and we're off!
        self.initialize()
        self.loop()

    def initialize(self):
        pygame.init()
        pygame.display.set_caption(self.caption)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font("fonts/visitor1.ttf", 20)

    # Draw a simple house. So snow can accumulate on top of its root also
    def drawHouse(self,surface):
        # draw the body of a green house
        #pygame.draw.rect(surface,(140,240,130), Rect((300,150), (130,50)))
        # draw a red roof
        #pygame.draw.polygon(surface,(255,0,0),[[298,150],[432,150],[365,140],[298,150]],0)
        img=pygame.image.load("forest.png")
        surface.blit(img,(0,0))
        # analyze the terrain
        if self.first_time:
            #check for the scene
            for i in range(self.width):
                for j in range(self.height):
                    if surface.get_at((i,j))!= self.background_color:
                        self.snowflake_line[i]=j
                        break
            self.first_time=False

    def loop(self):
        self.clock = pygame.time.Clock()
        while 1:
            gametime = self.clock.get_time()
            self.update(gametime)
            self.render(gametime)
            self.clock.tick(self.framerate)

    def update(self, gametime):

        # do we need to add more snow?
        if self.snowflake_counter > self.snowflake_frequency:
            self.snowflake_counter = 0
            snowflake = Snowflake(len(self.snowflakes), self.width, self.height, self.snowflake_size, self.foreground_color)
            self.snowflakes.append(snowflake)
        else:
            self.snowflake_counter += 1

        # what about some wind?
        w_chance = random.randint(0, 100)
        w_strength = 0
        if w_chance <= self.wind_chance:
            w_strength = random.randint(-self.wind_strength, self.wind_strength)

        # let it snow, let it snow, let it snow
        for snowflake in self.snowflakes:
            if snowflake.enabled:
                if w_strength != 0:
                    snowflake.wind = w_strength
                snowflake.update(gametime, self.snowflake_line)

        # update the other rubbish
        if self.show_text:
            self.fps_text = self.font.render("FPS: %d" % self.clock.get_fps(), 1, self.foreground_color)
            self.snowflake_text = self.font.render("Snowflakes: %d" % len(self.snowflakes), 1, self.foreground_color)
        else:
            self.fps_text = None
            self.snowflake_text = None

        self.handle_input(pygame.event.get())

    def render(self, gametime):
        surface = pygame.Surface(self.screen.get_size())
        surface.convert()
        surface.fill(self.background_color)
        self.drawHouse(surface)

        for snowflake in self.snowflakes:
            snowflake.draw(surface)

        if self.show_text:
            if self.fps_text == None:
                self.fps_text = self.font.render("FPS: %d" % self.clock.get_fps(), 1, self.foreground_color)
                self.snowflake_text = self.font.render("Snowflakes: %d" % len(self.snowflakes), 1, self.foreground_color)
            surface.blit(self.fps_text, (8, 6))
            surface.blit(self.snowflake_text, (8, 26))
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    if self.show_text:
                        self.show_text = False
                    else:
                        self.show_text = True
                elif event.key == pygame.K_q:
                    sys.exit()

if __name__ == "__main__":
    game = Game(640, 320, "Snow: a sprinkling of test flakes")