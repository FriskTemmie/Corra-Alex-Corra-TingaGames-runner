#python modules
import pygame, numpy, sys
#classes
import spritesheet, button


#oy mate, can you pass me the bottle o' water innit?
pygame.init()
pygame.freetype


#screen
WIDTH, HEIGHT = 1680, 945
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("Corra, Alex, Corra")


#miscellaneous 
GAME_FONT = pygame.freetype.SysFont('Mono', 32)
last_update = pygame.time.get_ticks()
BLACK = (0, 0, 0)
EMPTY = (0,0,0,0)
background_image_temp = spritesheet.SpriteSheet(pygame.image.load('sprites/background/placeholder.png').convert_alpha())
BACKGROUND = background_image_temp.get_image(0, 420, 240, 4, BLACK)


#"lanes"... oh boy.
LANE1_X, LANE2_X, LANE3_X = WIDTH*1/4, WIDTH*2/4, WIDTH*3/4
current_lane = 2
lane1 = pygame.Rect((LANE1_X-15, 0, 30, HEIGHT))
lane2 = pygame.Rect((LANE2_X-15, 0, 30, HEIGHT))
lane3 = pygame.Rect((LANE3_X-15, 0, 30, HEIGHT))
LANES_POS_LIST = [LANE1_X, LANE2_X, LANE3_X]


#player
PLAYER_INITIAL_SPEED = WIDTH*1/96
player_speed = 0
PLAYER_SIZE_X, PLAYER_SIZE_Y = 67, 50
PLAYER_SIZE_X_HALF = PLAYER_SIZE_X/2

PLAYER_INITIAL_X, PLAYER_INITIAL_Y = (LANE2_X - PLAYER_SIZE_X_HALF), (HEIGHT - PLAYER_SIZE_Y*1.25)
player = pygame.Rect((PLAYER_INITIAL_X, PLAYER_INITIAL_Y, PLAYER_SIZE_X, PLAYER_SIZE_Y))

is_jumping = False
time_jump = 0

is_player_selected = False


#player sheets
base_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base.png').convert_alpha())
base_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base_diagonal_R.png').convert_alpha())
base_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base_diagonal_L.png').convert_alpha())
base_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/base/sprite_sheet_base_jumping.png').convert_alpha())

temp_undertale_ref = button.Button(WIDTH/2-289, HEIGHT/2-76, (pygame.image.load('sprites/player/Fem/AMOTHERFUCKERUNDERTALEREFERENCE.png').convert_alpha()), 1)
#F_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F.png').convert_alpha())
#F_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F_diagonal_R.png').convert_alpha())
#F_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F_diagonal_L.png').convert_alpha())
#F_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Fem/sprite_sheet_alex_F_jumping.png').convert_alpha())

M_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_Alex_M.png').convert_alpha())
M_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_alex_M_diagonal_R.png').convert_alpha())
M_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_alex_M_diagonal_L.png').convert_alpha())
M_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/Masc/sprite_sheet_alex_M_jumping.png').convert_alpha())

NB_player_sprites_running = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB.png').convert_alpha())
NB_player_sprites_right = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB_diagonal_R.png').convert_alpha())
NB_player_sprites_left = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB_diagonal_L.png').convert_alpha())
NB_player_sprites_jumping = spritesheet.SpriteSheet(pygame.image.load('sprites/player/NB/sprite_sheet_alex_NB_jumping.png').convert_alpha())



#player animation
player_animation_running = []
player_animation_right = []
player_animation_left = []
player_animation_jumping = []
PLAYER_ANIMATION_STEPS = 6
PLAYER_ANIMATION_SPEED = 100
player_animation_current_frame = 0
player_current_animation = player_animation_running


#moving object (maybe a cyclist)
CYCLIST_SPEED = 10
CYCLIST_SIZE_X, CYCLIST_SIZE_Y = 50, 120
CYCLIST_COLOR = (0, 0, 255)
cyclist_timer = 1
cyclist_changer = False
cyclist = pygame.Rect((numpy.random.choice(LANES_POS_LIST)-CYCLIST_SIZE_X/2, HEIGHT-10, CYCLIST_SIZE_X, CYCLIST_SIZE_Y))


#buttons
button_start = button.Button(WIDTH/2-82, HEIGHT/2+200, (pygame.image.load('sprites/buttons/button_resume.png').convert_alpha()), 1)

button_F = button.Button(WIDTH/2-608, HEIGHT/2-82, (pygame.image.load('sprites/buttons/button_F.png').convert_alpha()), 1)
ela = button.Button(WIDTH/2-608, HEIGHT/2-226, (pygame.image.load('sprites/buttons/ela.png').convert_alpha()), 1)

button_M = button.Button(WIDTH/2-203, HEIGHT/2-82, (pygame.image.load('sprites/buttons/button_M.png').convert_alpha()), 1)
ele = button.Button(WIDTH/2-203, HEIGHT/2-226, (pygame.image.load('sprites/buttons/ele.png').convert_alpha()), 1)

button_NB = button.Button(WIDTH/2+202, HEIGHT/2-82, (pygame.image.load('sprites/buttons/button_NB.png').convert_alpha()), 1)
elu = button.Button(WIDTH/2+202, HEIGHT/2-226, (pygame.image.load('sprites/buttons/elu.png').convert_alpha()), 1)


#hard coded FPS so the game runs at the same speed in all machines... unless the machine can't run Corra, Alex, Corra at 60 fps. In that case, it'll go slower.
FPS = 60

def death():
    global last_update
    global current_lane
    global is_jumping
    global time_jump
    global player_animation_running
    global player_animation_right
    global player_animation_left
    global player_animation_jumping
    global player_animation_current_frame
    global player_speed
    global is_player_selected
    global player
    global cyclist_timer
    global cyclist_changer
    global cyclist

    WIN.fill(BLACK)

    last_update = pygame.time.get_ticks()
    current_lane = 2
    is_jumping = False
    time_jump = 0
    player_speed = 0
    is_player_selected = False
    player_animation_running = []
    player_animation_right = []
    player_animation_left = []
    player_animation_jumping = []
    player_animation_current_frame = 0
    player = pygame.Rect((PLAYER_INITIAL_X, PLAYER_INITIAL_Y, PLAYER_SIZE_X, PLAYER_SIZE_Y))
    cyclist_timer = 1
    cyclist_changer = False
    cyclist = pygame.Rect((numpy.random.choice(LANES_POS_LIST)-CYCLIST_SIZE_X/2, HEIGHT-10, CYCLIST_SIZE_X, CYCLIST_SIZE_Y))

    main_menu()


def main_menu():
    global player_animation_running
    global player_animation_right
    global player_animation_left
    global player_animation_jumping
    global is_player_selected

    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()


    run = True
    while run:
        clock.tick(FPS)
        
        WIN.fill(BLACK)
        surface.fill(EMPTY)

        if is_player_selected:
            button_start.draw(surface)
        else:
            ela.draw(surface)
            button_F.draw(surface)
            ele.draw(surface)
            button_M.draw(surface)
            elu.draw(surface)
            button_NB.draw(surface)
        
        if button_F.clicked:
            pass
            #for x in range(PLAYER_ANIMATION_STEPS):
                #player_animation_running.append(F_player_sprites_running.get_image(x, 60, 60, 4, BLACK))
                #player_animation_right.append(F_player_sprites_right.get_image(x, 60, 60, 4, BLACK))
                #player_animation_left.append(F_player_sprites_left.get_image(x, 60, 60, 4, BLACK))
                #player_animation_jumping.append(F_player_sprites_jumping.get_image(x, 60, 60, 4, BLACK))

            #is_player_selected = True
        elif button_M.clicked:
            for x in range(PLAYER_ANIMATION_STEPS):
                player_animation_running.append(M_player_sprites_running.get_image(x, 60, 60, 4, BLACK))
                player_animation_right.append(M_player_sprites_right.get_image(x, 60, 60, 4, BLACK))
                player_animation_left.append(M_player_sprites_left.get_image(x, 60, 60, 4, BLACK))
                player_animation_jumping.append(M_player_sprites_jumping.get_image(x, 60, 60, 4, BLACK))

            is_player_selected = True
            game_main()
        elif button_NB.clicked:
            for x in range(PLAYER_ANIMATION_STEPS):
                player_animation_running.append(NB_player_sprites_running.get_image(x, 60, 60, 4, BLACK))
                player_animation_right.append(NB_player_sprites_right.get_image(x, 60, 60, 4, BLACK))
                player_animation_left.append(NB_player_sprites_left.get_image(x, 60, 60, 4, BLACK))
                player_animation_jumping.append(NB_player_sprites_jumping.get_image(x, 60, 60, 4, BLACK))
            
            is_player_selected = True
            game_main()


        #runs through all pygame events
        for event in pygame.event.get():
            #checks if the screen should be closed
            if event.type == pygame.QUIT:
                #stops the while
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                pass


        #actually updates the window. HAVE to be the last thing here.\
        WIN.blit(surface, (0, 0))
        pygame.display.update()
                    

def pause():
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()


    run = True
    while run:
        clock.tick(FPS)

        surface.fill(EMPTY)
        button_start.draw(surface)
        
        if button_start.clicked:
            game_main()


        #runs through all pygame events
        for event in pygame.event.get():
            #checks if the screen should be closed
            if event.type == pygame.QUIT:
                #stops the while
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                #starts the game
                if event.key == pygame.K_ESCAPE:
                    surface.fill(EMPTY)
                    game_main()


        #actually updates the window. HAVE to be the last thing here.\
        WIN.blit(surface, (0, 0))
        pygame.display.update()


#updates the window
def game_draw_window():
    global points
    global is_jumping
    global time_jump
    global cyclist_changer
    global cyclist_timer
    global player_animation_current_frame
    global last_update
    global current_time
    global player_current_animation
    global player_speed

    #makes the mouse invisible.
    pygame.mouse.set_visible(False)


    #WIN.fill should be the first thing here. ALWAYS. Change it if you wanna know why. (afterthought: the global variables may come first)
    WIN.fill(BLACK)
    
    
    #moves the player from one "lane" to another
    player.x += player_speed
    if player.x >= LANE1_X - PLAYER_SIZE_X_HALF and player.x <= LANE1_X - PLAYER_SIZE_X_HALF + PLAYER_INITIAL_SPEED:
        player_speed = 0
        player.x = LANE1_X - PLAYER_SIZE_X_HALF
    elif player.x >= LANE2_X - PLAYER_SIZE_X_HALF and player.x <= LANE2_X - PLAYER_SIZE_X_HALF + PLAYER_INITIAL_SPEED - 5:
        player_speed = 0
        player.x = LANE2_X - PLAYER_SIZE_X_HALF
    elif player.x >= LANE3_X - PLAYER_SIZE_X_HALF and player.x <= LANE3_X - PLAYER_SIZE_X_HALF + PLAYER_INITIAL_SPEED:
        player_speed = 0
        player.x = LANE3_X - PLAYER_SIZE_X_HALF


    #makes the player jump
    if is_jumping:
    
        time_jump += 1

        if time_jump == 1:
            player_animation_current_frame = 0
            player_current_animation = player_animation_jumping
        elif time_jump == 36:
            time_jump = 0
            is_jumping = False
            player_animation_current_frame = 0
            player_current_animation = player_animation_running


    #moves the cyclist
    if cyclist.y >= HEIGHT:
        cyclist_changer = True

    if cyclist_changer == True:
        if cyclist_timer == 0:
            cyclist_timer = numpy.random.randint(70)
            cyclist.x = numpy.random.choice(LANES_POS_LIST)-CYCLIST_SIZE_X/2
            cyclist.y = -CYCLIST_SIZE_Y
            cyclist_changer = False
        else:
            cyclist_timer -= 1
        
    cyclist.y += CYCLIST_SPEED


    #updates player animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= PLAYER_ANIMATION_SPEED:
        if player_animation_current_frame < PLAYER_ANIMATION_STEPS-1:
            player_animation_current_frame += 1
        else:
            player_animation_current_frame = 0
            if player_current_animation == player_animation_right or player_animation_left:
                player_current_animation = player_animation_running
        
        last_update = current_time


    #draw the stuff on the screen
    WIN.blit(BACKGROUND, (0, 0))
    #pygame.draw.rect(WIN, (125, 125, 125), lane1)
    #pygame.draw.rect(WIN, (125, 125, 125), lane2)
    #pygame.draw.rect(WIN, (125, 125, 125), lane3)
    pygame.draw.rect(WIN, CYCLIST_COLOR, cyclist)
    pygame.draw.rect(surface, (100, 100, 100, 0), player)
    WIN.blit(player_current_animation[player_animation_current_frame], ((player.x - 88), (player.y - 161)))


    #collisions
    if pygame.Rect.colliderect(player, cyclist) and not is_jumping:
        death()


    #points
    #GAME_FONT.render_to(WIN, (WIDTH/2-25, 50), f'{player_points} | {player2_points}', (255, 255, 255))


    #actually updates the window. HAVE to be the last thing here.
    pygame.display.update()


#the actual game
def game_main():
    global current_lane
    global is_jumping
    global player_current_animation
    global player_animation_current_frame
    global player_speed

    clock = pygame.time.Clock()


    run = True
    while run:
        clock.tick(FPS)
        
        #runs through all pygame events
        for event in pygame.event.get():
            #checks if the screen should be closed
            if event.type == pygame.QUIT:
                #stops the while
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                #moves the player
                if event.key == pygame.K_a:
                    #player.move_ip(-player_speed, 0)
                    if current_lane != 1 and player_speed == 0:
                        player_speed = PLAYER_INITIAL_SPEED * -1
                        current_lane -= 1
                    
                    if is_jumping == False:
                        player_animation_current_frame = 0
                        player_current_animation = player_animation_left
                elif event.key == pygame.K_d:
                    #player.move_ip(player_speed, 0)
                    if current_lane != 3 and player_speed == 0:
                        player_speed = PLAYER_INITIAL_SPEED
                        current_lane += 1

                    if is_jumping == False:
                        player_animation_current_frame = 0
                        player_current_animation = player_animation_right

                if event.key == pygame.K_SPACE:
                    if is_jumping == False:
                        print("Not jumping")
                        is_jumping = True
                    else:
                        print("Already jumping")

                if event.key == pygame.K_ESCAPE:
                    pygame.draw.rect(surface, (100, 100, 100, 100), [0, 0, WIDTH, HEIGHT])
                    WIN.blit(surface, (0, 0))
                    pause()
        
        game_draw_window()


if __name__ == "__main__":
    main_menu()
