import pygame
from pygame.examples.music_drop_fade import volume
import pickle
import time

from Character import Player
from Enviroment import World
from UI import Button, Title


def main():
    pygame.init()

    screen = pygame.display.set_mode((720, 540))
    dimensions = [screen.get_width(), screen.get_height()]
    frame = pygame.time.Clock()

    # loading images
    main_title_icon = pygame.image.load("Assets/Titles.png")
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
    quit_button_icon = pygame.image.load("Assets/QuitBtn.png")
    quit_button_down_icon = pygame.image.load("Assets/QuitBtnDown.png")
    sub_tog_off = pygame.image.load("Assets/SubtitleTglOff.png")
    sub_tog_off_down = pygame.image.load("Assets/SubtitleTglOffDown.png")
    sub_tog_on = pygame.image.load("Assets/SubtitleTglOn.png")
    sub_tog_on_down = pygame.image.load("Assets/SubtitleTglOnDown.png")

    main_title_icon = pygame.transform.scale(main_title_icon, (500, 250))

    # loading fonts
    pixelType = pygame.font.Font("Fonts/Pixeltype.ttf", 50)


    tile_size = 30
    main_menu = True


    pickle_in = open('Level Data/data_3', 'rb')
    data3 = pickle.load(pickle_in)
    world3 = World(data3, '#2E4D4C')
 

    # creating instances of classes, creates the player, world and it's obstacles
    player1 = Player(pygame.Rect(60, dimensions[1] - 60, 25, 25), '#0A9B9A', 5, False,
                     False, 8, False, 0.53)
    
    spike_group = pygame.sprite.Group()



    world3.build_world(tile_size, spike_group)

    volume_label = pixelType.render("Volume - "+ str(player1.volume), True, "White")
    subtitles_label = pixelType.render("Subtitles", True, "White")

    # more instances of classes, creates the user interface
    play_button = Button(play_button_icon, play_button_down_icon, 150, 100, (dimensions[0] // 2) - 75, 300)
    pause_button = Button(pause_button_icon, pause_button_down_icon, 30, 30, dimensions[0] - 45, 45)
    pause_title_image = Title(pause_title_image, 200, 100, (dimensions[0] // 2) + 25, 25)
    resume_button = Button(resume_button_icon, resume_button_down_icon, 160, 50, (dimensions[0] // 2) + 25, 150)
    volume_up_button = Button(vol_up_button_icon, vol_up_button_down_icon, 25,25, 575, 250)
    volume_down_button = Button(vol_down_button_icon, vol_down_button_down_icon, 25, 25, 610, 250)
    subtitle_toggle_off = Button(sub_tog_off, sub_tog_off_down, 50, 25, 575, 300)
    subtitle_toggle_on = Button(sub_tog_on, sub_tog_on_down, 50, 25, 575, 300)
    quit_button = Button(quit_button_icon, quit_button_down_icon, 100, 50, (dimensions[0] // 2) + 25, 450)

    #main Pygame loop required to keep it running until the player closes the window
    run = True
    delta_time = 0
    while run ==  True:
        start = time.time()
        
        frame.tick(60)
        handle_events(run)

        if main_menu == True: # creates main menu (title, button)
             screen.blit(main_title_icon, ((dimensions[0] // 2) - 250, 25))
             if play_button.draw(screen): #if player clicks 'play':
                  main_menu = False
        else: # once main menu set to false, actual game begins
            player1.update_tile_list(world3.tileList)

            if pause_button.draw(screen):
                player1.is_paused = True

            if not player1.is_paused:
                player1.check_input()
                player1.update()
                draw_everything(screen, world3, player1, spike_group, pause_button)
                
                for spike in spike_group:
                     spike.animate(delta_time)

            elif player1.is_paused:
                if (pause_menu(screen, player1, pause_title_image, resume_button, volume_label, pixelType, volume_up_button,
                        volume_down_button, subtitles_label, subtitle_toggle_on, subtitle_toggle_off, quit_button)) == 6:
                    run = False


            if player1.is_paused and not resume_button.draw:
                pause_button.draw = False
                player1.is_paused = False

            if player1.check_if_dead(540, spike_group):
                death_sfx = pygame.mixer.Sound("Sounds/Death.wav")
                death_sfx.set_volume(player1.volume)
                if player1.volume > 0.04:
                    death_sfx.play()
                player1.rect.x, player1.rect.y = player1.spawnPoint
                player1.velocity = [0, 0]

        
        pygame.display.flip()  # display.flip updates entire screen, display.update updates what's in brackets

        end = time.time()
        delta_time = end - start

    pygame.quit()


def handle_events(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


def draw_everything(screen, world, player, enemies, pause):
    screen.fill('#0A141F')
    world.draw(screen)
    player.draw(screen)
    enemies.draw(screen)
    pause.draw(screen)


def pause_menu(screen, player, title, button1, text1, font, button2, button3, text2, button4, button5, button6):
    pygame.draw.rect(screen, '#000000', pygame.Rect(360, 0, 360, 540))
    title.draw(screen)

    if button1 is not None:
        if button1.draw(screen):
            player.is_paused = False

    text1 = font.render("Volume - "+ str(round(player.volume, 1)* 10), True, "White")
    screen.blit(text1, (386, 250))
    screen.blit(text2, (386, 300))

    if button2 is not None and button2.draw(screen):
            if not player.volume > 1.0:
                player.volume += 0.1
                print (player.volume)

    if button3 is not None and button3.draw(screen):
            if not player.volume < 0.1:
                player.volume -= 0.1
                print (player.volume)

    if button4 is not None and button4.draw(screen):
            if button5.draw(screen):
                return 4
        
    if button5 is not None and button5.draw(screen):
            if button4.draw(screen):  
                return 5
        
    if button6 is not None and button6.draw(screen):
            return 6


if __name__ == "__main__":
    main()