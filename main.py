import pygame
import numpy as np

# --- SETTINGS ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 60
COLS = 80
CELL_SIZE = SCREEN_WIDTH // COLS
STATUS_BAR_HEIGHT = 40
TITLE_Y = 100
CONTROLS_Y_START = 250
CONTROL_SPACING = 40
PROMPT_Y = 520
MENU_BG = (10, 10, 10)
FPS_MENU = 30
FPS_GAME = 10

# --- COLORS ---
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (255, 255, 255)
STATUS_BG = (20, 20, 20)
HIGHLIGHT = (100, 200, 100)
PAUSED_COLOR = (200, 50, 50)
RUNNING_COLOR = (50, 200, 50)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

grid = np.zeros((ROWS, COLS), dtype=int)
paused = True
generation = 0
in_menu = True

def draw_grid(surface, grid):
    surface.fill(DEAD_COLOR)
    for r in range(ROWS):
        for c in range(COLS):
            color = ALIVE_COLOR if grid[r, c] == 1 else DEAD_COLOR
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE + STATUS_BAR_HEIGHT, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, STATUS_BAR_HEIGHT), (x, SCREEN_HEIGHT))
    for y in range(STATUS_BAR_HEIGHT, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def get_neighbors(grid, r, c):
    total = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            total += grid[(r + i) % ROWS, (c + j) % COLS]
    return total

def update_grid(grid):
    new_grid = np.copy(grid)
    for r in range(ROWS):
        for c in range(COLS):
            neighbors = get_neighbors(grid, r, c)
            if grid[r, c] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[r, c] = 0
            elif grid[r, c] == 0 and neighbors == 3:
                new_grid[r, c] = 1
    return new_grid

def draw_status_bar(surface, paused, generation):
    pygame.draw.rect(surface, STATUS_BG, (0, 0, SCREEN_WIDTH, STATUS_BAR_HEIGHT))
    status_text = "PAUSED" if paused else "RUNNING"
    status_color = PAUSED_COLOR if paused else RUNNING_COLOR
    status_surf = font.render(f"Status: {status_text}", True, status_color)
    surface.blit(status_surf, (10, 10))
    gen_surf = font.render(f"Generation: {generation}", True, TEXT_COLOR)
    surface.blit(gen_surf, (SCREEN_WIDTH - 220, 10))

def draw_menu(surface):
    surface.fill(MENU_BG)
    title = big_font.render("Conway's Game of Life", True, HIGHLIGHT)
    surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, TITLE_Y))
    controls = [
        "Controls:",
        "Left Click - Make Cell Alive",
        "Right Click - Kill Cell",
        "Spacebar - Play / Pause",
        "C - Clear Board",
        "R - Randomize Grid",
        "ESC - Return to Menu / Quit",
    ]
    y = CONTROLS_Y_START
    for line in controls:
        text = font.render(line, True, TEXT_COLOR)
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
        y += CONTROL_SPACING
    prompt = font.render("Press SPACE to Start", True, HIGHLIGHT)
    surface.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, PROMPT_Y))

running = True
while running:
    if in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    in_menu = False
                    paused = True
                    generation = 0
                    grid = np.zeros((ROWS, COLS), dtype=int)
        draw_menu(screen)
        pygame.display.flip()
        clock.tick(FPS_MENU)
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_ESCAPE:
                in_menu = True
            elif event.key == pygame.K_c:
                grid = np.zeros((ROWS, COLS), dtype=int)
                generation = 0
            elif event.key == pygame.K_r:
                grid = np.random.randint(0, 2, (ROWS, COLS))
                generation = 0

    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > STATUS_BAR_HEIGHT:
            c = mouse_x // CELL_SIZE
            r = (mouse_y - STATUS_BAR_HEIGHT) // CELL_SIZE
            if 0 <= r < ROWS and 0 <= c < COLS:
                grid[r, c] = 1
    elif mouse_buttons[2]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > STATUS_BAR_HEIGHT:
            c = mouse_x // CELL_SIZE
            r = (mouse_y - STATUS_BAR_HEIGHT) // CELL_SIZE
            if 0 <= r < ROWS and 0 <= c < COLS:
                grid[r, c] = 0

    if not paused:
        grid = update_grid(grid)
        generation += 1

    draw_grid(screen, grid)
    draw_status_bar(screen, paused, generation)
    pygame.display.flip()
    clock.tick(FPS_GAME)

pygame.quit()
