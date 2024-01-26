import pygame
from collections import namedtuple
from random import randint

color = namedtuple("Colours",["r","g","b"])
BACKGROUND = color(r=50, g=50, b=50)
SNAKE = color(r=0, g=255, b=0)
FOOD = color(r=255, g=0, b=50)
TEXT = color(r=200, g=50, b=100)


WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_DIMENSIONS = WINDOW_WIDTH,WINDOW_HEIGHT
SEGMENT_SIZE = 20

KEY_MAP = {
    1073741903: "right",
    1073741904: "left",
    1073741905: "down",
    1073741906: "up"
}

pygame.init()
pygame.display.set_caption("SNAKE GAME")

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_DIMENSIONS)


def check_boundary_collision(snake_pos):
    x,y = snake_pos[0]
    return x in (-20,WINDOW_WIDTH) or y in (20,WINDOW_HEIGHT) or (x,y) in snake_pos[1:]


def check_food_collision(snake_pos, food_pos):
    if snake_pos[0] == food_pos:
        snake_pos.append(snake_pos[-1])
        return True 
    

def draw_obj(snake_pos,food_pos):
    pygame.draw.rect(screen, FOOD, [food_pos, (SEGMENT_SIZE,SEGMENT_SIZE)])

    for x,y in snake_pos:
        pygame.draw.rect(screen, SNAKE,[x, y, SEGMENT_SIZE, SEGMENT_SIZE])


def move_snake(snake_pos, direction):
    x,y = snake_pos[0]

    if direction == 'left':
        head = (x-SEGMENT_SIZE,y)
    elif direction == 'right':
        head = (x+SEGMENT_SIZE,y)
    elif direction == 'up':
        head = (x,y-SEGMENT_SIZE)
    elif direction == 'down':
        head = (x,y+SEGMENT_SIZE)
    
    snake_pos.insert(0,head)
    del snake_pos[-1]
    if snake_pos[0] in snake_pos: return
    


def press_key(event, current_direction):
    key = event.__dict__["key"]
    new_direction = KEY_MAP.get(key)
    all_direction = ("up","down","right","left")
    opposite = ({"up":"down"},{"left":"right"})

    if new_direction in all_direction and {new_direction:current_direction} not in opposite:
        return new_direction

    return current_direction


def new_food_pos(snake_pos):
    while True:
        x = randint(0,39) * SEGMENT_SIZE
        y = randint(2,41) * SEGMENT_SIZE
        food_pos = (x,y)

        if food_pos not in snake_pos:
            return food_pos
        else:
            return new_food_pos(snake_pos)
        

def snake_game():
    
    score = 0
    current_direction = "right"
    snake_pos = [(100,100),(80,100),(60,100)]
    food_pos = new_food_pos(snake_pos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                current_direction = press_key(event,current_direction)
       
        screen.fill(BACKGROUND)
        draw_obj(snake_pos, food_pos)

        font = pygame.font.Font(None,28)
        text = font.render(f"Score: {score}",True, TEXT)
        screen.blit(text,(10,10))

        pygame.display.update()

        move_snake(snake_pos,current_direction)

        if check_boundary_collision(snake_pos): return

        if check_food_collision(snake_pos, food_pos):
            food_pos = new_food_pos(snake_pos)
            score += 1
        clock.tick(10)

snake_game()
