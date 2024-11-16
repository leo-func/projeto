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
max_time = 5  # Tempo máximo para a resposta (em segundos)
time_left = max_time
calculation = ""
correct_answer = 0
input_answer = ""
bar_width = screen_width - 200
bar_height = 20
bar_x = 100
bar_y = 500
yellow_x = bar_x + bar_width - 5
time_decrease_rate = 0.03  # Reduz a velocidade da barra
ball_x = 0
ball_y = screen_height - 50
opacity = 255  # Inicializa a opacidade do texto "Perfeito!" para visível
fade_time = 0  # Tempo para o fade-out
fade_duration = 60  # Duração do fade-out (em iterações)
total_game_time = 60
game_timer = total_game_time
coins = 0
clock = pygame.time.Clock()



# Variáveis de controle de erros
max_errors = 3
errors = 0
balls = []  # Lista para armazenar as posições das bolas

# Estado do jogo
game_started = False
game_over = False

# Função para exibir a contagem regressiva
def countdown():
    for i in range(3):  # Contagem de 1 a 3
        screen.fill(WHITE)
        countdown_text = font.render(str(i + 1), True, BLACK)
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        time.sleep(1)  # Espera 1 segundo

    # Exibe "GO!"
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

# Função para desenhar a barra de tempo
def draw_timer_bar():
    # Calcula a posição da linha amarela com base no tempo restante
    yellow_x = bar_x + (bar_width - 5) * (time_left / max_time)  # A linha amarela move-se de acordo com o tempo

    # Desenha as partes da barra de tempo
    pygame.draw.rect(screen, SKY_BLUE, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width // 4, bar_height))
    pygame.draw.rect(screen, GREEN, (bar_x + 1.5 * (bar_width // 3), bar_y, bar_width // 2.0, bar_height))
    pygame.draw.rect(screen, YELLOW, (yellow_x, bar_y, 5, bar_height))  # Atualiza a posição da linha amarela

# Função para desenhar o cálculo e a pontuação
def draw_calculation():
    calc_text = font.render(calculation, True, BLACK)
    screen.blit(calc_text, (screen_width // 2 - calc_text.get_width() // 2, screen_height // 2 - 50))
    
    score_text = small_font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    input_text = small_font.render(f"Sua resposta: {input_answer}", True, BLACK)
    screen.blit(input_text, (screen_width // 2 - input_text.get_width() // 2, screen_height // 2 + 50))

# Função para desenhar a tela de Game Over
def draw_game_over():
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
    
    retry_text = small_font.render("Pressione 'R' para jogar novamente ou 'Q' para sair", True, BLACK)
    screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))

# Função para reiniciar o jogo
def reset_game():
    global score, time_left, input_answer, errors, game_over, balls, ball_x, fade_time, game_timer, total_game_time, coins
    score = 0
    time_left = max_time
    input_answer = ""
    errors = 0 
    balls.clear()  # Limpa a lista de bolas
    ball_x = 0  # Reseta o valor de ball_x para 0 quando o jogo reiniciar
    fade_time = 0  # Reseta o tempo do fade para 0
    game_over = False # Tela de game over desativada
    game_timer = total_game_time # Reseta o tempo para o valor padrão
    coins = 0
    generate_calculation()  # Gera um novo cálculo ao reiniciar o jogo

# Função para converter pontuação em score
def coin_counter():
    global coins
    coins = score // 2
    print(coins)

# Função para desenhar as moedas
def draw_coin_counter():
    coin_text = small_font.render(f"Moedas: {coins}", True, BLACK)
    screen.blit(coin_text, (10, 50))

# Função para desenhar as bolas de erro
def draw_balls():
    for ball in balls:
        pygame.draw.circle(screen, RED, ball, 20)

# Função para verificar se a entrada é um número inteiro
def is_valid_int(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False

# Fade-out do texto "Perfeito!"
def apply_opacity():
    global fade_time, opacity, perfect_text, good_text, bad_text
    if fade_time > 0:
        fade_time -= 1
        opacity = max(0, opacity - (255 // fade_duration))  # Reduz a opacidade gradualmente
        if perfect_text:
            perfect_text.set_alpha(opacity)
            screen.blit(perfect_text, (screen_width // 2 - perfect_text.get_width() // 2, screen_height // 2 - 100))
        if good_text:
            good_text.set_alpha(opacity)
            screen.blit(good_text, (screen_width // 2 - good_text.get_width() // 2, screen_height // 2 - 100))
        if bad_text:
            bad_text.set_alpha(opacity)
            screen.blit(bad_text, (screen_width // 2 - bad_text.get_width() // 2, screen_height // 2 - 100))

    else:
        fade_time = 0

# Chama a contagem regressiva antes do início do jogo
countdown()
game_started = True  # Marca que o jogo foi iniciado
generate_calculation()

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"

# Loop principal do jogo
running = True
while running:
    screen.fill(WHITE)  # Limpa a tela a cada iteração do loop
    delta_time = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Pressione 'R' para reiniciar
                    reset_game()
                elif event.key == pygame.K_q:  # Pressione 'Q' para sair
                    running = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_answer == "":
                        pass
                    elif is_valid_int(input_answer):
                        if int(input_answer) == correct_answer:
                            if time_left > max_time / 2:
                                score += 15
                                perfect_text = font.render("Perfeito!", True, GREEN)
                                good_text = None
                                bad_text = None

                                # Fade-in (já está visível) e fade-out controlados pelo tempo
                                fade_time = fade_duration  # Define o tempo máximo para o fade
                                opacity = 255

                                print("Perfeito!")
                            elif time_left > max_time / 4:
                                score += 10
                                good_text = font.render("Bom!", True, SKY_BLUE)
                                perfect_text = None
                                bad_text = None
                                fade_time = fade_duration
                                opacity = 255
                                print("Bom!")
                            else:
                                score += 5
                                bad_text = font.render("Ruim!", True, RED)
                                perfect_text = None
                                good_text = None
                                fade_time = fade_duration
                                opacity = 255
                                print("Ruim!")

                        else:
                            errors += 1
                            ball_x += 50  # Incrementa 50 pixels no deslocamento horizontal da bola
                            balls.append((ball_x, ball_y))  # Cria a bola na nova posição
                            if errors >= max_errors:
                                game_over = True
                        input_answer = ""  # Limpa a resposta do jogador
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
        if game_timer > 0:
            game_timer -= delta_time
        else:
            game_over = True
        if time_left > 0:
            time_left -= time_decrease_rate
        else:
            errors += 1
            ball_x += 50
            balls.append((ball_x, ball_y))
            if errors >= max_errors:
                game_over = True
            input_answer = ""
            generate_calculation()
            time_left = max_time

    if game_over:
        draw_game_over()
    else:
        # Desenhar barra de tempo
        draw_timer_bar()

        # Desenhar cálculo e pontuação
        draw_calculation()
        coin_counter() 

        # Desenhar moedas
        draw_coin_counter()

        # Desenhar as bolas
        draw_balls()

        # Fade
        apply_opacity()

        # Exibir o tempo restante global no formato "0:00"
        formatted_timer = format_time(game_timer)
        timer_text = small_font.render(f"Tempo restante: {formatted_timer}", True, BLACK)
        screen.blit(timer_text, (screen_width - timer_text.get_width() - 10, 10))

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de quadros
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()