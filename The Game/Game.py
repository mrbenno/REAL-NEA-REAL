#importing nessacary modules
import pygame
from pygame.examples.music_drop_fade import volume
import pickle
from os import path
import time

from Character import Player, Enemy
from Enviroment import World
from UI import Button, Title, Quiz

# defining the main function, contains most variables and instances of objects
def main():
    pygame.init() #initialises Pygame

    #creating a window, getting it's dimensions, and defining frame as the instance of Pygame's Clock class
    screen = pygame.display.set_mode((720, 540))
    pygame.display.set_caption('The Creator')
    dimensions = [screen.get_width(), screen.get_height()]
    frame = pygame.time.Clock()

    # loading images
    main_title_icon = pygame.image.load("Assets/Titles.png")
    play_button_icon = pygame.image.load("Assets/PlayBtn.png")
    play_button_down_icon = pygame.image.load("Assets/PlayBtnDown.png")
    fifties_title_icon = pygame.image.load("Assets/Title1950.png")
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
    quiz_title_icon = pygame.image.load("Assets/QuizTitle.png")

    # loading and resizing intro slides
    slide1 = pygame.image.load("Assets/Slide1.png")
    slide1 = pygame.transform.scale(slide1, (720, 540))
    slide2 = pygame.image.load("Assets/Slide2.png")
    slide2 = pygame.transform.scale(slide2, (720, 540))

    # storing the paths to voice line audio files
    voice_line_paths = [f"Sounds/Voice Lines/VoiceLine-{i}.wav" for i in range(1, 6)]

    # loading subtitle images and resizing them
    subtitles = []
    for i in range(1, 6):
        subtitles.append(pygame.image.load(f"Assets/Subtitles/Subtitle-{i}.png"))
    for i in range(len(subtitles)):
        subtitles[i] = pygame.transform.scale(subtitles[i], (580, 100))

    # loading fonts
    pixelType_title = pygame.font.Font("Fonts/Pixeltype.ttf", 50)
    pixelType_body = pygame.font.Font("Fonts/Pixeltype.ttf", 40)
    nimbus_bold = pygame.font.Font("Fonts/NimbusMono-Bold.otf", 15)

    tile_size = 30 #needed for the world building system to work
    main_menu = True # allows the program to start on the main menu
    level = 1 # tells the program what level to start on
    max_level = 5 # tells the program the highest level - allows for it to stop then
    intro = [False] # wrapped in list to allow modification in subroutines
    question = [False]
    result = [None, 0] # stores quiz result and timestamp
    has_played = [False, False, False, False, False] # ensures voice lines only play once per level
    subtitles_enabled = True

    white = ('#FFFFFF')
    black = ('#000000')

    # accessing the world files using the Pickle module
    if path.exists(f'Level Data/data_{level}'): # checks to see if a path exists for a select level
        pickle_in = open(f'Level Data/data_{level}', 'rb') # if true, file is opened and put into the pickle_in variable
        data = pickle.load(pickle_in) # the file's pickled contents are read and assigned to the data variable
    world = World(data) # the data variable is used to create an instance of the World class

    # creating player instance
    player1 = Player(pygame.Rect(60, dimensions[1] - 120, 25, 25), 5, False,
                     False, False, 8, 0.53)

    spike_group = pygame.sprite.Group() # used for hazards like spikes

    # rendering text
    description_1 = pixelType_body.render("Press SPACE to continue.", True, white)
    ending = pixelType_title.render("end", True, white)

    # setting up helper tooltips for each level
    tooltips = [
        [nimbus_bold.render("Press A and D to move left and right.", True, white), 
        nimbus_bold.render("Press ESC or the pause button for options.", True, white), 
        nimbus_bold.render("Go to the BLUE to complete the level.", True, white)], # level 1
        [nimbus_bold.render("Press W or SPACE to jump.", True, white)], # level 2
        [nimbus_bold.render("Watch out for the RED LAVA.", True, white)], # level 3
        [nimbus_bold.render("Watch out for the SPIKES too.", True, white)]] # level 4

    # more instances of classes, creates the menus and general user interface
    main_title = Title(main_title_icon, 500, 250, dimensions[0] // 2 - 250, 25)
    fifties_title = Title(fifties_title_icon, dimensions[0], dimensions[0] // 2, 0, 100)
    play_button = Button(play_button_icon, play_button_down_icon, 150, 100, (dimensions[0] // 2) - 75, 300)
    fifties_title_small = Title(fifties_title_icon, dimensions[0] // 2, dimensions[0] // 4, 0, 25)
    quiz_title = Title(quiz_title_icon, 320, 160, (dimensions[0] // 2) - 160, (dimensions[1] // 2) - 80)

    pause_button = Button(pause_button_icon, pause_button_down_icon, 30, 30, dimensions[0] - 75, 45)
    pause_title = Title(pause_title_image, 200, 100, (dimensions[0] // 2) + 25, 25)
    resume_button = Button(resume_button_icon, resume_button_down_icon, 160, 50, (dimensions[0] // 2) + 25, 150)
    volume_up_button = Button(vol_up_button_icon, vol_up_button_down_icon, 25,25, 610, 250)
    volume_down_button = Button(vol_down_button_icon, vol_down_button_down_icon, 25, 25, 575, 250)
    subtitle_toggle_off = Button(sub_tog_off, sub_tog_off_down, 50, 25, 575, 300)
    subtitle_toggle_on = Button(sub_tog_on, sub_tog_on_down, 50, 25, 575, 300)
    restart_button = Button(restart_button_icon, restart_button_icon_down, 160, 50, (dimensions[0] // 2) + 25, 375)
    quit_button = Button(quit_button_icon, quit_button_down_icon, 100, 50, (dimensions[0] // 2) + 25, 450)

    question_icon = pygame.image.load("Assets/Question1.png")
    choices = ("PARRY", "ELIZA", "ChatGPT", "Eugene Goostman") # quiz choices
    question_text = Quiz(question_icon, 480, 110, choices, 2)

    timer = [0] # for intro timing

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
                  intro_scene = True
                  
        else: # once main menu set to false, actual game begins
            if intro_scene == True:
                output = fifties_intro(screen, fifties_title, description_1, intro, timer, slide1, slide2)
                if output == True:
                    intro_scene = False
            
            if intro_scene == False:
                if pause_button.draw(screen):
                    player1.is_paused = True

                if not player1.is_paused:
                    # update game state while unpaused
                    player1.check_input()
                    player1.update()
                    draw_everything(screen, player1, world, subtitles_enabled, subtitles, level, spike_group, pause_button)
                      
                    for spike in spike_group:
                        spike.animate(delta_time)

                    # play level-specific voice line
                    if level <= len(voice_line_paths) and has_played[level - 1] == False:
                        current_voice_line = voice_line_paths[level - 1]
                        if player1.volume > 0.04:
                            pygame.mixer.music.load(voice_line_paths[level - 1])
                            pygame.mixer.music.set_volume(player1.volume)
                            pygame.mixer.music.play()
                        has_played[level - 1] = True

                    # show tooltips depending on level
                    if level <= 4:
                        for i, tooltip in enumerate(tooltips[level - 1]):
                            screen.blit(tooltip, (player1.rect.topright[0] + 5, player1.rect.topright[1] - 15 - i * 25))

                    game_over = player1.game_over(540, spike_group)

                    if game_over == -1:
                        # player has died
                        death_sfx = pygame.mixer.Sound("Sounds/Death.wav")
                        death_sfx.set_volume(player1.volume)
                        if player1.volume > 0.04:
                            death_sfx.play()
                        player1.rect.x, player1.rect.y = player1.spawn_point
                        player1.velocity = [0, 0]
                        game_over = 0
                    elif game_over == 1:
                        # level completed
                        pygame.mixer.music.pause()
                        level += 1
                        if level <= max_level:
                            data = []
                            world = level_reset(level, player1, spike_group)
                            world.build_world(tile_size, spike_group)
                            game_over = 0
                        else:
                            # game completed
                            player1.speed = 0
                            player1.volume = 0
                            screen.fill(black)
                            fifties_outro(screen, quiz_title, description_1, question_text, question, result, ending)

                elif player1.is_paused == True:
                    pygame.mixer.music.pause()

                    fifties_title_small.draw(screen)
                    pause_result = (pause_menu(screen, player1, pause_title, resume_button, pixelType_title, volume_up_button, volume_down_button, 
                                        restart_button, quit_button))
                    if pause_result == 1:
                        player1.is_paused = False
                        pygame.mixer.music.unpause()
                    
                    elif pause_result == 4:
                            player1.is_paused = False
                            level = 1
                            data = []
                            world = level_reset(level, player1, spike_group)
                            world.build_world(tile_size, spike_group)
                            has_played = [False, False, False, False, False]
                    
                    elif pause_result == 5:
                        run = False

                # rare edge case where player pauses via keyboard and then clicks back to game
                if player1.is_paused and not resume_button.draw:
                    pause_button.draw = False
                    player1.is_paused = False

        pygame.display.flip()  # note: display.flip updates entire screen, display.update updates what's in brackets

        # resetting the animation time etc
        end = time.time()        
        delta_time = end - start

    # pygame quits if run != True
    pygame.quit()


# subroutine responsible for checking if the user has quit the application
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


# self-explaintory
def draw_everything(screen, player, world, subs, sub, level, enemies, pause):
    screen.fill('#0A141F')
    world.draw(screen)
    player.update_tile_list(world.tile_list)
    if subs == True and level <= len(sub):
        screen.blit(sub[level - 1], (15, 15))
    player.draw(screen)
    enemies.draw(screen)
    pause.draw(screen)


# what runs when the app begins (after the main menu)
def fifties_intro(screen, title, text, intro, timer, slide1, slide2):
    screen.fill('#000000')

    if not intro[0]:
        title.draw(screen)
        screen.blit(text, (85, 450))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            intro[0] = True
            timer[0] = pygame.time.get_ticks()
            time.sleep(0.1)

    elif pygame.time.get_ticks() - timer[0] < 6000:
        screen.blit(slide1, (0, 0))
    elif pygame.time.get_ticks() - timer[0] < 10000:
        screen.blit(slide2, (0, 0))

    else:
        return True

    
def fifties_outro(screen, title, text, question, question_time, result, ending):
    screen.fill('#000000')

    if not question_time[0]:
        title.draw(screen)
        screen.blit(text, (85, 450))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            question_time[0] = True
            time.sleep(0.1)

    elif result[0] is None:
        drawn = question.draw(screen)
        if drawn:
            if question.check_answer(drawn, screen):
                result[0] = "correct"
            else:
                result[0] = "incorrect"
            result[1] = pygame.time.get_ticks()

    elif pygame.time.get_ticks() - result[1] < 5000:
        screen.fill('#000000')
        if result[0] == "correct":
            question.correct.draw(screen)
        else:
            question.incorrect.draw(screen)

    elif pygame.time.get_ticks() - result[1] < 15000:
        screen.blit(ending, (360, 270))

    else:
        return True


# builds and displays the pause menu
# also returns flags based on what button was clicked (resume, quit, etc)
def pause_menu(screen, player, title, button1, font, button2, button3, button4, button5):
    pygame.draw.rect(screen, '#000000', pygame.Rect(360, 0, 360, 540))
    title.draw(screen)

    if button1 is not None and button1.draw(screen):
        return 1

    text1 = font.render("Volume - "+ str(round(player.volume, 1)* 10), True, "White")
    screen.blit(text1, (386, 250))

    if button2 is not None and button2.draw(screen):
            if not player.volume > 1.0:
                player.volume += 0.1
                pygame.mixer.music.set_volume(player.volume)

    if button3 is not None and button3.draw(screen):
            if not player.volume < 0.1:
                player.volume -= 0.1
                pygame.mixer.music.set_volume(player.volume)
        
    if button4 is not None and button4.draw(screen): # restart game
        return 4
        
    if button5 is not None and button5.draw(screen): # quit game
        return 5


# resets a level by repositioning player, clearing spikes and loading new world data
def level_reset(level, player, spikes):
    player.rect.x, player.rect.y = player.spawn_point
    player.velocity = [0, 0]

    spikes.empty()

    if path.exists(f'Level Data/data_{level}'):
        pickle_in = open(f'Level Data/data_{level}', 'rb')
        data = pickle.load(pickle_in)
    world = World(data)

    return world


if __name__ == "__main__":
    main()