pub mod player;
pub mod game;
pub mod sweet;

use std::borrow::Cow;
use std::io::{self, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::thread;

use game::Game;

#[tokio::main]
async fn main() -> io::Result<()>  {
    let game = Arc::new(Mutex::new(Game::new(vec![], false, vec![])));
    let sockets: Arc<Mutex<Vec<TcpStream>>> = Arc::new(Mutex::new(vec![]));
    let listener = TcpListener::bind("127.0.0.1:8080").unwrap();

    //Game initialisation
    let mut id_player = 0;
    //Waiting for connection
    loop {
        match listener.accept() {
            Ok((socket, addr)) => {
                println!("new client: {:?}", addr);
                id_player +=1;

                // Ajouter le socket à la liste partagée
                let socket_clone = socket.try_clone()?;
                {
                    let mut sockets_guard = sockets.lock().unwrap();
                    sockets_guard.push(socket_clone);
                }
                
                {
                    let mut game_lock = game.lock().unwrap();
                    game_lock.create_player(id_player);
                    game_lock.add_sweets();
                }
                

                // Créer un thread pour gérer la connexion
                let game_clone = Arc::clone(&game);
                let sockets_thread = Arc::clone(&sockets);

                thread::spawn(move || {
                    handle_connection(id_player, socket, game_clone, sockets_thread)
                });
            },
                        Err(e) => println!("couldn't get client: {:?}", e),
        }   
    }

   
} 

fn handle_connection(id_player: i32, mut socket: TcpStream, game: Arc<std::sync::Mutex<Game>>, sockets: Arc<Mutex<Vec<TcpStream>>> ) {
    

        let mut buffer = [0; 1024];
        let client_addr = socket.peer_addr().expect("error addr");
        loop {
            match socket.read(&mut buffer) {
                Ok(0) => {
                    println!("Le client {:?} s'est déconnecté", client_addr);
                    break;
                }
                Ok(size) => {
                    let message = String::from_utf8_lossy(&buffer[..size]);
                    let game_lock = game.lock().unwrap();
                    let game_state = exec_cmd(message, id_player, game_lock);

                    //serialize game state to JSON
                    let response = serde_json::to_string(&*game_state).unwrap();
                    //println!("Message reçu de {:?}", response);

                    // Diffuser le message à tous les sockets
                    let sockets_guard = sockets.lock().unwrap();
                    for mut client_socket in sockets_guard.iter() {
                        if let Err(e) = client_socket.write_all(response.as_bytes()) {
                            eprintln!("Erreur lors de l'envoi du message : {:?}", e);
                        }
                    }
                }
                Err(e) => {
                    eprintln!("Erreur lors de la lecture depuis {:?} : {}", client_addr, e);
                    break;
                }
            }
        }
    

}

fn exec_cmd<'a>(message : Cow<'a, str>, id_player: i32, mut game: std::sync::MutexGuard<'a, Game>) -> std::sync::MutexGuard<'a, Game> {
    let str_message = message.into_owned();
    match str_message.as_str() {
        "up" => {
            game.update_player_position(id_player, str_message.as_str())
        }
        "down" => {
            game.update_player_position(id_player, str_message.as_str())
        }
        "left" => {
            game.update_player_position(id_player, str_message.as_str())
        }
        "right" => {
            game.update_player_position(id_player, str_message.as_str())
        }
        _ => {
            // Gérer d'autres commandes ou cas par défaut
            println!("Invalid command: {}", str_message);
        }
    }
    return game;
}

