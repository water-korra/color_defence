import pygame
import random
import math

pygame.init()

# Dimension
WIDTH, HEIGHT = 1200, 1000
SHOOTING_WHEEL_RADIUS = 684 // 4
SHOOTING_WHEEL_POSITION = (WIDTH // 2, HEIGHT // 2)

# Load the shooting wheel image
shooting_wheel_img = pygame.image.load("shooting_wheel.png")
shooting_wheel_img = pygame.transform.scale(shooting_wheel_img, (shooting_wheel_img.get_width() // 4, shooting_wheel_img.get_height() // 4))

# Constants
SEGMENT_COLORS = {"d": (0, 0, 255), "s": (255, 255, 0), "a": (255, 0, 0), "w": (0, 255, 0)}
ENEMY_RADIUS = 10
ENEMY_SPEED = 1
ENEMY_SPAWN_RATE = 40
FPS = 60
SCORE_FONT = pygame.font.SysFont('Arial', 30)

class Enemy:
    def __init__(self, pos, color, segment):
        self.pos = pos
        self.color = color
        self.segment = segment

    def move_towards_center(self, enemy_speed):
        direction = [SHOOTING_WHEEL_POSITION[0] - self.pos[0], SHOOTING_WHEEL_POSITION[1] - self.pos[1]]
        distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if distance != 0:
            direction = [direction[0] / distance, direction[1] / distance]
            self.pos[0] += direction[0] * enemy_speed
            self.pos[1] += direction[1] * enemy_speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, ENEMY_RADIUS)

    def collides_with_wheel(self):
        wheel_rect = shooting_wheel_img.get_rect(center=SHOOTING_WHEEL_POSITION)
        enemy_circle = pygame.Rect(self.pos[0] - ENEMY_RADIUS, self.pos[1] - ENEMY_RADIUS, 2 * ENEMY_RADIUS, 2 * ENEMY_RADIUS)
        return wheel_rect.colliderect(enemy_circle)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Wheel Game")
clock = pygame.time.Clock()

# Game variables
running = True
score = 0
enemies = {key: [] for key in SEGMENT_COLORS}
game_over = False
enemy_speed = ENEMY_SPEED
enemy_spawn_rate = ENEMY_SPAWN_RATE

def draw_shooting_wheel(screen):
    wheel_rect = shooting_wheel_img.get_rect(center=SHOOTING_WHEEL_POSITION)
    screen.blit(shooting_wheel_img, wheel_rect)

def create_enemy():
    segment_key = random.choice(list(SEGMENT_COLORS.keys()))
    segment_index = list(SEGMENT_COLORS.keys()).index(segment_key)
    angle_start = math.radians(90 * segment_index - 45)
    angle_end = angle_start + math.radians(90)
    angle = random.uniform(angle_start, angle_end)
    distance_from_center = max(WIDTH, HEIGHT) // 2
    x = SHOOTING_WHEEL_POSITION[0] + int(math.cos(angle) * distance_from_center)
    y = SHOOTING_WHEEL_POSITION[1] + int(math.sin(angle) * distance_from_center)
    return Enemy([x, y], SEGMENT_COLORS[segment_key], segment_key)

def display_end_game_message(screen, score):
    message_font = pygame.font.SysFont('Arial', 40)
    message_text = message_font.render(f"You lost, score is {score}. Restart? (Y/N)", True, (255, 255, 255))
    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(message_text, message_rect)
    pygame.display.flip()

# Main game loop
frame_count = 0
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    draw_shooting_wheel(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            for color_key, _ in SEGMENT_COLORS.items():
                if key_name == color_key:
                    if enemies[color_key]:
                        enemies[color_key].pop(0)
                        score += 1
                        break

    if frame_count % enemy_spawn_rate == 0:
        new_enemy = create_enemy()
        enemies[new_enemy.segment].append(new_enemy)

    for enemy_list in enemies.values():
        for enemy in enemy_list:
            enemy.move_towards_center(enemy_speed)
            enemy.draw(screen)
            if enemy.collides_with_wheel():
                game_over = True

    if game_over:
        display_end_game_message(screen, score)
        wait_for_restart = True
        while wait_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    wait_for_restart = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        score = 0
                        enemies = {key: [] for key in SEGMENT_COLORS}
                        game_over = False
                        wait_for_restart = False
                        enemy_speed = ENEMY_SPEED  
                        enemy_spawn_rate = ENEMY_SPAWN_RATE 
                    elif event.key == pygame.K_n:
                        running = False
                        wait_for_restart = False

    score_text = SCORE_FONT.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    frame_count += 1

    # Harden game with time
    if frame_count % (FPS * 10) == 0:
        enemy_speed += 0.1
        enemy_spawn_rate = max(20, enemy_spawn_rate - 5)

pygame.quit()
