import pygame
import sys
import random

pygame.init()
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
GRID_SIZE = 20 
CELL_WIDTH = (SCREEN_WIDTH) // GRID_SIZE 
CELL_HEIGHT = (SCREEN_HEIGHT)// GRID_SIZE 

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Path Finding Game")



INVADE_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_COLOR = (200, 200, 200)
BALL_COLOR = (255, 0, 0)
BOMB_COLOR = (0, 0, 0)
TEXT_COLOR = (0, 0, 255)

BALL_RADIUS = CELL_WIDTH // 4
ball_x = GRID_SIZE // 2
ball_y = GRID_SIZE // 2

BOMBS = set()
while len(BOMBS) < 50: 
    bomb_x = random.randint(0, GRID_SIZE - 1)
    bomb_y = random.randint(0, GRID_SIZE - 1)
    if (bomb_x, bomb_y) != (GRID_SIZE // 2, GRID_SIZE // 2):  
        BOMBS.add((bomb_x, bomb_y))

bomb_counts = [[0 for _ in range(GRID_SIZE )] for _ in range(GRID_SIZE)]


king_image = pygame.image.load('assets/king.png')
king_image = pygame.transform.scale(king_image, (CELL_WIDTH, CELL_HEIGHT))
tileset_field = pygame.image.load('assets\TileUnknown.png')
tileset_field = pygame.transform.scale(tileset_field, (SCREEN_WIDTH , SCREEN_HEIGHT ))
def calculate_bomb_counts():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (col, row) in BOMBS:
                bomb_counts[row][col] = -1  
            else:
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = col + dx, row + dy
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                            if (nx, ny) in BOMBS:
                                count += 1
                bomb_counts[row][col] = count

calculate_bomb_counts()


CLOCK = pygame.time.Clock()

# def draw_grid():
#     """Draw the grid on the screen."""
#     for x in range(0, SCREEN_WIDTH, CELL_WIDTH):
#         pygame.draw.line(SCREEN, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
#     for y in range(0, SCREEN_HEIGHT, CELL_HEIGHT):
#         pygame.draw.line(SCREEN, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_bombs():
    section_height = 50
    for bomb in BOMBS:
        x = bomb[0] * CELL_WIDTH + CELL_WIDTH // 2
        y = bomb[1] * CELL_HEIGHT + CELL_HEIGHT // 2 + section_height - CELL_HEIGHT
        if y >= section_height:
            pygame.draw.circle(SCREEN, BOMB_COLOR, (x, y), BALL_RADIUS // 2)


def draw_numbers():
    font = pygame.font.Font(None, 36)
    section_height = 50
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if (col, row) not in BOMBS and bomb_counts[row][col] > 0:
                text_surface = font.render(str(bomb_counts[row][col]), True, TEXT_COLOR)

                x = col * CELL_WIDTH + CELL_WIDTH // 2
                y = (row * CELL_HEIGHT) + CELL_HEIGHT // 2 + section_height - CELL_HEIGHT

                if y >= section_height:
                    text_rect = text_surface.get_rect(center=(x, y))
                    SCREEN.blit(text_surface, text_rect)

def draw_king():
    center_x = (GRID_SIZE // 2) * CELL_WIDTH
    center_y = (GRID_SIZE // 2) * CELL_HEIGHT
    SCREEN.blit(king_image, (center_x, center_y))

def show_message(text):
    font = pygame.font.Font(None, 48)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Load Sprites
sprite_sheet = pygame.image.load('assets/spy/SpriteSheet.png')
dead_sprite = pygame.image.load('assets/spy/Dead.png')

# Resize sprites
sprite_size = (CELL_WIDTH, CELL_HEIGHT)
dead_sprite = pygame.transform.scale(dead_sprite, sprite_size)

def load_sprite_frames(sheet, rows, cols):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // cols
    frame_height = sheet_height // rows
    for row in range(rows):
        for col in range(cols):
            frame = sheet.subsurface(pygame.Rect(
                col * frame_width, row * frame_height, frame_width, frame_height
            ))
            frame = pygame.transform.scale(frame, sprite_size)
            frames.append(frame)
    return frames

sprite_frames = load_sprite_frames(sprite_sheet, 7, 4)
current_frame = 0

DIRECTION_FRAMES = {
    "LEFT": [2, 6, 10, 14 ],       
    "UP": [1, 5, 13, 9],     
    "DOWN": [0, 4, 12, 4],   
    "RIGHT": [3, 7, 15, 11] 
}
current_direction = "UP"  
frame_index = 0 

def update_movement(keys):
    global ball_x, ball_y, current_direction, frame_index

    moved = False
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if ball_y > 0:
            ball_y -= 1
            current_direction = "UP"
            moved = True
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if ball_y < GRID_SIZE - 1:
            ball_y += 1
            current_direction = "DOWN"
            moved = True
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if ball_x > 0:
            ball_x -= 1
            current_direction = "LEFT"
            moved = True
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if ball_x < GRID_SIZE - 1:
            ball_x += 1
            current_direction = "RIGHT"
            moved = True

    # Update frame index only when moving
    if moved:
        frame_index = (frame_index + 1) % len(DIRECTION_FRAMES[current_direction])

# Update draw_character to use the correct frame based on direction
def draw_character(col, row):
    global frame_index, current_direction
    x = col * CELL_WIDTH 
    y = row * CELL_HEIGHT
    current_frame = DIRECTION_FRAMES[current_direction][frame_index]
    SCREEN.blit(sprite_frames[current_frame], (x, y))

# Show dead character
def show_dead_character(col, row):
    x = col * CELL_WIDTH
    y = row * CELL_HEIGHT
    SCREEN.blit(dead_sprite, (x, y))
# Add a global or class-level variable to track the button state
eye_button_activated = False
comp_button_activated = False
def draw_reserved_section():
    section_height = 50
    button_width, button_height = 60, 30
    button_gap = 10  # Gap between buttons

    # Button positions
    eye_button_x = SCREEN_WIDTH - (button_width * 2) - button_gap  # Position for "Eye" button
    comp_button_x = SCREEN_WIDTH - button_width - button_gap  # Position for "Comp" button
    button_y = (section_height - button_height) // 2  # Centered vertically

    # Draw reserved section background
    pygame.draw.rect(SCREEN, GRID_COLOR, (0, 0, SCREEN_WIDTH, section_height))

    # Draw "Eye" button
    eye_button_color = (100, 255, 100) if eye_button_activated else (200, 200, 200)
    pygame.draw.rect(SCREEN, eye_button_color, (eye_button_x, button_y, button_width, button_height))
    eye_image = pygame.image.load('assets/eye.png')  
    eye_image = pygame.transform.scale(eye_image, (button_width, button_height))
    SCREEN.blit(eye_image, (eye_button_x, button_y))  # Draw the eye image on the button

    # Draw "Comp" button
    comp_button_color = (100, 255, 100) if comp_button_activated else (200, 200, 200)
    pygame.draw.rect(SCREEN, comp_button_color, (comp_button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 24)
    comp_text_surface = font.render("Comp", True, (0, 0, 0))  # Black text
    comp_text_rect = comp_text_surface.get_rect(center=(comp_button_x + button_width // 2, button_y + button_height // 2))
    SCREEN.blit(comp_text_surface, comp_text_rect)  # Draw "Comp" text

    # Draw the number in the center of the reserved section
    font = pygame.font.Font(None, 36)
    number = bomb_counts[ball_y][ball_x]
    text_surface = font.render(str(number), True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, section_height // 2))
    SCREEN.blit(text_surface, text_rect)


    eye_button_rect = pygame.Rect(eye_button_x, button_y, button_width, button_height)
    comp_button_rect = pygame.Rect(comp_button_x, button_y, button_width, button_height)

    return eye_button_rect, comp_button_rect


import heapq

# Constants
WALL = -1 
EMPTY = 0  
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_neighbors(x, y):
    """Get neighboring cells (up, down, left, right)."""
    neighbors = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors


def astar(start, goal, grid):
    open_list = []
    closed_list = set()
    came_from = {}


    g_cost = {start: 0}  
    f_cost = {start: heuristic(start, goal)} 

    heapq.heappush(open_list, (f_cost[start], start))  

    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        closed_list.add(current)

        for neighbor in get_neighbors(*current):
            if neighbor in closed_list or grid[neighbor[1]][neighbor[0]] == WALL:
                continue
            
            tentative_g_cost = g_cost[current] + 1  

            if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = tentative_g_cost
                f_cost[neighbor] = tentative_g_cost + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_cost[neighbor], neighbor))

    return []  
def heuristic(a, b):
    """Heuristic function: Manhattan distance."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def update_movement_with_pathfinding():
    global ball_x, ball_y

    target_x, target_y = GRID_SIZE - 1, GRID_SIZE - 1  

    grid = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for bomb in BOMBS:
        grid[bomb[1]][bomb[0]] = WALL  


    path = astar((ball_x, ball_y), (target_x, target_y), grid)

    if path:

        next_x, next_y = path[0]
        ball_x, ball_y = next_x, next_y  







def win():

    font = pygame.font.Font(None, 48)
    text_surface = font.render("You Won!", True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000) 
    pygame.quit()
    sys.exit()


def is_valid_move(x, y, board):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and board[y][x] != 'M'
from queue import Queue
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


def simulate_kingdom_invasion(start, goal, board):
    path = bfs_path(start, goal, board)
    for pos in path:
        x, y = pos
        pygame.draw.rect(SCREEN, INVADE_COLOR, 
                         (x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        pygame.display.update()
        pygame.time.delay(50)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_WIDTH):
        pygame.draw.line(SCREEN, GRID_COLOR, (x, 50), (x, SCREEN_HEIGHT)) 
    for y in range(50, SCREEN_HEIGHT, CELL_HEIGHT): 
        pygame.draw.line(SCREEN, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
def draw_stuff():
    draw_bombs()
    draw_numbers()
def simulate_invasion() :
        simulate_kingdom_invasion((GRID_SIZE // 2, 0), (GRID_SIZE // 2, GRID_SIZE - 1), bomb_counts)  
        simulate_kingdom_invasion((GRID_SIZE // 2, GRID_SIZE - 1), (GRID_SIZE // 2, 0), bomb_counts) 
        simulate_kingdom_invasion((0, GRID_SIZE // 2), (GRID_SIZE - 1, GRID_SIZE // 2), bomb_counts) 
        simulate_kingdom_invasion((GRID_SIZE - 1, GRID_SIZE // 2), (0, GRID_SIZE // 2), bomb_counts) 
def main():
    global ball_x, ball_y, current_frame, eye_button_activated, comp_button_activated

    while True:

        SCREEN.fill(WHITE)  
        draw_reserved_section() 
        SCREEN.blit(tileset_field, (0, 50))  
        draw_grid()
        draw_king()
        if ball_x == 0 or ball_x == GRID_SIZE -1 or ball_y == GRID_SIZE - 1 or ball_y == 0:
            win()
        if (ball_x, ball_y) in BOMBS:
            show_dead_character(ball_x, ball_y) 
            show_message("BOMB! GAME OVER!")
            pygame.quit()
            sys.exit()
        else:
            draw_character(ball_x, ball_y)  
       # draw_numbers()
        
        eye_button_rect, comp_button_rect = draw_reserved_section() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                if eye_button_rect.collidepoint(event.pos): 
                    eye_button_activated = not eye_button_activated
                    print("Eye button clicked")
                elif comp_button_rect.collidepoint(event.pos):  
                    comp_button_activated = not comp_button_activated
                    print("Comp button clicked")
        if eye_button_activated :
            draw_stuff()
        if comp_button_activated :
            #simulate_invasion()
            update_movement_with_pathfinding() 
        keys = pygame.key.get_pressed()
        update_movement(keys)

        pygame.display.flip()
        CLOCK.tick(10)




if __name__ == "__main__":
    main()
