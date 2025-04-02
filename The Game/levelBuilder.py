#imports
import pygame   
import pickle

#initialisation
pygame.init()


clock = pygame.time.Clock()
frames = 60

screen = pygame.display.set_mode((720, 540))
pygame.display.set_caption('Level Editor')

white = ('#FFFFFF')
red   = ('#C1121F') 
green = ('#507C58')
blue  = ('#003049')
black = ('#000000')

world = [[0] * 24 for _ in range(18)]

filename = input("Would you like to load a level? ") 

try:
    with open(filename, 'rb') as file:
        world = pickle.load(file)
    
    print("successful load")
except:
    for x in range(len(world[0])):
        for y in range(len(world)):
            if not(x == 0 or x == len(world[0]) - 1 or y == 0 or y == len(world) - 1):
                continue 

        world[y][x] = 1

running = True 
tile_size = 30 

while running:
    screen.fill('#000000')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            break
    
    y = -1
    for row in world:
        y += 1

        x = -1
        for tile in row:
            x += 1
            if tile == 1:
                tile = pygame.Rect((tile_size * x, tile_size * y), (tile_size, tile_size))
                pygame.draw.rect(screen, white, tile)
            elif tile == 2:
                tile = pygame.Rect((tile_size * x, tile_size * y), (tile_size, tile_size))
                pygame.draw.rect(screen, green, tile)
            elif tile == 3:
                tile = pygame.Rect((tile_size * x, tile_size * y), (tile_size, tile_size))
                pygame.draw.rect(screen, red, tile)
            elif tile == 4:
                tile = pygame.Rect((tile_size * x, tile_size * y), (tile_size, tile_size))
                pygame.draw.rect(screen, blue, tile)

    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:
        position = pygame.mouse.get_pos()

        tile_x, tile_y = position[0] // tile_size, position[1] // tile_size
        world[tile_y][tile_x] += 1

        if world[tile_y][tile_x] == 5:
            world[tile_y][tile_x] = 0
    
    if mouse_pressed[2]:
        position = pygame.mouse.get_pos()

        tile_x, tile_y = position[0] // tile_size, position[1] // tile_size
        world[tile_y][tile_x] = 0
        print(world[tile_y][tile_x])


    clock.tick(frames)
    pygame.display.flip() 



save = input("which file would you like to save to? ")
if save == None:
    running = False
else:
    with open(save, "wb") as f:
        pickle.dump(world, f)