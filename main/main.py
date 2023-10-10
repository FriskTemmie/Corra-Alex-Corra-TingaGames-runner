import pygame
import numpy
import spritesheet


#oy mate, can you pass me the bottle o' water innit?
pygame.init()
pygame.freetype


#miscellaneous 
GAME_FONT = pygame.freetype.SysFont('Mono', 32)
last_update = pygame.time.get_ticks()
BLACK = (0, 0, 0)


#screen
WIDTH, HEIGHT = 1680, 945
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corra, Alex, Corra")


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
player_color = (255, 255, 255)
player = pygame.Rect((PLAYER_INITIAL_X, PLAYER_INITIAL_Y, PLAYER_SIZE_X, PLAYER_SIZE_Y))

is_jumping = False
time_jump = 0


#player sheets
player_sprite_sheet_running = pygame.image.load('sprites/sprite_sheet_base.png').convert_alpha()
player_sprites_running = spritesheet.SpriteSheet(player_sprite_sheet_running)

player_sprite_sheet_right = pygame.image.load('sprites/sprite_sheet_base_diagonal_R.png').convert_alpha()
player_sprites_right = spritesheet.SpriteSheet(player_sprite_sheet_right)

player_sprite_sheet_left = pygame.image.load('sprites/sprite_sheet_base_diagonal_L.png').convert_alpha()
player_sprites_left = spritesheet.SpriteSheet(player_sprite_sheet_left)

player_sprite_sheet_jumping = pygame.image.load('sprites/sprite_sheet_base_jumping.png').convert_alpha()
player_sprites_jumping = spritesheet.SpriteSheet(player_sprite_sheet_jumping)



#player animation
player_animation_running = []
player_animation_right = []
player_animation_left = []
player_animation_jumping = []
PLAYER_ANIMATION_STEPS = 6
PLAYER_ANIMATION_SPEED = 100
player_animation_current_frame = 0
player_current_animation = player_animation_running

for x in range(PLAYER_ANIMATION_STEPS):
    player_animation_running.append(player_sprites_running.get_image(x, 60, 60, 4, BLACK))
    player_animation_right.append(player_sprites_right.get_image(x, 60, 60, 4, BLACK))
    player_animation_left.append(player_sprites_left.get_image(x, 60, 60, 4, BLACK))
    player_animation_jumping.append(player_sprites_jumping.get_image(x, 60, 60, 4, BLACK))


#moving object (maybe a cyclist)
CYCLIST_SPEED = 10
CYCLIST_SIZE_X, CYCLIST_SIZE_Y = 50, 120
CYCLIST_COLOR = (0, 0, 255)
cyclist_timer = 1
cyclist_changer = False
cyclist = pygame.Rect((numpy.random.choice(LANES_POS_LIST)-CYCLIST_SIZE_X/2, HEIGHT-10, CYCLIST_SIZE_X, CYCLIST_SIZE_Y))


#hard coded FPS so the game runs at the same speed in all machines... unless the machine can't run Corra, Alex, Corra at 60 fps. In that case, it'll go slower.
FPS = 60


#updates the window
def draw_window():
    global points
    global is_jumping
    global player_color
    global time_jump
    global cyclist_changer
    global cyclist_timer
    global player_animation_current_frame
    global last_update
    global current_time
    global player_current_animation
    global player_speed

    #WIN.fill should be the first thing here. ALWAYS. Change it if you wanna know why. (afterthought: the global variables may come first)
    WIN.fill(BLACK)

    #temp
    x = 0
    while x < WIDTH:
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect((x, 0, 2, HEIGHT)))
        x += 120

    x = 0
    while x < HEIGHT:
        pygame.draw.rect(WIN, (255, 255, 255), pygame.Rect((0, x, WIDTH, 2)))
        x += 120
        
    
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
        player_color = (255, 0, 255)
        time_jump += 1

        if time_jump == 1:
            player_animation_current_frame = 0
            player_current_animation = player_animation_jumping
        elif time_jump == 36:
            time_jump = 0
            player_color = (255, 255, 255)
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
    pygame.draw.rect(WIN, (125, 125, 125), lane1)
    pygame.draw.rect(WIN, (125, 125, 125), lane2)
    pygame.draw.rect(WIN, (125, 125, 125), lane3)
    pygame.draw.rect(WIN, CYCLIST_COLOR, cyclist)
    pygame.draw.rect(WIN, player_color, player)
    WIN.blit(player_current_animation[player_animation_current_frame], ((player.x - 88), (player.y - 161)))


    #collision
    #collision1 = player.collidepoint(ball.x, ball.y)
    #collision2 = player2.collidepoint(ball.x*2, ball.y)


    #points
    #GAME_FONT.render_to(WIN, (WIDTH/2-25, 50), f'{player_points} | {player2_points}', (255, 255, 255))


    #actually updates the window. HAVE to be the last thing here.
    pygame.display.update()


#standart main function
def main():
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

            if event.type == pygame.KEYDOWN:
                #moves the player1
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
        
        draw_window()


    #actually quits the screen
    pygame.quit()


if __name__ == "__main__":
    main()
