import sys
import pygame
from pygame.locals import QUIT

pygame.init()

FPS = 30 #frames per second setting
fpsClock = pygame.time.Clock()

#set up the window
screen = pygame.display.set_mode((400, 300), pygame.RESIZABLE)
pygame.display.set_caption('animation')
icon_original = pygame.image.load('target_dart_icon.png').convert_alpha()
icon = pygame.transform.scale(icon_original, [icon_original.get_size()[i]*(32/icon_original.get_size()[0]) for i in range(2)])
icon_surface = pygame.Surface((max(icon.get_size()), max(icon.get_size())), pygame.SRCALPHA)
icon_surface.fill((0, 0, 0, 0))
icon_surface.blit(icon, [(max(icon.get_size()) - icon.get_size()[i])/2 for i in range(2)], special_flags=pygame.BLEND_RGBA_MAX)
pygame.display.set_icon(icon)

#set up the colors
white = (255, 255, 255)
black = (  0,   0,   0)
green = (0, 255, 0)
blue = (0, 0, 180)
red   = (255,   0,   0)

image  = pygame.image.load('Pictures/Blank5.png')
imagex = 360
imagey = 260
direction = 'left'

# text setting
# font_obj = pygame.font.Font('freesansbold.ttf', 32)
font_obj = pygame.font.SysFont('system', 32)
text_surface_obj = font_obj.render('Hello World!', True, green, blue)
text_rect_obj = text_surface_obj.get_rect()
text_rect_obj.center = (200, 150)

while True: # the main game loop
    screen.fill(white)

    # draw a green polygon onto the surface
    pygame.draw.polygon(screen, green, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

    # draw some blue lines onto the surface
    pygame.draw.line(screen, blue, (60, 60), (120, 60), 4)
    pygame.draw.line(screen, blue, (120, 60), (60, 120))
    pygame.draw.line(screen, blue, (60, 120), (120, 120), 4)

    # draw a blue circle onto the surface
    pygame.draw.circle(screen, blue, (300, 50), 20, 0)

    # draw a red ellipse onto the surface
    pygame.draw.ellipse(screen, red, (100, 150, 40,80), 1)

    # draw a red rectangle onto the surface
    pygame.draw.rect(screen,red, (200, 150, 100, 50))

    # draw the text onto the surface
    screen.blit(text_surface_obj, text_rect_obj)


    #the animation of the image
    if direction == 'right':
        imagex += 5
        if imagex == 360:
            direction = 'down'
    elif direction == 'down':
        imagey += 5
        if imagey == 260:
            direction = 'left'
    elif direction == 'left':
        imagex -= 5
        if imagex == 20:
            direction = 'up'
    elif direction == 'up':
        imagey -= 5
        if imagey == 20:
            direction = 'right'
    screen.blit(image, (imagex, imagey))

    pygame.display.update()
    fpsClock.tick(FPS)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
