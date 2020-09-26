import argparse, socket, json

# Add named command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--HOST', help='change the server host (default is localhost)')
parser.add_argument('--PORT', help='change the port (default is 5000)', type=int)
parser.add_argument('files', help='list of file names, separated by a space', nargs='*')
parser.add_argument('-i', help='list of file names, separated by a space', action="store_true")

args = parser.parse_args()

HOST = args.HOST or 'localhost'
PORT = args.PORT or 5000

# Console colors
CYAN = '\x1b[36m'
GREEN = '\x1b[32m'
RED = '\x1b[31m'
RESET = '\x1b[0m'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        try:
            files = args.files if not args.i else input(f'{CYAN}Enter filename(s):\n{RESET}').split()
            if files[0] == "/exit":
                print(f'{CYAN}Exiting interactive mode.{RESET}')
                s.close()
                break
            msg = json.dumps(files)
            s.send(msg.encode())
            response = json.loads(s.recv(1024))
            for key in response:
                print(f'{GREEN}{key}:{RESET}')
                print(response[key])
        except ConnectionRefusedError:
            print(RED + "Unable to connect to server." + RESET)
            break
        if not args.i:
            s.close()
            break