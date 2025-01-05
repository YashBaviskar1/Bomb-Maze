import pygame
import sys

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (200, 200, 200)
BALL_COLOR = (255, 0, 0)  
BOMB_COLOR = (0, 0, 0)

CLOCK = pygame.time.Clock()

GRID_SIZE = 10
CELL_WIDTH = SCREEN_WIDTH // GRID_SIZE
CELL_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BALL_RADIUS = CELL_WIDTH // 4  
ball_x = (GRID_SIZE // 2) * CELL_WIDTH + CELL_WIDTH // 2
ball_y = (GRID_SIZE // 2) * CELL_HEIGHT + CELL_HEIGHT // 2

BOMB_RADIUS = CELL_WIDTH // 8 



def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_WIDTH):
        pygame.draw.line(SCREEN, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_HEIGHT):
        pygame.draw.line(SCREEN, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))


def draw_ball(x, y):
    # print(x,y)
    pygame.draw.circle(SCREEN, BALL_COLOR, (x, y), BALL_RADIUS)

def draw_bomb(x, y) :
    pygame.draw.circle(SCREEN, BOMB_COLOR, (x,y), BOMB_RADIUS)


def draw_digits(x,y) : 
    font = pygame.font.Font(None, 36)
    text = font.render("1", True, BLACK)
    text_rect = text.get_rect(center=(x, y)) 
    SCREEN.blit(text, text_rect) 

def on_mouse_click(x,y) : 
    draw_bomb(x,y)
def main():
    global ball_x, ball_y
    bombs = []
    while True:
        SCREEN.fill(WHITE)
        draw_grid()
        draw_ball(ball_x, ball_y)
        draw_bomb(25,125)

        for bomb in bombs :
            draw_bomb(bomb[0], bomb[1])
        draw_digits(24, 175)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    x, y = pygame.mouse.get_pos()
                    bombs.append((x,y))
                    on_mouse_click(x,y)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w] and ball_y > CELL_HEIGHT // 2:
            ball_y -= CELL_HEIGHT  
        if keys[pygame.K_DOWN] and ball_y < SCREEN_HEIGHT - CELL_HEIGHT // 2:
            ball_y += CELL_HEIGHT  
        if keys[pygame.K_LEFT] and ball_x > CELL_WIDTH // 2:
            ball_x -= CELL_WIDTH  
        if keys[pygame.K_RIGHT] and ball_x < SCREEN_WIDTH - CELL_WIDTH // 2:
            ball_x += CELL_WIDTH  

        pygame.display.flip()
        CLOCK.tick(10)  


if __name__ == "__main__":
    main()
