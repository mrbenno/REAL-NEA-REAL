#importing nessacary modules
import pygame
from pygame.examples.music_drop_fade import volume
import pickle
from os import path
import time

from Character import Player
from Enviroment import World
from UI import Button, Title

# defining the main function, contains most variables and instances of objects
def main():
    pygame.init() #initialises Pygame

    #creating a window, getting it's dimensions, and defining frame as the instance of Pygame's Clock class
    screen = pygame.display.set_mode((720, 540))
    dimensions = [screen.get_width(), screen.get_height()]
    frame = pygame.time.Clock()

    # loading images
    main_title_icon = pygame.image.load("Assets/Titles.png")
    fifties_title_icon = pygame.image.load("Assets/Title1950.png")
    play_button_icon = pygame.image.load("Assets/PlayBtn.png")
    play_button_down_icon = pygame.image.load("Assets/PlayBtnDown.png")
    pause_title_image = pygame.image.load("Assets/PauseTitle.png")
    pause_button_icon = pygame.image.load("Assets/PauseBtn.png")
    pause_button_down_icon = pygame.image.load("Assets/PauseBtnDown.png")
    resume_button_icon = pygame.image.load("Assets/ResumeBtn.png")
    resume_button_down_icon = pygame.image.load("Assets/ResumeBtnDown.png")
    vol_up_button_icon = pygame.image.load("Assets/VolUpBtn.png")
    vol_up_button_down_icon = pygame.image.load("Assets/VolUpBtnDown.png")
    vol_down_button_icon = pygame.image.load("Assets/VolDownBtn.png")
    vol_down_button_down_icon = pygame.image.load("Assets/VolDownBtnDown.png")
    restart_button_icon = pygame.image.load("Assets/RestartBtn.png")
    restart_button_icon_down = pygame.image.load("Assets/RestartBtnDown.png")
    quit_button_icon = pygame.image.load("Assets/QuitBtn.png")
    quit_button_down_icon = pygame.image.load("Assets/QuitBtnDown.png")
    sub_tog_off = pygame.image.load("Assets/SubtitleTglOff.png")
    sub_tog_off_down = pygame.image.load("Assets/SubtitleTglOffDown.png")
    sub_tog_on = pygame.image.load("Assets/SubtitleTglOn.png")
    sub_tog_on_down = pygame.image.load("Assets/SubtitleTglOnDown.png")

    option_button_icon1 = pygame.image.load("Assets/Options/Options-1.png")
    option_button_icon2 = pygame.image.load("Assets/Options/Options-2.png")
    option_button_icon3 = pygame.image.load("Assets/Options/Options-3.png")
    option_button_icon4 = pygame.image.load("Assets/Options/Options-4.png")
    option_button_icon5 = pygame.image.load("Assets/Options/Options-5.png")
    option_button_icon6 = pygame.image.load("Assets/Options/Options-6.png")


    # loading fonts
    pixelType_title = pygame.font.Font("Fonts/Pixeltype.ttf", 50)
    pixelType_body = pygame.font.Font("Fonts/Pixeltype.ttf", 40)

    tile_size = 30 #needed for the world building system to work
    main_menu = True # allows the program to start on the main menu
    level = 1 # tells the program what level to start on
    max_level = 5 # tell the program what the highest level is

    # accessing the world files using the Pickle module
    if path.exists(f'Level Data/data_{level}'): # checks to see if a path exists for a select level
        pickle_in = open(f'Level Data/data_{level}', 'rb') # if true, file is opened and put into the pickle_in variable
        data = pickle.load(pickle_in) # the file's pickled contents are read and assigned to the data variable
    world = World(data, '#2E4D4C') # the data variable is used to create an instance of the World class
 

    # creating instances of classes, creates the player, world and it's obstacles
    player1 = Player(pygame.Rect(60, dimensions[1] - 120, 25, 25), '#0A9B9A', 5, False,
                     False, 8, False, 0.53)
    
    spike_group = pygame.sprite.Group()

    # rendering text
    description_1 = pixelType_body.render("Press SPACE to continue.", True, '#FFFFFF')
    paragraph_1 = pixelType_body.render(
         "After the multiple technological innovations of the 1940s,"
         "some of the more notable being Alan Turing's Bombe Machine, "
         "the fifties were looking to introduce even more of the sort.", True, '#FFFFFF')

    subtitles_label = pixelType_title.render("Subtitles", True, '#FFFFFF')

    # more instances of classes, creates the menus and general user interface
    nimbus_bold = pygame.font.Font("Fonts/NimbusMono-Bold.otf", 15)
    player_tooltip_1 = nimbus_bold.render("Press A and D to move left and right.", True, '#FFFFFF')
    player_tooltip_2 = nimbus_bold.render("Press SPACE to jump.", True, '#FFFFFF')
    player_tooltip_3 = nimbus_bold.render("Watch out for the RED LAVA.", True, '#FFFFFF')
    player_tooltip_4 = nimbus_bold.render("Watch out for the SPIKES too.", True, '#FFFFFF')

    main_title = Title(main_title_icon, 500, 250, dimensions[0] // 2 - 250, 25)
    fifties_title = Title(fifties_title_icon, dimensions[0], dimensions[0] // 2, 0, 100)
    play_button = Button(play_button_icon, play_button_down_icon, 150, 100, (dimensions[0] // 2) - 75, 300)
    fifties_title_small = Title(fifties_title_icon, dimensions[0] // 2, dimensions[0] // 4, 0, 25)

    pause_button = Button(pause_button_icon, pause_button_down_icon, 30, 30, dimensions[0] - 90, 45)
    pause_title_image = Title(pause_title_image, 200, 100, (dimensions[0] // 2) + 25, 25)
    resume_button = Button(resume_button_icon, resume_button_down_icon, 160, 50, (dimensions[0] // 2) + 25, 150)
    volume_up_button = Button(vol_up_button_icon, vol_up_button_down_icon, 25,25, 610, 250)
    volume_down_button = Button(vol_down_button_icon, vol_down_button_down_icon, 25, 25, 575, 250)
    subtitle_toggle_off = Button(sub_tog_off, sub_tog_off_down, 50, 25, 575, 300)
    subtitle_toggle_on = Button(sub_tog_on, sub_tog_on_down, 50, 25, 575, 300)
    restart_button = Button(restart_button_icon, restart_button_icon_down, 160, 50, (dimensions[0] // 2) + 25, 350)
    quit_button = Button(quit_button_icon, quit_button_down_icon, 100, 50, (dimensions[0] // 2) + 25, 450)

    #main Pygame loop required to keep it running until the player closes the window
    run = True
    delta_time = 0
    world.build_world(tile_size, spike_group)
    while run ==  True:
        start = time.time()
        
        frame.tick(60)
        handle_events()

        if main_menu == True: # creates main menu (title, button)
             main_title.draw(screen)
             if play_button.draw(screen): # if player clicks 'play':
                  main_menu = False
                  scene1 = True
                  
                  
        else: # once main menu set to false, actual game begins
            if scene1 == True:
                output = fifties_intro(screen, fifties_title, description_1, paragraph_1)  
                if output == True:
                    scene1 = False
            
            # if scene1 == False:
            #     if pause_button.draw(screen):
            #         player1.is_paused = True

            #     if not player1.is_paused:
            #         player1.check_input()
            #         player1.update()
            #         draw_everything(screen, player1, spike_group, pause_button)
                    
            #         for spike in spike_group:
            #             spike.animate(delta_time)

            #         world.draw(screen)
            #         player1.update_tile_list(world.tileList)

            #         game_over = player1.game_over(540, spike_group)
                    
            #         if game_over == -1:
            #             death_sfx = pygame.mixer.Sound("Sounds/Death.wav")
            #             death_sfx.set_volume(player1.volume)
            #             if player1.volume > 0.04:
            #                 death_sfx.play()
            #             level = 1
            #             data = []
            #             world = level_reset(level, player1, spike_group)
            #             world.build_world(tile_size, spike_group)
            #             player1.rect.x, player1.rect.y = player1.spawnPoint
            #             player1.velocity = [0, 0]
            #             game_over = 0
            #         elif game_over == 1:
            #             level += 1
            #             if level <= max_level:
            #                 data = []
            #                 world = level_reset(level, player1, spike_group)
            #                 world.build_world(tile_size, spike_group)
            #                 game_over = 0
            #             else:
            #                 screen.fill('#000000')

            #         if level == 1:
            #              screen.blit(player_tooltip_1, player1.rect.topright + (25, 25))
            #         elif level == 2:
            #              screen.blit(player_tooltip_2, player1.rect.topright)
            #         elif level == 3:
            #              screen.blit(player_tooltip_3, player1.rect.topright)
            #         elif level == 4:
            #              screen.blit(player_tooltip_4, player1.rect.topright)

            #     elif player1.is_paused:
            #         fifties_title_small.draw
            #         result = (pause_menu(screen, player1, pause_title_image, resume_button, pixelType_title, volume_up_button, volume_down_button, 
            #                             subtitles_label, subtitle_toggle_on, subtitle_toggle_off, restart_button, quit_button))
            #         if result == 6:
            #                 player1.is_paused = False
            #                 level = 1
            #                 data = []
            #                 world = level_reset(level, player1, spike_group)
            #                 world.build_world(tile_size, spike_group)
                    
            #         elif result == 7:
            #             run = False

            #     if player1.is_paused and not resume_button.draw:
            #         pause_button.draw = False
            #         player1.is_paused = False

        pygame.display.flip()  # display.flip updates entire screen, display.update updates what's in brackets

        end = time.time()
        delta_time = end - start

    pygame.quit()


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


def draw_everything(screen, player, enemies, pause):
    screen.fill('#0A141F')
    player.draw(screen)
    enemies.draw(screen)
    pause.draw(screen)

def fifties_intro(screen, title, text, text2):
    titles = True
    screen.fill('#000000')
    title.draw(screen)
    screen.blit(text, (85, 450))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
         titles = False

    if titles == False:
         screen.fill('#000000')
         screen.blit(text2, (25, 25))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return True


def pause_menu(screen, player, title, button1, font, button2, button3, text2, button4, button5, button6, button7):
    pygame.draw.rect(screen, '#000000', pygame.Rect(360, 0, 360, 540))
    title.draw(screen)

    if button1 is not None and button1.draw(screen):
            player.is_paused = False

    text1 = font.render("Volume - "+ str(round(player.volume, 1)* 10), True, "White")
    screen.blit(text1, (386, 250))
    screen.blit(text2, (386, 300))
    

    if button2 is not None and button2.draw(screen):
            if not player.volume > 1.0:
                player.volume += 0.1

    if button3 is not None and button3.draw(screen):
            if not player.volume < 0.1:
                player.volume -= 0.1

    if button4 is not None and button4.draw(screen):
            return 4
        
    if button5 is not None and button5.draw(screen): 
            return 5
        
    if button6 is not None and button6.draw(screen):
            return 6
    
    if button7 is not None and button7.draw(screen):
            return 7


def level_reset(level, player, spikes):
    player.rect.x, player.rect.y = player.spawnPoint
    player.velocity = [0, 0]

    spikes.empty()

    if path.exists(f'Level Data/data_{level}'):
        pickle_in = open(f'Level Data/data_{level}', 'rb')
        data = pickle.load(pickle_in)
    world = World(data, '#2E4D4C')

    return world


if __name__ == "__main__":
    main()