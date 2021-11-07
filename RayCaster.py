'''
gui
fuente: https://pastebin.com/XDQyDZUd
'''

import pygame, sys
from pygame.locals import *
from math import cos, sin, pi, atan2

RAY_AMOUNT = 150
SPRITE_BACKGROUND = (152, 0, 136, 255)

wallcolors = {
    '1': pygame.Color('red'),
    '2': pygame.Color('green'),
    '3': pygame.Color('blue'),
    '4': pygame.Color('yellow'),
    '5': pygame.Color('purple')
    }

wallTextures = {
    '1': pygame.image.load('textures/l1_w1.png'),
    '2': pygame.image.load('textures/l1_w2.png'),
    '3': pygame.image.load('textures/l1_w3.png'),
    '4': pygame.image.load('textures/l1_w4.png'),
    '5': pygame.image.load('textures/l1_w5.png')
    }

wallTextures2 = {
    '1': pygame.image.load('textures/l2_w1.png'),
    '2': pygame.image.load('textures/l2_w2.png'),
    '3': pygame.image.load('textures/l2_w3.png'),
    '4': pygame.image.load('textures/l2_w4.png'),
    '5': pygame.image.load('textures/l2_w5.png')
    }

wallTextures3 = {
    '1': pygame.image.load('textures/l3_w1.png'),
    '2': pygame.image.load('textures/l3_w2.png'),
    '3': pygame.image.load('textures/l3_w3.png'),
    '4': pygame.image.load('textures/l3_w4.png'),
    '5': pygame.image.load('textures/l3_w5.png')
    }

enemies = [{"x" : 100,
            "y" : 200,
            "sprite" : pygame.image.load('sprite1.png')},

           {"x" : 350,
            "y" : 150,
            "sprite" : pygame.image.load('sprite2.png')},

            {"x" : 300,
             "y" : 400,
             "sprite" : pygame.image.load('sprite3.png')}
    ]


class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.zbuffer = [float('inf') for z in range(self.width)]

        self.blocksize = 50
        self.wallheight = 50

        self.maxdistance = 300

        self.stepSize = 5
        self.turnSize = 5

        self.player = {
           'x' : 100,
           'y' : 100,
           'fov': 60,
           'angle': 0 }

        self.hitEnemy = False


    def load_map(self, filename):
        with open(filename) as file:
            for line in file.readlines():
                self.map.append( list(line.rstrip()) )

    def drawMinimap(self):
        minimapWidth = 100
        minimapHeight = 100


        minimapSurface = pygame.Surface( (500, 500 ) )
        minimapSurface.fill(pygame.Color("gray"))

        for x in range(0, 500, self.blocksize):
            for y in range(0, 500, self.blocksize):

                i = int(x/self.blocksize)
                j = int(y/self.blocksize)

                if j < len(self.map):
                    if i < len(self.map[j]):
                        if self.map[j][i] != ' ':
                            tex = wallTextures[self.map[j][i]]
                            tex = pygame.transform.scale(tex, (self.blocksize, self.blocksize) )
                            rect = tex.get_rect()
                            rect = rect.move((x,y))
                            minimapSurface.blit(tex, rect)

        rect = (int(self.player['x'] - 4), int(self.player['y']) - 4, 10,10)
        minimapSurface.fill(pygame.Color('black'), rect )

        for enemy in enemies:
            rect = (enemy['x'] - 4, enemy['y'] - 4, 10,10)
            minimapSurface.fill(pygame.Color('red'), rect )

        minimapSurface = pygame.transform.scale(minimapSurface, (minimapWidth,minimapHeight) )
        self.screen.blit(minimapSurface, (self.width - minimapWidth,self.height - minimapHeight))

    def drawSprite(self, obj, size):
        # Pitagoras
        spriteDist = ((self.player['x'] - obj['x']) ** 2 + (self.player['y'] - obj['y']) ** 2) ** 0.5

        # Angulo
        spriteAngle = atan2(obj['y'] - self.player['y'], obj['x'] - self.player['x']) * 180 / pi

        #Tamaño del sprite
        aspectRatio = obj['sprite'].get_width() / obj['sprite'].get_height()
        spriteHeight = (self.height / spriteDist) * size
        spriteWidth = spriteHeight * aspectRatio

        # Buscar el punto inicial para dibujar el sprite
        angleDif = (spriteAngle - self.player['angle']) % 360
        angleDif = (angleDif - 360) if angleDif > 180 else angleDif
        startX = angleDif * self.width / self.player['fov'] 
        startX += (self.width /  2) - (spriteWidth  / 2)
        startY = (self.height /  2) - (spriteHeight / 2)
        startX = int(startX)
        startY = int(startY)

        for x in range(startX, startX + int(spriteWidth)):
            if (0 < x < self.width) and self.zbuffer[x] >= spriteDist:
                for y in range(startY, startY + int(spriteHeight)):
                    tx = int((x - startX) * obj['sprite'].get_width() / spriteWidth )
                    ty = int((y - startY) * obj['sprite'].get_height() / spriteHeight )
                    texColor = obj['sprite'].get_at((tx, ty))
                    if texColor != SPRITE_BACKGROUND and texColor[3] > 128:
                        self.screen.set_at((x,y), texColor)

                        if y == self.height / 2:
                            self.zbuffer[x] = spriteDist
                            if x == self.width / 2:
                                self.hitEnemy = True
                            

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

                        return dist, self.map[j][i], tx


    def render(self):
        halfHeight = int(self.height / 2)

        for column in range(RAY_AMOUNT):
            angle = self.player['angle'] - (self.player['fov'] / 2) + (self.player['fov'] * column / RAY_AMOUNT)
            dist, id, tx = self.castRay(angle)

            rayWidth = int(( 1 / RAY_AMOUNT) * self.width)

            for i in range(rayWidth):
                self.zbuffer[column * rayWidth + i] = dist

            startX = int(( (column / RAY_AMOUNT) * self.width))

            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle)) * wallHeight
            h = self.height / (dist * cos( (angle - self.player["angle"]) * pi / 180)) * self.wallheight
            startY = int(halfHeight - h/2)
            endY = int(halfHeight + h/2)

            color_k = (1 - min(1, dist / self.maxdistance)) * 255

            tex = wallTextures[id]
            tex = pygame.transform.scale(tex, (tex.get_width() * rayWidth, int(h)))
            tx = int(tx * tex.get_width())
            self.screen.blit(tex, (startX, startY), (tx,0,rayWidth,tex.get_height()))


        self.hitEnemy = False
        for enemy in enemies:
            self.drawSprite(enemy, 50)

        sightRect = (int(self.width / 2 - 2), int(self.height / 2 - 2), 5,5 )
        self.screen.fill(pygame.Color('red') if self.hitEnemy else pygame.Color('white'), sightRect)

        self.drawMinimap()


width = 800
height = 600

pygame.init()
screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE )
screen.set_alpha(None)

rCaster = Raycaster(screen)
rCaster.load_map("map2.txt")

clock = pygame.time.Clock()
font = pygame.font.Font("wolfenstein.ttf",40)
fondo = pygame.image.load("fondo.jpg").convert()
fondo = pygame.transform.scale(fondo, (800, 600))


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, (255,255,255), color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
click = False
 


def main_menu():
    while True:
     
        screen.blit (fondo, [0, 0])
        draw_text('UVGenstein', font, (73, 150, 60), screen, 370, 20)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(350, 150, 100, 75)
        draw_text('Jugar', font, (255,255,255), screen, 400, 150)
        button_2 = pygame.Rect(350, 300, 100, 75)
        draw_text('Salir', font, (255,255,255), screen, 400, 300)
        if button_1.collidepoint((mx, my)):
            react1 = pygame.Rect(350, 155, 180, 65)
            pygame.draw.rect(screen, (200, 200, 200), react1)
            if click:
                level_1()
        if button_2.collidepoint((mx, my)):
            react1 = pygame.Rect(350, 300, 180, 65)
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

def level_1():
    isRunning = True
    while isRunning:

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False

            elif ev.type == pygame.KEYDOWN:
                
                

                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                    
                i = int(newX/rCaster.blocksize)
                j = int(newY/rCaster.blocksize)

                if rCaster.map[j][i] == ' ':
                    rCaster.player['x'] = newX
                    rCaster.player['y'] = newY
                    
                    
        newX = rCaster.player['x']
        newY = rCaster.player['y']
        forward = rCaster.player['angle'] * pi / 180
        right = (rCaster.player['angle'] + 90) * pi / 180            
        keys = pygame.key.get_pressed()         
        if keys[K_w]:
            newX += cos(forward) * rCaster.stepSize + 0.5
            newY += sin(forward) * rCaster.stepSize + 0.5
        elif keys[K_s]:
            newX -= cos(forward) * rCaster.stepSize + 0.5
            newY -= sin(forward) * rCaster.stepSize + 0.5
        elif keys[K_a]:
            newX -= cos(right) * rCaster.stepSize + 0.5
            newY -= sin(right) * rCaster.stepSize + 0.5
        elif keys[K_d]:
            newX += cos(right) * rCaster.stepSize + 0.5
            newY += sin(right) * rCaster.stepSize + 0.5
        elif keys[K_q]:
            rCaster.player['angle'] -= rCaster.turnSize + 0.5
        elif keys[K_e]:
            rCaster.player['angle'] += rCaster.turnSize + 0.5
 
                

        # Techo
        screen.fill(pygame.Color("saddlebrown"), (0, 0,  width, int(height / 2)))

        # Piso
        screen.fill(pygame.Color("dimgray"), (0, int(height / 2),  width, int(height / 2)))


        rCaster.render()

        #FPS
        screen.fill(pygame.Color("black"), (0,0,30,30) )
        screen.blit(updateFPS(), (0,0))
        clock.tick(60)

        draw_text('Nivel 1', font, (255, 255, 60), screen, 720, 5)
        pygame.display.flip()

main_menu()

pygame.quit()
