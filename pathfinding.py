import pygame
import random
import sys
from queue import Queue

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 900, 900
GRID_SIZE = 30
SQUARE_SIZE = WIDTH // GRID_SIZE
KING_POS = (GRID_SIZE // 2, GRID_SIZE // 2)
MINE_COUNT = 100
KING_COLOR = (255, 215, 0)
MINE_COLOR = (0, 0, 0)
INVADE_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (200, 200, 200)
KING_RADIUS = SQUARE_SIZE // 4

# Setup the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper: Kingdoms Invading')

# Game board initialization
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place mines on the board
def place_mines(board, mine_count):
    mines = set()
    while len(mines) < mine_count:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (x, y) != KING_POS:
            mines.add((x, y))
    for mine in mines:
        board[mine[1]][mine[0]] = 'M'


def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)
            if board[y][x] == 'M':
                pygame.draw.circle(screen, MINE_COLOR, rect.center, SQUARE_SIZE // 4)
    pygame.draw.circle(screen, KING_COLOR, 
                       (KING_POS[0] * SQUARE_SIZE + SQUARE_SIZE // 2,
                        KING_POS[1] * SQUARE_SIZE + SQUARE_SIZE // 2),
                       KING_RADIUS)

def is_valid_move(x, y, board):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[y][x] != 'M'

def bfs_path(start, goal, board):
    queue = Queue()
    queue.put((start, []))
    visited = set()
    visited.add(start)

    while not queue.empty():
        (current_x, current_y), path = queue.get()
        if (current_x, current_y) == goal:
            return path
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_x + dx, current_y + dy
            if is_valid_move(new_x, new_y, board) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.put(((new_x, new_y), path + [(new_x, new_y)]))
    return []

# Simulate an invading kingdom
def simulate_kingdom_invasion(start, board):
    path = bfs_path(start, KING_POS, board)
    for pos in path:
        x, y = pos
        pygame.draw.rect(screen, INVADE_COLOR, 
                         (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.display.update()
        pygame.time.delay(50)

# Main Game Loop
def main():
    place_mines(board, MINE_COUNT)
    running = True
    while running:
        draw_board(board)
        
        # Simulate invasions
        simulate_kingdom_invasion((GRID_SIZE // 2, 0), board)  # North
        simulate_kingdom_invasion((GRID_SIZE // 2, GRID_SIZE - 1), board)  # South
        simulate_kingdom_invasion((0, GRID_SIZE // 2), board)  # West
        simulate_kingdom_invasion((GRID_SIZE - 1, GRID_SIZE // 2), board)  # East

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
