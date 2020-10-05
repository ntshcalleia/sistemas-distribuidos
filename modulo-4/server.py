import argparse, socket, json, select, sys, threading

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
    logged_in = False
    username = ""
    while True:
        msg = conn.recv(1024).decode("utf-8")
        if not msg:
            # Close connection and remove user from list
            conn.close()
            if logged_in:
                print(f'{RED}User {username} {address} disconnected from server.{RESET}')
                del users[username]
            else:
                print(f'{RED}{address} disconnected from server.{RESET}')
            return
        if msg.upper() == "GET":
            print(f'{GREEN}{address} requested list of users.{RESET}')
            conn.send(json.dumps(users).encode())
        else:
            try:
                method, newUsername, listeningAddress = msg.split(" ", 2)
                method = method.upper()
                if method == "POST":
                    if newUsername == username:
                        conn.send(f'Your username is already {newUsername}'.encode())
                    elif newUsername in users:
                        conn.send(f'Username {newUsername} is already in use'.encode())
                    else:
                        if logged_in:
                            del users[username]
                        logged_in = True
                        users[newUsername] = eval(listeningAddress)
                        username = newUsername
                        conn.send("Successfully connected to network.".encode())
                        print(f'{GREEN}{address} successfully connected to network with username {username}.{RESET}')
                else:
                    raise Exception
            except:
                conn.send("Invalid request".encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    users = {}
    threads = []
    rlist = [sys.stdin, s]
    s.bind((HOST, PORT))
    s.listen(5)
    print(f'{CYAN}Server is listening on port {PORT}.{RESET}')
    print(f'{CYAN}For a list of available commands please type help.{RESET}')
    while True:
        read, write, excep = select.select(rlist, [], [])
        for ready in read:
            if ready == s:
                conn, address = s.accept()
                print(f'{GREEN}New connection: {address}{RESET}')
                user_thread = threading.Thread(target=handleConnection, args=(conn, address))
                threads.append(user_thread)
                user_thread.start()
            # Central server commands
            if ready == sys.stdin:
                cmd = input()
                if cmd == "help":
                    # List all available commands
                    print("TODO")
                elif cmd == "users":
                    # Print list of current users
                    print(f'{CYAN}{json.dumps(users)}{RESET}')
                elif cmd == "exit":
                    # Shut down server
                    for t in threads:
                        t.join()
                    s.close()
                    sys.exit()
                else:
                    print(f'{RED}Invalid command. Type help for list of commands.{RESET}')
