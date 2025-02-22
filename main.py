import socket
import threading
import sys
from datetime import datetime

class Peer:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.peers = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = True
        
    def start_server(self):
        """Start the server to listen for incoming connections"""
        self.socket.bind(('', self.port))
        self.socket.listen(5)
        print(f"Server listening on port {self.port}")
        
        # Start thread to handle incoming connections
        receive_thread = threading.Thread(target=self.receive_connections)
        receive_thread.start()
        
    def receive_connections(self):
        """Handle incoming connections from peers"""
        while self.running:
            try:
                client_socket, address = self.socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_peer,
                    args=(client_socket, address)
                )
                client_thread.start()
            except:
                if self.running:
                    print("\nError accepting connection")
                break
                
    def handle_peer(self, client_socket, address):
        """Handle messages from a connected peer"""
        peer_addr = (address[0], address[1])
        self.peers[peer_addr] = datetime.now()
        
        while self.running:
            try:
                message = client_socket.recv(1024).decode()
                if message:
                    if message.lower() == 'exit':
                        print(f"\nPeer {address[0]}:{address[1]} disconnected")
                        del self.peers[peer_addr]
                        client_socket.close()
                        break
                    print(f"\nReceived from {address[0]}:{address[1]}: {message}")
                    self.display_menu()
                else:
                    break
            except:
                break
                
        if peer_addr in self.peers:
            del self.peers[peer_addr]
        client_socket.close()
        
    def send_message(self, ip, port, message):
        """Send a message to a specific peer"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))
            
            client_socket.send(message.encode())
            print(f"Message sent to {ip}:{port}")

            if message.lower() != 'exit':
                self.peers[(ip, port)] = datetime.now()
            
            client_socket.close()
            
        except Exception as e:
            print(f"Error sending message to {ip}:{port}: {str(e)}")
            
    def query_peers(self):
        """Display list of connected peers"""
        if not self.peers:
            print("No connected Peers")
        else:
            print("Connected Peers:")
            for i, ((ip, port), _) in enumerate(self.peers.items(), 1):
                print(f"{i}. {ip}:{port}")
                
    def display_menu(self):
        """Display the main menu"""
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query connected peers")
        print("0. Quit")
        print("Enter choice: ", end='')
        
    def run(self):
        """Main loop to handle user input"""
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

def main():
    """Initialize and start the peer"""
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