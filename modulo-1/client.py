import argparse, socket

# Add named command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--HOST', help='change the server host (default is localhost)')
parser.add_argument('--PORT', help='change the port (default is 5000)', type=int)

args = parser.parse_args()

HOST = args.HOST or 'localhost'
PORT = args.PORT or 5000

# Console colors
CYAN = '\x1b[36m'
GREEN = '\x1b[32m'
RED = '\x1b[31m'
RESET = '\x1b[0m'

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def start(self):
        self.socket.connect((self.host, self.port))
        print(f'{GREEN}Connected to {self.host} on port {self.port}.{RESET}')
        while True:
            msg = input(f'{CYAN}Type your message:\n{RESET}')
            if msg == '/close': break
            self.socket.send(msg.encode())
            print(f'{CYAN}Message sent.{RESET}')
            response = self.socket.recv(1024)
            self.process(response)
        self.close()
    def process(self, msg):
        print(GREEN + 'Received message: ' + str(msg, encoding='utf-8') + RESET)
    def close(self):
        print(f'{RED}Connection closed.{RESET}')
        self.socket.close()

client = Client(HOST, PORT)
client.start()