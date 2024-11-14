import pygame
import random
import sys
import time

# Inicialize o Pygame
pygame.init()

# Configurações de tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
SALMON = (250, 128, 114)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)

# Fonte
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Configurações do jogo
score = 0
max_time = 5
time_left = max_time
calculation = ""
correct_answer = 0
input_answer = ""
bar_width = screen_width - 200
bar_height = 20
bar_x = 100
bar_y = 500
yellow_x = bar_x + bar_width - 5
time_decrease_rate = 0.03
ball_x = 0
ball_y = screen_height - 50
opacity = 255
fade_time = 0
fade_duration = 60

# Variáveis de controle de erros
max_errors = 3
errors = 0
balls = []

# Estado do jogo
game_started = False
game_over = False
current_scene = "menu"  # Adiciona estado inicial do jogo como "menu"

# Função para exibir a contagem regressiva
def countdown():
    for i in range(3):
        screen.fill(WHITE)
        countdown_text = font.render(str(3 - i), True, BLACK)
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        time.sleep(1)
    screen.fill(WHITE)
    final_text = font.render("GO!", True, BLACK)
    screen.blit(final_text, (screen_width // 2 - final_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    time.sleep(1)

# Função para gerar um novo cálculo
def generate_calculation():
    global calculation, correct_answer
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    calculation = f"{num1} + {num2}"
    correct_answer = num1 + num2

# Função para desenhar o menu principal
def draw_menu():
    screen.fill(WHITE)
    title_text = font.render("Menu Principal", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))

    # Botão para Iniciar o Jogo
    play_button = pygame.Rect(screen_width // 2 - 100, 250, 200, 50)
    pygame.draw.rect(screen, GREEN, play_button)
    play_text = small_font.render("Iniciar Jogo", True, BLACK)
    screen.blit(play_text, (play_button.centerx - play_text.get_width() // 2, play_button.centery - play_text.get_height() // 2))

    # Botão para Sair
    quit_button = pygame.Rect(screen_width // 2 - 100, 350, 200, 50)
    pygame.draw.rect(screen, RED, quit_button)
    quit_text = small_font.render("Sair", True, BLACK)
    screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))

    pygame.display.flip()
    return play_button, quit_button

# Funções para desenhar elementos do jogo
def draw_timer_bar():
    yellow_x = bar_x + (bar_width - 5) * (time_left / max_time)
    pygame.draw.rect(screen, SKY_BLUE, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width // 4, bar_height))
    pygame.draw.rect(screen, GREEN, (bar_x + 1.5 * (bar_width // 3), bar_y, bar_width // 2.0, bar_height))
    pygame.draw.rect(screen, YELLOW, (yellow_x, bar_y, 5, bar_height))

def draw_calculation():
    calc_text = font.render(calculation, True, BLACK)
    screen.blit(calc_text, (screen_width // 2 - calc_text.get_width() // 2, screen_height // 2 - 50))
    score_text = small_font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    input_text = small_font.render(f"Sua resposta: {input_answer}", True, BLACK)
    screen.blit(input_text, (screen_width // 2 - input_text.get_width() // 2, screen_height // 2 + 50))

def draw_game_over():
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
    retry_text = small_font.render("Pressione 'R' para jogar novamente ou 'Q' para sair", True, BLACK)
    screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))

def reset_game():
    global score, time_left, input_answer, errors, game_over, balls, ball_x, fade_time
    score = 0
    time_left = max_time
    input_answer = ""
    errors = 0
    balls.clear()
    ball_x = 0
    fade_time = 0
    game_over = False
    generate_calculation()

def draw_balls():
    for ball in balls:
        pygame.draw.circle(screen, RED, ball, 20)

def is_valid_int(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False

def apply_opacity():
    global fade_time, opacity, perfect_text, good_text, bad_text
    if fade_time > 0:
        fade_time -= 1
        opacity = max(0, opacity - (255 // fade_duration))
        if perfect_text:
            perfect_text.set_alpha(opacity)
            screen.blit(perfect_text, (screen_width // 2 - perfect_text.get_width() // 2, screen_height // 2 - 100))

# Loop principal do jogo
running = True
while running:
    if current_scene == "menu":
        play_button, quit_button = draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_scene == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    countdown()
                    current_scene = "game"
                    generate_calculation()
                elif quit_button.collidepoint(mouse_pos):
                    running = False

        elif current_scene == "game":
            # Código do jogo original aqui
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_answer == "":
                        pass
                    elif is_valid_int(input_answer):
                        if int(input_answer) == correct_answer:
                            score += 10  # Exemplo de pontuação
                        else:
                            errors += 1
                            if errors >= max_errors:
                                game_over = True
                        input_answer = ""
                        time_left = max_time
                        generate_calculation()
                    else:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    input_answer = input_answer[:-1]
                else:
                    if event.unicode.isdigit():
                        input_answer += event.unicode

            if not game_over:
                if time_left > 0:
                    time_left -= time_decrease_rate
                else:
                    errors += 1
                    if errors >= max_errors:
                        game_over = True
                    input_answer = ""
                    generate_calculation()
                    time_left = max_time

            if game_over:
                draw_game_over()
            else:
                screen.fill(WHITE)
                draw_timer_bar()
                draw_calculation()
                draw_balls()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
