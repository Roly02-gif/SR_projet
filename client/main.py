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
font = pygame.font.Font(None, 36)  # Police pour afficher le score

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

# Global variables for game state
players = []
sweets = []
player_id = None
player_score = 0

def receive_data():
    global players, sweets, player_id, player_score
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            game_state = json.loads(data)
            players = game_state["player_list"]
            sweets = game_state["sweets"]

            # Update player score
            if player_id is not None:
                for player in players:
                    if player["id_player"] == player_id:
                        player_score = player["score"]
                        break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

# Start receiving thread
threading.Thread(target=receive_data, daemon=True).start()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        sock.send("up".encode())
    elif keys[pygame.K_DOWN]:
        sock.send("down".encode())
    elif keys[pygame.K_LEFT]:
        sock.send("left".encode())
    elif keys[pygame.K_RIGHT]:
        sock.send("right".encode())

    # Draw everything
    screen.fill((0, 0, 0))

    # Draw players
    for player in players:
        x = int(player["pos_x"])
        y = int(player["pos_y"])
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 10)

    # Draw sweets
    for sweet in sweets:
        x = int(sweet["pos_x"])
        y = int(sweet["pos_y"])
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 5)

    # Draw player score
    score_text = font.render(f"Score: {player_score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()