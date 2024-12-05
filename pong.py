import pygame
import sys
import time

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
def main_game(singleplayer):
    # Paletas y bola
    paddle_width, paddle_height = 20, 100
    ball_size = 20

    left_paddle = pygame.Rect(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    right_paddle = pygame.Rect(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
    ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)

    # Velocidades
    ball_speed = [4, 4]
    paddle_speed = 5
    ai_speed = 4  # Velocidad de la IA

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

    while True:
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

        if singleplayer:
            # Movimiento de la IA
            if ball.centery < right_paddle.centery and right_paddle.top > 0:
                right_paddle.y -= ai_speed
            if ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
                right_paddle.y += ai_speed
        else:
            # Movimiento del jugador 2
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed

        # Movimiento de la bola, rebotes, puntuación, etc. (mantén el código existente aquí)


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

                clock.tick(60)

        # Movimiento de la bola
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Rebotes en la parte superior e inferior
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Detección de colisiones con las paletas
        if ball.colliderect(left_paddle):
            ball_speed[0] = abs(ball_speed[0])  # Asegurar que la bola vaya hacia la derecha
            ball_speed[1] += (ball.centery - left_paddle.centery) * 0.05  # Cambiar ángulo
        if ball.colliderect(right_paddle):
            ball_speed[0] = -abs(ball_speed[0])  # Asegurar que la bola vaya hacia la izquierda
            ball_speed[1] += (ball.centery - right_paddle.centery) * 0.05  # Cambiar ángulo

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
        
        # Incrementar la velocidad cada 5 segundos
        if elapsed_time > 0 and elapsed_time % 5 == 0:
            ball_speed[0] *= 1.05
            ball_speed[1] *= 1.05
            start_time = pygame.time.get_ticks()  # Reiniciar el tiempo

# Lógica principal
game_mode = show_menu()
if game_mode == "singleplayer":
    main_game(singleplayer=True)
elif game_mode == "multiplayer":
    main_game(singleplayer=False)
