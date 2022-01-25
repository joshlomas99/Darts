import time, os, sys
import pygame
from pygame.locals import QUIT
from pygame.color import THECOLORS as colors
from Darts import Demolition

# os.environ['SDL_VIDEO_WINDOW_POS'] = "384,200"
# os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
# os.environ['SDL_VIDEO_CENTERED'] = '1'
maximised_res = (1536, 801)
maximised_pos = "0,20"

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
    players = []

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

def profilePicture(window, centre, color, player, playerNum):
    try:
        image_original  = pygame.image.load('Pictures/' + player + '.png').convert()
    except:
        image_original  = pygame.image.load(f'Pictures/Blank{playerNum+1}.png').convert()
    image = pygame.transform.scale(image_original, [image_original.get_size()[i]*((window.get_size()[0]/15)/image_original.get_size()[0]) for i in range(2)])
    cropped_image  = pygame.Surface((max(image.get_size()), max(image.get_size())), pygame.SRCALPHA)

    image_pos = [centre[i] - max(image.get_size())/2 for i in range(2)]

    color = (*color[:3], color[3])
    pygame.draw.circle(window, color, [i + max(image.get_size())/2 for n, i in enumerate(image_pos)], min(image.get_size())/1.75)

    pygame.draw.circle(cropped_image, (255, 255, 255, 255), [i/2 for i in cropped_image.get_size()], min(image.get_size())/2)
    cropped_image.blit(image, [(max(image.get_size()) - image.get_size()[i])/2 for i in range(2)], special_flags=pygame.BLEND_RGBA_MIN)

    window.blit(cropped_image, image_pos)

    font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/50))
    text_surface_obj = font_obj.render(player, True, colors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (centre[0], centre[1] + window.get_size()[1]/9)

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

    font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    text_surface_obj = font_obj.render(str(score), True, colors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (bottom_centre[0], bottom_centre[1] - ((score_row+3)*(radius+gap)))

    window.blit(text_surface_obj, text_rect_obj)

def drawTurnMarker(window, centre, radius, filled=False):
    points = [[centre[0] - radius, centre[1] - radius], [centre[0] + radius, centre[1] - radius], [centre[0] + radius, centre[1] + radius], [centre[0] - radius, centre[1] + radius], [centre[0] - 2*radius, centre[1]]]
    if filled:
        pygame.draw.polygon(window, colors['white'], points)
    else:
        pygame.draw.polygon(window, colors['white'], points, width=1)

def drawTurnMarkers(window, centre, radius, turn=None):
    for t, height in enumerate([centre[1] - 3*radius, centre[1], centre[1] + 3*radius]):
        if t == turn:
            drawTurnMarker(window, [centre[0], height], radius, filled=True)
        else:
            drawTurnMarker(window, [centre[0], height], radius, filled=False)

def drawDemolition(window, player, turn, players, scores):
    window.fill([255,255,255])
    gradientRect( window, (95, 4, 107), (152, 88, 182), pygame.Rect( 0, 0, *window.get_size() ) )
    centres = [[window.get_size()[0]*(i/len(players) - (1-((len(players)-1)*(1/len(players))))/2), window.get_size()[1]*0.7 + (window.get_size()[1]*0.05*(len(players) < 6))] for i in range(1, (len(players)+1))]
    tower_colors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['cyan'], colors['orange']]
    tower_offcolors = [[j/2.5 for j in i] for i in tower_colors]

    for i in range(len(players)):
        profilePicture(window, centres[i], tower_colors[i], players[i], i)
        if len(players) == 6:
            radius = window.get_size()[0]/250
        elif len(players) > 6:
            print('Too many players!')
            pygame.quit()
            return
        else:
            radius = window.get_size()[0]/200
        if player == players[i]:
            drawTurnMarkers(window, [centres[i][0] + window.get_size()[0]/15, centres[i][1]], radius, turn)
        else:
            drawTurnMarkers(window, [centres[i][0] + window.get_size()[0]/15, centres[i][1]], radius, None)
        drawTower(window, tower_colors[i], tower_offcolors[i], [centres[i][0], centres[i][1] - window.get_size()[1]*0.2], scores[i], radius)

    margin = 0.02

    font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/50))
    text_surface_obj = font_obj.render('Demolition', True, colors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (window.get_size()[0]/2, max(window.get_size())*margin)

    window.blit(text_surface_obj, text_rect_obj)

    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [window.get_size()[0]/2 + text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    drawDiamond(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0]/2 - text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0]/2 + text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

    pygame.display.flip()

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

def playDemolition(player, turn, players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy'], scores = [180, 180, 180, 180, 180, 180]):
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    window = pygame.display.set_mode((info.current_w/2, (info.current_h-60)/2))

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # scores = [180, 26, 102, 84, 76, 18]
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # scores = [180, 180, 180, 180, 180]
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # scores = [86, 162, 151, 153]
    players = ['Josh', 'Ben', 'Luke']
    scores = [180, 180, 180]
    # players = ['Josh', 'Ben']
    # scores = [180, 180]

    drawDemolition(window, player, turn, players, scores)
    new_score = 30
    scores = updateScoreDemolition(window, 'Josh', 1, new_score, players, scores)

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {}'.format(x, y))
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

def setupDemolition(players, scores):
    pygame.init()

    info = pygame.display.Info()

    window = pygame.display.set_mode((info.current_w/2, (info.current_h-60)/2))
    drawDemolition(window, players[0], 0, players, scores)
    return window

def drawCross(window, centre, radius, back_color, fore_color):
    pygame.draw.circle(window, back_color, centre, radius)
    pygame.draw.circle(window, fore_color, centre, radius, width=1)
    pygame.draw.line(window, fore_color, [centre[i] - (int(radius/(2**0.5)) - 1) for i in range(2)], [centre[i] + (int(radius/(2**0.5)) - 1) for i in range(2)])
    pygame.draw.line(window, fore_color, [centre[0] - (int(radius/(2**0.5)) - 1), centre[1] + (int(radius/(2**0.5)) - 1)], [centre[0] + (int(radius/(2**0.5)) - 1), centre[1] - (int(radius/(2**0.5)) - 1)])

def drawCrossTest():
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
    players = []

    window = pygame.display.set_mode((info.current_w/2, (info.current_h-60)/2))
    window.fill(colors['yellow'])

    drawCross(window, [window.get_size()[i]/2 for i in [0, 1]], min(window.get_size())/2*0.75, colors['white'], colors['black'])

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
    font = pygame.font.Font('freesansbold.ttf', fontsize)
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
    font = pygame.font.Font('freesansbold.ttf', fontsize)
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
        pygame.draw.rect(window, colors['grey40'], pygame.Rect([leftButton_center[i] - leftButton_button_size[i]/2 for i in [0, 1]], leftButton_button_size))
    if rightHover:
        pygame.draw.rect(window, colors['grey40'], pygame.Rect([rightButton_center[i] - rightButton_button_size[i]/2 for i in [0, 1]], rightButton_button_size))
    window.blit(text_surface_obj, text_rect_obj)
    drawHalfDiamond(window, fore_color, [centre[0] - (width/2)*0.9, centre[1]], (box_rect_obj.h/2)*0.6, 'right')
    drawHalfDiamond(window, fore_color, [centre[0] + (width/2)*0.9, centre[1]], (box_rect_obj.h/2)*0.6, 'left')

    return leftButton_center, leftButton_button_size, rightButton_center, rightButton_button_size

def drawArrowSelectorTest():
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    resolutions, resolution_index = [], 0
    for resolution in pygame.display.list_modes():
        resolutions.append(' × '.join([str(i) for i in resolution]))
    resolutions.reverse()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygame.display.set_mode((info.current_w, (info.current_h-60)), pygame.RESIZABLE)
    window.fill(colors['blue'])

    buttons = drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], colors['white'], colors['black'])
    leftButton_center, leftButton_button_size = buttons[0], buttons[1]
    rightButton_center, rightButton_button_size = buttons[2], buttons[3]

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        window.fill(colors['blue'])

        mouse_on_leftButton, mouse_on_rightButton = False, False
        if abs(x - leftButton_center[0]) <= leftButton_button_size[0]/2 and abs(y - leftButton_center[1]) <= leftButton_button_size[1]/2:
            mouse_on_leftButton = True
            drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], colors['white'], colors['black'], True, False)


        elif abs(x - rightButton_center[0]) <= rightButton_button_size[0]/2 and abs(y - rightButton_center[1]) <= rightButton_button_size[1]/2:
            mouse_on_rightButton = True
            drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], colors['white'], colors['black'], False, True)

        else:
            drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], colors['white'], colors['black'])

        pygame.display.flip()

        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_leftButton:
                    resolution_index -= 1
                    resolution_index %= len(resolutions)

                if mouse_on_rightButton:
                    resolution_index += 1
                    resolution_index %= len(resolutions)

def drawBorders(window, title, margin, radius, color, outline_color=None):
    title_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/50))
    title_text_surface_obj = title_font_obj.render(title, True, colors['white'])
    title_text_rect_obj = title_text_surface_obj.get_rect()
    title_text_rect_obj_center = (window.get_size()[0]/2, max(window.get_size())*margin)
    drawTextWithOutline(window, title, int(window.get_size()[0]/50), title_text_rect_obj_center, color,
                    outline_color, 2)

    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    drawDiamond(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, colors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

def drawMenu(window, players, addingPlayer=False):
    window.fill(colors['white'])
    gradientRect( window, (63, 72, 204), (0, 162, 232), pygame.Rect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200

    drawBorders(window, 'Darts', margin, radius, colors['white'])

    play_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    if len(players) > 0:
        play_button_size = drawTextWithOutline(window, 'Play', int(window.get_size()[0]/30),
                                           play_text_rect_obj_center, colors['white'], colors['black'], 2)
    else:
        play_button_size = drawTextWithOutline(window, 'Play', int(window.get_size()[0]/30),
                                           play_text_rect_obj_center, colors['red'], None, 2)

    addPlayer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    if len(players) < 6:
        addPlayer_button_size = drawTextWithOutline(window, 'Add Player', int(window.get_size()[0]/30),
                                                addPlayer_text_rect_obj_center, colors['white'], colors['black'], 2, not addingPlayer)
    else:
        addPlayer_button_size = drawTextWithOutline(window, 'Add Player', int(window.get_size()[0]/30),
                                                addPlayer_text_rect_obj_center, colors['red'], colors['red'], 2, not addingPlayer)

    settings_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.5)
    settings_button_size = drawTextWithOutline(window, 'Settings', int(window.get_size()[0]/30),
                                       settings_text_rect_obj_center, colors['white'], colors['black'], 2)

    quit_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.8)
    quit_button_size = drawTextWithOutline(window, 'Quit', int(window.get_size()[0]/30),
                                       quit_text_rect_obj_center, colors['white'], colors['black'], 2)

    playerColors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['cyan'], colors['orange']]
    crossDims = []
    for i in range(len(players)):
        picCentre = [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4]
        profilePicture(window, picCentre, playerColors[i], players[i], i)
        crossCentre = [picCentre[0] + window.get_size()[0]/33, picCentre[1] - window.get_size()[0]/33]
        crossRadius = window.get_size()[0]/100
        crossDims.append([crossCentre, crossRadius])

    pygame.display.flip()

    return [play_button_size, play_text_rect_obj_center, addPlayer_button_size, addPlayer_text_rect_obj_center,
            settings_button_size, settings_text_rect_obj_center, quit_button_size, quit_text_rect_obj_center,
            crossDims]

def addPlayer(window, addPlayer_button_size, players):
    font = pygame.font.Font(None, int(window.get_size()[0]/30))
    clock = pygame.time.Clock()
    width, height = addPlayer_button_size
    input_box_centre = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    input_box = pygame.Rect(*input_box_centre, width, height)
    input_box.center = input_box_centre
    color_inactive = colors['grey59']
    color_active = colors['white']
    color = color_active
    active = True
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

    drawBorders(window, 'Play', margin, radius, colors['white'])

    demolition_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    demolition_button_size = drawTextWithOutline(window, 'Demolition', int(window.get_size()[0]/30),
                                             demolition_text_rect_obj_center, colors['white'], colors['black'], 2)

    killer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    killer_button_size = drawTextWithOutline(window, 'Killer', int(window.get_size()[0]/30),
                                         killer_text_rect_obj_center, colors['white'], colors['black'], 2)

    back_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.8)
    back_button_size = drawTextWithOutline(window, 'Back', int(window.get_size()[0]/30),
                                       back_text_rect_obj_center, colors['white'], colors['black'], 2)

    playerColors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['cyan'], colors['orange']]
    for i in range(len(players)):
       profilePicture(window, [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4],
                      playerColors[i], players[i], i)

    pygame.display.flip()

    return [demolition_button_size, demolition_text_rect_obj_center, killer_button_size, killer_text_rect_obj_center,
            back_button_size, back_text_rect_obj_center]

def drawSettingsMenu(window, curr_resolution, resLeftHover, resRightHover):
    window.fill(colors['white'])
    gradientRect( window, (80, 80, 80), (180, 180, 180), pygame.Rect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200
    centre_margin = window.get_size()[0]/30

    drawBorders(window, 'Settings', margin, radius, colors['white'])

    font = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    resolution_text_surface_obj = font.render('Display Resolution', True, colors['white']).convert_alpha()
    resolution_text_rect_obj_center = (window.get_size()[0]/2 - resolution_text_surface_obj.get_rect().w/2 - centre_margin,
                                       window.get_size()[1]*0.2)
    drawTextWithOutline(window, 'Display Resolution', int(window.get_size()[0]/30),
                                           resolution_text_rect_obj_center, colors['white'], colors['black'], 2)

    buttons = drawArrowSelector(window, [window.get_size()[0]/2 + (window.get_size()[0]/3)/2 + centre_margin,
                                         window.get_size()[1]*0.2], int(window.get_size()[0]/30),
                                window.get_size()[0]/3, curr_resolution, colors['white'], colors['black'],
                                resLeftHover, resRightHover)
    leftButton_center, leftButton_button_size = buttons[0], buttons[1]
    rightButton_center, rightButton_button_size = buttons[2], buttons[3]

    font = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    back_text_surface_obj = font.render('Back', True, colors['white']).convert_alpha()
    back_text_rect_obj_center = (window.get_size()[0]/2 - back_text_surface_obj.get_rect().w/2 - centre_margin,
                                       window.get_size()[1]*0.8)
    back_button_size = drawTextWithOutline(window, 'Back', int(window.get_size()[0]/30),
                                       back_text_rect_obj_center, colors['white'], colors['black'], 2)

    font = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    apply_text_surface_obj = font.render('Apply', True, colors['white']).convert_alpha()
    apply_text_rect_obj_center = (window.get_size()[0]/2 + apply_text_surface_obj.get_rect().w/2 + centre_margin,
                                       window.get_size()[1]*0.8)
    apply_button_size = drawTextWithOutline(window, 'Apply', int(window.get_size()[0]/30),
                                       apply_text_rect_obj_center, colors['white'], colors['black'], 2)

    pygame.display.flip()

    return [leftButton_center, leftButton_button_size, rightButton_center, rightButton_button_size,
            back_button_size, back_text_rect_obj_center, apply_button_size, apply_text_rect_obj_center]

def resizeTest():
    pygame.init()
    # Create the window, saving it to a variable.
    surface = pygame.display.set_mode((350, 250), pygame.RESIZABLE)
    pygame.display.set_caption("Example resizable window")
    
    while True:
        surface.fill((255,255,255))
    
        # Draw a red rectangle that resizes with the window.
        pygame.draw.rect(surface, (200,0,0), (surface.get_width()/3,
          surface.get_height()/3, surface.get_width()/3,
          surface.get_height()/3))
    
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
    
            if event.type == pygame.VIDEORESIZE:
                # There's some code to add back window content here.
                surface = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)

def main():
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    resolutions, resolution_index = [], -1
    for resolution in pygame.display.list_modes():
        resolutions.append(' × '.join([str(i) for i in resolution]))
    resolutions.reverse()
    curr_resolution = resolutions[resolution_index]

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    players = []

    # window = pygame.display.set_mode((0, 0), pygame.RESIZABLE, pygame.FULLSCREEN)
    fullscreen = False
    os.environ['SDL_VIDEO_WINDOW_POS'] = maximised_pos
    window = pygame.display.set_mode(maximised_res, pygame.RESIZABLE)

    buttons = drawMenu(window, players)
    play_button_size, play_text_rect_obj_center = buttons[0], buttons[1]
    addPlayer_button_size, addPlayer_text_rect_obj_center = buttons[2], buttons[3]
    settings_button_size, settings_text_rect_obj_center = buttons[4], buttons[5]
    quit_button_size, quit_text_rect_obj_center = buttons[6], buttons[7]
    crossDims = buttons[8]

    menu = 'main'

    while True:
        underline_thickness = 2*(int(max(window.get_size())/500) + 1)
        if menu == 'main':
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))
    
            buttons = drawMenu(window, players)
            play_button_size, play_text_rect_obj_center = buttons[0], buttons[1]
            addPlayer_button_size, addPlayer_text_rect_obj_center = buttons[2], buttons[3]
            settings_button_size, settings_text_rect_obj_center = buttons[4], buttons[5]
            quit_button_size, quit_text_rect_obj_center = buttons[6], buttons[7]
            crossDims = buttons[8]
            mouse_on_cross = []

            for crossCentre, crossRadius in crossDims:
                if (x - crossCentre[0])**2 + (y - crossCentre[1])**2 <= crossRadius**2:
                    drawCross(window, crossCentre, crossRadius, colors['red'], colors['white'])
                    mouse_on_cross.append(True)
                else:
                    drawCross(window, crossCentre, crossRadius, colors['white'], colors['black'])
                    mouse_on_cross.append(False)

            mouse_on_play, mouse_on_addPlayer, mouse_on_settings, mouse_on_quit = False, False, False, False
            if len(players) > 0 and abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
                drawUnderlineWithOutline(window, play_text_rect_obj_center, play_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_play = True
    
            if len(players) < 6 and abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
                drawUnderlineWithOutline(window, addPlayer_text_rect_obj_center, addPlayer_button_size,
                                     underline_thickness, colors['white'], colors['black'], 2)
                mouse_on_addPlayer = True
    
            if abs(x - settings_text_rect_obj_center[0]) <= settings_button_size[0] and abs(y - settings_text_rect_obj_center[1]) <= settings_button_size[1]:
                drawUnderlineWithOutline(window, settings_text_rect_obj_center, settings_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_settings = True
    
            if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
                drawUnderlineWithOutline(window, quit_text_rect_obj_center, quit_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_quit = True
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_on_play:
                        menu = 'play'
                        
                    if mouse_on_addPlayer:
                        buttons = drawMenu(window, players, True)
                        players += addPlayer(window, buttons[2], players)

                    if mouse_on_settings:
                        menu = 'settings'
                        buttons = drawSettingsMenu(window, resolutions[resolution_index], False, False)
                        leftButton_center, leftButton_button_size = buttons[0], buttons[1]
                        rightButton_center, rightButton_button_size = buttons[2], buttons[3]
                        back_button_size, back_text_rect_obj_center = buttons[4], buttons[5]
                        apply_button_size, apply_text_rect_obj_center = buttons[6], buttons[7]

                    if any(mouse_on_cross):
                        players.pop(mouse_on_cross.index(True))

                    if mouse_on_quit:
                        pygame.quit()
                        return

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        if fullscreen:
                            pygame.display.quit()
                            os.environ['SDL_VIDEO_WINDOW_POS'] = maximised_pos
                            pygame.display.init()
                            window = pygame.display.set_mode(maximised_res, pygame.RESIZABLE)
                        else:
                            pygame.display.quit()
                            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                            pygame.display.init()
                            window = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
                        fullscreen = not fullscreen

                elif event.type == pygame.VIDEORESIZE:
                    window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if menu == 'settings':
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

            mouse_on_leftButton, mouse_on_rightButton, mouse_on_back, mouse_on_apply = False, False, False, False
            if abs(x - leftButton_center[0]) <= leftButton_button_size[0]/2 and abs(y - leftButton_center[1]) <= leftButton_button_size[1]/2:
                mouse_on_leftButton = True
                drawSettingsMenu(window, resolutions[resolution_index], True, False)

            elif abs(x - rightButton_center[0]) <= rightButton_button_size[0]/2 and abs(y - rightButton_center[1]) <= rightButton_button_size[1]/2:
                mouse_on_rightButton = True
                drawSettingsMenu(window, resolutions[resolution_index], False, True)
    
            else:
                drawSettingsMenu(window, resolutions[resolution_index], False, False)
    
            if abs(x - back_text_rect_obj_center[0]) <= back_button_size[0] and abs(y - back_text_rect_obj_center[1]) <= back_button_size[1]:
                drawUnderlineWithOutline(window, back_text_rect_obj_center, back_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_back = True
    
            if abs(x - apply_text_rect_obj_center[0]) <= apply_button_size[0] and abs(y - apply_text_rect_obj_center[1]) <= apply_button_size[1]:
                drawUnderlineWithOutline(window, apply_text_rect_obj_center, apply_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_apply = True
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_on_leftButton:
                        resolution_index -= 1
                        resolution_index %= len(resolutions)
    
                    if mouse_on_rightButton:
                        resolution_index += 1
                        resolution_index %= len(resolutions)

                    if mouse_on_apply:
                        if curr_resolution != resolutions[resolution_index]:
                            new_res_ratio = int(resolutions[-1].split(' × ')[0])/int(resolutions[resolution_index].split(' × ')[0])
                            window = pygame.display.set_mode([res/new_res_ratio for res in maximised_res], pygame.RESIZABLE)
                            buttons = drawSettingsMenu(window, resolutions[resolution_index], False, False)
                            leftButton_center, leftButton_button_size = buttons[0], buttons[1]
                            rightButton_center, rightButton_button_size = buttons[2], buttons[3]
                            back_button_size, back_text_rect_obj_center = buttons[4], buttons[5]
                            apply_button_size, apply_text_rect_obj_center = buttons[6], buttons[7]
                            curr_resolution = resolutions[resolution_index]

                    if mouse_on_back:
                        menu = 'main'
    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu = 'main'

                    if event.key == pygame.K_F11:
                        if fullscreen:
                            pygame.display.quit()
                            os.environ['SDL_VIDEO_WINDOW_POS'] = maximised_pos
                            pygame.display.init()
                            window = pygame.display.set_mode(maximised_res, pygame.RESIZABLE)
                        else:
                            pygame.display.quit()
                            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                            pygame.display.init()
                            window = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
                        fullscreen = not fullscreen

                elif event.type == pygame.VIDEORESIZE:
                    window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if menu == 'play':
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))
    
            buttons = drawGameMenu(window, players)
            demolition_button_size, demolition_text_rect_obj_center = buttons[0], buttons[1]
            killer_button_size, killer_text_rect_obj_center = buttons[2], buttons[3]
            back_button_size, back_text_rect_obj_center = buttons[4], buttons[5]

            mouse_on_demolition, mouse_on_killer, mouse_on_back = False, False, False
            if abs(x - demolition_text_rect_obj_center[0]) <= demolition_button_size[0] and abs(y - demolition_text_rect_obj_center[1]) <= demolition_button_size[1]:
                drawUnderlineWithOutline(window, demolition_text_rect_obj_center, demolition_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_demolition = True
    
            if len(players) < 6 and abs(x - killer_text_rect_obj_center[0]) <= killer_button_size[0] and abs(y - killer_text_rect_obj_center[1]) <= killer_button_size[1]:
                drawUnderlineWithOutline(window, killer_text_rect_obj_center, killer_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_killer = True
    
            if abs(x - back_text_rect_obj_center[0]) <= back_button_size[0] and abs(y - back_text_rect_obj_center[1]) <= back_button_size[1]:
                drawUnderlineWithOutline(window, back_text_rect_obj_center, back_button_size, underline_thickness,
                                     colors['white'], colors['black'], 2)
                mouse_on_back = True
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_on_demolition:
                        game = Demolition(window, players)
                        game.play()
                        menu = 'play'
                        
                    if mouse_on_killer:
                        print('Killer')
    
                    if mouse_on_back:
                        menu = 'main'
    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu = 'main'
                    if event.key == pygame.K_F11:
                        if fullscreen:
                            pygame.display.quit()
                            os.environ['SDL_VIDEO_WINDOW_POS'] = maximised_pos
                            pygame.display.init()
                            window = pygame.display.set_mode(maximised_res, pygame.RESIZABLE)
                        else:
                            pygame.display.quit()
                            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
                            pygame.display.init()
                            window = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
                        fullscreen = not fullscreen

                elif event.type == pygame.VIDEORESIZE:
                    window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        sys.exit(1)
