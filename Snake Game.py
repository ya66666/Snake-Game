import pygame, time
import random, math

# Initalize
pygame.init()

# Screen size
SCALE = 2 
SCREEN_WIDTH = 300 * SCALE
SCREEN_HEIGHT = 300 * SCALE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GRID_SIZE = 10 * SCALE

# Color, and font for game text
WHITE = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Matrix of the screen -> map[i][j]
map = [[False for x in range((SCREEN_WIDTH) // GRID_SIZE)] for y in range((SCREEN_HEIGHT) // GRID_SIZE)]

# Title 
pygame.display.set_caption("Snake Game")
snake_icon = pygame.image.load('snake.png')
pygame.display.set_icon(snake_icon)

# Snake
snake = pygame.image.load('Green Dot.png')
snake = pygame.transform.scale(snake, (GRID_SIZE, GRID_SIZE))
snakeX = random.randint(10, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE
snakeY = random.randint(10, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE
snake_moveX = snake_moveY = 0

# Apple
apple = pygame.image.load('Red Dot.png')
apple = pygame.transform.scale(apple, (GRID_SIZE, GRID_SIZE))
appleX = random.randint(0, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE
appleY = random.randint(0, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE

# Snake body Queue
snake_body = [(snakeX, snakeY)]
snake_length = 1
snake_tail = (snakeX, snakeY)

def Intialize():
    global map, snake_body, snake_length, snake_tail, ignore_position, x_or_y
    del map
    map = [[False for x in range((SCREEN_WIDTH) // GRID_SIZE)] for y in range((SCREEN_HEIGHT) // GRID_SIZE)]
    Snake_respawn()
    Spawn_new_apple()
    snake_body = [(snakeX, snakeY)]
    snake_length = 1
    snake_tail = (snakeX, snakeY)
    ignore_position = ""
    x_or_y = True

def Snake_respawn():
    global snakeX, snakeY, snake_moveX, snake_moveY
    snakeX = random.randint(10, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE
    snakeY = random.randint(10, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE
    snake_moveX = snake_moveY = 0

# Update the whole corrdinate of body, add the new snakeX and snakeY, remove the end of the body
def Update_body():
    global snake_body, snake_tail, map
    # Update Snake body Queue
    snake_tail = snake_body.pop(0)
    snake_body.append((snakeX, snakeY))

    # Update map
    map[snakeY // GRID_SIZE][snakeX // GRID_SIZE] = True
    map[snake_tail[1] // GRID_SIZE][snake_tail[0] // GRID_SIZE] = False

# Add the last snake tail to the snake body
def Add_body():
    global snake_body, snake_length
    # Add Snake body Queue
    snake_body.insert(0, snake_tail)
    # Add map
    map[snake_tail[1] // GRID_SIZE][snake_tail[0] // GRID_SIZE] = True

# Eat apple
def Eat_apple( x1, y1, x2, y2 ):
    return x1 == x2 and y1 == y2

# Spawn apple in empty place
def Spawn_new_apple():
    global appleX, appleY
    spawn_in_empty = False
    while not spawn_in_empty:
        if map[appleY // GRID_SIZE][appleX // GRID_SIZE]:
            appleX = random.randint(0, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE
            appleY = random.randint(0, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE
        else:
            spawn_in_empty = True

# Show Snake on the screen
def Snake():
    for i in snake_body:
        screen.blit(snake, i)
    
# Show Apple on the screen
def Apple(x, y):
    screen.blit(apple, (x, y))

def isCollision():
    return map[snakeY // GRID_SIZE][snakeX // GRID_SIZE] 

def Out_of_Bound():
    global snakeX, snakeY, game_over
    return ( snakeX < 0 or snakeX > SCREEN_WIDTH - GRID_SIZE or
        snakeY < 0 or snakeY > SCREEN_HEIGHT - GRID_SIZE )

# Draw game over text
def Draw_game_over():
    game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(game_over_text, text_rect)

def Draw_Win():
    win_text = font.render('You Win! Press SPACE to restart', True, WHITE)
    text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(win_text, text_rect)

# move in x -> true, move in y -> false
x_or_y = True

# The input key that should be ignore, 
# Press a -> ignore "d"
# Press d -> ignore "a"
# Press w -> ignore "s"
# Press s -> ignore "w"
ignore_position = ""

# FPS
TARGET_FPS = 10
clock = pygame.time.Clock()

running = True
game_over = win = False
while running:
    # Control the FPS of the game, TARGET_FPS = 10, 10 frames per second, 1000ms/10 = 100ms per frame
    clock.tick(TARGET_FPS)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if game_over or win:
                if event.key == pygame.K_SPACE:
                    Intialize()
                    game_over = win = False
                    
                continue
            
            if ( (event.key == pygame.K_w or event.key == pygame.K_UP) and ignore_position != "s" ):
                x_or_y = False
                ignore_position = "w"
                snake_moveY = -GRID_SIZE
            elif ( (event.key == pygame.K_s or event.key == pygame.K_DOWN) and ignore_position != "w" ):
                x_or_y = False
                ignore_position = "s"
                snake_moveY = GRID_SIZE
            elif ( (event.key == pygame.K_a or event.key == pygame.K_LEFT) and ignore_position != "d" ):
                x_or_y = True
                ignore_position = "a"
                snake_moveX = -GRID_SIZE
            elif ( (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and ignore_position != "a" ):
                x_or_y = True
                ignore_position = "d"
                snake_moveX = GRID_SIZE
        
    if game_over:
        Draw_game_over()

    elif win:
        Draw_Win()

    else:
        if x_or_y: 
            snake_moveY = 0
        else:
            snake_moveX = 0
            
        if snake_moveX != 0 or snake_moveY != 0:
            snakeX += snake_moveX
            snakeY += snake_moveY
            if Out_of_Bound() or isCollision():
                game_over = True
                continue

            Update_body()
        
        if Eat_apple(snakeX, snakeY, appleX, appleY):
            snake_length += 1
            Add_body()
            if snake_length == (SCREEN_WIDTH // GRID_SIZE) * (SCREEN_HEIGHT // GRID_SIZE):
                win = True
                continue
            else:
                Spawn_new_apple()

        Snake()
        Apple(appleX, appleY)

    pygame.display.update()

pygame.quit()
