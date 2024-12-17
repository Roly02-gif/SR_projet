import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Couleurs
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Dimensions des carrés
SQUARE_SIZE = 50

# Vitesse de déplacement des carrés
PLAYER_SPEED = 5
BOT_SPEED = 3

# Paramètres des ronds
CIRCLE_RADIUS = 15
NUM_CIRCLES = 20

# Configuration de la police pour le texte
font = pygame.font.SysFont(None, 36)

# Variables globales
game_started = False  # Indique si le jeu a commencé

def reset_game():
    """Réinitialise le jeu."""
    global player_x, player_y, bot_x, bot_y, circles, player_score, bot_score, game_over, winner
    # Position initiale du joueur rouge (à droite)
    player_x = SCREEN_WIDTH - SQUARE_SIZE - 10
    player_y = SCREEN_HEIGHT // 2 - SQUARE_SIZE // 2

    # Position initiale du bot vert (à gauche)
    bot_x = 10
    bot_y = SCREEN_HEIGHT // 2 - SQUARE_SIZE // 2

    # Génération aléatoire des positions des cercles
    circles = [
        (random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS),
         random.randint(CIRCLE_RADIUS, SCREEN_HEIGHT - CIRCLE_RADIUS))
        for _ in range(NUM_CIRCLES)
    ]
    player_score = 0
    bot_score = 0
    game_over = False
    winner = None

# Variables globales du jeu
reset_game()

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Carré Rouge et Ronds Bleus")

def draw_start_screen():
    """Affiche l'écran d'accueil."""
    screen.fill(BLACK)
    title_text = font.render("Carré Rouge et Ronds Bleus", True, WHITE)
    play_button_text = font.render("Jouer", True, BLACK)

    # Afficher le titre
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))

    # Dessiner le bouton "Jouer"
    play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 300, 200, 50)
    pygame.draw.rect(screen, GRAY, play_button_rect)
    screen.blit(play_button_text, (play_button_rect.x + play_button_rect.width // 2 - play_button_text.get_width() // 2,
                                   play_button_rect.y + play_button_rect.height // 2 - play_button_text.get_height() // 2))

    return play_button_rect

def handle_collision(rect1, rect2, dx, dy):
    """Gère les collisions entre deux rectangles.
    Si rect1 entre en collision avec rect2, on empêche rect1 de se déplacer dans la direction dx/dy.
    """
    if rect1.colliderect(rect2):
        if dx > 0:  # Déplacement à droite
            rect1.x = rect2.left - rect1.width
        elif dx < 0:  # Déplacement à gauche
            rect1.x = rect2.right
        if dy > 0:  # Déplacement vers le bas
            rect1.y = rect2.top - rect1.height
        elif dy < 0:  # Déplacement vers le haut
            rect1.y = rect2.bottom
    return rect1.x, rect1.y

# Boucle principale du jeu
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_started:  # Si le jeu n'a pas commencé, vérifier les clics sur le bouton
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                play_button_rect = draw_start_screen()
                if play_button_rect.collidepoint(event.pos):
                    game_started = True  # Commence la partie

        elif game_over:  # Si le jeu est terminé, vérifier les touches pour recommencer
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

    if not game_started:
        # Dessiner l'écran d'accueil
        play_button_rect = draw_start_screen()
    else:
        # Gestion des touches pour le déplacement (si le jeu n'est pas terminé)
        if not game_over:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0  # Déplacements horizontaux et verticaux
            if keys[pygame.K_UP]:
                dy -= PLAYER_SPEED
            if keys[pygame.K_DOWN]:
                dy += PLAYER_SPEED
            if keys[pygame.K_LEFT]:
                dx -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                dx += PLAYER_SPEED

            # Calcul de la nouvelle position du joueur
            player_x += dx
            player_y += dy

            # Empêcher le joueur rouge de sortir de la fenêtre
            player_x = max(0, min(SCREEN_WIDTH - SQUARE_SIZE, player_x))
            player_y = max(0, min(SCREEN_HEIGHT - SQUARE_SIZE, player_y))

            # Déplacement aléatoire du bot vert
            bot_dx, bot_dy = 0, 0
            bot_direction = random.choice(["up", "down", "left", "right"])
            if bot_direction == "up" and bot_y > 0:
                bot_dy -= BOT_SPEED
            if bot_direction == "down" and bot_y < SCREEN_HEIGHT - SQUARE_SIZE:
                bot_dy += BOT_SPEED
            if bot_direction == "left" and bot_x > 0:
                bot_dx -= BOT_SPEED
            if bot_direction == "right" and bot_x < SCREEN_WIDTH - SQUARE_SIZE:
                bot_dx += BOT_SPEED

            bot_x += bot_dx
            bot_y += bot_dy

            # Vérification des collisions entre le joueur et le bot
            player_rect = pygame.Rect(player_x, player_y, SQUARE_SIZE, SQUARE_SIZE)
            bot_rect = pygame.Rect(bot_x, bot_y, SQUARE_SIZE, SQUARE_SIZE)
            player_x, player_y = handle_collision(player_rect, bot_rect, dx, dy)
            bot_x, bot_y = handle_collision(bot_rect, player_rect, bot_dx, bot_dy)

            # Vérification des collisions entre les joueurs et les cercles
            new_circles = []
            for circle in circles:
                circle_rect = pygame.Rect(
                    circle[0] - CIRCLE_RADIUS, circle[1] - CIRCLE_RADIUS,
                    CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2
                )
                if player_rect.colliderect(circle_rect):
                    player_score += 1  # Incrémenter le score du joueur rouge
                elif bot_rect.colliderect(circle_rect):
                    bot_score += 1  # Incrémenter le score du bot vert
                else:
                    new_circles.append(circle)
            circles = new_circles

            # Vérifier si tous les ronds ont été collectés
            if not circles and not game_over:
                game_over = True
                if player_score > bot_score:
                    winner = "Joueur Rouge"
                elif bot_score > player_score:
                    winner = "Bot Vert"
                else:
                    winner = "Égalité"

        # Dessin à l'écran
        screen.fill(BLACK)  # Remplir l'écran avec du noir

        # Dessiner les carrés
        pygame.draw.rect(screen, RED, (player_x, player_y, SQUARE_SIZE, SQUARE_SIZE))  # Joueur rouge
        pygame.draw.rect(screen, GREEN, (bot_x, bot_y, SQUARE_SIZE, SQUARE_SIZE))  # Bot vert

        # Dessiner les cercles bleus
        for circle in circles:
            pygame.draw.circle(screen, BLUE, circle, CIRCLE_RADIUS)

        # Afficher les scores
        player_score_text = font.render(f"Rouge: {player_score}", True, WHITE)
        bot_score_text = font.render(f"Vert: {bot_score}", True, WHITE)
        screen.blit(player_score_text, (10, 10))
        screen.blit(bot_score_text, (10, 40))

        # Afficher le message de fin si le jeu est terminé
        if game_over:
            if winner == "Égalité":
                message_text = font.render(f"Égalité ! Appuyez sur R pour recommencer.", True, WHITE)
            else:
                message_text = font.render(f"{winner} gagne ! Appuyez sur R pour recommencer.", True, WHITE)
            screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2))

    # Mettre à jour l'écran
    pygame.display.flip()

    # Limiter la vitesse de la boucle (60 FPS)
    pygame.time.Clock().tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()