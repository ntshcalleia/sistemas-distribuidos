# Start the server and handle communication with clients
import argparse, socket, json, select, sys, threading
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

def handleConnection(conn, address):
    while True:
        msg = conn.recv(1024)
        if not msg:
            conn.close()
            return
        files = json.loads(msg)
        print(f'{GREEN}{address} requested file(s) {files}.{RESET}')
        result = {}
        for file in files:
            result[file] = word_counter.process(file)
        msg = json.dumps(result)
        conn.send(msg.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    clients = []
    rlist = [sys.stdin, s]
    s.bind((HOST, PORT))
    s.listen(5)
    print(f'{CYAN}Server is listening on port {PORT}.{RESET}')
    while True:
        read, write, excep = select.select(rlist, [], [])
        for ready in read:
            if ready == s:
                conn, address = s.accept()
                client = threading.Thread(target=handleConnection, args=(conn, address))
                client.start()
                clients.append(client)
            if ready == sys.stdin:
                cmd = input()
                if cmd == "/exit":
                    for c in clients:
                        c.join()
                    s.close()
                    sys.exit()