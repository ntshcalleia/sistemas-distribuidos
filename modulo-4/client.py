import argparse, socket, json, select, sys, threading

# Add named command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--HOST', help='change the central server host (default is localhost)')
parser.add_argument('--PORT', help='change the central server port (default is 5000)', type=int)

args = parser.parse_args()

HOST = args.HOST or 'localhost'
PORT = args.PORT or 5000

# Console colors
CYAN = '\x1b[36m'
GREEN = '\x1b[32m'
RED = '\x1b[31m'
RESET = '\x1b[0m'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        users = {}
        connections = {}
        threads = []
        rlist = [sys.stdin, s]
        server.connect((HOST, PORT))
        print(f'{CYAN}Connected to central server.{RESET}')
        s.bind((socket.gethostbyname(socket.gethostname()), 0)) # OS will automatically assign an available port
        s.listen(5)
        print(f'{CYAN}For a list of available commands please type help.{RESET}')
        while True:
            read, write, excep = select.select(rlist, [], [])
            for ready in read:
                if ready == s:
                    # Handle new socket connection
                    conn, address = s.accept()
                    print(f'{GREEN}{address} is requesting connection.')
                    user = input(f'{CYAN}Please set username or type reject to reject it.{RESET}\n')
                    if user == "reject":
                        conn.close()
                        print(f'{CYAN}Connection rejected.{RESET}')
                    else:    
                        connections[user] = conn
                        print(f'{GREEN}Successfully connected to {user} {address}.{RESET}')
                        rlist.append(conn)
                elif ready == sys.stdin:
                    cmd = input()
                    if cmd == "help":
                        # List all available commands
                        print("TODO")
                    elif cmd == "users":
                        # Retrieve list of users from central server
                        server.send("GET".encode())
                        res = server.recv(1024)
                        users = json.loads(res)
                        print(f'{GREEN}{json.dumps(users)}{RESET}')
                    elif cmd == "connections":
                        # Print list of peers that are connected to you
                        if not connections:
                            print(f'{GREEN}No active peer connections.{RESET}')
                        else:
                            for key in connections:
                                print(f'{GREEN}{key}: {connections[key].getpeername()}{RESET}')
                    elif cmd == "exit":
                        server.close()
                        for t in threads:
                            t.join()
                        sys.exit()
                    else:
                        try:
                            request, value = cmd.split(" ", 1)
                            if request == "login":
                                server.send(f'POST {value} {s.getsockname()}'.encode())
                                res = server.recv(1024)
                                print(GREEN + res.decode("utf-8") + RESET)
                            elif request == "disconnect":
                                conn = connections[value]
                                del connections[value]
                                rlist.remove(conn)
                                conn.close()
                                print(f'{GREEN}Connection with {value} was closed.{RESET}')
                            elif request == "connect":
                                # Connect with peer
                                if value not in users:
                                    # Retrieve updated list
                                    server.send("GET".encode())
                                    res = server.recv(1024)
                                    users = json.loads(res)
                                if value in users:
                                    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                    conn.connect(tuple(users[value]))
                                    rlist.append(conn)
                                    connections[value] = conn
                                    print(f'{GREEN}Successfully connected to {value} {conn.getpeername()}{RESET}')
                                else:
                                    print(f'{RED}Couldn\'t find user {value}{RESET}')
                            elif request in connections:
                                connections[request].send(value.encode())
                            else:
                                raise Exception
                        except:
                            print(f'{RED}Invalid command. Type help for list of commands.{RESET}')
                else:
                    # Receive message from socket connection
                    msg = ready.recv(1024).decode("utf-8")
                    if not msg:
                        for key in connections:
                            if connections[key] == ready:
                                print(f'{GREEN}Connection with {key} was closed.{RESET}')
                                del connections[key]
                                break
                        rlist.remove(ready)
                        ready.close()
                    else:
                        for key in connections:
                            if connections[key] == ready:
                                print(f'{CYAN}{key}:{RESET} {msg}')
                                break