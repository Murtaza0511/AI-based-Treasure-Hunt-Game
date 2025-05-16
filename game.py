import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 820, 820
ROWS, COLS = 14, 14  # Grid size 14x14

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Treasure Race")
clock = pygame.time.Clock()

WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GRAY = (255,255,255), (0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (200,200,200)
font = pygame.font.SysFont("Arial", 26)
big_font = pygame.font.SysFont("Arial", 72)

goal = [ROWS - 1, COLS - 1]

players = [
    {"pos": [0, 0], "color": BLUE, "score": 0, "speed": 1, "alive": True, "controls": {'up':pygame.K_UP,'down':pygame.K_DOWN,'left':pygame.K_LEFT,'right':pygame.K_RIGHT}},
    {"pos": [0, 1], "color": GREEN, "score": 0, "speed": 1, "alive": True, "controls": {'up':pygame.K_w,'down':pygame.K_s,'left':pygame.K_a,'right':pygame.K_d}},
]

treasures = [[random.randint(0, ROWS-1), random.randint(0, COLS-1)] for _ in range(20)]
powerups = [[random.randint(0, ROWS-1), random.randint(0, COLS-1)] for _ in range(5)]
guards = [{"pos": [random.randint(5,ROWS-1), random.randint(5,COLS-1)]} for _ in range(4)]

game_state = "title"
fade_alpha = 255
winner = None
guard_timer, guard_delay = 1400, 1400

def get_tile_size():
    return min(screen.get_width() // COLS, screen.get_height() // ROWS)

def draw_grid():
    tile_size = get_tile_size()
    for x in range(0, tile_size * COLS, tile_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, tile_size * ROWS))
    for y in range(0, tile_size * ROWS, tile_size):
        pygame.draw.line(screen, GRAY, (0, y), (tile_size * COLS, y))

def draw_guard(pos):
    tile_size = get_tile_size()
    x = pos[1] * tile_size + tile_size // 2
    y = pos[0] * tile_size + tile_size // 2
    pygame.draw.circle(screen, RED, (x, y), tile_size // 3)
    pygame.draw.rect(screen, RED, (x - tile_size//6, y, tile_size//3, tile_size//5))
    pygame.draw.rect(screen, BLACK, (x - tile_size//6 - 2, y - tile_size//2, tile_size//3 + 4, tile_size//10))

def draw_entities():
    tile_size = get_tile_size()
    for t in treasures:
        pygame.draw.circle(screen, YELLOW, (t[1]*tile_size+tile_size//2, t[0]*tile_size+tile_size//2), tile_size//5)
    for p in powerups:
        pygame.draw.circle(screen, WHITE, (p[1]*tile_size+tile_size//2, p[0]*tile_size+tile_size//2), tile_size//6)
    for g in guards:
        draw_guard(g["pos"])
    for i, player in enumerate(players):
        if player["alive"]:
            pygame.draw.circle(screen, player["color"], (player["pos"][1]*tile_size+tile_size//2, player["pos"][0]*tile_size+tile_size//2), tile_size//4)
        score_text = font.render(f"P{i+1}: {player['score']}", True, player["color"])
        screen.blit(score_text, (10+i*150, 10))

def draw_goal_arrow():
    tile_size = get_tile_size()
    x = goal[1] * tile_size + tile_size // 2
    y = goal[0] * tile_size + tile_size // 2

    arrow_color = (255, 50, 50)
    pygame.draw.polygon(screen, arrow_color, [
        (x, y - tile_size // 3),
        (x + tile_size // 4, y),
        (x + tile_size // 8, y),
        (x + tile_size // 8, y + tile_size // 3),
        (x - tile_size // 8, y + tile_size // 3),
        (x - tile_size // 8, y),
        (x - tile_size // 4, y)
    ])

    finish_label = font.render("FINISH", True, WHITE)
    screen.blit(finish_label, (x - finish_label.get_width() // 2, y - tile_size // 2 - 20))

def move_guards():
    positions = {tuple(g["pos"]) for g in guards}
    for guard in guards:
        targets = [p["pos"] for p in players if p["alive"]]
        if not targets: return
        tx, ty = min(targets, key=lambda t: abs(t[0]-guard["pos"][0]) + abs(t[1]-guard["pos"][1]))
        dx, dy = tx - guard["pos"][0], ty - guard["pos"][1]
        new_pos = list(guard["pos"])
        if abs(dx) > abs(dy):
            new_pos[0] += (1 if dx > 0 else -1)
        elif dy != 0:
            new_pos[1] += (1 if dy > 0 else -1)
        if tuple(new_pos) not in positions:
            positions.discard(tuple(guard["pos"]))
            guard["pos"] = new_pos
            positions.add(tuple(new_pos))

def check_collisions():
    global game_state, winner
    for player in players:
        if not player["alive"]:
            continue
        if player["pos"] in treasures:
            treasures.remove(player["pos"])
            player["score"] += 1
        if player["pos"] in powerups:
            powerups.remove(player["pos"])
            player["speed"] = 2
            pygame.time.set_timer(pygame.USEREVENT+1, 3000, True)
        for guard in guards:
            if player["pos"] == guard["pos"]:
                player["alive"] = False

    for i, player in enumerate(players):
        if player["alive"] and player["score"] >= 6 and player["pos"] == goal:
            winner = f"P{i+1}"
            game_state = "gameover"
            return

    if all(not p["alive"] or p["score"] < 6 for p in players):
        if sum(p["alive"] for p in players) == 0:
            winner = "Guards"
            game_state = "gameover"

def draw_title():
    global fade_alpha
    screen.fill(BLACK)
    text = big_font.render("Treasure Race", True, YELLOW)
    prompt = font.render("Press any key to start", True, GRAY)
    instruction1 = font.render("Player 1 (Blue): Use Arrow Keys", True, BLUE)
    instruction2 = font.render("Player 2 (Green): Use W A S D", True, GREEN)
    win_condition = font.render("Goal: Collect 6 treasures and reach the bottom-right corner first", True, RED)
    screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - 80))
    screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, screen.get_height()//2 + 20))
    screen.blit(instruction1, (WIDTH // 2 - instruction1.get_width() // 2, 700))
    screen.blit(instruction2, (WIDTH // 2 - instruction2.get_width() // 2, 730))
    screen.blit(win_condition, (WIDTH // 2 - win_condition.get_width() // 2, 760))

    if fade_alpha > 0:
        fade = pygame.Surface((screen.get_width(), screen.get_height()))
        fade.set_alpha(fade_alpha)
        fade.fill(BLACK)
        screen.blit(fade, (0, 0))
        fade_alpha -= 4

def draw_gameover():
    screen.fill(BLACK)
    over = big_font.render(f"{winner} Wins!", True, RED if winner == "Guards" else GREEN)
    prompt = font.render("Press R to replay", True, WHITE)
    screen.blit(over, (screen.get_width()//2 - over.get_width()//2, screen.get_height()//2 - 80))
    screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, screen.get_height()//2 + 20))

while True:
    dt = clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        if game_state == "title" and event.type == pygame.KEYDOWN:
            game_state = "playing"
        if event.type == pygame.USEREVENT+1:
            for p in players: p["speed"] = 1
        if game_state == "gameover" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            for p in players:
                p["pos"] = [0, 0] if p["color"] == BLUE else [0, 1]
                p["score"], p["speed"], p["alive"] = 0, 1, True
            treasures = [[random.randint(0, ROWS-1), random.randint(0, COLS-1)] for _ in range(20)]
            powerups = [[random.randint(0, ROWS-1), random.randint(0, COLS-1)] for _ in range(5)]
            guards = [{"pos": [random.randint(5,ROWS-1), random.randint(5,COLS-1)]} for _ in range(4)]
            game_state = "title"
            fade_alpha = 255

        if event.type == pygame.KEYDOWN and game_state == "playing":
            for player in players:
                if not player["alive"]: continue
                if event.key == player["controls"]["up"] and player["pos"][0] > 0:
                    player["pos"][0] -= 1
                elif event.key == player["controls"]["down"] and player["pos"][0] < ROWS - 1:
                    player["pos"][0] += 1
                elif event.key == player["controls"]["left"] and player["pos"][1] > 0:
                    player["pos"][1] -= 1
                elif event.key == player["controls"]["right"] and player["pos"][1] < COLS - 1:
                    player["pos"][1] += 1

    if game_state == "playing":
        guard_timer += dt
        if guard_timer >= guard_delay:
            move_guards()
            guard_timer = 0
        check_collisions()
        draw_grid()
        draw_entities()
        draw_goal_arrow()
    elif game_state == "title":
        draw_title()
    elif game_state == "gameover":
        draw_gameover()

    pygame.display.flip()
