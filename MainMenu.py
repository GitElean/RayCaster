# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 20:01:15 2021

@author: Elean Rivas

No funcional
fuentes :https://pastebin.com/XDQyDZUd
"""
#!/usr/bin/python3.4
# Setup Python ----------------------------------------------- #
import pygame, sys
import RayCaster as rc
 
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('UVGenstein')
screen = pygame.display.set_mode((1000, 500),0,32)
 
font = pygame.font.Font("wolfenstein.ttf",40)
fondo = pygame.image.load("fondo.jpg").convert()
fondo = pygame.transform.scale(fondo, (1000, 500))
 
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, (255,255,255), color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
click = False
 
def main_menu():
    while True:
     
        screen.blit (fondo, [0, 0])
        draw_text('UVGenstein', font, (73, 150, 60), screen, 470, 20)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(450, 150, 100, 75)
        draw_text('Jugar', font, (255,255,255), screen, 370, 150)
        button_2 = pygame.Rect(450, 300, 100, 75)
        draw_text('Salir', font, (255,255,255), screen, 370, 300)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                exit()
        pygame.draw.rect(screen, (30, 200, 30), button_1)
        pygame.draw.rect(screen, (30, 200, 30), button_2)
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)
 
def game():
    rc.level1()
        
 
def game_pause():
    pass


def exit():
    pygame.quit()
    sys.exit()
    

main_menu()