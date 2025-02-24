# Team members :- 
- Prince Kumar 230051013
- Vikrant 230001082
- Yash Vijay Kumbhkarn 230001083

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
   git clone https://github.com/Princekumarofficial/symmetrical-octo-sniffle
   cd symmetrical-octo-sniffle
   ```
2. Run the script:
   ```sh
   python main.py
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
Enter your name: P1
Enter your port number: 8080
Server listening on port 8080

***** Menu *****
1. Send message
2. Query connected peers
0. Quit
Enter choice:
127.0.0.1:8080 CipherSurge Hi

***** Menu *****
1. Send message
2. Query connected peers
0. Quit
Enter choice:
```

## Known Issues & Improvements

- Could add encryption for more secure communication.
- Improve UI with a graphical interface.

---
