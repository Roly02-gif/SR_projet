import pygame
import socket
import threading
import json

# Configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080
WIDTH, HEIGHT = 800, 600

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

# Global variables for game state
num_player = -1
players = []
sweets = []
player_id = 0
player_score = 0
in_menu = True  # State to check if in menu
in_end_screen = False  # State to check if in end screen
already_end_screen = False

def receive_data():
    global players, sweets, player_id, player_score, in_end_screen
    buffer = ""
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            
            buffer += data
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                
                if message.find("{") == -1:
                    print(message)
                    player_id = message
                    continue
                
                print(message)
                game_state = json.loads(message)
                players = game_state["player_list"]
                sweets = game_state["sweets"]
                
                if player_id is not None:
                    for player in players:
                        if int(player["id_player"]) == int(player_id):
                            player_score = player["score"]
                            break
                
                if in_end_screen:
                    if game_state.get("start", True):
                        in_end_screen = False
                if not game_state.get("start", True):
                    if not already_end_screen:
                        in_end_screen = True
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

# Start receiving thread
threading.Thread(target=receive_data, daemon=True).start()

def draw_menu():
    screen.fill((0, 0, 0))
    title_text = font.render("Bienvenue dans le jeu!", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    
    play_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_button)
    play_text = font.render("Jouer", True, (0, 0, 0))
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 + 10))
    
    return play_button

def get_winner():
    max_score = -1
    winner_id = -1
    for player in players:
        if player["score"] > max_score:
            max_score = player["score"]
            winner_id = player["id_player"]
    return winner_id, max_score

def has_highest_score():
    """
    Vérifie si le joueur actuel a le score le plus élevé.
    """
    if not players:
        return False
    max_score = max(player["score"] for player in players)
    return player_score == max_score

def draw_end_screen():
    screen.fill((0, 0, 0))
    winner_id, max_score = get_winner()
    
    if int(winner_id) == int(player_id):
        end_text = font.render("Vous avez gagné!", True, (255, 255, 255))
    else:
        end_text = font.render(f"Vous avez perdu! Le gagnant est le joueur {winner_id}", True, (255, 255, 255))
    
    screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 3))
    
    restart_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
    pygame.draw.rect(screen, (255, 0, 0), restart_button)
    restart_text = font.render("Restart", True, (0, 0, 0))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
    
    return restart_button

running = True
while running:
    if in_menu:
        play_button = draw_menu()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    sock.send("init".encode())
                    in_menu = False
    elif in_end_screen:
        restart_button = draw_end_screen()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    sock.send("restart".encode())
                    already_end_screen = False
                    in_end_screen = False
                    in_menu = False
    else:
        already_end_screen = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            sock.send("up".encode())
        if keys[pygame.K_DOWN]:
            sock.send("down".encode())
        if keys[pygame.K_LEFT]:
            sock.send("left".encode())
        if keys[pygame.K_RIGHT]:
            sock.send("right".encode())

        # Draw game elements
        screen.fill((0, 0, 0))
        
        for player in players:
            x = int(player["pos_x"])
            y = int(player["pos_y"])
            # Dessiner le joueur actuel en blanc, les autres en rouge
            if int(player["id_player"]) == int(player_id):
                pygame.draw.circle(screen, (255, 255, 255), (x, y), 10)  
            else:
                pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)  

        for sweet in sweets:
            x = int(sweet["pos_x"])
            y = int(sweet["pos_y"])
            pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)
        
        # Afficher le score en jaune si le joueur a le meilleur score, sinon en blanc
        if has_highest_score():
            score_text = font.render(f"Score: {player_score}", True, (255, 255, 0)) 
        else:
            score_text = font.render(f"Score: {player_score}", True, (255, 255, 255)) 
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(30)

pygame.quit()