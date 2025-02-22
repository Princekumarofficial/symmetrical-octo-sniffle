# Peer-to-Peer Chat System

## Overview
This is a simple Peer-to-Peer (P2P) chat system that allows multiple users to connect and exchange messages over a network. Each peer acts as both a client and a server, enabling direct communication without a central server.

## Features
- Start a peer server to accept connections
- Send messages to other peers using their IP and port
- Handle multiple connections using threading
- Display a list of currently connected peers
- Simple text-based menu for easy interaction

## How It Works
1. Each peer runs the script and provides their name and port number.
2. The peer starts listening for incoming connections.
3. Users can send messages to other peers by entering their IP and port.
4. Messages are exchanged in real time, and peers can disconnect by sending an `exit` message.

## Installation
### Prerequisites
- Python 3.x

### Steps to Run
1. Clone this repository:
   ```sh
   git clone https://github.com/yourusername/peer-to-peer-chat.git
   cd peer-to-peer-chat
   ```
2. Run the script:
   ```sh
   python peer_chat.py
   ```
3. Enter your name and the port number to start the peer.
4. Use the menu options to send messages or check connected peers.

## Usage
### Commands
- `1` → Send a message
- `2` → Query connected peers
- `0` → Exit the chat

### Example Interaction
```sh
Enter your name: Alice
Enter your port number: 5000
Server listening on port 5000

***** Menu *****
1. Send message
2. Query connected peers
0. Quit
Enter choice: 1
Enter the recipient's IP address: 192.168.1.10
Enter the recipient's port number: 5001
Enter your message: Hello from Alice!
Message sent to 192.168.1.10:5001
```
```sh
Enter your name: Alice
Enter your port number: 5000
Server listening on port 5000

***** Menu *****
1. Send message
2. Query connected peers
0. Quit
Enter choice: 2
Connected Peers:
1. 192.168.1.10:5001
2. 192.168.1.15:5002
```
## Known Issues & Improvements
- Currently, peers are not automatically removed if they unexpectedly disconnect.
- Could add encryption for more secure communication.
- Improve UI with a graphical interface.

## Contributing
Feel free to fork the repository, create a new branch, and submit a pull request with any improvements or bug fixes!

## License
This project is open-source and available under the MIT License.

---
Happy chatting! 🎉
