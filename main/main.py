import pygame
import numpy

#oy mate, can you pass me the bottle o' water innit?
pygame.init()
pygame.freetype

#miscelanius
GAME_FONT = pygame.freetype.SysFont('Mono', 32)
#pygame.key.set_repeat()
print(pygame.key.get_repeat())

#screen
WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Untitled")

#player
PLAYER_SPEED = WIDTH*1/4
PLAYER_SIZE_X, PLAYER_SIZE_Y = 67, 125
player_x_pos, player_y_pos = (WIDTH/2 - PLAYER_SIZE_X/2), (HEIGHT - PLAYER_SIZE_Y*1.25)
player_color = (255, 255, 255)
player = pygame.Rect((player_x_pos, player_y_pos, PLAYER_SIZE_X, PLAYER_SIZE_Y))
points = 0
is_jumping = False
time_jump = 0

#"lanes"... oh boy.
LANE1_X, LANE2_X, LANE3_X = WIDTH*1/4, WIDTH*2/4, WIDTH*3/4
current_lane = 2
lane1 = pygame.Rect((LANE1_X-15, 0, 30, HEIGHT))
lane2 = pygame.Rect((LANE2_X-15, 0, 30, HEIGHT))
lane3 = pygame.Rect((LANE3_X-15, 0, 30, HEIGHT))
LANES_POS_LIST = [LANE1_X, LANE2_X, LANE3_X]

#moving object (maybe a cyclist)
CYCLIST_SPEED = 10
CYCLIST_SIZE_X, CYCLIST_SIZE_Y = 50, 120
CYCLIST_COLOR = (0, 0, 255)
cyclist_timer = 1
cyclist_changer = False
cyclist = pygame.Rect((numpy.random.choice(LANES_POS_LIST)-CYCLIST_SIZE_X/2, HEIGHT-10, CYCLIST_SIZE_X, CYCLIST_SIZE_Y))

#hard coded FPS so the game runs at the same speed in all machines... unless the machine can't run <GAME_NAME HERE> at 60 fps. In that case, it'll go slower.
FPS = 60

#updates the window
def draw_window():
    global points
    global is_jumping
    global player_color
    global time_jump
    global cyclist_changer
    global cyclist_timer
    #WIN.fill should be the first thing here. ALWAYS. Change it if you wanna know why.
    WIN.fill((0, 0, 0))

    #makes the player jump
    if is_jumping:
        player_color = (255, 0, 255)
        time_jump+= 1
        if time_jump == 1:
            player.x+= 20
            player.y-= 30
        elif time_jump == 45:
            time_jump = 0
            player_color = (255, 255, 255)
            player.x-= 20
            player.y+= 30
            is_jumping = False

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

    pygame.draw.rect(WIN, (125, 125, 125), lane1)
    pygame.draw.rect(WIN, (125, 125, 125), lane2)
    pygame.draw.rect(WIN, (125, 125, 125), lane3)
    pygame.draw.rect(WIN, CYCLIST_COLOR, cyclist)
    pygame.draw.rect(WIN, player_color, player)

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
                    #player.move_ip(-PLAYER_SPEED, 0)
                    if current_lane != 1:
                        player.x -= PLAYER_SPEED
                        current_lane -= 1
                elif event.key == pygame.K_d:
                    #player.move_ip(PLAYER_SPEED, 0)
                    if current_lane != 3:
                        player.x += PLAYER_SPEED
                        current_lane += 1
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
