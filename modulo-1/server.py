import argparse, socket

# Add named command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--HOST', help='change the server host (default is localhost)')
parser.add_argument('--PORT', help='change the port (default is 5000)')

args = parser.parse_args()

HOST = args.HOST or 'localhost'
PORT = int(args.PORT) or 5000

# Console colors
CYAN = '\x1b[36m'
GREEN = '\x1b[32m'
RED = '\x1b[31m'
RESET = '\x1b[0m'

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
    def start(self):
        self.socket.listen(1)
        print(f'{CYAN}Server is listening on port {self.port}.{RESET}')
        self.conn, self.address = self.socket.accept()
        print(f'{GREEN}Connected to {self.address}{RESET}')
        while True:
            msg = self.conn.recv(1024)
            if not msg: break
            self.process(msg)
        self.close()
    def process(self, msg):
        print(GREEN + 'Received message: ' + str(msg, encoding='utf-8') + RESET)
        self.conn.send(msg)
        print(f'{CYAN}Message echoed back to {self.address}{RESET}')
    def close(self):
        print(f'{RED}Connection closed. Server is shutting down.{RESET}')
        self.conn.close()
        self.socket.close()

server = Server(HOST, PORT)
server.start()