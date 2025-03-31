import pygame
from pygame.examples.music_drop_fade import volume

from Character import Player
from Enviroment import World
from UI import Button, Title


def main():
    pygame.init()

    screen = pygame.display.set_mode((720, 540))
    dimensions = [screen.get_width(), screen.get_height()]
    frame = pygame.time.Clock()


    tile_size = 30

    data3 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1],
    ]


    # loading fonts
    pixelType = pygame.font.Font("Fonts\Pixeltype.ttf", 50)

    # loading images
    pause_title_image = pygame.image.load("Assets/PauseTitle.PNG")
    pause_button_icon = pygame.image.load("Assets/PauseBtn.PNG")
    pause_button_down_icon = pygame.image.load("Assets/PauseBtnDown.PNG")
    resume_button_icon = pygame.image.load("Assets/ResumeBtn.png")
    resume_button_down_icon = pygame.image.load("Assets/ResumeBtnDown.png")
    vol_up_button_icon = pygame.image.load("Assets/VolUpBtn.png")
    vol_up_button_down_icon = pygame.image.load("Assets/VolUpBtnDown.png")
    vol_down_button_icon = pygame.image.load("Assets/VolDownBtn.png")
    vol_down_button_down_icon = pygame.image.load("Assets/VolDownBtnDown.png")
    quit_button_icon = pygame.image.load("Assets/QuitBtn.png")
    quit_button_down_icon = pygame.image.load("Assets/QuitBtnDown.png")

    # creating instances of classes, creates the player, world and it's obstacles
    player1 = Player(pygame.Rect(60, dimensions[1] - 60, 25, 25), '#0A9B9A', 5, False,
                     False, 8, False, 1)
    spike_group = pygame.sprite.Group()
    world3 = World(data3, '#2E4D4C')
    world3.build_world(tile_size, spike_group)

    volume_label = pixelType.render("Volume - "+ str(player1.volume), True, "White")
    subtitles_label = pixelType.render("Subtitles", True, "White")

    # more instances of classes, creates the user interface
    pause_button = Button(pause_button_icon, pause_button_down_icon, 30, 30, dimensions[0] - 45, 45)
    pause_title_image = Title(pause_title_image, 200, 100, (dimensions[0] // 2) + 25, 25)
    resume_button = Button(resume_button_icon, resume_button_down_icon, 160, 50, (dimensions[0] // 2) + 25, 150)
    volume_up_button = Button(vol_up_button_icon, vol_up_button_down_icon, 25,25, 575, 250)
    volume_down_button = Button(vol_down_button_icon, vol_down_button_down_icon, 25, 25, 610, 250)
    quit_button = Button(quit_button_icon, quit_button_down_icon, 100, 50, (dimensions[0] // 2) + 25, 450)


    #main Pygame loop required to keep it running until the player closes the window
    while True:
        handle_events()

        player1.update_tile_list(world3.tileList)

        if pause_button.draw(screen):
            player1.is_paused = True

        if not player1.is_paused:
            player1.check_input()
            player1.update()
            draw_everything(screen, world3, player1, spike_group, pause_button)

        elif player1.is_paused:
            print (player1.volume)
            if (pause_menu(screen, player1, pause_title_image, resume_button, volume_label, volume_up_button,
                       volume_down_button, subtitles_label, quit_button)) == 4:
                pygame.quit()


        if player1.is_paused and not resume_button.draw:
            pause_button.draw = False
            player1.is_paused = False

        if player1.check_if_dead(540, spike_group):
            death_sfx = pygame.mixer.Sound("Sounds/Death.wav")
            death_sfx.set_volume(player1.volume)
            death_sfx.play()
            player1.rect.x, player1.rect.y = player1.spawnPoint
            player1.velocity = [0, 0]

        pygame.display.flip()  # display.flip updates entire screen, display.update updates what's in brackets
        frame.tick(60)

    # return newScale


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def draw_everything(screen, world, player, enemies, pause):
    screen.fill('#0A141F')
    world.draw(screen)
    player.draw(screen)
    enemies.draw(screen)
    pause.draw(screen)


def pause_menu(screen, player, title, button1, text1, button2, button3, text2, button4):
    pygame.draw.rect(screen, '#000000', pygame.Rect(360, 0, 360, 540))
    title.draw(screen)

    if button1 is not None:
        if button1.draw(screen):
            player.is_paused = False

    screen.blit(text1, (386, 250))
    screen.blit(text2, (386, 300))

    if button2 is not None:
        if button2.draw(screen):
            player.volume += 0.5

    if button3 is not None:
        if button3.draw(screen):
            player.volume -= 0.5

    if button4 is not None:
        if button4.draw(screen):
            return 4


if __name__ == "__main__":
    main()