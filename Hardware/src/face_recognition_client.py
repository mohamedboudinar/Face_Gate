import socket
import os

class ImageClient:
    def __init__(self, server_ip='172.21.80.11', server_port=4899, images_dir='C:/Users/Mohamed Boudinar/Downloads/testimages/'):
        self.server_ip = server_ip
        self.server_port = server_port
        self.images_dir = images_dir
        self.socket = None

    def __str__(self):
        """Return a string representation of the instance."""
        return f"ImageClient(server_ip={self.server_ip}, server_port={self.server_port}, images_dir={self.images_dir})"

    def __repr__(self):
        """Return an unambiguous string representation of the instance."""
        return f"ImageClient(server_ip={self.server_ip!r}, server_port={self.server_port!r}, images_dir={self.images_dir!r})"

    def __enter__(self):
        """Initialize and return the instance for use in a with statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the socket when exiting the with statement."""
        self.close_socket()

    def __del__(self):
        """Destructor to ensure the socket is closed when the instance is deleted."""
        self.close_socket()

    def __eq__(self, other):
        """Check if two instances are equal."""
        if isinstance(other, ImageClient):
            return (self.server_ip == other.server_ip and
                    self.server_port == other.server_port and
                    self.images_dir == other.images_dir)
        return False

    def __ne__(self, other):
        """Check if two instances are not equal."""
        return not self.__eq__(other)

    def __hash__(self):
        """Return a hash value of the instance."""
        return hash((self.server_ip, self.server_port, self.images_dir))

    def __call__(self, name):
        """Send all images for a given person."""
        self.send_images(name)

    def close_socket(self):
        """Close the socket if it's open."""
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_image(self, name, image_path):
        """Send a single image to the server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_ip, self.server_port))
            self.socket = s  # Set the socket as the instance attribute

            # Send the name of the person
            name_bytes = name.encode('utf-8')
            name_length = len(name_bytes)
            s.sendall(str(name_length).zfill(4).encode('utf-8'))
            s.sendall(name_bytes)

            # Send the image name
            image_name = os.path.basename(image_path)
            image_name_bytes = image_name.encode('utf-8')
            image_name_length = len(image_name_bytes)
            s.sendall(str(image_name_length).zfill(4).encode('utf-8'))
            s.sendall(image_name_bytes)

            # Send the image data
            with open(image_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    s.sendall(chunk)

    def send_images(self, name):
        """Send all images in the specified directory."""
        image_files = [f for f in os.listdir(self.images_dir) if f.endswith('.jpg')]
        for image_file in image_files:
            image_path = os.path.join(self.images_dir, image_file)
            self.send_image(name, image_path)

    def receive_success_signal(self):
        """Receive a success signal from the server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.bind((self.server_ip, self.server_port))
            client_socket.listen(1)
            print(f"Waiting for success signal on {self.server_ip}:{self.server_port}")
            conn, addr = client_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                signal = conn.recv(1024)
                if signal == b"True":
                    print("Received success signal from server")
                    flag = True 
                elif signal == b"False":
                    flag = False
                else:
                    print("Received unexpected signal from server")
                    flag = False 
                
                return flag

# Usage example
if __name__ == '__main__':
    with ImageClient() as client:
        print(client)
        client('ines') 
        #res = client.receive_success_signal()
        #print(res)res)