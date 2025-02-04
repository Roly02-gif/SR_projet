use std::io::{Read, Write};
use std::net::TcpStream;
use std::{thread, time};
use rand::Rng;

fn start_bot(id: usize) {
    let mut stream = TcpStream::connect("127.0.0.1:8080").expect("Impossible de se connecter au serveur");

    let mut buffer = [0; 1024];

    // Lire l'ID envoyé par le serveur
    let size = stream.read(&mut buffer).unwrap_or(0);
    if size == 0 {
        println!("Bot {}: déconnecté immédiatement", id);
        return;
    }
    let id_joueur = String::from_utf8_lossy(&buffer[..size]);
    println!("Bot {}: connecté avec ID {}", id, id_joueur);

    if let Err(_) = stream.write_all(b"init") {
        println!("Bot {}: Erreur lors de l'envoi de 'init'", id);
        return;
    }

    // Lire la réponse après l'initialisation
    let _ = stream.read(&mut buffer);

    let commands = ["up", "down", "left", "right"];

    //Random move
    loop {
        let mut rng = rand::rng();
        let command = commands[rng.random_range(0..commands.len())]; // Choix aléatoire

       
        if let Err(_) = stream.write_all(command.as_bytes()) {
            println!("Bot {}: Erreur lors de l'envoi de '{}'", id, command);
            break;
        }

        // Pause aléatoire pour simuler un joueur humain
        let duration = time::Duration::from_millis(rng.random_range(500..1500));
        thread::sleep(duration);

        // Lire l'état du jeu
        let size = stream.read(&mut buffer).unwrap_or(0);
        if size == 0 {
            println!("Bot {}: Déconnecté du serveur", id);
            break;
        }

        // Affichage de la réponse
        let response = String::from_utf8_lossy(&buffer[..size]);
        println!("Bot {}: état du jeu {}", id, response);
    }
}

fn main() {
    let num_bots = 1000; 

    let mut handles = vec![];

    for i in 0..num_bots {
        handles.push(thread::spawn(move || {
            start_bot(i);
        }));
    }

    // Attendre la fin de tous les bots
    for handle in handles {
        handle.join().unwrap();
    }
}