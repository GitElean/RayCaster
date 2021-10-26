'''
gui
fuente: https://pastebin.com/XDQyDZUd
'''

import pygame, sys
from pygame.locals import *
from math import cos, sin, pi

RAY_AMOUNT = 30

wallcolors = {
    '1': pygame.Color('red'),
    '2': pygame.Color('green'),
    '3': pygame.Color('blue'),
    '4': pygame.Color('yellow'),
    '5': pygame.Color('purple')
    }

wallTextures = {
    '1': pygame.image.load('wall1.png'),
    '2': pygame.image.load('wall2.png'),
    '3': pygame.image.load('wall3.png'),
    '4': pygame.image.load('wall4.png'),
    '5': pygame.image.load('wall5.png')
    }


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.blocksize = 50
        self.wallheight = 50

        self.maxdistance = 300

        self.stepSize = 5
        self.turnSize = 5

        self.player = {
           'x' : 100,
           'y' : 175,
           'fov': 60,
           'angle': 180 }


    def load_map(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append( list(line.rstrip()) )

    def drawBlock(self, x, y, id):
        tex = wallTextures[id]
        tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize) )
        rect = tex.get_rect()
        rect = rect.move((x,y))
        self.screen.blit(tex, rect)


    def drawPlayerIcon(self, color):
        if self.player['x'] < self.width / 2:
            rect = (self.player['x'] - 2, self.player['y'] - 2, 5,5)
            self.screen.fill(color, rect )

    def castRay(self, angle):
        rads = angle * pi / 180
        dist = 0
        stepSize = 1
        stepX = stepSize * cos(rads)
        stepY = stepSize * sin(rads)

        playerPos = (self.player['x'],self.player['y'] )

        x = playerPos[0]
        y = playerPos[1]

        while True:
            dist += stepSize      

            x += stepX
            y += stepY

            i = int(x/self.blocksize)
            j = int(y/self.blocksize)

            if j < len(self.map):
                if i < len(self.map[j]):
                    if self.map[j][i] != ' ':

                        hitX = x - i*self.blocksize
                        hitY = y - j*self.blocksize

                        hit = 0

                        if 1 < hitX < self.blocksize-1:
                            if hitY < 1:
                                hit = self.blocksize - hitX
                            elif hitY >= self.blocksize-1:
                                hit = hitX
                        elif 1 < hitY < self.blocksize-1:
                            if hitX < 1:
                                hit = hitY
                            elif hitX >= self.blocksize-1:
                                hit = self.blocksize - hitY

                        tx = hit / self.blocksize

                        pygame.draw.line(self.screen,pygame.Color('white'), playerPos, (x,y))
                        return dist, self.map[j][i], tx


    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)

        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):

                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if j < len(self.map):
                    if i < len(self.map[j]):
                        if self.map[j][i] != ' ':
                            self.drawBlock(x, y, self.map[j][i])

        self.drawPlayerIcon(pygame.Color('black'))

        for column in range(RAY_AMOUNT):
            angle = self.player['angle'] - (self.player['fov'] / 2) + (self.player['fov'] * column / RAY_AMOUNT)
            dist, id, tx = self.castRay(angle)

            rayWidth = int(( 1 / RAY_AMOUNT) * halfWidth)

            startX = halfWidth + int(( (column / RAY_AMOUNT) * halfWidth))

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle)) * wallHeight
            h = self.height / (dist * cos( (angle - self.player["angle"]) * pi / 180)) * self.wallheight
            startY = int(halfHeight - h/2)
            endY = int(halfHeight + h/2)

            color_k = (1 - min(1, dist / self.maxdistance)) * 255

            tex = wallTextures[id]
            tex = pygame.transform.scale(tex, (tex.get_width() * rayWidth, int(h)))
            tex.fill((color_k,color_k,color_k), special_flags=pygame.BLEND_MULT)
            tx = int(tx * tex.get_width())
            self.screen.blit(tex, (startX, startY), (tx,0,rayWidth,tex.get_height()))

        # Columna divisora
        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), pygame.Color('black'))
            self.screen.set_at( (halfWidth+1, i), pygame.Color('black'))
            self.screen.set_at( (halfWidth-1, i), pygame.Color('black'))


width = 1000
height = 500

pygame.init()
screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL )
screen.set_alpha(None)

rCaster = Raycaster(screen)
rCaster.load_map("map2.txt")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

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
        draw_text('Jugar', font, (255,255,255), screen, 500, 150)
        button_2 = pygame.Rect(450, 300, 100, 75)
        draw_text('Salir', font, (255,255,255), screen, 500, 300)
        if button_1.collidepoint((mx, my)):
            react1 = pygame.Rect(450, 155, 180, 65)
            pygame.draw.rect(screen, (200, 200, 200), react1)
            if click:
                juego()
        if button_2.collidepoint((mx, my)):
            react1 = pygame.Rect(450, 300, 180, 65)
            pygame.draw.rect(screen, (200, 200, 200), react1)
            if click:
                exit()
        
        
 
        click = False
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if ev.type == MOUSEBUTTONDOWN:
                if ev.button == 1:
                    click = True
            if ev.type == KEYDOWN:
                if ev.key == K_UP:
                    mx = 500
                    my = 170
            if ev.type == KEYDOWN:
                if ev.key == K_DOWN:
                    mx = 500
                    my = 320
            if ev.type == KEYDOWN:
                if ev.key == K_SPACE:
                    click = True
        pygame.display.update()
        clock.tick(60)

def exit():
    pygame.quit()
    sys.exit()

def updateFPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

def juego():
    isRunning = True
    while isRunning:
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            elif ev.type == pygame.KEYDOWN:
                newX = rCaster.player['x']
                newY = rCaster.player['y']
                forward = rCaster.player['angle'] * pi / 180
                right = (rCaster.player['angle'] + 90) * pi / 180

                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                elif ev.key == pygame.K_w:
                    newX += cos(forward) * rCaster.stepSize
                    newY += sin(forward) * rCaster.stepSize
                elif ev.key == pygame.K_s:
                    newX -= cos(forward) * rCaster.stepSize
                    newY -= sin(forward) * rCaster.stepSize
                elif ev.key == pygame.K_a:
                    newX -= cos(right) * rCaster.stepSize
                    newY -= sin(right) * rCaster.stepSize
                elif ev.key == pygame.K_d:
                    newX += cos(right) * rCaster.stepSize
                    newY += sin(right) * rCaster.stepSize
                elif ev.key == pygame.K_q:
                    rCaster.player['angle'] -= rCaster.turnSize
                elif ev.key == pygame.K_e:
                    rCaster.player['angle'] += rCaster.turnSize

                i = int(newX/rCaster.blocksize)
                j = int(newY/rCaster.blocksize)

                if rCaster.map[j][i] == ' ':
                    rCaster.player['x'] = newX
                    rCaster.player['y'] = newY


        screen.fill(pygame.Color("gray"))

        # Techo
        screen.fill(pygame.Color("saddlebrown"), (int(width / 2), 0,  int(width / 2), int(height / 2)))

        # Piso
        screen.fill(pygame.Color("dimgray"), (int(width / 2), int(height / 2),  int(width / 2), int(height / 2)))


        rCaster.render()

        #FPS
        
        screen.blit(updateFPS(), (0,0))
        clock.tick(60)
        
        #nivel
        
        draw_text('Nivel 1', font, (255, 255, 60), screen, 500, 0)
        
        
        pygame.display.flip()

main_menu()
pygame.quit()
