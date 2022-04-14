from os import environ as osEnviron
import time, sys
from math import sin, cos, pi
from random import random
import threading
import pygame
from pygame.locals import QUIT
from pygame.color import THECOLORS as pygameColors
maximised_res = (1536, 801)
maximised_pos = "0,20"

# os.environ['SDL_VIDEO_WINDOW_POS'] = "384,200"
# os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
# os.environ['SDL_VIDEO_CENTERED'] = '1'

def blankTestFunction():
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygame.display.set_mode((info.current_w/2, (info.current_h-60)/2))

    # test function here

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        # test function here

        pygame.display.flip()

        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

def gradientRect(window, top_colour, bottom_colour, target_rect):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, top_colour, (0, 0), (1, 0))
    pygame.draw.line(colour_rect, bottom_colour, (0, 1), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)

def profilePicture(window, centre, color, player, playerNum, width=None):
    if width == None:
        width = window.get_size()[0]/15
    try:
        image_original  = pygame.image.load('Pictures/' + player + '.png').convert()
    except:
        image_original  = pygame.image.load(f'Pictures/Blank{playerNum+1}.png').convert()
    image = pygame.transform.scale(image_original, [image_original.get_size()[i]*(width/image_original.get_size()[0]) for i in range(2)])
    cropped_image  = pygame.Surface((max(image.get_size()), max(image.get_size())), pygame.SRCALPHA)

    image_pos = [centre[i] - max(image.get_size())/2 for i in range(2)]

    color = (*color[:3], color[3])
    pygame.draw.circle(window, color, [i + max(image.get_size())/2 for i in image_pos], min(image.get_size())/1.75)

    pygame.draw.circle(cropped_image, (255, 255, 255, 255), [i/2 for i in cropped_image.get_size()], min(image.get_size())/2)
    cropped_image.blit(image, [(max(image.get_size()) - image.get_size()[i])/2 for i in range(2)], special_flags=pygame.BLEND_RGBA_MIN)

    window.blit(cropped_image, image_pos)

    font_obj = pygame.font.SysFont('system', int(width/2))
    text_surface_obj = font_obj.render(player, True, pygameColors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (centre[0], centre[1] + width*0.9)

    window.blit(text_surface_obj, text_rect_obj)

def drawDiamond(window, color, centre, radius):
    points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0]+radius, centre[1]], [centre[0], centre[1]-radius]]
    pygame.draw.polygon(window, color, points)

def drawHalfDiamond(window, color, centre, radius, side):
    if side == 'left':
        points = [[centre[0], centre[1]+radius], [centre[0]+radius, centre[1]], [centre[0], centre[1]-radius]]
    elif side == 'right':
        points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0], centre[1]-radius]]
    elif side == 'top':
        points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0]+radius, centre[1]]]
    pygame.draw.polygon(window, color, points)

def drawTower(window, color, off_color, bottom_centre, score, radius, gap=3):
    count, score_row = 0, -1
    for row in range(22):
        if row < 10:
            horizontal, vertical = (i - (row*(radius+gap)) for i in bottom_centre)
            for column in range(row+1)[::-1]:
                drawDiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius)
                count += 1
                if count == score:
                    score_row = 1*row
                    color = off_color

        elif row == 21:
            vertical = bottom_centre[1] - (row*(radius+gap))
            horizontal = bottom_centre[0] - (9*(radius+gap))
            for column in range(10)[::-1]:
                drawHalfDiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius, 'top')
                count += 1
                if count == score:
                    score_row = 1*row
                    color = off_color
        else:
            vertical = bottom_centre[1] - (row*(radius+gap))
            if row%2 == 0:
                horizontal = bottom_centre[0] - (10*(radius+gap))
                for column in range(11)[::-1]:
                    if column == 0:
                        drawHalfDiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius, 'left')
                        count += 1
                        if count == score:
                            score_row = 1*row
                            color = off_color
                    elif column < 10:
                        drawDiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius)
                        count += 1
                        if count == score:
                            score_row = 1*row
                            color = off_color
                    else:
                        drawHalfDiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius, 'right')
                        count += 1
                        if count == score:
                            score_row = 1*row
                            color = off_color
    
            else:
                horizontal = bottom_centre[0] - (9*(radius+gap))
                for column in range(10)[::-1]:
                    drawDiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius)
                    count += 1
                    if count == score:
                        score_row = 1*row
                        color = off_color

    font_obj = pygame.font.SysFont('system', int(window.get_size()[0]/20))
    text_surface_obj = font_obj.render(str(score), True, pygameColors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (bottom_centre[0], bottom_centre[1] - ((score_row+3)*(radius+gap)))

    window.blit(text_surface_obj, text_rect_obj)

def drawTurnMarker(window, centre, radius, filled=False, left=True):
    if left:
        # top left, top right, bottom right, bottom left, centre double left
        points = [[centre[0] - radius, centre[1] - radius], [centre[0] + radius, centre[1] - radius], [centre[0] + radius, centre[1] + radius], [centre[0] - radius, centre[1] + radius], [centre[0] - 2*radius, centre[1]]]
    else:
        # top right, top left, bottom left, bottom right, centre double right
        points = [[centre[0] + radius, centre[1] - radius], [centre[0] - radius, centre[1] - radius], [centre[0] - radius, centre[1] + radius], [centre[0] + radius, centre[1] + radius], [centre[0] + 2*radius, centre[1]]]
    if filled:
        pygame.draw.polygon(window, pygameColors['white'], points)
    else:
        pygame.draw.polygon(window, pygameColors['white'], points, width=1)

def drawTurnMarkers(window, centre, radius, turn=None, left=True):
    for t, height in enumerate([centre[1] - 3*radius, centre[1], centre[1] + 3*radius]):
        drawTurnMarker(window, [centre[0], height], radius, t == turn, left)

def drawDemolition(window, player, turn, players, scores, FPS=30):
    window.fill([255,255,255])
    gradientRect( window, (95, 4, 107), (152, 88, 182), pygame.Rect( 0, 0, *window.get_size() ) )
    centres = [[window.get_size()[0]*(i/len(players) - (1-((len(players)-1)*(1/len(players))))/2), window.get_size()[1]*0.7 + (window.get_size()[1]*0.05*(len(players) < 6))] for i in range(1, (len(players)+1))]
    tower_colors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    tower_offcolors = [[j/2.5 for j in i] for i in tower_colors]
    
    if len(players) == 6:
        radius = window.get_size()[0]/250
    elif len(players) > 6:
        print('Too many players!')
        pygame.quit()
        return
    else:
        radius = window.get_size()[0]/200

    for i in range(len(players)):
        profilePicture(window, centres[i], tower_colors[i], players[i], i)
        if player == players[i]:
            drawTurnMarkers(window, [centres[i][0] + window.get_size()[0]/15, centres[i][1]], radius, turn)
        else:
            drawTurnMarkers(window, [centres[i][0] + window.get_size()[0]/15, centres[i][1]], radius, None)
        drawTower(window, tower_colors[i], tower_offcolors[i], [centres[i][0], centres[i][1] - window.get_size()[1]*0.2], scores[i], radius)

    drawBorders(window, 'Demolition', 0.02, radius, pygameColors['white'])
    pygame.display.flip()

def inputScoreDemolition(window, player, turn, players, scores, FPS=30):
    centres = [[window.get_size()[0]*(i/len(players) - (1-((len(players)-1)*(1/len(players))))/2), window.get_size()[1]*0.7 + (window.get_size()[1]*0.05*(len(players) < 6))] for i in range(1, (len(players)+1))]
    tower_colors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    tower_offcolors = [[j/2.5 for j in i] for i in tower_colors]

    font = pygame.font.SysFont('system', int(window.get_size()[0]/30))
    fpsClock = pygame.time.Clock()
    width, height = window.get_size()[0]/10, window.get_size()[1]/10
    input_box_centre = [centres[turn][0], centres[turn][1] + window.get_size()[1]/5]
    input_box = pygame.Rect(*input_box_centre, width, height)
    input_box.center = input_box_centre
    color_inactive = tower_offcolors[turn]
    color_active = tower_colors[turn]
    color = color_active
    active = True
    text = ''

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return []
                if active:
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif (len(text) < 1 and event.unicode) and ...:
                        text += event.unicode

        drawDemolition(window, player, turn, players, scores, FPS)
        txt_surface = font.render(text, True, tower_colors[turn])
        height = txt_surface.get_height()+10
        input_box.h = height
        input_box.center = input_box_centre
        window.blit(txt_surface, [input_box_centre[i] - txt_surface.get_size()[i]/2 for i in range(2)])
        # pygame.draw.rect(window, pygameColors['white'], input_box)
        pygame.draw.rect(window, color, input_box, 2)

        pygame.display.flip()
        fpsClock.tick(FPS)


def updateScoreDemolition(window, player, turn, new_score, players, scores):
    old_score = scores[players.index(player)]
    min_delay, max_delay = 0.005, 0.04
    if new_score > old_score:
        print('Error: new score must be less than or equal to old score')
        return
    else:
        while scores[players.index(player)] > new_score:
            pygame.event.get()
            scores[players.index(player)] -= 1
            drawDemolition(window, player, turn, players, scores)
            time.sleep(((min_delay - max_delay)/(old_score-new_score))*abs(scores[players.index(player)]-new_score+1)-(((min_delay - max_delay)/(old_score-new_score))*abs(old_score+1-new_score+1)))
            # time.sleep(((np.sqrt(max_delay)/(old_score-new_score+1))*(old_score-scores[players.index(player)]+1))**2)

    return scores

def drawCross(window, centre, radius, back_color, fore_color):
    pygame.draw.circle(window, back_color, centre, radius)
    pygame.draw.circle(window, fore_color, centre, radius, width=1)
    pygame.draw.line(window, fore_color, [centre[i] - (int(radius/(2**0.5)) - 1) for i in range(2)], [centre[i] + (int(radius/(2**0.5)) - 1) for i in range(2)])
    pygame.draw.line(window, fore_color, [centre[0] - (int(radius/(2**0.5)) - 1), centre[1] + (int(radius/(2**0.5)) - 1)], [centre[0] + (int(radius/(2**0.5)) - 1), centre[1] - (int(radius/(2**0.5)) - 1)])

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def drawTextWithOutline(window, text, fontsize, centre, color, outline_color=None, outline_thickness=2, blit=True):
    font = pygame.font.SysFont('system', fontsize)
    text_surface_obj = font.render(text, True, color).convert_alpha()
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = centre

    if blit:
        if outline_color != None:
            outline_text = font.render(text, True, outline_color).convert_alpha()
            for dx, dy in _circlepoints(outline_thickness):
                window.blit(outline_text, (dx + centre[0] - int(text_rect_obj.width/2) + 1, dy + centre[1] - int(text_rect_obj.height/2) - 1))

        window.blit(text_surface_obj, text_rect_obj)

    text_size = 1*text_rect_obj.size

    return text_size

def drawLineWithOutline(window, centre, width, thickness, color, outline_color=None, outline_thickness=2, direction='horizontal'):
    if direction == 'horizontal':
        if outline_color != None:
            for dx, dy in _circlepoints(outline_thickness):
                point_left, point_right = [centre[0] - width/2 + dx + 1, centre[1] + dy - 1], [centre[0] + width/2 + dx + 1, centre[1] + dy - 1]
                pygame.draw.line(window, outline_color, point_left, point_right, thickness)
        
        point_left, point_right = [centre[0] - width/2, centre[1]], [centre[0] + width/2, centre[1]]
        pygame.draw.line(window, color, point_left, point_right, thickness)

def drawUnderlineWithOutline(window, text_rect_obj_center, button_size, thickness, color, outline_color=None, outline_thickness=2, direction='horizontal'):
    if direction == 'horizontal':
        drawLineWithOutline(window, [text_rect_obj_center[0], text_rect_obj_center[1] + button_size[1]/1.5], button_size[0], thickness, color, outline_color, outline_thickness)

def drawRectWithOutline(window, rect, color, outline_color, outline_thickness):
    outline_rect = rect.copy()
    outline_rect.w += 2*outline_thickness
    outline_rect.h += 2*outline_thickness
    outline_rect.center = rect.center
    pygame.draw.rect(window, outline_color, outline_rect)
    pygame.draw.rect(window, color, rect)

def drawArrowSelector(window, centre, fontsize, width, curr_option, fore_color, back_color, leftHover=False, rightHover=False):
    font = pygame.font.SysFont('system', fontsize)
    text_surface_obj = font.render(curr_option, True, fore_color).convert_alpha()
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = centre
    box_rect_obj = text_rect_obj.copy()
    box_rect_obj.w = width
    box_rect_obj.center = centre
    leftButton_center, leftButton_button_size = [centre[0] - (width/2)*0.9 - (box_rect_obj.h/2)*0.6/2, centre[1]], ((width/2)*0.2 - (box_rect_obj.h/2)*0.6, box_rect_obj.h)
    rightButton_center, rightButton_button_size = [centre[0] + (width/2)*0.9 + (box_rect_obj.h/2)*0.6/2, centre[1]], ((width/2)*0.2 - (box_rect_obj.h/2)*0.6, box_rect_obj.h)

    drawRectWithOutline(window, box_rect_obj, back_color, fore_color, 2)
    if leftHover:
        pygame.draw.rect(window, pygameColors['grey40'], pygame.Rect([leftButton_center[i] - leftButton_button_size[i]/2 for i in [0, 1]], leftButton_button_size))
    if rightHover:
        pygame.draw.rect(window, pygameColors['grey40'], pygame.Rect([rightButton_center[i] - rightButton_button_size[i]/2 for i in [0, 1]], rightButton_button_size))
    window.blit(text_surface_obj, text_rect_obj)
    drawHalfDiamond(window, fore_color, [centre[0] - (width/2)*0.9, centre[1]], (box_rect_obj.h/2)*0.6, 'right')
    drawHalfDiamond(window, fore_color, [centre[0] + (width/2)*0.9, centre[1]], (box_rect_obj.h/2)*0.6, 'left')

    return leftButton_center, leftButton_button_size, rightButton_center, rightButton_button_size

def drawBorders(window, title, margin, radius, color, outline_color=None):
    title_font_obj = pygame.font.SysFont('system', int(window.get_size()[0]/40))
    title_text_surface_obj = title_font_obj.render(title, True, pygameColors['white'])
    title_text_rect_obj = title_text_surface_obj.get_rect()
    title_text_rect_obj_center = (window.get_size()[0]/2, max(window.get_size())*margin)
    drawTextWithOutline(window, title, int(window.get_size()[0]/40), title_text_rect_obj_center, color,
                    outline_color, 2)

    pygame.draw.line(window, pygameColors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, pygameColors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, pygameColors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    drawDiamond(window, pygameColors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

def drawMenu(window, players, addingPlayer=False):
    window.fill(pygameColors['white'])
    gradientRect( window, (63, 72, 204), (0, 162, 232), pygame.Rect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200

    drawBorders(window, 'Darts', margin, radius, pygameColors['white'])

    play_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    if len(players) > 1:
        play_button_size = drawTextWithOutline(window, 'Play', int(window.get_size()[0]/20),
                                           play_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)
    else:
        play_button_size = drawTextWithOutline(window, 'Play', int(window.get_size()[0]/20),
                                           play_text_rect_obj_center, pygameColors['red'], None, 2)

    addPlayer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    if len(players) < 6:
        addPlayer_button_size = drawTextWithOutline(window, 'Add Player', int(window.get_size()[0]/20),
                                                addPlayer_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2, not addingPlayer)
    else:
        addPlayer_button_size = drawTextWithOutline(window, 'Add Player', int(window.get_size()[0]/20),
                                                addPlayer_text_rect_obj_center, pygameColors['red'], pygameColors['red'], 2, not addingPlayer)

    settings_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.5)
    settings_button_size = drawTextWithOutline(window, 'Settings', int(window.get_size()[0]/20),
                                       settings_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    quit_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.8)
    quit_button_size = drawTextWithOutline(window, 'Quit', int(window.get_size()[0]/20),
                                       quit_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    playerColors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    crossDims = []
    for i in range(len(players)):
        picCentre = [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4]
        profilePicture(window, picCentre, playerColors[i], players[i], i)
        crossCentre = [picCentre[0] + window.get_size()[0]/33, picCentre[1] - window.get_size()[0]/33]
        crossRadius = window.get_size()[0]/100
        crossDims.append([crossCentre, crossRadius])

    return [play_button_size, play_text_rect_obj_center, addPlayer_button_size, addPlayer_text_rect_obj_center,
            settings_button_size, settings_text_rect_obj_center, quit_button_size, quit_text_rect_obj_center,
            crossDims]

def addPlayer(window, addPlayer_button_size, players):
    font = pygame.font.SysFont('system', int(window.get_size()[0]/20))
    clock = pygame.time.Clock()
    width, height = addPlayer_button_size[0], addPlayer_button_size[1]*1.25
    input_box_centre = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    input_box = pygame.Rect(*input_box_centre, width, height)
    input_box.center = input_box_centre
    color_inactive = pygameColors['grey59']
    color_active = pygameColors['white']
    color = color_active
    active = True
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return []
                if active:
                    if event.key == pygame.K_RETURN:
                        return [text]
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        drawMenu(window, players, True)
        txt_surface = font.render(text, True, color)
        width = max(width, txt_surface.get_width()+10)
        input_box.w = width
        input_box.center = input_box_centre
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(window, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def drawGameMenu(window, players):
    window.fill([255,255,255])
    gradientRect( window, (0, 204, 51), (0, 255, 128), pygame.Rect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200

    drawBorders(window, 'Play', margin, radius, pygameColors['white'])

    demolition_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    demolition_button_size = drawTextWithOutline(window, 'Demolition', int(window.get_size()[0]/20),
                                             demolition_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    killer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    killer_button_size = drawTextWithOutline(window, 'Killer', int(window.get_size()[0]/20),
                                         killer_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    back_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.8)
    back_button_size = drawTextWithOutline(window, 'Back', int(window.get_size()[0]/20),
                                       back_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    playerColors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    for i in range(len(players)):
       profilePicture(window, [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4],
                      playerColors[i], players[i], i)

    return [demolition_button_size, demolition_text_rect_obj_center, killer_button_size, killer_text_rect_obj_center,
            back_button_size, back_text_rect_obj_center]

def drawSettingsMenu(window, curr_resolution, resLeftHover, resRightHover):
    window.fill(pygameColors['white'])
    gradientRect( window, (80, 80, 80), (180, 180, 180), pygame.Rect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200
    centre_margin = window.get_size()[0]/30

    drawBorders(window, 'Settings', margin, radius, pygameColors['white'])

    font = pygame.font.SysFont('system', int(window.get_size()[0]/20))
    resolution_text_surface_obj = font.render('Display Resolution', True, pygameColors['white']).convert_alpha()
    resolution_text_rect_obj_center = (window.get_size()[0]/2 - resolution_text_surface_obj.get_rect().w/2 - centre_margin,
                                       window.get_size()[1]*0.2)
    drawTextWithOutline(window, 'Display Resolution', int(window.get_size()[0]/20),
                                           resolution_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    buttons = drawArrowSelector(window, [window.get_size()[0]/2 + (window.get_size()[0]/3)/2 + centre_margin,
                                         window.get_size()[1]*0.2], int(window.get_size()[0]/20),
                                window.get_size()[0]/3, curr_resolution, pygameColors['white'], pygameColors['black'],
                                resLeftHover, resRightHover)
    leftButton_center, leftButton_button_size = buttons[0], buttons[1]
    rightButton_center, rightButton_button_size = buttons[2], buttons[3]

    font = pygame.font.SysFont('system', int(window.get_size()[0]/20))
    back_text_surface_obj = font.render('Back', True, pygameColors['white']).convert_alpha()
    back_text_rect_obj_center = (window.get_size()[0]/2 - back_text_surface_obj.get_rect().w/2 - centre_margin,
                                       window.get_size()[1]*0.8)
    back_button_size = drawTextWithOutline(window, 'Back', int(window.get_size()[0]/20),
                                       back_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    font = pygame.font.SysFont('system', int(window.get_size()[0]/20))
    apply_text_surface_obj = font.render('Apply', True, pygameColors['white']).convert_alpha()
    apply_text_rect_obj_center = (window.get_size()[0]/2 + apply_text_surface_obj.get_rect().w/2 + centre_margin,
                                       window.get_size()[1]*0.8)
    apply_button_size = drawTextWithOutline(window, 'Apply', int(window.get_size()[0]/20),
                                       apply_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    return [leftButton_center, leftButton_button_size, rightButton_center, rightButton_button_size,
            back_button_size, back_text_rect_obj_center, apply_button_size, apply_text_rect_obj_center]

def drawSegment(window, centre, outer_radius, inner_radius, start_angle, end_angle, color):
    bounding_rect  = pygame.Surface((2*(2**0.5)*outer_radius, 2*(2**0.5)*outer_radius), pygame.SRCALPHA)
    bounding_rect.fill((0, 0, 0, 0))

    return_pos = [centre[i] - (2**0.5)*outer_radius for i in range(2)]

    pygame.draw.circle(bounding_rect, color, [bounding_rect.get_size()[i]/2 for i in [0, 1]], outer_radius)

    if end_angle - start_angle < pi/2:
        centre_angle = (end_angle + start_angle)/2
        points = [[bounding_rect.get_size()[i]/2 for i in [0, 1]]]
        for offset in [end_angle - centre_angle, pi/4, (3*pi)/4, (5*pi)/4, (7*pi)/4, start_angle - centre_angle]:
            x = bounding_rect.get_size()[0]/2 + outer_radius*(2**0.5)*sin(centre_angle+offset)
            y = bounding_rect.get_size()[1]/2 - outer_radius*(2**0.5)*cos(centre_angle+offset)
            points.append([x, y])
        pygame.draw.polygon(bounding_rect, (0, 0, 0, 0), points)
        pygame.draw.circle(bounding_rect, (0, 0, 0, 0), [bounding_rect.get_size()[i]/2 for i in [0, 1]], inner_radius)

    window.blit(bounding_rect, return_pos, special_flags=pygame.BLEND_RGBA_MAX)

def drawJaggedArc(window, centre, radius, color, width, start_angle, end_angle, jag_width, jag_num):
    points = []
    angle_range = abs(end_angle - start_angle)/jag_num
    for n, prop in enumerate(range(jag_num+1)):
        curr_angle = start_angle + angle_range*prop
        x = centre[0] + radius*sin(curr_angle) + (((-1)**n)*random()*jag_width*radius)
        y = centre[1] - radius*cos(curr_angle) - (((-1)**n)*random()*jag_width*radius)
        points.append([x, y])
    pygame.draw.lines(window, color, False, points, width)

    return points

def generateJaggedArc(centre, radius, start_angle, end_angle, jag_width, jag_num, fix_startandend=False):
    if fix_startandend:
        points = [fix_startandend[0]]
        angle_range = abs(end_angle - start_angle)/jag_num
        for n, prop in enumerate(range(1, jag_num)):
            curr_angle = start_angle + angle_range*prop
            x = centre[0] + radius*sin(curr_angle)
            y = centre[1] - radius*cos(curr_angle)
            x += (((-1)**(x > centre[0]))*((-1)**n)*random()*jag_width*radius)
            y += (((-1)**(y > centre[1]))*((-1)**n)*random()*jag_width*radius)
            points.append([x, y])
        points.append(fix_startandend[1])

    else:
        points = []
        angle_range = abs(end_angle - start_angle)/jag_num
        for n, prop in enumerate(range(jag_num+1)):
            curr_angle = start_angle + angle_range*prop
            x = centre[0] + radius*sin(curr_angle)
            y = centre[1] - radius*cos(curr_angle)
            x += (((-1)**(x > centre[0]))*((-1)**n)*random()*jag_width*radius)
            y += (((-1)**(y > centre[1]))*((-1)**n)*random()*jag_width*radius)
            points.append([x, y])

    return points

def generateJaggedArcsFixed(centre, outer_radius, inner_radius, start_angle, end_angle, jag_width, jag_num):
    fixed_points_inner = generateJaggedArc(centre, inner_radius, start_angle, end_angle, 0, 2)
    fixed_points_1_3 = generateJaggedArc(centre, outer_radius*(1/3), start_angle, end_angle, jag_width, jag_num,
                                         [[centre[0] + outer_radius*(1/3)*sin(start_angle),
                                           centre[1] - outer_radius*(1/3)*cos(start_angle)],
                                          [centre[0] + outer_radius*(1/3)*sin(end_angle),
                                           centre[1] - outer_radius*(1/3)*cos(end_angle)]])
    fixed_points_2_3 = generateJaggedArc(centre, outer_radius*(2/3), start_angle, end_angle, jag_width, jag_num,
                                         [[centre[0] + outer_radius*(2/3)*sin(start_angle),
                                           centre[1] - outer_radius*(2/3)*cos(start_angle)],
                                          [centre[0] + outer_radius*(2/3)*sin(end_angle),
                                           centre[1] - outer_radius*(2/3)*cos(end_angle)]])
    fixed_points_outer = generateJaggedArc(centre, outer_radius, start_angle, end_angle, 0, 20)

    return [fixed_points_inner, fixed_points_1_3, fixed_points_2_3, fixed_points_outer]

def drawSplitSegment(window, centre, outer_radius, inner_radius, start_angle, end_angle, on_colors, off_colors,
                     split_color, split_width, jag_width, jag_num, fixed, specialSegmentRadius=False):

    if on_colors[0]:
        points_inner = generateJaggedArc(centre, inner_radius, start_angle, end_angle, 0, 2)
        points_1_3_in = generateJaggedArc(centre, outer_radius*(1/3), start_angle, end_angle, jag_width, jag_num)
    else:
        points_inner = generateJaggedArc(centre, inner_radius, start_angle, end_angle, 0, 2,
                                          [[centre[0] + inner_radius*sin(start_angle),
                                            centre[1] - inner_radius*cos(start_angle)],
                                          [centre[0] + inner_radius*sin(end_angle),
                                            centre[1] - inner_radius*cos(end_angle)]])
        points_1_3_in = generateJaggedArc(centre, outer_radius*(1/3), start_angle, end_angle, jag_width, jag_num,
                                          [[centre[0] + outer_radius*(1/3)*sin(start_angle),
                                            centre[1] - outer_radius*(1/3)*cos(start_angle)],
                                          [centre[0] + outer_radius*(1/3)*sin(end_angle),
                                            centre[1] - outer_radius*(1/3)*cos(end_angle)]])

    if on_colors[1]:
        points_1_3_out = generateJaggedArc(centre, outer_radius*(1/3), start_angle, end_angle, jag_width, jag_num)
        points_2_3_in = generateJaggedArc(centre, outer_radius*(2/3), start_angle, end_angle, jag_width, jag_num)
    else:
        points_1_3_out = generateJaggedArc(centre, outer_radius*(1/3), start_angle, end_angle, jag_width, jag_num,
                                            [[centre[0] + outer_radius*(1/3)*sin(start_angle),
                                              centre[1] - outer_radius*(1/3)*cos(start_angle)],
                                            [centre[0] + outer_radius*(1/3)*sin(end_angle),
                                              centre[1] - outer_radius*(1/3)*cos(end_angle)]])
        points_2_3_in = generateJaggedArc(centre, outer_radius*(2/3), start_angle, end_angle, jag_width, jag_num,
                                          [[centre[0] + outer_radius*(2/3)*sin(start_angle),
                                            centre[1] - outer_radius*(2/3)*cos(start_angle)],
                                            [centre[0] + outer_radius*(2/3)*sin(end_angle),
                                            centre[1] - outer_radius*(2/3)*cos(end_angle)]])

    if on_colors[2]:
        points_2_3_out = generateJaggedArc(centre, outer_radius*(2/3), start_angle, end_angle, jag_width, jag_num)
        points_outer = generateJaggedArc(centre, outer_radius*1.03, start_angle, end_angle, jag_width, jag_num)
    else:
        points_2_3_out = generateJaggedArc(centre, outer_radius*(2/3), start_angle, end_angle, jag_width, jag_num,
                                          [[centre[0] + outer_radius*(2/3)*sin(start_angle),
                                            centre[1] - outer_radius*(2/3)*cos(start_angle)],
                                          [centre[0] + outer_radius*(2/3)*sin(end_angle),
                                            centre[1] - outer_radius*(2/3)*cos(end_angle)]])
        points_outer = generateJaggedArc(centre, outer_radius, start_angle, end_angle, 0, 20,
                                          [[centre[0] + outer_radius*sin(start_angle),
                                            centre[1] - outer_radius*cos(start_angle)],
                                          [centre[0] + outer_radius*sin(end_angle),
                                            centre[1] - outer_radius*cos(end_angle)]])

    if specialSegmentRadius:
        if on_colors[2]:
            pygame.draw.polygon(window, on_colors[0], points_1_3_in + points_inner[::-1])
            pygame.draw.polygon(window, on_colors[1], points_2_3_in + points_1_3_out[::-1])
            pygame.draw.polygon(window, off_colors[2], points_outer + points_2_3_out[::-1])
            points_special = generateJaggedArc(centre, specialSegmentRadius, start_angle, end_angle, jag_width, jag_num,
                                               [[centre[0] + specialSegmentRadius*sin(start_angle),
                                                 centre[1] - specialSegmentRadius*cos(start_angle)],
                                                [centre[0] + specialSegmentRadius*sin(end_angle),
                                                 centre[1] - specialSegmentRadius*cos(end_angle)]])
            pygame.draw.polygon(window, on_colors[2], points_special + points_inner[::-1])
        elif on_colors[1]:
            pygame.draw.polygon(window, on_colors[0], points_1_3_in + points_2_3_out[::-1])
            pygame.draw.polygon(window, off_colors[1], fixed[2] + fixed[1][::-1])
            pygame.draw.polygon(window, off_colors[2], fixed[3] + fixed[2][::-1])
            points_special = generateJaggedArc(centre, specialSegmentRadius, start_angle, end_angle, jag_width, jag_num,
                                               [[centre[0] + specialSegmentRadius*sin(start_angle),
                                                 centre[1] - specialSegmentRadius*cos(start_angle)],
                                                [centre[0] + specialSegmentRadius*sin(end_angle),
                                                 centre[1] - specialSegmentRadius*cos(end_angle)]])
            pygame.draw.polygon(window, on_colors[1], points_special + points_1_3_out[::-1])
        else:
            pygame.draw.polygon(window, off_colors[0], fixed[1] + fixed[0][::-1])
            pygame.draw.polygon(window, off_colors[1], fixed[2] + fixed[1][::-1])
            pygame.draw.polygon(window, off_colors[2], fixed[3] + fixed[2][::-1])
            points_special = generateJaggedArc(centre, specialSegmentRadius, start_angle, end_angle, jag_width, jag_num,
                                               [[centre[0] + specialSegmentRadius*sin(start_angle),
                                                 centre[1] - specialSegmentRadius*cos(start_angle)],
                                                [centre[0] + specialSegmentRadius*sin(end_angle),
                                                 centre[1] - specialSegmentRadius*cos(end_angle)]])
            pygame.draw.polygon(window, on_colors[0], points_special + points_inner[::-1])
    else:
        if on_colors[0]:
            pygame.draw.polygon(window, on_colors[0], points_1_3_in + points_inner[::-1])
        else:
            pygame.draw.polygon(window, off_colors[0], fixed[1] + fixed[0][::-1])

        if on_colors[1]:
            pygame.draw.polygon(window, on_colors[1], points_2_3_in + points_1_3_out[::-1])
        else:
            pygame.draw.polygon(window, off_colors[1], fixed[2] + fixed[1][::-1])

        if on_colors[2]:
            pygame.draw.polygon(window, on_colors[2], points_outer + points_2_3_out[::-1])
        else:
            pygame.draw.polygon(window, off_colors[2], fixed[3] + fixed[2][::-1])

    if on_colors[0]:
        pygame.draw.lines(window, split_color, False, points_inner, split_width)
        pygame.draw.lines(window, split_color, False, points_1_3_in, split_width)
    else:
        pygame.draw.lines(window, split_color, False, fixed[0], split_width)
        pygame.draw.lines(window, split_color, False, fixed[1], split_width)

    if on_colors[1]:
        pygame.draw.lines(window, split_color, False, points_2_3_in, split_width)
    else:
        pygame.draw.lines(window, split_color, False, fixed[2], split_width)

    if on_colors[2]:
        pygame.draw.lines(window, split_color, False, points_outer, split_width)
    else:
        pygame.draw.lines(window, split_color, False, fixed[3], split_width)

    pygame.draw.lines(window, split_color, False, [points_inner[0], points_1_3_in[0], points_1_3_out[0],
                                                 points_2_3_in[0], points_2_3_out[0], points_outer[0]], split_width)
    pygame.draw.lines(window, split_color, False, [points_inner[-1], points_1_3_in[-1], points_1_3_out[-1],
                                                 points_2_3_in[-1], points_2_3_out[-1], points_outer[-1]], split_width)

def drawSegmentTest(n):
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygame.display.set_mode((info.current_w, (info.current_h-60)))
    gradientRect( window, (136/5, 0, 21/5), (240, 0, 36), pygame.Rect( 0, 0, *window.get_size() ) )

    drawDartBoard(window, [window.get_size()[i]/2 for i in [0, 1]], window.get_size()[1]*0.3, pygameColors['white'])

    centre = [window.get_size()[i]/2 for i in [0, 1]]
    outer_radius, inner_radius = window.get_size()[1]*0.3, window.get_size()[1]*0.3*(16/170)
    start_angle, end_angle, jag_width, jag_num = pi/20, (3*pi)/20, 0.02, 10
    fixed = generateJaggedArcsFixed(centre, outer_radius, inner_radius, start_angle, end_angle, jag_width, jag_num)

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {}'.format(x, y))

        window.fill(pygameColors['white'])
        gradientRect( window, (136/5, 0, 21/5), (240, 0, 36), pygame.Rect( 0, 0, *window.get_size() ) )
        drawDartBoard(window, [window.get_size()[i]/2 for i in [0, 1]], window.get_size()[1]*0.3, pygameColors['white'])

        if n == 0:
            colors = [False, False, False]
        if n == 1:
            colors = [pygameColors['red'], False, False]
        if n == 2:
            colors = [pygameColors['red'], pygameColors['red'], False]
        if n == 3:
            colors = [pygameColors['red'], pygameColors['red'], pygameColors['red']]
        drawSplitSegment(window, centre, outer_radius, inner_radius, start_angle, end_angle, colors,
                         [pygameColors['darkred']]*3, pygameColors['black'], 5, jag_width, jag_num, fixed)

        pygame.display.flip()

        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

def drawDartBoard(window, centre, radius, color, width=3):

    pygame.draw.circle(window, color, centre, radius, width)
    pygame.draw.circle(window, color, centre, radius*(162/170), width)
    pygame.draw.circle(window, color, centre, radius*(107/170), width)
    pygame.draw.circle(window, color, centre, radius*(99/170), width)
    pygame.draw.circle(window, color, centre, radius*(16/170), width)
    pygame.draw.circle(window, color, centre, radius*(6.35/170), width)

    for angle in range(20):
        inner_x = centre[0] + radius*(16/170)*sin(((angle+0.5)/20)*2*pi)
        inner_y = centre[1] + radius*(16/170)*cos(((angle+0.5)/20)*2*pi)
        outer_x = centre[0] + radius*sin(((angle+0.5)/20)*2*pi)
        outer_y = centre[1] + radius*cos(((angle+0.5)/20)*2*pi)
        inner_x += (-1)**(inner_x > centre[0])
        inner_y += (-1)**(inner_y > centre[1])
        outer_x += (-1)**(outer_x > centre[0])
        outer_y += (-1)**(outer_y > centre[1])
        pygame.draw.line(window, color, (inner_x, inner_y), (outer_x, outer_y), width)

def dartBoardAngles(n):
    starts = [0.5, 7.5, 9.5, 2.5, 18.5, 4.5, 11.5, 13.5, 16.5, 5.5,
              14.5, 17.5, 3.5, 15.5, 6.5, 12.5, 8.5, 1.5, 10.5, 19.5]
    return [((starts[n-1]-0.1)/20)*2*pi, ((starts[n-1]+1.1)/20)*2*pi]

def cartesianFromPolar(centre, radius, angle):
    x = centre[0] + radius*sin(angle)
    y = centre[1] - radius*cos(angle)
    return [x, y]

def drawRoundMarker(window, centre, height, roundNum):
    drawTextWithOutline(window, 'ROUND', int(window.get_size()[0]/45), [centre[0], centre[1] - height],
                        pygameColors['white'])
    for i in range(1, 7)[::-1]:
        if roundNum < 7 and 7-i == roundNum:
            pygame.draw.circle(window, pygameColors['white'], [centre[0], centre[1] - (i*height)/7],
                             window.get_size()[0]/200)
        else:
            pygame.draw.circle(window, pygameColors['white'], [centre[0], centre[1] - (i*height)/7],
                             window.get_size()[0]/200, width=1)
    drawTextWithOutline(window, '-×2-', int(window.get_size()[0]/45), [centre[0], centre[1]], pygameColors['white'])
    for i in range(1, 4):
        if roundNum >= 7 and i+6 == roundNum:
            pygame.draw.circle(window, pygameColors['white'], [centre[0], centre[1] + (i*height)/7],
                             window.get_size()[0]/200)
        else:
            pygame.draw.circle(window, pygameColors['white'], [centre[0], centre[1] + (i*height)/7],
                             window.get_size()[0]/200, width=1)
    drawTextWithOutline(window, '-×3-', int(window.get_size()[0]/45), [centre[0], centre[1] + (4*height)/7],
                        pygameColors['white'])
    for i in range(5, 8)[::-1]:
        if roundNum >= 7 and i+5 == roundNum:
            pygame.draw.circle(window, pygameColors['white'], [centre[0], centre[1] + (i*height)/7],
                             window.get_size()[0]/200)
        else:
            pygame.draw.circle(window, pygameColors['white'], [centre[0], centre[1] + (i*height)/7],
                             window.get_size()[0]/200, width=1)

def drawKiller(window, player, turn, players, positions, segments, roundNum, fixed, dartBoardRadius,
               specialSegmentRadius=False):
    gradientRect( window, (136/5, 0, 21/5), (240, 0, 36), pygame.Rect( 0, 0, *window.get_size() ) )
    segment_colors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    segment_offcolors = [[j/2.5 for j in i] for i in segment_colors]

    centre = [window.get_size()[i]/2 for i in [0, 1]]
    drawDartBoard(window, centre, dartBoardRadius, pygameColors['white'])

    for i in range(len(players)):
        angles = dartBoardAngles(positions[i])
        if specialSegmentRadius and i == specialSegmentRadius[0]:
            drawSplitSegment(window, centre, dartBoardRadius, dartBoardRadius*(16/170),
                             *angles, [segment_colors[i]]*segments[i] + [False]*(3-segments[i]),
                             [segment_offcolors[i]]*3, pygameColors['black'], 5, segments[i]*0.01, 10, fixed[i],
                             specialSegmentRadius[1])
        else:
            drawSplitSegment(window, centre, dartBoardRadius, dartBoardRadius*(16/170),
                             *angles, [segment_colors[i]]*segments[i] + [False]*(3-segments[i]),
                             [segment_offcolors[i]]*3, pygameColors['black'], 5, segments[i]*0.01, 10, fixed[i])
        if segments[i] == 3:
            skullCentre = cartesianFromPolar(centre, dartBoardRadius*0.85, sum(angles)/2)
            skullImage_original  = pygame.image.load('KillerSkull.png').convert()
            skullImage = pygame.transform.scale(skullImage_original, [skullImage_original.get_size()[i]*(dartBoardRadius*0.2/skullImage_original.get_size()[0]) for i in range(2)])
            skullImage_rotated = pygame.transform.rotate(skullImage, -(sum(angles)/2)*(180/pi))
            new_rect = skullImage_rotated.get_rect(center = skullCentre)
            window.blit(skullImage_rotated, new_rect, special_flags=pygame.BLEND_RGBA_MIN)

        textCentre = cartesianFromPolar(centre, dartBoardRadius*1.2, sum(angles)/2)
        drawTextWithOutline(window, str(positions[i]), int(window.get_size()[0]/30), textCentre, segment_colors[i],
                            pygameColors['black'], 2)
        if positions[i] == 20:
            picture_x = textCentre[0] + ((-1)**(textCentre[0] < centre[0]))*dartBoardRadius*0.5
            turnMarker_x = textCentre[0] + ((-1)**(textCentre[0] < centre[0]))*dartBoardRadius*0.8
        else:
            picture_x = textCentre[0] + ((-1)**(textCentre[0] < centre[0]))*dartBoardRadius*0.35
            turnMarker_x = textCentre[0] + ((-1)**(textCentre[0] < centre[0]))*dartBoardRadius*0.65

        profilePicture(window, [picture_x, textCentre[1]], segment_colors[i], players[i], i, window.get_size()[0]/25)
        if player == players[i]:
            drawTurnMarkers(window, [turnMarker_x, textCentre[1]], window.get_size()[0]/200, turn,
                            textCentre[0] > centre[0])
        else:
            drawTurnMarkers(window, [turnMarker_x, textCentre[1]], window.get_size()[0]/200, None,
                            textCentre[0] > centre[0])
        
    drawRoundMarker(window, [window.get_size()[0]*0.95, centre[1]], window.get_size()[1]*0.25, roundNum)
    drawBorders(window, 'Killer', 0.02, window.get_size()[0]/200, pygameColors['white'])

def updateKiller(window, player, turn, players, positions, segments, roundNum, fixed, dartBoardRadius, direction,
                 fpsClock, FPS):
    if segments[players.index(player)] == 0:
        radius = dartBoardRadius*(16/170)
        finalRadius = dartBoardRadius*((segments[players.index(player)] + direction)/3)
    elif segments[players.index(player)] == 1 and direction == -1:
        radius = dartBoardRadius*(segments[players.index(player)]/3)
        finalRadius = dartBoardRadius*(16/170)
    else:
        radius = dartBoardRadius*(segments[players.index(player)]/3)
        finalRadius = dartBoardRadius*((segments[players.index(player)] + direction)/3)

    dradius = abs(finalRadius - radius)

    while (direction == 1 and radius < finalRadius) or (direction == -1 and radius > finalRadius):

        radius += direction*(dradius/(FPS*2))

        drawKiller(window, player, turn, players, positions, segments, roundNum, fixed, dartBoardRadius,
                   [players.index(player), radius])

        pygame.display.flip()

        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

def drawKillerTest(window, _):
    
    FPS = 120 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Liv', 'Rosie']
    positions = [9, 17, 7, 20, 18, 10]
    segments = [3, 1, 0, 2, 3, 1]
    # segments = [3, 3, 3, 3, 3, 3]
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []
    
    osEnviron['SDL_VIDEO_WINDOW_POS'] = maximised_pos
    fullscreen = False

    dartBoardRadius = window.get_size()[1]*0.3

    fixed = []
    for i in range(len(players)):
        fixed.append(generateJaggedArcsFixed([window.get_size()[i]/2 for i in [0, 1]], dartBoardRadius,
                                             dartBoardRadius*(16/170), *dartBoardAngles(positions[i]),
                                             0.02, 10))

    specialRadius, direction = dartBoardRadius*(107/170), 1

    numFrames, frameCheck = 0, time.time()

    while True:
        if specialRadius >= dartBoardRadius*1.03:
            direction = -1
        elif specialRadius <= dartBoardRadius*(107/170):
            direction = 1
        specialRadius += direction*((dartBoardRadius*(1.03 - (107/170)))/(FPS*2))

        drawKiller(window, players[0], 0, players, positions, segments, 5, fixed, dartBoardRadius, [4, specialRadius])

        pygame.display.flip()

        fpsClock.tick(FPS)
        numFrames += 1
        if time.time() - frameCheck > 1:
            pygame.display.set_caption('Darts - Killer - {0} fps'.format(numFrames))
            numFrames, frameCheck = 0, time.time()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if fullscreen:
                        pygame.display.quit()
                        osEnviron['SDL_VIDEO_WINDOW_POS'] = maximised_pos
                        pygame.display.init()
                        window = pygame.display.set_mode(maximised_res, pygame.RESIZABLE)
                    else:
                        pygame.display.quit()
                        osEnviron['SDL_VIDEO_WINDOW_POS'] = "0,0"
                        pygame.display.init()
                        window = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
                    fullscreen = not fullscreen

            elif event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                dartBoardRadius = window.get_size()[1]*0.35
            
                fixed = []
                for i in range(len(players)):
                    fixed.append(generateJaggedArcsFixed([window.get_size()[i]/2 for i in [0, 1]], dartBoardRadius,
                                                         dartBoardRadius*(16/170), *dartBoardAngles(positions[i]),
                                                         0.02, 10))

def threadingTest():
    global stop_threads
    
    def background():
        while True:
            time.sleep(3)
            print('disarm me by typing disarm')
            if stop_threads:
                break


    def other_function():
        print('You disarmed me! Dying now.')

    # now threading1 runs regardless of user input
    stop_threads = False
    threading1 = threading.Thread(target=background)
    threading1.daemon = True
    threading1.start()
    
    while True:
        if input() == 'disarm':
            stop_threads = True
            threading1.join()
            other_function()
            break
        else:
            print('not disarmed')



