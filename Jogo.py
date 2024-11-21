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
perfect_counter = 0
good_counter = 0
bad_counter = 0
coins = 0
clock = pygame.time.Clock()
in_menu = True
countdown_active = False
stage_2_bool = False
stage_3_bool = False
infinity_mode_bool = False
left_reduction = 0
difficulty = 0

# Botões

button_start = pygame.Rect(screen_width // 2 - 100, 200, 200, 50)  # Botão "Iniciar Jogo"
button_instructions = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)  # Botão "Instruções"
button_quit = pygame.Rect(screen_width // 2 - 100, 400, 200, 50)  # Botão "Sair"
button_quit_stage = pygame.Rect(screen_width // 2 - 100, 500, 200, 50)  # Botão "Sair" em fases
stage_1 = pygame.Rect(screen_width // 2 - 100, 100, 200, 50)
stage_2 = pygame.Rect(screen_width // 2 - 100, 200, 200, 50)
stage_3 = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)
infinity_mode = pygame.Rect(screen_width // 2 - 100, 400, 200, 50)

# Variáveis de controle de erros
max_errors = 10
errors = 0
balls = []  # Lista para armazenar as posições das bolas

# Estado do jogo
game_started = False
game_over = False

# Desenhar menu

def draw_menu():
    screen.fill(WHITE)
    
    # Título
    title_text = font.render("Bem-vindo ao Jogo!", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
    
    # Botões
    pygame.draw.rect(screen, SKY_BLUE, button_start)
    pygame.draw.rect(screen, SKY_BLUE, button_instructions)
    pygame.draw.rect(screen, SKY_BLUE, button_quit)
    
    # Textos nos botões
    start_text = small_font.render("Iniciar Jogo", True, BLACK)
    instructions_text = small_font.render("Instruções", True, BLACK)
    quit_text = small_font.render("Sair", True, BLACK)
    
    screen.blit(start_text, (button_start.centerx - start_text.get_width() // 2, button_start.centery - start_text.get_height() // 2))
    screen.blit(instructions_text, (button_instructions.centerx - instructions_text.get_width() // 2, button_instructions.centery - instructions_text.get_height() // 2))
    screen.blit(quit_text, (button_quit.centerx - quit_text.get_width() // 2, button_quit.centery - quit_text.get_height() // 2))

# Desenhar fases

def draw_stages():
    screen.fill(WHITE)

    # Título

    title_text = font.render("Fases", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 30))

    # Botões
    pygame.draw.rect(screen, SKY_BLUE, stage_1)
    pygame.draw.rect(screen, SKY_BLUE, stage_2)
    pygame.draw.rect(screen, SKY_BLUE, stage_3)
    pygame.draw.rect(screen, SKY_BLUE, infinity_mode)
    

    # Textos nos botões

    stage_1_text = small_font.render("Fase 1", True, BLACK)
    stage_2_text = small_font.render("Fase 2", True, BLACK)
    stage_3_text = small_font.render("Fase 3", True, BLACK)
    infinity_mode_text = small_font.render("Modo infinito", True, BLACK)
    


    screen.blit(stage_1_text, (stage_1.centerx - stage_1_text.get_width() // 2, stage_1.centery - stage_1_text.get_height() // 2))
    screen.blit(stage_2_text, (stage_2.centerx - stage_2_text.get_width() // 2, stage_2. centery - stage_2_text.get_height() // 2))
    screen.blit(stage_3_text, (stage_3.centerx - stage_3_text.get_width() // 2, stage_3.centery - stage_3_text.get_height() // 2))
    screen.blit(infinity_mode_text, (infinity_mode.centerx - infinity_mode_text.get_width() // 2, infinity_mode.centery - infinity_mode_text.get_height() // 2))

    button_back = pygame.Rect(screen_width // 2 - 100, 500, 200, 50)
    pygame.draw.rect(screen, SKY_BLUE, button_back)
    back_text = small_font.render("Voltar", True, BLACK)
    screen.blit(back_text, (button_back.centerx - back_text.get_width() // 2, button_back.centery - back_text.get_height() // 2))
    return button_back
   
    


# Desenhar instruções

def draw_instructions():
    screen.fill(WHITE)
    instructions = [
        "Instruções do jogo:",
        "1. Resolva os cálculos antes do tempo acabar.",
        "2. Use os números no teclado para inserir sua resposta.",
        "3. Pressione 'Enter' para confirmar.",
        "4. Evite cometer muitos erros!",
        "Pressione 'Voltar' para retornar ao menu."
    ]
    y = 100
    for line in instructions:
        instruction_text = small_font.render(line, True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, y))
        y += 50
    
    # Botão de voltar
    button_back = pygame.Rect(screen_width // 2 - 100, 500, 200, 50)
    pygame.draw.rect(screen, SKY_BLUE, button_back)
    back_text = small_font.render("Voltar", True, BLACK)
    screen.blit(back_text, (button_back.centerx - back_text.get_width() // 2, button_back.centery - back_text.get_height() // 2))
    return button_back

# Função para gerar um novo cálculo
def generate_calculation():
    global calculation, correct_answer, num1, num2
    if stage_3_bool:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        calculation = f"{num1} x {num2}"
        correct_answer = num1 * num2
    elif stage_2_bool:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        calculation = f"{num1} - {num2}"
        correct_answer = num1 - num2
    else:
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

def draw_life_bar():
    pygame.draw.rect(screen, RED, ((bar_x + 530) + left_reduction, bar_y - 440, bar_width // 4 - left_reduction, bar_height - 15))


    

# Função para desenhar o cálculo e a pontuação
def draw_calculation():
    calc_text = font.render(calculation, True, BLACK)
    screen.blit(calc_text, (screen_width // 2 - calc_text.get_width() // 2, screen_height // 2 - 50))
    
    score_text = small_font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    input_text = small_font.render(f"Sua resposta: {input_answer}", True, BLACK)
    screen.blit(input_text, (screen_width // 2 - input_text.get_width() // 2, screen_height // 2 + 50))

# Função para analisar rank
def rank():
    temp = []
    if accuracy == 100:
        temp.append('A')
    elif 95 <= accuracy <= 99.99:
        temp.append('B')
    elif 85 <= accuracy <= 94.99:
        temp.append('C')
    elif 70 <= accuracy <= 84.99:
        temp.append('D')
    elif 50 <= accuracy <= 69.99:
        temp.append('E')
    elif 0 <= accuracy <= 49.99:
        temp.append('F')
    
    convert = ''.join(temp)
    return convert

# Função para desenhar a tela de Game Over
def draw_game_over():
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))

    ranked = rank()

    rank_text = small_font.render(f"Rank: {ranked} ", True, RED)
    screen.blit(rank_text, (screen_width // 2 - rank_text.get_width() // 2, 10))

    text_lines = [
        f"Perfeito: {perfect_counter}x",
        f"Bom: {good_counter}x",
        f"Ruim: {bad_counter}x"
    ]

    # Calcular a altura total do bloco de texto
    total_text_height = len(text_lines) * small_font.get_linesize()

    # Posição inicial do bloco (centralizado verticalmente)
    start_y = (screen_height - total_text_height) // 2
    

    for line in text_lines:
        # Renderiza o texto atual
        accuracy_text = small_font.render(line, True, BLACK)
        # Calcula a posição horizontal para centralizar cada linha
        text_x = (screen_width - accuracy_text.get_width()) // 2
        # Blita o texto na posição centralizada
        screen.blit(accuracy_text, (text_x, start_y))
        # Avança para a próxima linha
        start_y += small_font.get_linesize()

    
    retry_text = small_font.render("Pressione 'R' para jogar novamente ou 'Q' para sair", True, BLACK)
    screen.blit(retry_text, (screen_width // 2 - retry_text.get_width() // 2, screen_height // 2 + 50))

# Função para reiniciar o jogo
def reset_game():
    global score, time_left, input_answer, errors, game_over, balls, ball_x, fade_time, game_timer, total_game_time, coins, perfect_counter, good_counter, bad_counter, left_reduction
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
    perfect_counter = 0
    good_counter = 0
    bad_counter = 0
    game_started = True
    left_reduction = 0
    generate_calculation()  # Gera um novo cálculo ao reiniciar o jogo

# Função para exibir a contagem regressiva
def countdown():
    global countdown_active, game_timer
    countdown_active = True
    for i in range(3, 0, -1):  # Contagem de 3 a 1
        screen.fill(WHITE)
        countdown_text = font.render(str(i), True, BLACK)
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # Espera 1 segundo

    # Exibe "GO!"
    screen.fill(WHITE)
    go_text = font.render("GO!", True, GREEN)
    screen.blit(go_text, (screen_width // 2 - go_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()
    pygame.time.wait(1000)
    
    countdown_active = False  # Contagem regressiva concluída
    total_game_time = 65
    game_timer = total_game_time


# Função para converter pontuação em moedas
def coin_counter():
    global coins
    coins = score // 2
    print(coins)

# Função para desenhar a precisão
def draw_accuracy():
    acurracy = estimate_accuracy()
    acurracy_text = small_font.render(f"{acurracy:.2f} %", True, BLACK)
    screen.blit(acurracy_text, (10, 50))


# Função para verificar se a entrada é um número inteiro
def is_valid_int(input_string):
    if input_string in ("+", "-"):  # Permite apenas sinais sem números temporariamente
        return True
    try:
        int(input_string)  # Tenta converter para inteiro
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

# Função para contar a precisão
def estimate_accuracy():
    total_answers = perfect_counter + good_counter + bad_counter + errors
    penalty_factor = 5
    
    global accuracy

    if total_answers > 0:
        accuracy = ((perfect_counter * 1.0) + (good_counter * 0.75) + (bad_counter * 0.5)) / total_answers * 100
        accuracy -= errors * penalty_factor
        accuracy = max(accuracy, 0)
    else:
        accuracy = 0
    return accuracy




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
        if in_menu == True:
            draw_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_start.collidepoint(mouse_pos):  # Botão "Iniciar Jogo"
                    in_menu = "stages"
                elif button_instructions.collidepoint(mouse_pos):  # Botão "Instruções"
                    in_menu = "instructions"
                elif button_quit.collidepoint(mouse_pos):  # Botão "Sair"
                    running = False
        elif in_menu == "instructions":
            button_back = draw_instructions()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_back.collidepoint(mouse_pos):  # Botão "Voltar"
                    in_menu = True

        elif in_menu == "stages":
            button_back = draw_stages()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if stage_1.collidepoint(mouse_pos):
                    countdown()
                    game_started = True
                    time_left = max_time
                    in_menu = False
                    generate_calculation()
                elif stage_2.collidepoint(mouse_pos):
                    countdown()
                    stage_2_bool = True
                    game_started = True
                    time_left = max_time
                    in_menu = False
                    generate_calculation()
                
                elif stage_3.collidepoint(mouse_pos):
                    countdown()
                    stage_3_bool = True
                    game_started = True
                    time_left = max_time
                    in_menu = False
                    generate_calculation()
                elif infinity_mode.collidepoint(mouse_pos):
                    countdown()
                    infinity_mode_bool = True
                    game_started = True
                    in_menu = False
                    
                elif button_back.collidepoint(mouse_pos):
                    in_menu = True
        
        elif game_over:
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
                                perfect_counter += 1

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
                                good_counter += 1
                                print("Bom!")
                            else:
                                score += 5
                                bad_text = font.render("Ruim!", True, RED)
                                perfect_text = None
                                good_text = None
                                fade_time = fade_duration
                                opacity = 255
                                bad_counter += 1
                                print("Ruim!")

                        else:
                            errors += 1
                            left_reduction += 20
                            left_reduction = min(left_reduction, bar_width // 2)
                            if left_reduction == 160:
                                game_over = True
                                  
                        input_answer = ""  # Limpa a resposta do jogador
                        time_left = max_time
                        generate_calculation()
                    else:
                        pass
                elif event.unicode.isdigit() or event.unicode in "+-":  # Apenas números ou sinais
                    if is_valid_int(input_answer + event.unicode):  # Valida a entrada acumulada
                        input_answer += event.unicode                
                elif event.key == pygame.K_BACKSPACE:
                    input_answer = input_answer[:-1]
                else:
                    if event.unicode.isdigit():
                        input_answer += event.unicode
    if game_started == True:
        if not countdown_active:
            if not game_over:
                if game_timer > 0:
                    game_timer -= delta_time
                else:
                    game_over = True
                if time_left > 0:
                    time_left -= time_decrease_rate
                else:
                    errors += 1
                    left_reduction += 20
                    if left_reduction == 160:
                        game_over = True
                    input_answer = ""
                    generate_calculation()
                    time_left = max_time
    if in_menu:
        if in_menu == "instructions":
            draw_instructions()
        elif in_menu == "stages":
            draw_stages()

        else:
            draw_menu()

    elif game_over:
        draw_game_over()
        rank()
        
    else:
        # Desenhar barra de tempo
        draw_timer_bar()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        # Desenhar cálculo e pontuação
        draw_calculation()

        # Desenhar moedas
        draw_accuracy()

        # Desenhar barra de vida
        draw_life_bar()

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