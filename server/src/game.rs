use rand::Rng;
use player::Player;
use sweet::Sweet;

#[path = "player.rs"] mod player;
#[path = "sweet.rs"] mod sweet;

#[derive(serde::Serialize)]
#[derive(Clone)]
pub struct Game{
    player_list: Vec<player::Player>,
    start: bool,
    sweets: Vec<sweet::Sweet>
}

pub enum Command{
    Up ,
    Down,
    Left,
    Right,
}

impl Game {
    //Constructor
    pub fn new(player_list: Vec<player::Player>, start:bool, sweets: Vec<sweet::Sweet>) -> Self {
        Self{player_list, start, sweets}
    }

    pub fn create_player(&mut self, id_player: i32) {
        let (pos_x, pos_y) = (rand::rng().random_range(100.0..=800.0), rand::rng().random_range(100.0..=600.0));
        let player = player::Player::new(id_player, pos_x, pos_y, 0);
        self.player_list.push(player);
    }
    
    pub fn delete_player(&mut self,id_player: i32)-> &mut Game{
        for i in 0..self.player_list.len() {
            if self.player_list[i].get_id_player() == id_player {
                self.player_list.remove(i);
            }
        }
        return self;
    }
    pub fn get_players(&self) -> &Vec<player::Player> {
        return &self.player_list;
    } 

    pub fn get_player(&self, id_player: i32) -> Option<&Player> {

        for _player in &self.player_list {
            if _player.get_id_player() == id_player {
                return Some(_player);
            }
        }
        None
    }

    pub fn restart_game(&mut self) {
        self.sweets.clear();
        
        for _ in 0..self.player_list.iter().len() {
            self.add_sweets();
        }
        for player in self.player_list.iter_mut() {
            player.reset_score(); 
            player.update_position(rand::rng().random_range(100.0..=800.0), rand::rng().random_range(100.0..=600.0));
        }
        self.start = true;   
    }

    pub fn update_player_position(&mut self, id_player: i32, cmd: &str) {
        if cmd == "restart" {
            if !self.start {
                self.restart_game();
            }
            return;
        }

        let player_list_clone = self.player_list.clone();
        if let Some(player) = self.player_list.iter_mut().find(|p| p.get_id_player() == id_player) {
            let current_x = player.get_x();
            let current_y = player.get_y();
            let mut new_x = current_x;
            let mut new_y = current_y;
            let step = 5.0;

            match cmd {
                "up" => new_y -= step,
                "down" => new_y += step,
                "left" => new_x -= step,
                "right" => new_x += step,
                _ => eprintln!("Invalid command: {}", cmd),
            }
            
            let collision_radius = 10.0;
            let screen_width = 800.0;
            let screen_height = 600.0;
            
            if new_x < collision_radius {
                new_x = collision_radius;
            } else if new_x > screen_width - collision_radius {
                new_x = screen_width - collision_radius;
            }
            if new_y < collision_radius {
                new_y = collision_radius;
            } else if new_y > screen_height - collision_radius {
                new_y = screen_height - collision_radius;
            }

            let collision_detected = player_list_clone.iter().any(|other| {
                if other.get_id_player() != id_player {
                    let dx = new_x - other.get_x();
                    let dy = new_y - other.get_y();
                    let distance = (dx * dx + dy * dy).sqrt();
                    distance < (collision_radius * 2.0)
                } else {
                    false
                }
            });

            if !collision_detected {
                player.update_position(new_x, new_y);
            } else {
                eprintln!("Collision entre joueurs détectée, déplacement annulé pour le joueur {}", id_player);
            }


            self.sweets.retain(|sweet| {
                let dx = sweet.get_x() - player.get_x();
                let dy = sweet.get_y() - player.get_y();
                let distance = (dx * dx + dy * dy).sqrt();
                if distance < 10.0 {
                    player.update_score();
                    false // Remove sweet
                } else {
                    true // Keep sweet
                }
            });

            // Game over (no sweets)
            if self.sweets.is_empty() {
                self.start = false;
            }
            

        } else {
            eprintln!("Player with id {:?} not found", id_player);
        }

    }

    pub fn add_sweets(&mut self) {
        for _i in 0..5 {
            let new_sweet = Sweet::new(rand::rng().random_range(100.0..=800.0), rand::rng().random_range(100.0..=600.0));
            self.sweets.push(new_sweet);
        }
    }

    pub fn get_sweets(&self) -> &Vec<sweet::Sweet> {
        return &self.sweets;
    }


}