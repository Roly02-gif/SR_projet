# 🎮 Sweets Collector - Distributed Multiplayer Game

This project aims to develop a multiplayer networked game where several players move around a shared map to collect "sweets" (candies). The player who collects the most sweets wins the match. The system is based on a robust client-server architecture, with a high-performance server written in Rust and an interactive client built with Python and Pygame.

## 📂 Repository Contents

- `client/`: Python client source code using Pygame.
- `server/`: Rust server source code.
- `test_charge_server/`: Load-test for rust server.
- `README.md`: This file.

## 🚀 Features

- 🔗 Simple and efficient client-server architecture.
- 🧠 Server built with Rust for high performance and memory safety.
- 🎮 Python/Pygame client with 2D graphical interface.
- 🧾 Real-time display of player scores, sweets, and connected players.
- ⚔️ Collision detection between players and objects.
- 📡 Regular synchronization between server and all clients.
- 👥 Real-time management of player connections and disconnections.

## ⚙️ Technologies Used

| Component | Language | Framework / Library |
|----------|----------|----------------------|
| Server   | Rust     | Tokio, Serde         |
| Client   | Python   | Pygame               |

## 🏗️ Architecture Overview

The system follows a **classic client-server model** :
```plaintext
          +-----------+   TCP(socket)    +-----------+
          |           |<---------------->|           |
          |  Client 1 |                  |           |
          | (Python + |                  |           |
          |  Pygame)  |                  |           |
          +-----------+                  |   Server  |
                                         |  (Rust)   |
          +-----------+                  |           |
          |           |<---------------->|           |
          |  Client 2 |   TCP(socket)    +-----------+
          |           |
          +-----------+
```
🔧 Server Responsibilities (Rust)
- Manage player connections and disconnections.
- Maintain the game state: player positions, sweets, scores.
- Detect collisions between players and sweets.
- Periodically broadcast the game state to all connected clients.
- Declare the winner at the end of the game.

🎨 Client Responsibilities (Python)
- Connect to the server and receive game state updates.
- Render the map, players, and sweets on screen.
- Capture user inputs (arrow keys) for player movement.
- Send movement commands to the server.
- Display real-time scores and the leaderboard.

## 🧪 Testing

- ✅ **Unit Tests** to validate game logic (game creation, movement, sweet collection, etc.).
- 🔁 **Load Testing** with 1000 simulated bots to evaluate server robustness and performance under stress.

## 🛠️ Potential Improvements

- ✨ New gameplay elements: power-ups, obstacles, additional game modes (co-op, time trial...).
- ⚙️ Server performance optimizations: caching, data compression, multi-server scaling.
- 🔐 Security enhancements: DoS protection, client data validation, cheat detection.

## 🧭 Running the Project

### Prerequisites

- 🦀 Rust installed ([https://www.rust-lang.org/](https://www.rust-lang.org/))
- 🐍 Python 3.x installed
- 📦 Pygame installed via pip:

```bash
pip install pygame
```
### Run the Server
```bash
cd server
cargo run
```

### Run the Client
```bash
cd client
python main.py
```

### Run the load-test
```bash
cd test_charge_server
cargo run
```

