import pygame, random

#Functions
def create_pipe():
    random_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (width + 100, random_height))
    top_pipe = pipe_surface.get_rect(midbottom = (width + 100, random_height-225))
    return bottom_pipe, top_pipe

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > 700:
            screen.blit(pipe_surface, pipe)
        else:
            flip_surface = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_surface, pipe)

def move_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx < -100:
            pipes.pop(0)
        else:
            pipe.centerx -= 5
    return pipes

def check_collisions(pipes):
    count = 0
    for pipe in pipes:
        if bird_rect.colliderect(pipe) and count == 0:
            return False
            count = 1
        else:
            count = 0
    if bird_rect.centery <= 18:
        bird_rect.centery = 18
        return True
    elif bird_rect.centery >= 675 - 18:
        bird_rect.centery = 675 - 18
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

#Screen Sizes
width = 432
height = 768

#Pygame init
pygame.init()

#Creation of title, screen and fps
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

#Game Variables
gravity = 0.25
bird_movement = 0
game_active = True

#Creation of surfaces
#Background surface
bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (width, height))

#Floor surface
floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface, (width, 168))
floor_x_position = 0

#Bird surface
bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (51, 36))
bird_rect = bird_surface.get_rect(center = (75, height/2))

#Pipe surface
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface, (78, 480))
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_list = []
pipe_height = [500, 400, 300]

#Loop
run = True
while run:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 9
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.centery = height/2
                bird_movement = -9
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            print(pipe_list)
    
    #Background 
    screen.blit(bg_surface, (0, 0))
    
    if game_active:
        #Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        bird_rotated = rotate_bird(bird_surface)
        screen.blit(bird_rotated, bird_rect)
        game_active = check_collisions(pipe_list)

        #Pipes
        draw_pipes(pipe_list)
        pipe_list = move_pipes(pipe_list)

    #Floor
    screen.blit(floor_surface, (floor_x_position, 675))
    screen.blit(floor_surface, (floor_x_position + 432, 675))
    floor_x_position -= 1
    if floor_x_position <= -432:
        floor_x_position = 0

    #Update and fps
    pygame.display.update()
    clock.tick(120)

#Pygame quit
pygame.quit()