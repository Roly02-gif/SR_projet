#[derive(serde::Serialize)]
#[derive(Debug)]
#[derive(Copy, Clone)]
pub struct Player{
    id_player: i32,
    pos_x: f64,
    pos_y: f64,
    score: i32
}

impl Player {
    //Constructor
    pub fn new(id_player: i32, pos_x: f64, pos_y: f64, score: i32) -> Self {
        Self{id_player, pos_x, pos_y, score}
    }

    pub fn get_id_player(self) -> i32{
        return self.id_player;
    }
    // Update player's position
    pub fn update_position(&mut self, new_x: f64, new_y: f64) {
        self.pos_x = new_x;
        self.pos_y = new_y;
    }

    // Update the player's score
    pub fn update_score(&mut self) {
        self.score += 1;
    }

    // Display player information
    pub fn display_info(&self) {
        println!("Player: {:?}, Position: ({}, {}), Score: {}",
            self.id_player, self.pos_x, self.pos_y, self.score);
    }

    pub fn get_x(&self) -> f64{
        return self.pos_x;
    }

    pub fn get_y(&self) -> f64 {
        return self.pos_y;
    }
    pub fn reset_score(&mut self){
        self.score=0;
    }


}