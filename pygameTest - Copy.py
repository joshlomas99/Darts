from sys import exit as sysExit
from pygame import init as pygameInit, quit as pygameQuit, Surface as pygameSurface
from pygame import BLEND_RGBA_MAX as pygameBLEND_RGBA_MAX, SRCALPHA as pygameSRCALPHA
from pygame import RESIZABLE as pygameRESIZABLE
from pygame.time import Clock as pygameTimeClock
from pygame.display import set_mode as pygameDisplaySet_mode, set_caption as pygameDisplaySet_caption
from pygame.display import set_icon as pygameDisplaySet_icon
from pygame.display import update as pygameDisplayUpdate
from pygame.image import load as pygameImageLoad
# from pygame.font import Font as pygameFontFont
from pygame.font import SysFont as pygameFontSysFont
from pygame.draw import polygon as pygameDrawPolygon, line as pygameDrawLine, circle as pygameDrawCircle
from pygame.draw import ellipse as pygameDrawEllipse, rect as pygameDrawRect
from pygame.transform import scale as pygameTransformScale
from pygame.event import get as pygameEventGet
from pygame.locals import QUIT as pygameLocalsQUIT

pygameInit()

FPS = 30 #frames per second setting
fpsClock = pygameTimeClock()

#set up the window
screen = pygameDisplaySet_mode((400, 300), pygameRESIZABLE)
pygameDisplaySet_caption('animation')
icon_original = pygameImageLoad('target_dart_icon.png').convert_alpha()
icon = pygameTransformScale(icon_original, [icon_original.get_size()[i]*(32/icon_original.get_size()[0]) for i in range(2)])
icon_surface = pygameSurface((max(icon.get_size()), max(icon.get_size())), pygameSRCALPHA)
icon_surface.fill((0, 0, 0, 0))
icon_surface.blit(icon, [(max(icon.get_size()) - icon.get_size()[i])/2 for i in range(2)], special_flags=pygameBLEND_RGBA_MAX)
pygameDisplaySet_icon(icon)

#set up the colors
white = (255, 255, 255)
black = (  0,   0,   0)
green = (0, 255, 0)
blue = (0, 0, 180)
red   = (255,   0,   0)

image  = pygameImageLoad('Pictures/Blank5.png')
imagex = 360
imagey = 260
direction = 'left'

# text setting
# font_obj = pygameFontFont('freesansbold.ttf', 32)
font_obj = pygameFontSysFont('system', 32)
text_surface_obj = font_obj.render('Hello World!', True, green, blue)
text_rect_obj = text_surface_obj.get_rect()
text_rect_obj.center = (200, 150)

while True: # the main game loop
    screen.fill(white)

    # draw a green polygon onto the surface
    pygameDrawPolygon(screen, green, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

    # draw some blue lines onto the surface
    pygameDrawLine(screen, blue, (60, 60), (120, 60), 4)
    pygameDrawLine(screen, blue, (120, 60), (60, 120))
    pygameDrawLine(screen, blue, (60, 120), (120, 120), 4)

    # draw a blue circle onto the surface
    pygameDrawCircle(screen, blue, (300, 50), 20, 0)

    # draw a red ellipse onto the surface
    pygameDrawEllipse(screen, red, (100, 150, 40,80), 1)

    # draw a red rectangle onto the surface
    pygameDrawRect(screen,red, (200, 150, 100, 50))

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

    pygameDisplayUpdate()
    fpsClock.tick(FPS)

    for event in pygameEventGet():
        if event.type == pygameLocalsQUIT:
            pygameQuit()
            sysExit(0)
