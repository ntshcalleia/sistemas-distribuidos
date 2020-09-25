# Start the server and handle communication with clients
import argparse, socket, json
import word_counter

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f'{CYAN}Server is listening on port {PORT}.{RESET}')
    while True:
        conn, address = s.accept()
        msg = conn.recv(1024)
        files = json.loads(msg)
        print(f'{GREEN}{address} requested file(s) {files}.{RESET}')
        result = {}
        for file in files:
            result[file] = word_counter.process(file)
        msg = json.dumps(result)
        conn.send(msg.encode())
        conn.close()