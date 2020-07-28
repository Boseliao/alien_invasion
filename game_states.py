# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:06:38 2020

@author: Boseliao
"""

class GameStates():
    
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_state()
        self.game_active = False
        self.score = 0
        self.high_score = 0
        
    def reset_state(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
