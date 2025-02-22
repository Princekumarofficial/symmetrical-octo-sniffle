import socket
import threading
import sys
from datetime import datetime
from typing import Dict, Tuple

class Peer:
    """
    A class to represent a peer in a peer-to-peer network.
    
    Attributes:
    -----------
    name : str
        The name of the peer.
    port : int
        The port number on which the peer listens for incoming connections.
    peers : dict
        A dictionary to store connected peers with their connection time.
    socket : socket.socket
        The socket object for the peer.
    running : bool
        A flag to indicate whether the peer is running.
    """
    
    def __init__(self, name: str, port: int) -> None:
        """
        Initialize the peer with a name and port number.
        
        Parameters:
        -----------
        name : str
            The name of the peer.
        port : int
            The port number on which the peer listens for incoming connections.
        """
        self.name: str = name
        self.port: int = port
        self.peers: Dict[Tuple[str, int], datetime] = {}  # Dictionary to store connected peers {(ip, port): connection_time}
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running: bool = True
        
    def start_server(self) -> None:
        """Start the server to listen for incoming connections."""
        self.socket.bind(('', self.port))
        self.socket.listen(5)
        print(f"Server listening on port {self.port}")
        
        # Start thread to handle incoming connections
        receive_thread = threading.Thread(target=self.receive_connections)
        receive_thread.start()
        
    def receive_connections(self) -> None:
        """Handle incoming connections from peers."""
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                # Start a new thread to handle this client's messages
                client_thread = threading.Thread(
                    target=self.handle_peer,
                    args=(client_socket, address)
                )
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"\nError accepting connection: {str(e)}")
                break
                
    def handle_peer(self, client_socket: socket.socket, address: Tuple[str, int]) -> None:
        """
        Handle messages from a connected peer.
        
        Parameters:
        -----------
        client_socket : socket.socket
            The socket object for the connected peer.
        address : tuple
            The address of the connected peer.
        """
        peer_addr: Tuple[str, int] = (address[0], address[1])
        self.peers[peer_addr] = datetime.now()
        
        while self.running:
            try:
                message = client_socket.recv(1024).decode()
                decoded_message = message.split('CipherSurge')[-1].strip()
                if message:
                    if decoded_message.lower() == 'exit':
                        print(f"\nPeer {address[0]}:{address[1]} disconnected")
                        del self.peers[peer_addr]
                        client_socket.close()
                        break
                    print(f"\n{message}")
                    self.display_menu()
                else:
                    break
            except Exception as e:
                print(f"Error handling peer {address[0]}:{address[1]}: {str(e)}")
                break
                
        if peer_addr in self.peers:
            del self.peers[peer_addr]
        client_socket.close()
        
    def send_message(self, ip: str, port: int, message: str) -> None:
        """
        Send a message to a specific peer.
        
        Parameters:
        -----------
        ip : str
            The IP address of the recipient peer.
        port : int
            The port number of the recipient peer.
        message : str
            The message to be sent.
        """
        try:
            # Create a new socket for sending the message
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))

            message = f"{ip}:{port} CipherSurge {message}"
            
            # Send the message
            client_socket.send(message.encode())
            print(f"Message sent to {ip}:{port}")
            
            # Add to peers list if not an exit message
            if message.lower() != 'exit':
                self.peers[(ip, port)] = datetime.now()
            
            client_socket.close()
            
        except Exception as e:
            print(f"Error sending message to {ip}:{port}: {str(e)}")
            
    def query_peers(self) -> None:
        """Display list of connected peers."""
        if not self.peers:
            print("No connected Peers")
        else:
            print("Connected Peers:")
            for i, ((ip, port), _) in enumerate(self.peers.items(), 1):
                print(f"{i}. {ip}:{port}")
                
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query connected peers")
        print("0. Quit")
        print("Enter choice: ", end='')
        
    def run(self) -> None:
        """Main loop to handle user input."""
        self.start_server()
        
        while self.running:
            self.display_menu()
            try:
                choice = input().strip()
                
                if choice == '1':
                    ip = input("Enter the recipient's IP address: ")
                    port = int(input("Enter the recipient's port number: "))
                    message = input("Enter your message: ")
                    self.send_message(ip, port, message)
                    
                elif choice == '2':
                    self.query_peers()
                    
                elif choice == '0':
                    print("Exiting")
                    self.running = False
                    self.socket.close()
                    sys.exit(0)
                    
            except ValueError:
                print("Invalid input. Please try again.")
            except Exception as e:
                print(f"Error: {str(e)}")

def main() -> None:
    """Initialize and start the peer."""
    name = input("Enter your name: ")
    port = int(input("Enter your port number: "))
    
    peer = Peer(name, port)
    try:
        peer.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        peer.running = False
        peer.socket.close()
        sys.exit(0)

if __name__ == "__main__":
    main()