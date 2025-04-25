import socket
import os

class ImageReceiverServer:
    def __init__(self, host, port, buffer_size=4096, save_base_folder='received_images'):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.save_base_folder = save_base_folder
        self.server_socket = None
        self.run = True
        self.MAX_NUMBER_IMAGES = 10 - 1 # from 0 to 9 Indexing

    def __str__(self):
        """Return a string representation of the instance."""
        return (f"ImageReceiverServer(host={self.host}, port={self.port}, "
                f"buffer_size={self.buffer_size}, save_base_folder={self.save_base_folder})")

    def __repr__(self):
        """Return an unambiguous string representation of the instance."""
        return (f"ImageReceiverServer(host={self.host!r}, port={self.port!r}, "
                f"buffer_size={self.buffer_size!r}, save_base_folder={self.save_base_folder!r})")

    def __del__(self):
        """Destructor to ensure the server socket is closed when the instance is deleted."""
        self.stop_server()
    
    def start_server(self):
        """Start the server to receive images."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        cnt_images = 0
        print(f"Server started at {self.host}:{self.port}")
        print("Waiting for new connection...")
        self.run = True
        try:
            while self.run:
                if cnt_images >= self.MAX_NUMBER_IMAGES:
                    self.run = False
                    break
                conn, addr = self.server_socket.accept()
                with conn:
                    print(f"Connected by {addr}")
                    
                    # Read name length and name
                    name_length = int(conn.recv(4).decode('utf-8'))
                    name = conn.recv(name_length).decode('utf-8')
                    
                    # Create a directory for the person if it doesn't exist
                    person_folder = os.path.join(self.save_base_folder, name)
                    if not os.path.exists(person_folder):
                        os.makedirs(person_folder)

                    print(f"Receiving images for: {name}")

                    while True:
                        # Read image name length and image name
                        image_name_length = conn.recv(4)
                        if not image_name_length:
                            break
                        image_name_length = int(image_name_length.decode('utf-8'))
                        image_name = conn.recv(image_name_length).decode('utf-8')

                        print(f"Receiving image: {image_name}")

                        # Receive image data
                        image_data = bytearray()
                        while True:
                            part = conn.recv(self.buffer_size)
                            if not part:
                                break
                            image_data.extend(part)

                        # Save the image
                        image_path = os.path.join(person_folder, image_name)
                        with open(image_path, 'wb') as f:
                            f.write(image_data)
                        print(f"Saved image to {image_path}")

                    print(f"Finished receiving images for: {name}")
                    cnt_images = cnt_images + 1

        except KeyboardInterrupt:
            print("Server shutting down...")

    def stop_server_looping(self):
        self.run = False
    
    def start_server_looping(self):
        self.run = True

    def stop_server(self):
        """Stop the server and close the socket."""
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None

    def send_success_signal(self):
        """Send a success signal to the client."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as signal_socket:
            try:
                signal_socket.connect((self.host, self.port))
                signal_socket.sendall(b"True")
                print(f"Success signal sent to {self.host}:{self.port}")
            except Exception as e:
                print(f"Failed to send success signal: {e}")

    def send_refused_signal(self):
        """Send a success signal to the client."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as signal_socket:
            try:
                signal_socket.connect((self.host, self.port))
                signal_socket.sendall(b"False")
                print(f"Success signal sent to {self.host}:{self.port}")
            except Exception as e:
                print(f"Failed to send success signal: {e}") 


# Usage example
if __name__ == '__main__':
    src = ImageReceiverServer('0.0.0.0', 4899)
    src.start_server()