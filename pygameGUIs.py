from time import sleep
from math import sin, cos, pi
from random import random
from pygame import init as pygameInit, quit as pygameQuit, Surface as pygameSurface, Rect as pygameRect
from pygame import SRCALPHA as pygameSRCALPHA, BLEND_RGBA_MIN as pygameBLEND_RGBA_MIN
from pygame import RESIZABLE as pygameRESIZABLE, MOUSEBUTTONDOWN as pygameMOUSEBUTTONDOWN
from pygame import KEYDOWN as pygameKEYDOWN, K_ESCAPE as pygameK_ESCAPE, K_RETURN as pygameK_RETURN
from pygame import K_BACKSPACE as pygameK_BACKSPACE, BLEND_RGBA_MAX as pygameBLEND_RGBA_MAX
from pygame.time import Clock as pygameTimeClock
from pygame.display import Info as pygameDisplayInfo, set_mode as pygameDisplaySet_mode
from pygame.display import set_caption as pygameDisplaySet_caption, flip as pygameDisplayFlip
from pygame.display import list_modes as pygameDisplayList_modes
from pygame.event import get as pygameEventGet
from pygame.mouse import get_pos as pygameMouseGet_pos
from pygame.draw import line as pygameDrawLine, circle as pygameDrawCircle, polygon as pygameDrawPolygon
from pygame.draw import rect as pygameDrawRect, lines as pygameDrawLines, arc as pygameDrawArc
from pygame.transform import smoothscale as pygameTransformSmoothscale, scale as pygameTransformScale
from pygame.image import load as pygameImageLoad
from pygame.font import Font as pygameFontFont
from pygame.locals import QUIT as pygameLocalsQUIT
from pygame.color import THECOLORS as pygameColors

# os.environ['SDL_VIDEO_WINDOW_POS'] = "384,200"
# os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
# os.environ['SDL_VIDEO_CENTERED'] = '1'

def blankTestFunction():
    pygameInit()
    
    FPS = 30 #frames per second setting
    fpsClock = pygameTimeClock()

    info = pygameDisplayInfo()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygameDisplaySet_mode((info.current_w/2, (info.current_h-60)/2))

    # test function here

    while True:
        x, y = pygameMouseGet_pos()
        pygameDisplaySet_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        # test function here

        pygameDisplayFlip()

        fpsClock.tick(FPS)
        for event in pygameEventGet():
            if event.type == pygameLocalsQUIT:
                pygameQuit()
                return

def gradientRect(window, top_colour, bottom_colour, target_rect):
    colour_rect = pygameSurface((2, 2))
    pygameDrawLine(colour_rect, top_colour, (0, 0), (1, 0))
    pygameDrawLine(colour_rect, bottom_colour, (0, 1), (1, 1))
    colour_rect = pygameTransformSmoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)

def profilePicture(window, centre, color, player, playerNum):
    try:
        image_original  = pygameImageLoad('Pictures/' + player + '.png').convert()
    except:
        image_original  = pygameImageLoad(f'Pictures/Blank{playerNum+1}.png').convert()
    image = pygameTransformScale(image_original, [image_original.get_size()[i]*((window.get_size()[0]/15)/image_original.get_size()[0]) for i in range(2)])
    cropped_image  = pygameSurface((max(image.get_size()), max(image.get_size())), pygameSRCALPHA)

    image_pos = [centre[i] - max(image.get_size())/2 for i in range(2)]

    color = (*color[:3], color[3])
    pygameDrawCircle(window, color, [i + max(image.get_size())/2 for i in image_pos], min(image.get_size())/1.75)

    pygameDrawCircle(cropped_image, (255, 255, 255, 255), [i/2 for i in cropped_image.get_size()], min(image.get_size())/2)
    cropped_image.blit(image, [(max(image.get_size()) - image.get_size()[i])/2 for i in range(2)], special_flags=pygameBLEND_RGBA_MIN)

    window.blit(cropped_image, image_pos)

    font_obj = pygameFontFont('freesansbold.ttf', int(window.get_size()[0]/50))
    text_surface_obj = font_obj.render(player, True, pygameColors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (centre[0], centre[1] + window.get_size()[1]/9)

    window.blit(text_surface_obj, text_rect_obj)

def drawDiamond(window, color, centre, radius):
    points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0]+radius, centre[1]], [centre[0], centre[1]-radius]]
    pygameDrawPolygon(window, color, points)

def drawHalfDiamond(window, color, centre, radius, side):
    if side == 'left':
        points = [[centre[0], centre[1]+radius], [centre[0]+radius, centre[1]], [centre[0], centre[1]-radius]]
    elif side == 'right':
        points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0], centre[1]-radius]]
    elif side == 'top':
        points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0]+radius, centre[1]]]
    pygameDrawPolygon(window, color, points)

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

    font_obj = pygameFontFont('freesansbold.ttf', int(window.get_size()[0]/30))
    text_surface_obj = font_obj.render(str(score), True, pygameColors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (bottom_centre[0], bottom_centre[1] - ((score_row+3)*(radius+gap)))

    window.blit(text_surface_obj, text_rect_obj)

def drawTurnMarker(window, centre, radius, filled=False):
    points = [[centre[0] - radius, centre[1] - radius], [centre[0] + radius, centre[1] - radius], [centre[0] + radius, centre[1] + radius], [centre[0] - radius, centre[1] + radius], [centre[0] - 2*radius, centre[1]]]
    if filled:
        pygameDrawPolygon(window, pygameColors['white'], points)
    else:
        pygameDrawPolygon(window, pygameColors['white'], points, width=1)

def drawTurnMarkers(window, centre, radius, turn=None):
    for t, height in enumerate([centre[1] - 3*radius, centre[1], centre[1] + 3*radius]):
        if t == turn:
            drawTurnMarker(window, [centre[0], height], radius, filled=True)
        else:
            drawTurnMarker(window, [centre[0], height], radius, filled=False)

def drawDemolition(window, player, turn, players, scores):
    window.fill([255,255,255])
    gradientRect( window, (95, 4, 107), (152, 88, 182), pygameRect( 0, 0, *window.get_size() ) )
    centres = [[window.get_size()[0]*(i/len(players) - (1-((len(players)-1)*(1/len(players))))/2), window.get_size()[1]*0.7 + (window.get_size()[1]*0.05*(len(players) < 6))] for i in range(1, (len(players)+1))]
    tower_colors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    tower_offcolors = [[j/2.5 for j in i] for i in tower_colors]

    for i in range(len(players)):
        profilePicture(window, centres[i], tower_colors[i], players[i], i)
        if len(players) == 6:
            radius = window.get_size()[0]/250
        elif len(players) > 6:
            print('Too many players!')
            pygameQuit()
            return
        else:
            radius = window.get_size()[0]/200
        if player == players[i]:
            drawTurnMarkers(window, [centres[i][0] + window.get_size()[0]/15, centres[i][1]], radius, turn)
        else:
            drawTurnMarkers(window, [centres[i][0] + window.get_size()[0]/15, centres[i][1]], radius, None)
        drawTower(window, tower_colors[i], tower_offcolors[i], [centres[i][0], centres[i][1] - window.get_size()[1]*0.2], scores[i], radius)

    margin = 0.02

    font_obj = pygameFontFont('freesansbold.ttf', int(window.get_size()[0]/50))
    text_surface_obj = font_obj.render('Demolition', True, pygameColors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (window.get_size()[0]/2, max(window.get_size())*margin)

    window.blit(text_surface_obj, text_rect_obj)

    pygameDrawLine(window, pygameColors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygameDrawLine(window, pygameColors['white'], [window.get_size()[0]/2 + text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygameDrawLine(window, pygameColors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    drawDiamond(window, pygameColors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0]/2 - text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0]/2 + text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

    pygameDisplayFlip()

def updateScoreDemolition(window, player, turn, new_score, players, scores):
    old_score = scores[players.index(player)]
    min_delay, max_delay = 0.005, 0.04
    if new_score > old_score:
        print('Error: new score must be less than or equal to old score')
        return
    else:
        while scores[players.index(player)] > new_score:
            pygameEventGet()
            scores[players.index(player)] -= 1
            drawDemolition(window, player, turn, players, scores)
            sleep(((min_delay - max_delay)/(old_score-new_score))*abs(scores[players.index(player)]-new_score+1)-(((min_delay - max_delay)/(old_score-new_score))*abs(old_score+1-new_score+1)))
            # sleep(((np.sqrt(max_delay)/(old_score-new_score+1))*(old_score-scores[players.index(player)]+1))**2)

    return scores

def drawCross(window, centre, radius, back_color, fore_color):
    pygameDrawCircle(window, back_color, centre, radius)
    pygameDrawCircle(window, fore_color, centre, radius, width=1)
    pygameDrawLine(window, fore_color, [centre[i] - (int(radius/(2**0.5)) - 1) for i in range(2)], [centre[i] + (int(radius/(2**0.5)) - 1) for i in range(2)])
    pygameDrawLine(window, fore_color, [centre[0] - (int(radius/(2**0.5)) - 1), centre[1] + (int(radius/(2**0.5)) - 1)], [centre[0] + (int(radius/(2**0.5)) - 1), centre[1] - (int(radius/(2**0.5)) - 1)])
    pygameInit()
    
    FPS = 30 #frames per second setting
    fpsClock = pygameTimeClock()

    info = pygameDisplayInfo()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygameDisplaySet_mode((info.current_w/2, (info.current_h-60)/2))
    window.fill(pygameColors['yellow'])

    drawCross(window, [window.get_size()[i]/2 for i in [0, 1]], min(window.get_size())/2*0.75, pygameColors['white'], pygameColors['black'])

    while True:
        x, y = pygameMouseGet_pos()
        pygameDisplaySet_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        # test function here

        pygameDisplayFlip()

        fpsClock.tick(FPS)
        for event in pygameEventGet():
            if event.type == pygameLocalsQUIT:
                pygameQuit()
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
    font = pygameFontFont('freesansbold.ttf', fontsize)
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
                pygameDrawLine(window, outline_color, point_left, point_right, thickness)
        
        point_left, point_right = [centre[0] - width/2, centre[1]], [centre[0] + width/2, centre[1]]
        pygameDrawLine(window, color, point_left, point_right, thickness)

def drawUnderlineWithOutline(window, text_rect_obj_center, button_size, thickness, color, outline_color=None, outline_thickness=2, direction='horizontal'):
    if direction == 'horizontal':
        drawLineWithOutline(window, [text_rect_obj_center[0], text_rect_obj_center[1] + button_size[1]/1.5], button_size[0], thickness, color, outline_color, outline_thickness)

def drawRectWithOutline(window, rect, color, outline_color, outline_thickness):
    outline_rect = rect.copy()
    outline_rect.w += 2*outline_thickness
    outline_rect.h += 2*outline_thickness
    outline_rect.center = rect.center
    pygameDrawRect(window, outline_color, outline_rect)
    pygameDrawRect(window, color, rect)

def drawArrowSelector(window, centre, fontsize, width, curr_option, fore_color, back_color, leftHover=False, rightHover=False):
    font = pygameFontFont('freesansbold.ttf', fontsize)
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
        pygameDrawRect(window, pygameColors['grey40'], pygameRect([leftButton_center[i] - leftButton_button_size[i]/2 for i in [0, 1]], leftButton_button_size))
    if rightHover:
        pygameDrawRect(window, pygameColors['grey40'], pygameRect([rightButton_center[i] - rightButton_button_size[i]/2 for i in [0, 1]], rightButton_button_size))
    window.blit(text_surface_obj, text_rect_obj)
    drawHalfDiamond(window, fore_color, [centre[0] - (width/2)*0.9, centre[1]], (box_rect_obj.h/2)*0.6, 'right')
    drawHalfDiamond(window, fore_color, [centre[0] + (width/2)*0.9, centre[1]], (box_rect_obj.h/2)*0.6, 'left')

    return leftButton_center, leftButton_button_size, rightButton_center, rightButton_button_size
    pygameInit()
    
    FPS = 30 #frames per second setting
    fpsClock = pygameTimeClock()

    info = pygameDisplayInfo()

    resolutions, resolution_index = [], 0
    for resolution in pygameDisplayList_modes():
        resolutions.append(' × '.join([str(i) for i in resolution]))
    resolutions.reverse()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygameDisplaySet_mode((info.current_w, (info.current_h-60)), pygameRESIZABLE)
    window.fill(pygameColors['blue'])

    buttons = drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], pygameColors['white'], pygameColors['black'])
    leftButton_center, leftButton_button_size = buttons[0], buttons[1]
    rightButton_center, rightButton_button_size = buttons[2], buttons[3]

    while True:
        x, y = pygameMouseGet_pos()
        pygameDisplaySet_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        window.fill(pygameColors['blue'])

        mouse_on_leftButton, mouse_on_rightButton = False, False
        if abs(x - leftButton_center[0]) <= leftButton_button_size[0]/2 and abs(y - leftButton_center[1]) <= leftButton_button_size[1]/2:
            mouse_on_leftButton = True
            drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], pygameColors['white'], pygameColors['black'], True, False)


        elif abs(x - rightButton_center[0]) <= rightButton_button_size[0]/2 and abs(y - rightButton_center[1]) <= rightButton_button_size[1]/2:
            mouse_on_rightButton = True
            drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], pygameColors['white'], pygameColors['black'], False, True)

        else:
            drawArrowSelector(window, [window.get_size()[i]/2 for i in [0, 1]], 60, 500, resolutions[resolution_index], pygameColors['white'], pygameColors['black'])

        pygameDisplayFlip()

        fpsClock.tick(FPS)
        for event in pygameEventGet():
            if event.type == pygameLocalsQUIT:
                pygameQuit()
                return

            elif event.type == pygameMOUSEBUTTONDOWN:
                if mouse_on_leftButton:
                    resolution_index -= 1
                    resolution_index %= len(resolutions)

                if mouse_on_rightButton:
                    resolution_index += 1
                    resolution_index %= len(resolutions)

def drawBorders(window, title, margin, radius, color, outline_color=None):
    title_font_obj = pygameFontFont('freesansbold.ttf', int(window.get_size()[0]/50))
    title_text_surface_obj = title_font_obj.render(title, True, pygameColors['white'])
    title_text_rect_obj = title_text_surface_obj.get_rect()
    title_text_rect_obj_center = (window.get_size()[0]/2, max(window.get_size())*margin)
    drawTextWithOutline(window, title, int(window.get_size()[0]/50), title_text_rect_obj_center, color,
                    outline_color, 2)

    pygameDrawLine(window, pygameColors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygameDrawLine(window, pygameColors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygameDrawLine(window, pygameColors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    drawDiamond(window, pygameColors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    drawDiamond(window, pygameColors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

def drawMenu(window, players, addingPlayer=False):
    window.fill(pygameColors['white'])
    gradientRect( window, (63, 72, 204), (0, 162, 232), pygameRect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200

    drawBorders(window, 'Darts', margin, radius, pygameColors['white'])

    play_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    if len(players) > 0:
        play_button_size = drawTextWithOutline(window, 'Play', int(window.get_size()[0]/30),
                                           play_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)
    else:
        play_button_size = drawTextWithOutline(window, 'Play', int(window.get_size()[0]/30),
                                           play_text_rect_obj_center, pygameColors['red'], None, 2)

    addPlayer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    if len(players) < 6:
        addPlayer_button_size = drawTextWithOutline(window, 'Add Player', int(window.get_size()[0]/30),
                                                addPlayer_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2, not addingPlayer)
    else:
        addPlayer_button_size = drawTextWithOutline(window, 'Add Player', int(window.get_size()[0]/30),
                                                addPlayer_text_rect_obj_center, pygameColors['red'], pygameColors['red'], 2, not addingPlayer)

    settings_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.5)
    settings_button_size = drawTextWithOutline(window, 'Settings', int(window.get_size()[0]/30),
                                       settings_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    quit_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.8)
    quit_button_size = drawTextWithOutline(window, 'Quit', int(window.get_size()[0]/30),
                                       quit_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    playerColors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    crossDims = []
    for i in range(len(players)):
        picCentre = [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4]
        profilePicture(window, picCentre, playerColors[i], players[i], i)
        crossCentre = [picCentre[0] + window.get_size()[0]/33, picCentre[1] - window.get_size()[0]/33]
        crossRadius = window.get_size()[0]/100
        crossDims.append([crossCentre, crossRadius])

    pygameDisplayFlip()

    return [play_button_size, play_text_rect_obj_center, addPlayer_button_size, addPlayer_text_rect_obj_center,
            settings_button_size, settings_text_rect_obj_center, quit_button_size, quit_text_rect_obj_center,
            crossDims]

def addPlayer(window, addPlayer_button_size, players):
    font = pygameFontFont(None, int(window.get_size()[0]/30))
    clock = pygameTimeClock()
    width, height = addPlayer_button_size
    input_box_centre = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    input_box = pygameRect(*input_box_centre, width, height)
    input_box.center = input_box_centre
    color_inactive = pygameColors['grey59']
    color_active = pygameColors['white']
    color = color_active
    active = True
    text = ''
    while True:
        for event in pygameEventGet():
            if event.type == pygameQuit:
                pygameQuit()
                return
            if event.type == pygameMOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygameKEYDOWN:
                if event.key == pygameK_ESCAPE:
                    return []
                if active:
                    if event.key == pygameK_RETURN:
                        return [text]
                    elif event.key == pygameK_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        drawMenu(window, players, True)
        txt_surface = font.render(text, True, color)
        width = max(width, txt_surface.get_width()+10)
        input_box.w = width
        input_box.center = input_box_centre
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygameDrawRect(window, color, input_box, 2)

        pygameDisplayFlip()
        clock.tick(30)

def drawGameMenu(window, players):
    window.fill([255,255,255])
    gradientRect( window, (0, 204, 51), (0, 255, 128), pygameRect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200

    drawBorders(window, 'Play', margin, radius, pygameColors['white'])

    demolition_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    demolition_button_size = drawTextWithOutline(window, 'Demolition', int(window.get_size()[0]/30),
                                             demolition_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    killer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    killer_button_size = drawTextWithOutline(window, 'Killer', int(window.get_size()[0]/30),
                                         killer_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    back_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.8)
    back_button_size = drawTextWithOutline(window, 'Back', int(window.get_size()[0]/30),
                                       back_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    playerColors = [pygameColors['red'], pygameColors['blue'], pygameColors['green'], pygameColors['yellow'], pygameColors['cyan'], pygameColors['orange']]
    for i in range(len(players)):
       profilePicture(window, [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4],
                      playerColors[i], players[i], i)

    pygameDisplayFlip()

    return [demolition_button_size, demolition_text_rect_obj_center, killer_button_size, killer_text_rect_obj_center,
            back_button_size, back_text_rect_obj_center]

def drawSettingsMenu(window, curr_resolution, resLeftHover, resRightHover):
    window.fill(pygameColors['white'])
    gradientRect( window, (80, 80, 80), (180, 180, 180), pygameRect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200
    centre_margin = window.get_size()[0]/30

    drawBorders(window, 'Settings', margin, radius, pygameColors['white'])

    font = pygameFontFont('freesansbold.ttf', int(window.get_size()[0]/30))
    resolution_text_surface_obj = font.render('Display Resolution', True, pygameColors['white']).convert_alpha()
    resolution_text_rect_obj_center = (window.get_size()[0]/2 - resolution_text_surface_obj.get_rect().w/2 - centre_margin,
                                       window.get_size()[1]*0.2)
    drawTextWithOutline(window, 'Display Resolution', int(window.get_size()[0]/30),
                                           resolution_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    buttons = drawArrowSelector(window, [window.get_size()[0]/2 + (window.get_size()[0]/3)/2 + centre_margin,
                                         window.get_size()[1]*0.2], int(window.get_size()[0]/30),
                                window.get_size()[0]/3, curr_resolution, pygameColors['white'], pygameColors['black'],
                                resLeftHover, resRightHover)
    leftButton_center, leftButton_button_size = buttons[0], buttons[1]
    rightButton_center, rightButton_button_size = buttons[2], buttons[3]

    font = pygameFontFont('freesansbold.ttf', int(window.get_size()[0]/30))
    back_text_surface_obj = font.render('Back', True, pygameColors['white']).convert_alpha()
    back_text_rect_obj_center = (window.get_size()[0]/2 - back_text_surface_obj.get_rect().w/2 - centre_margin,
                                       window.get_size()[1]*0.8)
    back_button_size = drawTextWithOutline(window, 'Back', int(window.get_size()[0]/30),
                                       back_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    font = pygameFontFont('freesansbold.ttf', int(window.get_size()[0]/30))
    apply_text_surface_obj = font.render('Apply', True, pygameColors['white']).convert_alpha()
    apply_text_rect_obj_center = (window.get_size()[0]/2 + apply_text_surface_obj.get_rect().w/2 + centre_margin,
                                       window.get_size()[1]*0.8)
    apply_button_size = drawTextWithOutline(window, 'Apply', int(window.get_size()[0]/30),
                                       apply_text_rect_obj_center, pygameColors['white'], pygameColors['black'], 2)

    pygameDisplayFlip()

    return [leftButton_center, leftButton_button_size, rightButton_center, rightButton_button_size,
            back_button_size, back_text_rect_obj_center, apply_button_size, apply_text_rect_obj_center]

def drawSegment(window, centre, outer_radius, inner_radius, start_angle, end_angle, color):
    bounding_rect  = pygameSurface((2*(2**0.5)*outer_radius, 2*(2**0.5)*outer_radius), pygameSRCALPHA)
    bounding_rect.fill((0, 0, 0, 0))

    return_pos = [centre[i] - (2**0.5)*outer_radius for i in range(2)]

    pygameDrawCircle(bounding_rect, color, [bounding_rect.get_size()[i]/2 for i in [0, 1]], outer_radius)

    if end_angle - start_angle < pi/2:
        centre_angle = (end_angle + start_angle)/2
        points = [[bounding_rect.get_size()[i]/2 for i in [0, 1]]]
        for offset in [end_angle - centre_angle, pi/4, (3*pi)/4, (5*pi)/4, (7*pi)/4, start_angle - centre_angle]:
            x = bounding_rect.get_size()[0]/2 + outer_radius*(2**0.5)*sin(centre_angle+offset)
            y = bounding_rect.get_size()[1]/2 - outer_radius*(2**0.5)*cos(centre_angle+offset)
            points.append([x, y])
        pygameDrawPolygon(bounding_rect, (0, 0, 0, 0), points)
        pygameDrawCircle(bounding_rect, (0, 0, 0, 0), [bounding_rect.get_size()[i]/2 for i in [0, 1]], inner_radius)

    window.blit(bounding_rect, return_pos, special_flags=pygameBLEND_RGBA_MAX)

def drawJaggedArc(window, centre, radius, color, width, start_angle, end_angle, jag_width, jag_num):
    points = []
    angle_range = abs(end_angle - start_angle)/jag_num
    for n, prop in enumerate(range(jag_num+1)):
        curr_angle = start_angle + angle_range*prop
        x = centre[0] + radius*sin(curr_angle) + (((-1)**n)*random()*jag_width*radius)
        y = centre[1] - radius*cos(curr_angle) - (((-1)**n)*random()*jag_width*radius)
        points.append([x, y])
    pygameDrawLines(window, color, False, points, width)

def drawJaggedArcTest():
    pygameInit()
    
    FPS = 30 #frames per second setting
    fpsClock = pygameTimeClock()

    info = pygameDisplayInfo()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygameDisplaySet_mode((info.current_w/1.5, (info.current_h-60)/1.5))
    gradientRect( window, (136/5, 0, 21/5), (240, 0, 36), pygameRect( 0, 0, *window.get_size() ) )

    drawJaggedArc(window, [window.get_size()[i]/2 for i in [0, 1]], window.get_size()[1]*0.4, pygameColors['blue'],
                  3, 0, pi/10, 0.02, 10)

    while True:
        x, y = pygameMouseGet_pos()
        pygameDisplaySet_caption('{}, {}'.format(x, y))

        # test function here

        pygameDisplayFlip()

        fpsClock.tick(FPS)
        for event in pygameEventGet():
            if event.type == pygameLocalsQUIT:
                pygameQuit()
                return

def drawSplitSegment(window, centre, outer_radius, inner_radius, start_angle, end_angle, color, split_color,
                     split_width, jag_width, jag_num):
    drawSegment(window, centre, outer_radius, inner_radius, start_angle, end_angle, color)
    drawJaggedArc(window, centre, outer_radius*(2/3), split_color, split_width, start_angle, end_angle, jag_width,
                  jag_num)
    drawJaggedArc(window, centre, outer_radius*(1/3), split_color, split_width, start_angle, end_angle, jag_width,
                  jag_num)
    drawJaggedArc(window, centre, outer_radius, split_color, split_width, start_angle, end_angle, 0, 20)
    drawJaggedArc(window, centre, inner_radius, split_color, split_width, start_angle, end_angle, 0, 2)
    pygameDrawLine(window, split_color, [centre[0]+inner_radius*sin(start_angle), centre[1]-inner_radius*cos(start_angle)],
                   [centre[0]+outer_radius*sin(start_angle), centre[1]-outer_radius*cos(start_angle)], split_width)
    pygameDrawLine(window, split_color, [centre[0]+inner_radius*sin(end_angle), centre[1]-inner_radius*cos(end_angle)],
                   [centre[0]+outer_radius*sin(end_angle), centre[1]-outer_radius*cos(end_angle)], split_width)


def drawSegmentTest():
    pygameInit()
    
    FPS = 30 #frames per second setting
    fpsClock = pygameTimeClock()

    info = pygameDisplayInfo()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    window = pygameDisplaySet_mode((info.current_w/1.5, (info.current_h-60)/1.5))
    gradientRect( window, (136/5, 0, 21/5), (240, 0, 36), pygameRect( 0, 0, *window.get_size() ) )

    drawDartBoard(window, [window.get_size()[i]/2 for i in [0, 1]], window.get_size()[1]*0.4, pygameColors['white'])

    while True:
        x, y = pygameMouseGet_pos()
        pygameDisplaySet_caption('{}, {}'.format(x, y))

        drawSplitSegment(window, [window.get_size()[i]/2 for i in [0, 1]], window.get_size()[1]*0.4, window.get_size()[1]*0.4*(16/170),
                         pi/20, (3*pi)/20, pygameColors['red'], pygameColors['black'], 4, 0.02, 10)

        pygameDisplayFlip()

        fpsClock.tick(FPS)
        for event in pygameEventGet():
            if event.type == pygameLocalsQUIT:
                pygameQuit()
                return

def drawDartBoard(window, centre, radius, fore_color, filled=[False]*20, width=1, split_fills=False):
    board_rect = pygameRect(0, 0, 2*radius, 2*radius)
    board_rect.center = centre
    starts = [1.5, 8.5, 10.5, 3.5, 19.5, 5.5, 12.5, 14.5, 17.5, 6.5, 15.5, 18.5, 4.5, 16.5, 7.5, 13.5, 9.5, 2.5, 11.5,
              0.5]
    if any(filled):
        for n, fill in enumerate(filled):
            if fill:
                if split_fills:
                    drawSplitSegment(window, centre, radius, radius*(16/170), (starts[n]/20)*2*pi,
                                     ((starts[n]-1)/20)*2*pi, fill, split_fills, width+3, 0.02, 10)
                else:
                    drawSegment(window, centre, radius, radius*(16/170), (starts[n]/20)*2*pi, ((starts[n]-1)/20)*2*pi,
                            fill)

    pygameDrawCircle(window, fore_color, centre, radius, width)
    pygameDrawCircle(window, fore_color, centre, radius*(162/170), width)
    pygameDrawCircle(window, fore_color, centre, radius*(107/170), width)
    pygameDrawCircle(window, fore_color, centre, radius*(99/170), width)
    pygameDrawCircle(window, fore_color, centre, radius*(16/170), width)
    pygameDrawCircle(window, fore_color, centre, radius*(6.35/170), width)

    for angle in range(20):
        inner_x = centre[0] + radius*(16/170)*sin(((angle+0.5)/20)*2*pi)
        inner_y = centre[1] + radius*(16/170)*cos(((angle+0.5)/20)*2*pi)
        outer_x = centre[0] + radius*sin(((angle+0.5)/20)*2*pi)
        outer_y = centre[1] + radius*cos(((angle+0.5)/20)*2*pi)
        pygameDrawLine(window, fore_color, (inner_x, inner_y), (outer_x, outer_y), width)

def drawDartBoardTest(n):
    pygameInit()
    
    FPS = 30 #frames per second setting
    fpsClock = pygameTimeClock()

    info = pygameDisplayInfo()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    # players = ['Josh']
    # players = []

    filled = []
    for i in range(20):
        if i+1 in n:
            filled.append(pygameColors['blue'])
        else:
            filled.append(False)

    window = pygameDisplaySet_mode((info.current_w/1.5, (info.current_h-60)/1.5))

    drawDartBoard(window, [window.get_size()[i]/2 for i in [0, 1]], window.get_size()[1]*0.4, pygameColors['white'],
                  filled)

    while True:
        x, y = pygameMouseGet_pos()
        pygameDisplaySet_caption('{}, {}'.format(x, y))

        # test function here

        pygameDisplayFlip()

        fpsClock.tick(FPS)
        for event in pygameEventGet():
            if event.type == pygameLocalsQUIT:
                pygameQuit()
                return

