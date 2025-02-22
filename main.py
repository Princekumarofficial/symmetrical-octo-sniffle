import socket
import threading
import sys
from datetime import datetime
from typing import Dict, Tuple

class Peer:
    def __init__(self, name: str, port: int) -> None:
        self.name: str = name
        self.port: int = port
        self.peers: Dict[Tuple[str, int], datetime] = {}
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running: bool = True
        self.connections: Dict[Tuple[str, int], socket.socket] = {}

    def start_server(self) -> None:
        self.socket.bind(('', self.port))
        self.socket.listen(5)
        print(f"Server listening on port {self.port}")
        
        receive_thread = threading.Thread(target=self.receive_connections)
        receive_thread.daemon = True
        receive_thread.start()

    def receive_connections(self) -> None:
        while self.running:
            try:
                self.socket.settimeout(1.0)
                try:
                    client_socket, address = self.socket.accept()
                    
                    peer_port_data = client_socket.recv(1024).decode()
                    if peer_port_data.startswith("PORT:"):
                        peer_port = int(peer_port_data.split(":")[1])
                        client_socket.send(f"PORT:{self.port}".encode())
                        
                        address = (address[0], peer_port)
                    
                    client_thread = threading.Thread(
                        target=self.handle_peer,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
            except Exception as e:
                if self.running:
                    print(f"\nError accepting connection: {str(e)}")
                break

    def connect_to_peer(self, ip: str, port: int) -> socket.socket:
        peer_addr = (ip, port)
        if peer_addr not in self.connections:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(5.0)
                client_socket.connect((ip, port))
                
                client_socket.send(f"PORT:{self.port}".encode())
                
                peer_port_data = client_socket.recv(1024).decode()
                if peer_port_data.startswith("PORT:"):
                    peer_port = int(peer_port_data.split(":")[1])
                    peer_addr = (ip, peer_port)
                
                self.connections[peer_addr] = client_socket
                
                receive_thread = threading.Thread(
                    target=self.handle_peer,
                    args=(client_socket, peer_addr)
                )
                receive_thread.daemon = True
                receive_thread.start()
                
                return client_socket
            except Exception as e:
                print(f"Error connecting to peer {ip}:{port}: {str(e)}")
                return None
        return self.connections[peer_addr]

    def handle_peer(self, client_socket: socket.socket, address: Tuple[str, int]) -> None:
        peer_addr = address
        self.peers[peer_addr] = datetime.now()
        
        while self.running:
            try:
                client_socket.settimeout(1.0)
                try:
                    message = client_socket.recv(1024).decode()
                    if message:
                        if not message.startswith("PORT:"):
                            decoded_message = message.split('CipherSurge')[-1].strip()
                            if decoded_message.lower() == 'exit':
                                print(f"\nPeer {address[0]}:{address[1]} disconnected")
                                self.disconnect_peer(peer_addr)
                                break
                            print(f"\n{message}")
                            self.peers[peer_addr] = datetime.now()
                            self.display_menu()
                    else:
                        break
                except socket.timeout:
                    if not self.running:
                        break
                    continue
            except Exception as e:
                if self.running:
                    print(f"Error handling peer {address[0]}:{address[1]}: {str(e)}")
                break
                
        self.disconnect_peer(peer_addr)

    def send_message(self, ip: str, port: int, message: str) -> None:
        try:
            client_socket = self.connect_to_peer(ip, port)
            if client_socket:
                message = f"{ip}:{port} CipherSurge {message}"
                client_socket.send(message.encode())
                print(f"Message sent to {ip}:{port}")
                
                peer_addr = (ip, port)
                self.peers[peer_addr] = datetime.now()
                
        except Exception as e:
            print(f"Error sending message to {ip}:{port}: {str(e)}")
            peer_addr = (ip, port)
            if peer_addr in self.connections:
                del self.connections[peer_addr]

    def disconnect_peer(self, peer_addr: Tuple[str, int]) -> None:
        try:
            if peer_addr in self.peers:
                del self.peers[peer_addr]
            if peer_addr in self.connections:
                self.connections[peer_addr].close()
                del self.connections[peer_addr]
        except Exception as e:
            print(f"Error disconnecting peer {peer_addr}: {str(e)}")

    def query_peers(self) -> None:
        if not self.peers:
            print("No connected Peers")
        else:
            print("Connected Peers:")
            for i, ((ip, port), _) in enumerate(self.peers.items(), 1):
                print(f"{i}. {ip}:{port}")

    def display_menu(self) -> None:
        print("\n***** Menu *****")
        print("1. Send message")
        print("2. Query connected peers")
        print("0. Quit")
        print("Enter choice: ", end='')

    def cleanup(self) -> None:
        """Clean up all connections when shutting down."""
        try:
            print("Cleaning up connections...")
            self.running = False
            
            # Send exit message to all connected peers
            for peer_addr, conn in list(self.connections.items()):
                try:
                    conn.send(f"{peer_addr[0]}:{peer_addr[1]} CipherSurge exit".encode())
                except:
                    pass
                self.disconnect_peer(peer_addr)
            
            # Close the listening socket
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.socket.close()
            
            print("Cleanup completed")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def run(self) -> None:
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
                    print("Exiting...")
                    self.cleanup()
                    print("Goodbye!")
                    sys.exit(0)
                    
            except ValueError:
                print("Invalid input. Please try again.")
            except Exception as e:
                print(f"Error: {str(e)}")

def main() -> None:
    name = input("Enter your name: ")
    port = int(input("Enter your port number: "))
    
    peer = Peer(name, port)
    try:
        peer.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        peer.cleanup()
        print("Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()