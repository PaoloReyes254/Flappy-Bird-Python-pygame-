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

def display_score(game_active):
    if game_active:
        score_surface = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (width/2, 75))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (width/2, 75))
        screen.blit(score_surface, score_rect)

        high_score_surface = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (width/2, 625))
        screen.blit(high_score_surface, high_score_rect)

def add_score(pipes, score):
    if len(pipes) > 0:
        pipe = pipes[0]
        if pipe[0] == 73:
            score += 1
            score_sound.play()
    return score

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
score = 0
high_score = 0
sound_count = 0
death_count = 0

#Creation of surfaces
#Background surface
bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (width, height))

#Floor surface
floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface, (width, 168))
floor_x_position = 0

#Bird surface
bird_downflap = pygame.transform.scale(pygame.image.load("assets/bluebird-downflap.png").convert_alpha(), (51, 36))
bird_midflap = pygame.transform.scale(pygame.image.load("assets/bluebird-midflap.png").convert_alpha(), (51, 36))
bird_upflap = pygame.transform.scale(pygame.image.load("assets/bluebird-upflap.png").convert_alpha(), (51, 36))
bird_list = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 1
bird_surface = bird_list[1]
bird_rect = bird_surface.get_rect(center = (75, height/2)) 
FLAPEVENT = pygame.USEREVENT + 1 
pygame.time.set_timer(FLAPEVENT, 200)

#Pipe surface
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface, (78, 480))
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_list = []
pipe_height = [500, 400, 300]

#Text surface
score_font = pygame.font.Font("04B_19.ttf", 40)

#Game over surface
game_over_surface = pygame.transform.scale(pygame.image.load("assets/message.png").convert_alpha(), (276, 400))
game_over_rect = game_over_surface.get_rect(center = (width/2, height/2 - 30))

#Sounds
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")

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
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                if sound_count == 0:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.centery = height/2
                    bird_movement = -9
                    bird_index = 1
                    score = 0
                    flap_sound.play()
                    sound_count = 1
                else:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.centery = height/2
                    bird_movement = -9
                    bird_index = 1
                    score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == FLAPEVENT:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface = bird_list[bird_index]
            bird_rect = bird_surface.get_rect(center = (75, bird_rect.centery))

    #Background 
    screen.blit(bg_surface, (0, 0))
    
    if game_active:
        death_count = 0
        #Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        bird_rotated = rotate_bird(bird_surface)
        screen.blit(bird_rotated, bird_rect)
        game_active = check_collisions(pipe_list)

        #Pipes
        draw_pipes(pipe_list)
        pipe_list = move_pipes(pipe_list)

        #Text displaying
        score = add_score(pipe_list, score)
        display_score(game_active)

        if score >= 50:
            bird_downflap = pygame.transform.scale(pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(), (51, 36))
            bird_midflap = pygame.transform.scale(pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(), (51, 36))
            bird_upflap = pygame.transform.scale(pygame.image.load("assets/yellowbird-upflap.png").convert_alpha(), (51, 36)) 
            bird_list = [bird_downflap, bird_midflap, bird_upflap]
            pipe_surface = pygame.transform.scale(pygame.image.load("assets/pipe-red.png").convert(), (78, 480))
            bg_surface = pygame.transform.scale(pygame.image.load("assets/background-night.png").convert(), (width, height))
        else:
            bird_downflap = pygame.transform.scale(pygame.image.load("assets/bluebird-downflap.png").convert_alpha(), (51, 36))
            bird_midflap = pygame.transform.scale(pygame.image.load("assets/bluebird-midflap.png").convert_alpha(), (51, 36))
            bird_upflap = pygame.transform.scale(pygame.image.load("assets/bluebird-upflap.png").convert_alpha(), (51, 36))
            bird_list = [bird_downflap, bird_midflap, bird_upflap]
            pipe_surface = pygame.transform.scale(pygame.image.load("assets/pipe-green.png").convert(), (78, 480))
            bg_surface = pygame.transform.scale(pygame.image.load("assets/background-day.png").convert(), (width, height))
            
    else:
        if death_count == 0:
            death_sound.play()
            death_count = 1
        sound_count = 0
        if score > high_score:
            high_score = score
        display_score(game_active)
        screen.blit(game_over_surface, game_over_rect)

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