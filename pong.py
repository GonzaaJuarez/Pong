import pygame
import sys
import time
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Fuentes
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Función para dibujar texto en pantalla
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Función para mostrar el contador
def countdown():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        draw_text(str(i), font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(0.5)  # Esperar medio segundo entre números

def show_winner(screen, winner, score_left, score_right, font, small_font):
    screen.fill((0, 0, 0))  # Fondo negro

    # Texto del ganador y del puntaje final
    winner_text = f"{winner} WIN!"
    score_text = f"Final Score: {score_left} - {score_right}"

    # Dibujar textos usando la función draw_text
    draw_text(winner_text, font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(score_text, small_font, GRAY, screen, WIDTH // 2, HEIGHT // 2 + 50)

    pygame.display.flip()  # Actualizar la pantalla

    # Esperar unos segundos antes de cerrar el juego
    pygame.time.wait(5000)  # 7 segundos

def show_difficultys():
    difficultys = ["Easy", "Normal", "Hard"]  # Dificultades
    selected_difficulty = 1  # Por defecto: Normal

    while True:
        screen.fill(BLACK)
        draw_text("Select Difficulty", small_font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        
        # Dibujar las opciones con borde de rectángulo
        for i, difficulty in enumerate(difficultys):
            text_obj = small_font.render(difficulty, True, WHITE)
            text_rect = text_obj.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            
            if i == selected_difficulty:  # Dibujar solo el borde del rectángulo
                pygame.draw.rect(screen, WHITE, 
                                 text_rect.inflate(20, 10),  # Ajustar tamaño del borde
                                 width=3,  # Espesor del borde
                                 border_radius=10)  # Esquinas redondeadas

            # Dibujar el texto encima del rectángulo
            color = WHITE if i == selected_difficulty else GRAY
            draw_text(difficulty, small_font, color, screen, WIDTH // 2, HEIGHT // 2 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):  # Navegar hacia arriba
                    selected_difficulty = (selected_difficulty - 1) % len(difficultys)
                if event.key in (pygame.K_s, pygame.K_DOWN):  # Navegar hacia abajo
                    selected_difficulty = (selected_difficulty + 1) % len(difficultys)
                if event.key == pygame.K_RETURN:
                    return selected_difficulty

# Función para mostrar el menú
def show_menu():
    options = ["Singleplayer", "Multiplayer", "Quit"]  # Opciones del menú
    selected_option = 0  # Índice de la opción seleccionada

    while True:
        screen.fill(BLACK)

        # Título del juego
        draw_text("GonRez's Game", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)

        # Dibujar las opciones con borde de rectángulo
        for i, option in enumerate(options):
            text_obj = small_font.render(option, True, WHITE)
            text_rect = text_obj.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            
            if i == selected_option:  # Dibujar solo el borde del rectángulo
                pygame.draw.rect(screen, WHITE, 
                                 text_rect.inflate(20, 10),  # Ajustar tamaño del borde
                                 width=3,  # Espesor del borde
                                 border_radius=10)  # Esquinas redondeadas

            # Dibujar el texto encima del rectángulo
            color = WHITE if i == selected_option else GRAY
            draw_text(option, small_font, color, screen, WIDTH // 2, HEIGHT // 2 + i * 50)

        pygame.display.flip()

        # Manejo de eventos del menú
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):  # Mover hacia arriba
                    selected_option = (selected_option - 1) % len(options)
                if event.key in (pygame.K_s, pygame.K_DOWN):  # Mover hacia abajo
                    selected_option = (selected_option + 1) % len(options)
                if event.key == pygame.K_RETURN:  # Confirmar selección
                    if selected_option == 0:  # "Singleplayer"
                        return "singleplayer"
                    if selected_option == 1:  # "Multiplayer"
                        return "multiplayer"
                    if selected_option == 2:  # "Quit"
                        pygame.quit()
                        sys.exit()

# Función de pausa
def pause_game():
    paused = True
    while paused:
        screen.fill(BLACK)
        draw_text("Paused", font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        draw_text("Press ESC to Resume", small_font, GRAY, screen, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Esc para reanudar
                    paused = False

# Función principal del juego
def main_game(singleplayer, ai_speed, ai_reaction_time, precision_offset, error_chance):
    # Paletas y bola
    paddle_width, paddle_height = 20, 100
    ball_size = 20

    left_paddle = pygame.Rect(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)

    # Velocidades
    ball_speed = [4, 4]
    paddle_speed = 5

    # Marcador
    left_score = 0
    right_score = 0

    # Contador de inicio
    countdown_start_time = pygame.time.get_ticks()  # Tiempo inicial para el conteo
    countdown_running = True  # Bandera para saber si el contador está activo

    # Reloj para controlar la velocidad del juego
    clock = pygame.time.Clock()

    #Aumento de velocidad de la bola
    start_time = pygame.time.get_ticks()

    # Variable de ejecución
    running = True

    # Contador para medir el tiempo o la cantidad de cuadros que han pasado desde el inicio del juego o una acción específica.
    frame_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pausar el juego
                    pause_game()

        # Movimiento de las paletas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed

        # Limitar el movimiento de las paletas
        left_paddle.y = max(0, min(left_paddle.y, HEIGHT - left_paddle.height))

        if singleplayer:
            # Movimiento de la IA
            if ball.centery < right_paddle.centery and right_paddle.top > 0:
                right_paddle.y -= ai_speed
            if ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
                right_paddle.y += ai_speed

            # Implementar reacción basada en tiempo
            if frame_count % ai_reaction_time == 0:  # Reaccionar solo en ciertos frames
                if ball.centery < right_paddle.centery and right_paddle.top > 0:
                    right_paddle.y -= ai_speed
                elif ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
                    right_paddle.y += ai_speed

            # Movimiento de la IA con precisión ajustada
            target_y = ball.centery + precision_offset
            if target_y < right_paddle.centery and right_paddle.top > 0:
                right_paddle.y -= ai_speed
            elif target_y > right_paddle.centery and right_paddle.bottom < HEIGHT:
                right_paddle.y += ai_speed
            
            # Decisión basada en probabilidad
            if random.random() > error_chance:  # Solo mover si no ocurre error
                if ball.centery < right_paddle.centery and right_paddle.top > 0:
                    right_paddle.y -= ai_speed
                elif ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
                    right_paddle.y += ai_speed
        else:
            # Movimiento del jugador 2
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed

        # Limitar el movimiento de la paleta derecha
        right_paddle.y = max(0, min(right_paddle.y, HEIGHT - right_paddle.height))

        # Verificar si el contador sigue corriendo
        if countdown_running:
            while countdown_running:
                elapsed_time = (pygame.time.get_ticks() - countdown_start_time) // 1000  # Tiempo en segundos
                if elapsed_time >= 3:  # Si el contador ha terminado
                    countdown_running = False
                    break

                # Dibujar el contador
                screen.fill(BLACK)
                draw_text(str(3 - elapsed_time), font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
                pygame.draw.rect(screen, WHITE, left_paddle)
                pygame.draw.rect(screen, WHITE, right_paddle)
                pygame.display.flip()

                # Manejar eventos para permitir pausa
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # Pausar el juego
                            pause_game()
                            countdown_start_time = pygame.time.get_ticks()  # Ajustar el inicio del conteo tras pausar

                # Movimiento de las paletas
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and left_paddle.top > 0:
                    left_paddle.y -= paddle_speed
                if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
                    left_paddle.y += paddle_speed
                if keys[pygame.K_UP] and right_paddle.top > 0:
                    right_paddle.y -= paddle_speed
                if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                    right_paddle.y += paddle_speed

                #Limita 60 FPS
                clock.tick(60)

        # Movimiento de la bola
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Rebotes en la parte superior e inferior
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]
            ball_speed[0] += 0.2 * (-1 if ball_speed[0] < 0 else 1)  # Pequeño ajuste en X

        # Detección de colisiones con las paletas
        if ball.colliderect(left_paddle):
            offset = (ball.centery - left_paddle.centery) / (paddle_height / 2)
            ball_speed[0] = abs(ball_speed[0])  # Asegurar dirección hacia la derecha
            ball_speed[1] += offset * 3  # Ajustar sensibilidad
            ball_speed[1] = max(min(ball_speed[1], 8), -8)  # Limitar velocidad vertical
        if ball.colliderect(right_paddle):
            offset = (ball.centery - right_paddle.centery) / (paddle_height / 2)
            ball_speed[0] = -abs(ball_speed[0])  # Asegurar dirección hacia la izquierda
            ball_speed[1] += offset * 3  # Ajustar sensibilidad
            ball_speed[1] = max(min(ball_speed[1], 8), -8)  # Limitar velocidad vertical

        # Rebote con efecto spin
        if ball.colliderect(left_paddle):
            if keys[pygame.K_w]:  # Si la paleta se mueve hacia arriba
                ball_speed[1] -= 2
            if keys[pygame.K_s]:  # Si la paleta se mueve hacia abajo
                ball_speed[1] += 2

        # Movimiento suave con fricción
        target_y = left_paddle.y
        if keys[pygame.K_w]:
            target_y -= paddle_speed
        if keys[pygame.K_s]:
            target_y += paddle_speed
        target_y = max(0, min(target_y, HEIGHT - left_paddle.height))
        left_paddle.y += (target_y - left_paddle.y) * 0.2
        left_paddle.y = max(0, min(left_paddle.y, HEIGHT - left_paddle.height))

        # Detección de puntuaciones
        if ball.left <= 0:  # Punto para la derecha
            right_score += 1
            ball.x, ball.y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_speed = [4, 4]
            countdown_start_time = pygame.time.get_ticks()
            countdown_running = True
        if ball.right >= WIDTH:  # Punto para la izquierda
            left_score += 1
            ball.x, ball.y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_speed = [-4, -4]
            countdown_start_time = pygame.time.get_ticks()
            countdown_running = True

        # Winner
        if singleplayer:
            if left_score >= 11 and left_score - right_score >= 2:
                show_winner(screen, "Player", left_score, right_score, font, small_font)
                running = False
            elif right_score >= 11 and right_score - left_score >= 2:
                show_winner(screen, "CPU", left_score, right_score, font, small_font)
                running = False
            elif left_score >= 10 and right_score >= 10:
                # Continúa hasta que haya una diferencia de 2 puntos
                if abs(left_score - right_score) >= 2:
                    if left_score > right_score:
                        show_winner(screen, "Player", left_score, right_score, font, small_font)
                        running = False
                    else:
                        show_winner(screen, "CPU", left_score, right_score, font, small_font)
                        running = False
        else:
            if left_score >= 11 and left_score - right_score >= 2:
                show_winner(screen, "Player 1", left_score, right_score, font, small_font)
                running = False
            elif right_score >= 11 and right_score - left_score >= 2:
                show_winner(screen, "Player 2", left_score, right_score, font, small_font)
                running = False
            elif left_score >= 10 and right_score >= 10:
                # Continúa hasta que haya una diferencia de 2 puntos
                if abs(left_score - right_score) >= 2:
                    if left_score > right_score:
                        show_winner(screen, "Player 1", left_score, right_score, font, small_font)
                        running = False
                    else:
                        show_winner(screen, "Player 2", left_score, right_score, font, small_font)
                        running = False

        # Dibujar todo
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Dibujar el marcador
        draw_text(str(left_score), font, WHITE, screen, WIDTH // 4, 50)
        draw_text(str(right_score), font, WHITE, screen, 3 * WIDTH // 4, 50)

        pygame.display.flip()
        clock.tick(60)
        
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  # Tiempo en segundos

        # Aumento en el Contador la cantidad de cuadros que han pasado desde el inicio del juego o una acción específica.
        frame_count += 1


# Lógica principal
game_mode = show_menu()
if game_mode == "singleplayer":
    # Selección de dificultad
    difficulty = show_difficultys()
    # Asignar velocidad de la IA según dificultad
    if difficulty == 0:  # Easy
        ai_speed = 2
        ai_reaction_time = 20  # Mayor retraso
        precision_offset = 40  # IA más imprecisa
        error_chance = 0.5  # 50% de ignorar el movimiento
    elif difficulty == 1:  # Normal
        ai_speed = 3.5
        ai_reaction_time = 10
        precision_offset = 20
        error_chance = 0.3
    elif difficulty == 2:  # Hard
        ai_speed = 5
        ai_reaction_time = 5  # Manor retraso
        precision_offset = 10  # IA más precisa
        error_chance = 0.1  # Siempre intenta alcanzar la bola

    # Iniciar juego en modo Singleplayer
    main_game(singleplayer=True, ai_speed=ai_speed, ai_reaction_time=ai_reaction_time, precision_offset=precision_offset, error_chance=error_chance)

elif game_mode == "multiplayer":
    # Iniciar juego en modo Multiplayer
    main_game(singleplayer=False, ai_speed=None, ai_reaction_time=None, precision_offset=None, error_chance=None)