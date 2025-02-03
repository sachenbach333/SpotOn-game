
import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("On The Dot Game")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (255, 255, 255)  # White background

PLAYER_COLORS = [RED, GREEN, PURPLE, YELLOW]

# Game modes
game_modes = {
    "easy": 240,  # 4 minutes
    "difficult": 120,  # 2 minutes
    "very difficult": 60,  # 1 minute
    "genius": 30  # 30 seconds
}

# Generate deck of 30 pattern cards with four different colored dots
pattern_cards = []
for _ in range(30):
    pattern = [(random.randint(50, 550), random.randint(50, 550), random.choice(PLAYER_COLORS)) for _ in range(4)]
    pattern_cards.append(pattern)

# Load player cards (transparent with outlined colors)
cards = []
for color in PLAYER_COLORS:
    card = pygame.Surface((200, 200), pygame.SRCALPHA)
    pygame.draw.rect(card, color, (0, 0, 200, 200), 5)  # Outline
    cards.append(card)

# Initial settings
card_positions = [(100, 100), (300, 100), (100, 300), (300, 300)]
card_rotations = [0, 0, 0, 0]
selected_card = None
current_pattern = random.choice(pattern_cards)
num_players = 1  # Default single-player mode
game_mode = "easy"  # Default game mode
time_limit = game_modes[game_mode]
start_time = time.time()

def draw_game():
    screen.fill(BACKGROUND_COLOR)
    # Draw pattern card
    for x, y, color in current_pattern:
        pygame.draw.circle(screen, color, (x, y), 10)
    # Draw player cards
    for i, (pos, rotation) in enumerate(zip(card_positions, card_rotations)):
        rotated_card = pygame.transform.rotate(cards[i], rotation)
        screen.blit(rotated_card, pos)
    # Display remaining time
    remaining_time = max(0, int(time_limit - (time.time() - start_time)))
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time Left: {remaining_time}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))
    pygame.display.flip()

    if remaining_time == 0:
        print("Time's up! Game Over.")
        pygame.quit()
        exit()

def check_match():
    global current_pattern, card_rotations
    player_dots = []
    for i, (pos, rotation) in enumerate(zip(card_positions, card_rotations)):
        rotated_card = pygame.transform.rotate(cards[i], rotation)
        card_rect = rotated_card.get_rect(topleft=pos)
        player_dots.append((card_rect.centerx, card_rect.centery))
    if sorted(player_dots) == sorted([(x, y) for x, y, _ in current_pattern]):
        print("Match Found! Drawing new pattern...")
        current_pattern = random.choice(pattern_cards)
        card_rotations = [0, 0, 0, 0]  # Reset positions

drawing = True
while drawing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            drawing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i, (pos, _) in enumerate(card_positions):
                card_rect = pygame.Rect(pos[0], pos[1], 200, 200)
                if card_rect.collidepoint(x, y):
                    selected_card = i
        elif event.type == pygame.KEYDOWN and selected_card is not None:
            if event.key == pygame.K_r:
                card_rotations[selected_card] = (card_rotations[selected_card] + 90) % 360
            elif event.key == pygame.K_f:
                cards[selected_card] = pygame.transform.flip(cards[selected_card], True, False)
            elif event.key == pygame.K_RETURN:
                check_match()
    draw_game()

pygame.quit()
