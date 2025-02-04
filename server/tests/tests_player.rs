#[cfg(test)]
mod tests {
    use sr_project::player::Player;
    
    #[test]
    fn test_create_player() {
        let player = Player::new(1, 50.0, 50.0, 0);
        assert_eq!(player.get_id_player(), 1);
        assert_eq!(player.get_x(), 50.0);
        assert_eq!(player.get_y(), 50.0);
        assert_eq!(player.get_score(), 0);
    }
    
    #[test]
    fn test_update_position() {
        let mut player = Player::new(2, 100.0, 200.0, 0);
        player.update_position(150.0, 250.0);
        assert_eq!(player.get_x(), 150.0);
        assert_eq!(player.get_y(), 250.0);
    }

    #[test]
    fn test_update_score() {
        let mut player = Player::new(3, 0.0, 0.0, 5);
        player.update_score();
        assert_eq!(player.get_score(), 6);
    }
    
}