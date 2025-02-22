class newDefs:
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