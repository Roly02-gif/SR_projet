#[cfg(test)]
mod tests {
    use sr_project::game::Game;
    
    #[test]
    fn test_create_game() {
        let game = Game::new(vec![], true, vec![]);
        assert_eq!(game.get_players().len(), 0);
    }
    
    #[test]
    fn test_add_and_remove_player() {
        let mut game = Game::new(vec![], true, vec![]);
        game.create_player(1);
        assert_eq!(game.get_players().len(), 1);
        game.delete_player(1);
        assert_eq!(game.get_players().len(), 0);
    }

    #[test]
    fn test_update_player_position() {
        let mut game = Game::new(vec![], true, vec![]);
        game.create_player(1);
        let init_pos_x = game.get_players()[0].get_x();
        game.update_player_position(1, "right");
        let player = game.get_player(1).unwrap();
        assert_eq!(player.get_x(), init_pos_x+5.0);
    }

    #[test]
    fn test_add_sweet() {
        let mut game = Game::new(vec![], true, vec![]);
        game.add_sweets();
        assert_eq!(game.get_sweets().len(), 5);
    }
    


}