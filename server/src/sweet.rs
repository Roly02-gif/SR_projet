#[derive(Copy, Clone)]
#[derive(serde::Serialize)]
#[derive(Debug)]
pub struct Sweet {
    pos_x: f64,
    pos_y: f64,
}

impl Sweet {
    pub fn new(pos_x: f64, pos_y: f64) -> Self {
        Self{pos_x, pos_y}
    }

    pub fn get_x(&self) -> f64{
        return self.pos_x;
    }

    pub fn get_y(&self) -> f64{
        return self.pos_y;
    }
}