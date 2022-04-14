import os, sys, time
import pygame
from pygame.locals import QUIT
from pygame.color import THECOLORS as pygameColors
from pygameGUIs import drawMenu, drawGameMenu, drawSettingsMenu, addPlayer, drawCross, drawUnderlineWithOutline
from Games import Demolition
maximised_res = (1536, 801)
maximised_pos = "0,20"

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
    numFrames, frameCheck = 0, time.time()

    while True:
        underline_thickness = 2*(int(max(window.get_size())/500) + 1)
        if menu == 'main':
            x, y = pygame.mouse.get_pos()
            pygame.display.set_caption('Darts - Menu')
    
            buttons = drawMenu(window, players)
            play_button_size, play_text_rect_obj_center = buttons[0], buttons[1]
            addPlayer_button_size, addPlayer_text_rect_obj_center = buttons[2], buttons[3]
            settings_button_size, settings_text_rect_obj_center = buttons[4], buttons[5]
            quit_button_size, quit_text_rect_obj_center = buttons[6], buttons[7]
            crossDims = buttons[8]
            mouse_on_cross = []

            for crossCentre, crossRadius in crossDims:
                if (x - crossCentre[0])**2 + (y - crossCentre[1])**2 <= crossRadius**2:
                    drawCross(window, crossCentre, crossRadius, pygameColors['red'], pygameColors['white'])
                    mouse_on_cross.append(True)
                else:
                    drawCross(window, crossCentre, crossRadius, pygameColors['white'], pygameColors['black'])
                    mouse_on_cross.append(False)

            mouse_on_play, mouse_on_addPlayer, mouse_on_settings, mouse_on_quit = False, False, False, False
            if len(players) > 0 and abs(x - play_text_rect_obj_center[0]) <= play_button_size[0] and abs(y - play_text_rect_obj_center[1]) <= play_button_size[1]:
                drawUnderlineWithOutline(window, play_text_rect_obj_center, play_button_size, underline_thickness,
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_play = True
    
            if len(players) < 6 and abs(x - addPlayer_text_rect_obj_center[0]) <= addPlayer_button_size[0] and abs(y - addPlayer_text_rect_obj_center[1]) <= addPlayer_button_size[1]:
                drawUnderlineWithOutline(window, addPlayer_text_rect_obj_center, addPlayer_button_size,
                                     underline_thickness, pygameColors['white'], pygameColors['black'], 2)
                mouse_on_addPlayer = True
    
            if abs(x - settings_text_rect_obj_center[0]) <= settings_button_size[0] and abs(y - settings_text_rect_obj_center[1]) <= settings_button_size[1]:
                drawUnderlineWithOutline(window, settings_text_rect_obj_center, settings_button_size, underline_thickness,
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_settings = True
    
            if abs(x - quit_text_rect_obj_center[0]) <= quit_button_size[0] and abs(y - quit_text_rect_obj_center[1]) <= quit_button_size[1]:
                drawUnderlineWithOutline(window, quit_text_rect_obj_center, quit_button_size, underline_thickness,
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_quit = True
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            numFrames += 1
            if time.time() - frameCheck > 1:
                pygame.display.set_caption('Darts - Menu - {0} fps'.format(numFrames))
                numFrames, frameCheck = 0, time.time()

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
            pygame.display.set_caption('Darts - Settings')

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
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_back = True
    
            if abs(x - apply_text_rect_obj_center[0]) <= apply_button_size[0] and abs(y - apply_text_rect_obj_center[1]) <= apply_button_size[1]:
                drawUnderlineWithOutline(window, apply_text_rect_obj_center, apply_button_size, underline_thickness,
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_apply = True
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            numFrames += 1
            if time.time() - frameCheck > 1:
                pygame.display.set_caption('Darts - Settings - {0} fps'.format(numFrames))
                numFrames, frameCheck = 0, time.time()

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
            pygame.display.set_caption('Darts - Play')
    
            buttons = drawGameMenu(window, players)
            demolition_button_size, demolition_text_rect_obj_center = buttons[0], buttons[1]
            killer_button_size, killer_text_rect_obj_center = buttons[2], buttons[3]
            back_button_size, back_text_rect_obj_center = buttons[4], buttons[5]

            mouse_on_demolition, mouse_on_killer, mouse_on_back = False, False, False
            if abs(x - demolition_text_rect_obj_center[0]) <= demolition_button_size[0] and abs(y - demolition_text_rect_obj_center[1]) <= demolition_button_size[1]:
                drawUnderlineWithOutline(window, demolition_text_rect_obj_center, demolition_button_size, underline_thickness,
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_demolition = True
    
            if len(players) < 6 and abs(x - killer_text_rect_obj_center[0]) <= killer_button_size[0] and abs(y - killer_text_rect_obj_center[1]) <= killer_button_size[1]:
                drawUnderlineWithOutline(window, killer_text_rect_obj_center, killer_button_size, underline_thickness,
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_killer = True
    
            if abs(x - back_text_rect_obj_center[0]) <= back_button_size[0] and abs(y - back_text_rect_obj_center[1]) <= back_button_size[1]:
                drawUnderlineWithOutline(window, back_text_rect_obj_center, back_button_size, underline_thickness,
                                     pygameColors['white'], pygameColors['black'], 2)
                mouse_on_back = True
    
            pygame.display.flip()
    
            fpsClock.tick(FPS)
            numFrames += 1
            if time.time() - frameCheck > 1:
                pygame.display.set_caption('Darts - Play - {0} fps'.format(numFrames))
                numFrames, frameCheck = 0, time.time()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_on_demolition:
                        pygame.display.set_caption('Darts - Demolition')
                        game = Demolition(window, players, fpsClock, FPS)
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
