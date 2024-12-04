import pygame
import sys

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

# Función para mostrar el menú
def show_menu():
    while True:
        screen.fill(BLACK)

        # Título del juego
        draw_text("Pong Game", font, WHITE, screen, WIDTH // 2, HEIGHT // 3)

        # Opciones del menú
        draw_text("Press ENTER to Play", small_font, GRAY, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to Quit", small_font, GRAY, screen, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()

        # Manejo de eventos del menú
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter para iniciar
                    return  # Salir del menú y empezar el juego
                if event.key == pygame.K_ESCAPE:  # Esc para salir
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
def main_game():
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

    # Reloj para controlar la velocidad del juego
    clock = pygame.time.Clock()

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
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        # Movimiento de la bola
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Rebotes en la parte superior e inferior
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] = -ball_speed[1]

        # Detección de colisiones con las paletas
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed[0] = -ball_speed[0]

         # Detección de puntuaciones
        if ball.left <= 0:  # Punto para la derecha
            right_score += 1
            ball.x, ball.y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_speed = [4, 4]
        if ball.right >= WIDTH:  # Punto para la izquierda
            left_score += 1
            ball.x, ball.y = WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2
            ball_speed = [-4, -4]

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

# Lógica principal
show_menu()
main_game()
