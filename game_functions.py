# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 17:28:33 2020

@author: Boseliao
"""

import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)

def check_events(ai_settings,states,screen,ship,bullets,aliens,play_button,sb):
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings,states,screen,play_button,
                                  ship,bullets,aliens,mouse_x,mouse_y,sb)
                
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event,ai_settings,screen,ship,bullets)
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    ship.moving_left = False
                    
def check_play_button(ai_settings,states,screen,play_button,
                      ship,bullets,aliens,mouse_x,mouse_y,sb):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not states.game_active:
        pygame.mouse.set_visible(False)
        states.reset_state()
        states.game_active = True
        
        aliens.empty()
        bullets.empty()
        
        create_fleet(ai_settings, screen, ship, aliens)
        ai_settings.initialize_dynamic_settings()
        ship.center_ship()
        
        #reset scoreboard
        sb.prep_score()
        sb.prep_level()
        sb.prep_ships()
                
def update_screen(ai_settings,states,sb,screen,ship,aliens,bullets,play_button):
    
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    
    if not states.game_active:
        play_button.draw_button()
    
    pygame.display.flip()
    
def update_bullets(ai_settings, states, screen, sb, ship, aliens, bullets):
    
    bullets.update()
        
    #remove dispeared bullet
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collision(ai_settings, states, screen,
                                 sb, ship, aliens, bullets)
        
def check_bullet_alien_collision(ai_settings, states, screen, sb,
                                 ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            
            states.score += ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(states,sb)
    
    if len(aliens) == 0:
        bullets.empty()
        
        states.level += 1
        sb.prep_level()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

#alien
def get_number_alien_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width-2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, alien_height, ship_height):
    available_space_y = (ai_settings.screen_height-
                         (3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = (2*row_number+1)*alien.rect.width
    aliens.add(alien)
            
def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_alien_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, alien.rect.height
                                  , ship.rect.height)
    for row_number in range(number_rows):
        
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens
                         , alien_number, row_number)
            
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings, states, screen, ship, aliens, bullets, sb):
    if states.ships_left > 0:
        
        states.ships_left -= 1
    
        aliens.empty()
        bullets.empty()
        
        sb.prep_ships()
    
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    
        sleep(0.5)
    else:
        states.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, states, screen, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom > screen_rect.bottom:
            ship_hit(ai_settings, states, screen, ship, aliens, bullets, sb)
            break
    
def update_aliens(ai_settings, states, screen, ship, aliens, bullets, sb):
    
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, states, screen, ship, aliens, bullets, sb)
        
    check_aliens_bottom(ai_settings, states, screen, ship, aliens, bullets, sb)
    
def check_high_score(states,sb):
    if states.score > states.high_score:
        states.high_score = states.score
        sb.prep_high_score()
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
