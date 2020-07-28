# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:31:46 2020

@author: Boseliao
"""

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    
    def __init__(self,ai_settings,screen,states):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings
        self.states = states
        
        self.txt_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
    def prep_score(self):
        rounded_score = int(round(self.states.score,-1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.txt_color,
                                          self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right-20
        self.score_rect.top = 20
        
    def prep_high_score(self):
        rounded_high_score = int(round(self.states.high_score,-1))
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.txt_color,
                                          self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20
        
    def prep_level(self):
        level_str = "{:,}".format(self.states.level)
        self.level_image = self.font.render(level_str, True, self.txt_color,
                                          self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right-20
        self.level_rect.top = self.score_rect.bottom + 10
        
    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.states.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10 + ship_number*ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
        
    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)