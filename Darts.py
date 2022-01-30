from os import environ as osEnviron
from sys import exit as sysExit
from pygame import init as pygameInit, quit as pygameQuit
from pygame import VIDEORESIZE as pygameVIDEORESIZE, RESIZABLE as pygameRESIZABLE, KEYDOWN as pygameKEYDOWN
from pygame import MOUSEBUTTONDOWN as pygameMOUSEBUTTONDOWN, K_ESCAPE as pygameK_ESCAPE, K_F11 as pygameK_F11
from pygame.time import Clock as pygameTimeClock
from pygame.display import Info as pygameDisplayInfo, set_mode as pygameDisplaySet_mode
from pygame.display import set_caption as pygameDisplaySet_caption, flip as pygameDisplayFlip
from pygame.display import list_modes as pygameDisplayList_modes, init as pygameDisplayInit, quit as pygameDisplayQuit
from pygame.event import get as pygameEventGet
from pygame.mouse import get_pos as pygameMouseGet_pos
from pygame.locals import QUIT as pygameLocalsQUIT
from pygame.color import THECOLORS as pygameColors
from pygameGUIs import drawMenu, drawGameMenu, drawSettingsMenu, addPlayer, drawCross, drawUnderlineWithOutline
from Games import Demolition
maximised_res = (1536, 801)
maximised_pos = "0,20"

def main():
    pygameInit()
    
    FPS = 30 #frames per second setting
    fpsClock = pygameTimeClock()

    info = pygameDisplayInfo()

    resolutions, resolution_index = [], -1
    for resolution in pygameDisplayList_modes():
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
    osEnviron['SDL_VIDEO_WINDOW_POS'] = maximised_pos
    window = pygameDisplaySet_mode(maximised_res, pygameRESIZABLE)

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
            x, y = pygameMouseGet_pos()
            pygameDisplaySet_caption('Darts - Menu')
    
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
    
            pygameDisplayFlip()
    
            fpsClock.tick(FPS)
            for event in pygameEventGet():
                if event.type == pygameLocalsQUIT:
                    pygameQuit()
                    return
    
                elif event.type == pygameMOUSEBUTTONDOWN:
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
                        pygameQuit()
                        return

                elif event.type == pygameKEYDOWN:
                    if event.key == pygameK_F11:
                        if fullscreen:
                            pygameDisplayQuit()
                            osEnviron['SDL_VIDEO_WINDOW_POS'] = maximised_pos
                            pygameDisplayInit()
                            window = pygameDisplaySet_mode(maximised_res, pygameRESIZABLE)
                        else:
                            pygameDisplayQuit()
                            osEnviron['SDL_VIDEO_WINDOW_POS'] = "0,0"
                            pygameDisplayInit()
                            window = pygameDisplaySet_mode((info.current_w, info.current_h), pygameRESIZABLE)
                        fullscreen = not fullscreen

                elif event.type == pygameVIDEORESIZE:
                    window = pygameDisplaySet_mode((event.w, event.h), pygameRESIZABLE)

        if menu == 'settings':
            x, y = pygameMouseGet_pos()
            pygameDisplaySet_caption('Darts - Settings')

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

                    if mouse_on_apply:
                        if curr_resolution != resolutions[resolution_index]:
                            new_res_ratio = int(resolutions[-1].split(' × ')[0])/int(resolutions[resolution_index].split(' × ')[0])
                            window = pygameDisplaySet_mode([res/new_res_ratio for res in maximised_res], pygameRESIZABLE)
                            buttons = drawSettingsMenu(window, resolutions[resolution_index], False, False)
                            leftButton_center, leftButton_button_size = buttons[0], buttons[1]
                            rightButton_center, rightButton_button_size = buttons[2], buttons[3]
                            back_button_size, back_text_rect_obj_center = buttons[4], buttons[5]
                            apply_button_size, apply_text_rect_obj_center = buttons[6], buttons[7]
                            curr_resolution = resolutions[resolution_index]

                    if mouse_on_back:
                        menu = 'main'
    
                elif event.type == pygameKEYDOWN:
                    if event.key == pygameK_ESCAPE:
                        menu = 'main'

                    if event.key == pygameK_F11:
                        if fullscreen:
                            pygameDisplayQuit()
                            osEnviron['SDL_VIDEO_WINDOW_POS'] = maximised_pos
                            pygameDisplayInit()
                            window = pygameDisplaySet_mode(maximised_res, pygameRESIZABLE)
                        else:
                            pygameDisplayQuit()
                            osEnviron['SDL_VIDEO_WINDOW_POS'] = "0,0"
                            pygameDisplayInit()
                            window = pygameDisplaySet_mode((info.current_w, info.current_h), pygameRESIZABLE)
                        fullscreen = not fullscreen

                elif event.type == pygameVIDEORESIZE:
                    window = pygameDisplaySet_mode((event.w, event.h), pygameRESIZABLE)

        if menu == 'play':
            x, y = pygameMouseGet_pos()
            pygameDisplaySet_caption('Darts - Play')
    
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
    
            pygameDisplayFlip()
    
            fpsClock.tick(FPS)
            for event in pygameEventGet():
                if event.type == pygameLocalsQUIT:
                    pygameQuit()
                    return
    
                elif event.type == pygameMOUSEBUTTONDOWN:
                    if mouse_on_demolition:
                        pygameDisplaySet_caption('Darts - Demolition')
                        game = Demolition(window, players)
                        game.play()
                        menu = 'play'
                        
                    if mouse_on_killer:
                        print('Killer')
    
                    if mouse_on_back:
                        menu = 'main'
    
                elif event.type == pygameKEYDOWN:
                    if event.key == pygameK_ESCAPE:
                        menu = 'main'
                    if event.key == pygameK_F11:
                        if fullscreen:
                            pygameDisplayQuit()
                            osEnviron['SDL_VIDEO_WINDOW_POS'] = maximised_pos
                            pygameDisplayInit()
                            window = pygameDisplaySet_mode(maximised_res, pygameRESIZABLE)
                        else:
                            pygameDisplayQuit()
                            osEnviron['SDL_VIDEO_WINDOW_POS'] = "0,0"
                            pygameDisplayInit()
                            window = pygameDisplaySet_mode((info.current_w, info.current_h), pygameRESIZABLE)
                        fullscreen = not fullscreen

                elif event.type == pygameVIDEORESIZE:
                    window = pygameDisplaySet_mode((event.w, event.h), pygameRESIZABLE)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        sysExit(1)
