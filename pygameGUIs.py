import time, os, random
import tkinter as tk
import pygame
from pygame.locals import QUIT
from pygame.color import THECOLORS as colors

os.environ['SDL_VIDEO_WINDOW_POS'] = "384,200"

def movableWindow():
    
    w, h = 400, 500
    
    # Tkinter Stuffs
    root = tk.Tk()
    embed = tk.Frame(root, width=w, height=h)
    embed.pack()
    
    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib' # This was needed to work on my windows machine.
    
    root.update()
    
    # Pygame Stuffs
    pygame.display.init()
    screen = pygame.display.set_mode((w, h))
    
    # This just gets the size of your screen (assuming the screen isn't affected by display scaling).
    screen_full_size = pygame.display.list_modes()[0]
    
    # Basic Pygame loop
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
    
                if event.key == pygame.K_SPACE:
                    # Press space to move the window to a random location.
                    r_w = random.randint(0, screen_full_size[0])
                    r_h = random.randint(0, screen_full_size[1])
                    root.geometry("+"+str(r_w)+"+"+str(r_h))
    
        # Set to green just so we know when it is finished loading.
        screen.fill((0, 220, 0))
    
        pygame.display.flip()
    
        root.update()
    
    pygame.quit()
    root.destroy()

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

def profilePicTest():
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    window = pygame.display.set_mode((info.current_w, info.current_h-60))
    gradientRect( window, (95, 4, 107), (152, 88, 182), pygame.Rect( 0, 0, *window.get_size() ) )

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    players = ['Josh', 'Ben', 'Luke']
    centres = [[window.get_size()[0]/(len(players)+1)*i, window.get_size()[1]*0.8] for i in range(1, (len(players)+1))]
    tower_colors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['cyan'], colors['orange']]

    for i in range(len(players)):
        profilePicture(window, centres[i], tower_colors[i], players[i])

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {}'.format(x, y))
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

def gradientTest():
    # Window size
    WINDOW_WIDTH    = 400
    WINDOW_HEIGHT   = 400
    
    ### initialisation
    pygame.init()
    window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
    pygame.display.set_caption("Gradient Rect")
    
    # Update the window
    window.fill( ( 0,0,0 ) )
    gradientRect( window, (95, 4, 107), (152, 88, 182), pygame.Rect( 100,100, 100, 50 ) )

    ### Main Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

def draw_diamond(window, color, centre, radius):
    points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0]+radius, centre[1]], [centre[0], centre[1]-radius]]
    pygame.draw.polygon(window, color, points)

def draw_halfdiamond(window, color, centre, radius, side):
    if side == 'left':
        points = [[centre[0], centre[1]+radius], [centre[0]+radius, centre[1]], [centre[0], centre[1]-radius]]
    elif side == 'right':
        points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0], centre[1]-radius]]
    elif side == 'top':
        points = [[centre[0]-radius, centre[1]], [centre[0], centre[1]+radius], [centre[0]+radius, centre[1]]]
    pygame.draw.polygon(window, color, points)

def draw_tower(window, color, off_color, bottom_centre, score, radius, gap=3):
    count, score_row = 0, -1
    for row in range(22):
        if row < 10:
            horizontal, vertical = (i - (row*(radius+gap)) for i in bottom_centre)
            for column in range(row+1)[::-1]:
                draw_diamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius)
                count += 1
                if count == score:
                    score_row = 1*row
                    color = off_color

        elif row == 21:
            vertical = bottom_centre[1] - (row*(radius+gap))
            horizontal = bottom_centre[0] - (9*(radius+gap))
            for column in range(10)[::-1]:
                draw_halfdiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius, 'top')
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
                        draw_halfdiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius, 'left')
                        count += 1
                        if count == score:
                            score_row = 1*row
                            color = off_color
                    elif column < 10:
                        draw_diamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius)
                        count += 1
                        if count == score:
                            score_row = 1*row
                            color = off_color
                    else:
                        draw_halfdiamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius, 'right')
                        count += 1
                        if count == score:
                            score_row = 1*row
                            color = off_color
    
            else:
                horizontal = bottom_centre[0] - (9*(radius+gap))
                for column in range(10)[::-1]:
                    draw_diamond(window, color, (horizontal + 2*column*(radius+gap), vertical), radius)
                    count += 1
                    if count == score:
                        score_row = 1*row
                        color = off_color

    font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    text_surface_obj = font_obj.render(str(score), True, colors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (bottom_centre[0], bottom_centre[1] - ((score_row+3)*(radius+gap)))

    window.blit(text_surface_obj, text_rect_obj)

def diamondsTest():
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    window = pygame.display.set_mode((info.current_w, info.current_h-60))
    window.fill(colors['white'])

    draw_tower(window, colors['red'], [window.get_size()[0]/7, window.get_size()[1]*0.7])

    pygame.display.flip()

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {}'.format(x, y))
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

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

def turnMarkerTest():
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    window = pygame.display.set_mode((info.current_w, info.current_h-60))
    gradientRect( window, (95, 4, 107), (152, 88, 182), pygame.Rect( 0, 0, *window.get_size() ) )

    players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke']
    centres = [[window.get_size()[0]/(len(players)+1)*i, window.get_size()[1]*0.8] for i in range(1, (len(players)+1))]
    tower_colors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['cyan'], colors['orange']]

    for i in range(len(players)):
        profilePicture(window, centres[i], tower_colors[i], players[i])
        drawTurnMarkers(window, [centres[i][0] + window.get_size()[0]/15, centres[i][1]], 10, None)

    pygame.display.flip()

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {}'.format(x, y))
        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

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
        draw_tower(window, tower_colors[i], tower_offcolors[i], [centres[i][0], centres[i][1] - window.get_size()[1]*0.2], scores[i], radius)

    margin = 0.02

    font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/50))
    text_surface_obj = font_obj.render('Demolition', True, colors['white'])
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (window.get_size()[0]/2, max(window.get_size())*margin)

    window.blit(text_surface_obj, text_rect_obj)

    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [window.get_size()[0]/2 + text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    draw_diamond(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0]/2 - text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0]/2 + text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

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

def drawMenu(window, players, addingPlayer=False):
    window.fill([255,255,255])
    gradientRect( window, (63, 72, 204), (0, 162, 232), pygame.Rect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200

    title_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/50))
    title_text_surface_obj = title_font_obj.render('Darts', True, colors['white'])
    title_text_rect_obj = title_text_surface_obj.get_rect()
    title_text_rect_obj.center = (window.get_size()[0]/2, max(window.get_size())*margin)

    window.blit(title_text_surface_obj, title_text_rect_obj)

    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    draw_diamond(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

    play_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    play_text_surface_obj = play_font_obj.render('Play', True, colors['white'])
    play_text_rect_obj = play_text_surface_obj.get_rect()
    play_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    play_text_rect_obj.center = play_text_rect_obj_center
    play_button_size = 1*play_text_rect_obj.size
    window.blit(play_text_surface_obj, play_text_rect_obj)

    addPlayer_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    if len(players) < 6:
        addPlayer_text_surface_obj = addPlayer_font_obj.render('Add Player', True, colors['white'])
    else:
        addPlayer_text_surface_obj = addPlayer_font_obj.render('Add Player', True, colors['red'])
    addPlayer_text_rect_obj = addPlayer_text_surface_obj.get_rect()
    addPlayer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    addPlayer_text_rect_obj.center = addPlayer_text_rect_obj_center
    addPlayer_button_size = 1*addPlayer_text_rect_obj.size
    if not addingPlayer:
        window.blit(addPlayer_text_surface_obj, addPlayer_text_rect_obj)

    quit_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    quit_text_surface_obj = quit_font_obj.render('Quit', True, colors['white'])
    quit_text_rect_obj = quit_text_surface_obj.get_rect()
    quit_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.7)
    quit_text_rect_obj.center = quit_text_rect_obj_center
    quit_button_size = quit_text_rect_obj.size
    window.blit(quit_text_surface_obj, quit_text_rect_obj)

    playerColors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['cyan'], colors['orange']]
    for i in range(len(players)):
       profilePicture(window, [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4],
                      playerColors[i], players[i], i)

    pygame.display.flip()

    return [play_button_size, play_text_rect_obj_center, addPlayer_button_size, addPlayer_text_rect_obj_center,
            quit_button_size, quit_text_rect_obj_center]

def menuTest():
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

    buttons = drawMenu(window, players)
    play_button_size, play_text_rect_obj_center = buttons[0], buttons[1]
    addPlayer_button_size, addPlayer_text_rect_obj_center = buttons[2], buttons[3]
    quit_button_size, quit_text_rect_obj_center = buttons[4], buttons[5]

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        drawMenu(window, players)

        if abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
            pygame.draw.line(window, colors['white'], [play_text_rect_obj_center[0] - play_button_size[0]/2, play_text_rect_obj_center[1] + play_button_size[1]/2], [play_text_rect_obj_center[0] + play_button_size[0]/2, play_text_rect_obj_center[1] + play_button_size[1]/2], width=3)

        if len(players) < 6 and abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
            pygame.draw.line(window, colors['white'], [addPlayer_text_rect_obj_center[0] - addPlayer_button_size[0]/2, addPlayer_text_rect_obj_center[1] + addPlayer_button_size[1]/2], [addPlayer_text_rect_obj_center[0] + addPlayer_button_size[0]/2, addPlayer_text_rect_obj_center[1] + addPlayer_button_size[1]/2], width=3)

        if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
            pygame.draw.line(window, colors['white'], [quit_text_rect_obj_center[0] - quit_button_size[0]/2, quit_text_rect_obj_center[1] + quit_button_size[1]/2], [quit_text_rect_obj_center[0] + quit_button_size[0]/2, quit_text_rect_obj_center[1] + quit_button_size[1]/2], width=3)

        pygame.display.flip()

        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
                    print('Play!')
                    
                if len(players) < 6 and abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
                    buttons = drawMenu(window, players, True)
                    players.append(addPlayer(window, buttons[2], players))

                if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
                    print('Quit')
                    pygame.quit()
                    return

def addPlayer(window, addPlayer_button_size, players):
    font = pygame.font.Font(None, int(window.get_size()[0]/30))
    clock = pygame.time.Clock()
    dims = (width, height) = addPlayer_button_size
    input_box_centre = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    input_box = pygame.Rect(*input_box_centre, width, height)
    input_box.center = input_box_centre
    color_inactive = colors['grey59']
    color_active = colors['white']
    color = color_inactive
    active = False
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        drawMenu(window, players, True)
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(width, txt_surface.get_width()+10)
        input_box.w = width
        input_box.center = input_box_centre
        # Blit the text.
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(window, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def addPlayerTest():
    pygame.init()
    
    FPS = 30 #frames per second setting
    fpsClock = pygame.time.Clock()

    info = pygame.display.Info()

    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren', 'Izzy']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel', 'Lauren']
    # players = ['Josh', 'Ben', 'Luke', 'Rachel']
    # players = ['Josh', 'Ben', 'Luke']
    # players = ['Josh', 'Ben']
    players = ['Josh']

    window = pygame.display.set_mode((info.current_w/2, (info.current_h-60)/2))

    buttons = drawMenu(window, players)
    play_button_size, play_text_rect_obj_center = buttons[0], buttons[1]
    quit_button_size, quit_text_rect_obj_center = buttons[2], buttons[3]
    addPlayer_button_size, addPlayer_text_rect_obj_center = buttons[4], buttons[5]

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        drawMenu(window, players)

        if abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
            pygame.draw.line(window, colors['white'], [play_text_rect_obj_center[0] - play_button_size[0]/2, play_text_rect_obj_center[1] + play_button_size[1]/2], [play_text_rect_obj_center[0] + play_button_size[0]/2, play_text_rect_obj_center[1] + play_button_size[1]/2], width=3)

        if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
            pygame.draw.line(window, colors['white'], [quit_text_rect_obj_center[0] - quit_button_size[0]/2, quit_text_rect_obj_center[1] + quit_button_size[1]/2], [quit_text_rect_obj_center[0] + quit_button_size[0]/2, quit_text_rect_obj_center[1] + quit_button_size[1]/2], width=3)

        if abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
            pygame.draw.line(window, colors['white'], [addPlayer_text_rect_obj_center[0] - addPlayer_button_size[0]/2, addPlayer_text_rect_obj_center[1] + addPlayer_button_size[1]/2], [addPlayer_text_rect_obj_center[0] + addPlayer_button_size[0]/2, addPlayer_text_rect_obj_center[1] + addPlayer_button_size[1]/2], width=3)

        pygame.display.flip()

        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
                    print('Play!')
                    
                if abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
                    buttons = drawMenu(window, players, True)
                    players.append(addPlayer(window, buttons[2], players))

                if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
                    print('Quit')
                    pygame.quit()
                    return

def drawGameMenu(window, players):
    window.fill([255,255,255])
    gradientRect( window, (0, 204, 51), (0, 255, 128), pygame.Rect( 0, 0, *window.get_size() ) )

    margin = 0.02
    radius = window.get_size()[0]/200

    title_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/50))
    title_text_surface_obj = title_font_obj.render('Play', True, colors['white'])
    title_text_rect_obj = title_text_surface_obj.get_rect()
    title_text_rect_obj.center = (window.get_size()[0]/2, max(window.get_size())*margin)

    window.blit(title_text_surface_obj, title_text_rect_obj)

    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], width=1)
    pygame.draw.line(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], width=1)
    draw_diamond(window, colors['white'], [max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, window.get_size()[1] - max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0] - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0]/2 - title_text_rect_obj.width - max(window.get_size())*margin, max(window.get_size())*margin], radius)
    draw_diamond(window, colors['white'], [window.get_size()[0]/2 + title_text_rect_obj.width + max(window.get_size())*margin, max(window.get_size())*margin], radius)

    demolition_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    demolition_text_surface_obj = demolition_font_obj.render('Demolition', True, colors['white'])
    demolition_text_rect_obj = demolition_text_surface_obj.get_rect()
    demolition_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.2)
    demolition_text_rect_obj.center = demolition_text_rect_obj_center
    demolition_button_size = 1*demolition_text_rect_obj.size
    window.blit(demolition_text_surface_obj, demolition_text_rect_obj)

    killer_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    killer_text_surface_obj = killer_font_obj.render('Killer', True, colors['white'])
    killer_text_rect_obj = killer_text_surface_obj.get_rect()
    killer_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.35)
    killer_text_rect_obj.center = killer_text_rect_obj_center
    killer_button_size = 1*killer_text_rect_obj.size
    window.blit(killer_text_surface_obj, killer_text_rect_obj)

    back_font_obj = pygame.font.Font('freesansbold.ttf', int(window.get_size()[0]/30))
    back_text_surface_obj = back_font_obj.render('Back', True, colors['white'])
    back_text_rect_obj = back_text_surface_obj.get_rect()
    back_text_rect_obj_center = (window.get_size()[0]/2, window.get_size()[1]*0.7)
    back_text_rect_obj.center = back_text_rect_obj_center
    back_button_size = back_text_rect_obj.size
    window.blit(back_text_surface_obj, back_text_rect_obj)

    playerColors = [colors['red'], colors['blue'], colors['green'], colors['yellow'], colors['cyan'], colors['orange']]
    for i in range(len(players)):
       profilePicture(window, [(5*(i%2 != 0) + (i%2 == 0))*window.get_size()[0]/6, (i//2 + 1)*window.get_size()[1]/4],
                      playerColors[i], players[i], i)

    pygame.display.flip()

    return [demolition_button_size, demolition_text_rect_obj_center, killer_button_size, killer_text_rect_obj_center,
            back_button_size, back_text_rect_obj_center]

def gameMenuTest():
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

    buttons = drawGameMenu(window, players)
    demolition_button_size, demolition_text_rect_obj_center = buttons[0], buttons[1]
    killer_button_size, killer_text_rect_obj_center = buttons[2], buttons[3]
    back_button_size, back_text_rect_obj_center = buttons[4], buttons[5]

    while True:
        x, y = pygame.mouse.get_pos()
        pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))

        drawGameMenu(window, players)

        if abs(x - demolition_text_rect_obj_center[0]) <= demolition_button_size[0] and abs(y - demolition_text_rect_obj_center[1]) <= demolition_button_size[1]:
            pygame.draw.line(window, colors['white'], [demolition_text_rect_obj_center[0] - demolition_button_size[0]/2, demolition_text_rect_obj_center[1] + demolition_button_size[1]/2], [demolition_text_rect_obj_center[0] + demolition_button_size[0]/2, demolition_text_rect_obj_center[1] + demolition_button_size[1]/2], width=3)

        if len(players) < 6 and abs(x - killer_text_rect_obj_center[0]) <= killer_button_size[0] and abs(y - killer_text_rect_obj_center[1]) <= killer_button_size[1]:
            pygame.draw.line(window, colors['white'], [killer_text_rect_obj_center[0] - killer_button_size[0]/2, killer_text_rect_obj_center[1] + killer_button_size[1]/2], [killer_text_rect_obj_center[0] + killer_button_size[0]/2, killer_text_rect_obj_center[1] + killer_button_size[1]/2], width=3)

        if abs(x - back_text_rect_obj_center[0]) <= back_button_size[0] and abs(y - back_text_rect_obj_center[1]) <= back_button_size[1]:
            pygame.draw.line(window, colors['white'], [back_text_rect_obj_center[0] - back_button_size[0]/2, back_text_rect_obj_center[1] + back_button_size[1]/2], [back_text_rect_obj_center[0] + back_button_size[0]/2, back_text_rect_obj_center[1] + back_button_size[1]/2], width=3)

        pygame.display.flip()

        fpsClock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if abs(x - demolition_text_rect_obj_center[0]) <= demolition_button_size[0] and abs(y - demolition_text_rect_obj_center[1]) <= demolition_button_size[1]:
                    print('Demolition')
                    
                if len(players) < 6 and abs(x - killer_text_rect_obj_center[0]) <= killer_button_size[0] and abs(y - killer_text_rect_obj_center[1]) <= killer_button_size[1]:
                    print('Killer')

                if abs(x - back_text_rect_obj_center[0]) <= back_button_size[0] and abs(y - back_text_rect_obj_center[1]) <= back_button_size[1]:
                    print('Back')
                    return window

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('Back')
                    return window

def multiMenuTest():
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

    buttons = drawMenu(window, players)
    play_button_size, play_text_rect_obj_center = buttons[0], buttons[1]
    addPlayer_button_size, addPlayer_text_rect_obj_center = buttons[2], buttons[3]
    quit_button_size, quit_text_rect_obj_center = buttons[4], buttons[5]

    menu = 'main'

    while True:
        if menu == 'main':
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))
    
            drawMenu(window, players)
    
            if abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
                pygame.draw.line(window, colors['white'], [play_text_rect_obj_center[0] - play_button_size[0]/2, play_text_rect_obj_center[1] + play_button_size[1]/2], [play_text_rect_obj_center[0] + play_button_size[0]/2, play_text_rect_obj_center[1] + play_button_size[1]/2], width=3)
    
            if len(players) < 6 and abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
                pygame.draw.line(window, colors['white'], [addPlayer_text_rect_obj_center[0] - addPlayer_button_size[0]/2, addPlayer_text_rect_obj_center[1] + addPlayer_button_size[1]/2], [addPlayer_text_rect_obj_center[0] + addPlayer_button_size[0]/2, addPlayer_text_rect_obj_center[1] + addPlayer_button_size[1]/2], width=3)
    
            if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
                pygame.draw.line(window, colors['white'], [quit_text_rect_obj_center[0] - quit_button_size[0]/2, quit_text_rect_obj_center[1] + quit_button_size[1]/2], [quit_text_rect_obj_center[0] + quit_button_size[0]/2, quit_text_rect_obj_center[1] + quit_button_size[1]/2], width=3)
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
                        menu = 'play'
                        
                    if len(players) < 6 and abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
                        buttons = drawMenu(window, players, True)
                        players.append(addPlayer(window, buttons[2], players))
    
                    if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
                        print('Quit')
                        pygame.quit()
                        return

        if menu == 'play':
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption('{}, {} - {}, {}'.format(x, y, abs(x - window.get_size()[0]/2), abs(y - window.get_size()[1]/2)))
    
            buttons = drawGameMenu(window, players)
            demolition_button_size, demolition_text_rect_obj_center = buttons[0], buttons[1]
            killer_button_size, killer_text_rect_obj_center = buttons[2], buttons[3]
            back_button_size, back_text_rect_obj_center = buttons[4], buttons[5]

            if abs(x - demolition_text_rect_obj_center[0]) <= demolition_button_size[0] and abs(y - demolition_text_rect_obj_center[1]) <= demolition_button_size[1]:
                pygame.draw.line(window, colors['white'], [demolition_text_rect_obj_center[0] - demolition_button_size[0]/2, demolition_text_rect_obj_center[1] + demolition_button_size[1]/2], [demolition_text_rect_obj_center[0] + demolition_button_size[0]/2, demolition_text_rect_obj_center[1] + demolition_button_size[1]/2], width=3)
    
            if len(players) < 6 and abs(x - killer_text_rect_obj_center[0]) <= killer_button_size[0] and abs(y - killer_text_rect_obj_center[1]) <= killer_button_size[1]:
                pygame.draw.line(window, colors['white'], [killer_text_rect_obj_center[0] - killer_button_size[0]/2, killer_text_rect_obj_center[1] + killer_button_size[1]/2], [killer_text_rect_obj_center[0] + killer_button_size[0]/2, killer_text_rect_obj_center[1] + killer_button_size[1]/2], width=3)
    
            if abs(x - back_text_rect_obj_center[0]) <= back_button_size[0] and abs(y - back_text_rect_obj_center[1]) <= back_button_size[1]:
                pygame.draw.line(window, colors['white'], [back_text_rect_obj_center[0] - back_button_size[0]/2, back_text_rect_obj_center[1] + back_button_size[1]/2], [back_text_rect_obj_center[0] + back_button_size[0]/2, back_text_rect_obj_center[1] + back_button_size[1]/2], width=3)
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if abs(x - demolition_text_rect_obj_center[0]) <= demolition_button_size[0] and abs(y - demolition_text_rect_obj_center[1]) <= demolition_button_size[1]:
                        print('Demolition')
                        
                    if len(players) < 6 and abs(x - killer_text_rect_obj_center[0]) <= killer_button_size[0] and abs(y - killer_text_rect_obj_center[1]) <= killer_button_size[1]:
                        print('Killer')
    
                    if abs(x - back_text_rect_obj_center[0]) <= back_button_size[0] and abs(y - back_text_rect_obj_center[1]) <= back_button_size[1]:
                        menu = 'main'
    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu = 'main'