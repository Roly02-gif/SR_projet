use tokio::net::{TcpListener, TcpStream};

use std::io::{self};

#[tokio::main]
async fn main() -> io::Result<()> {
    println!("Server ...");
    let server = TcpListener::bind("127.0.0.1:8080").await?;

    match server.accept().await {
        Ok((_socket, addr)) => println!("new client: {:?}", addr),
                    Err(e) => println!("couldn't get client: {:?}", e),
    }

    Ok(())
}