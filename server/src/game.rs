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

    pub fn update_player_position(&mut self, id_player: i32, cmd: &str) {
        if let Some(player) = self.player_list.iter_mut().find(|p| p.get_id_player() == id_player) {
            let pos_x = player.get_x();
            let pos_y = player.get_y();
            match cmd {
                "up" => player.update_position(pos_x, pos_y - 5.0),
                "down" => player.update_position(pos_x, pos_y + 5.0),
                "left" => player.update_position(pos_x - 5.0, pos_y),
                "right" => player.update_position(pos_x + 5.0, pos_y),
                _ => eprintln!("Invalid command: {}", cmd),
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
            eprintln!("Player with address {:?} not found", id_player);
        }

    }

    pub fn add_sweets(&mut self) {
        for _i in 0..5 {
            let new_sweet = Sweet::new(rand::rng().random_range(100.0..=800.0), rand::rng().random_range(100.0..=600.0));
            self.sweets.push(new_sweet);
        }
    }


}