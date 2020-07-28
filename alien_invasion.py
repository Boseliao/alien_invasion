# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 09:16:08 2020

@author: Boseliao
"""

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf
from game_states import GameStates
from button import Button
from scoreboard import Scoreboard

def run_game():
    pygame.init()
    
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    pygame.display.set_caption("alien invasion")
    
    play_button = Button(ai_settings, screen, "Play")
    
    ship = Ship(ai_settings, screen)
    aliens = Group()
    bullets = Group()
    states = GameStates(ai_settings)
    sb = Scoreboard(ai_settings,screen,states)
    
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    while True:
        
        gf.check_events(ai_settings,states,screen,ship,bullets,
                        aliens,play_button,sb)   
        if states.game_active:
            
            ship.update()
            gf.update_bullets(ai_settings, states, screen, sb, ship,
                              aliens, bullets)
            gf.update_aliens(ai_settings, states, screen, ship,
                             aliens, bullets, sb)
        
        gf.update_screen(ai_settings,states,sb,screen,ship,aliens,
                         bullets, play_button)
        
run_game()
