from http.client import HTTPResponse
import socket
import threading
from time import sleep

from socketTools import *
from COMMCODES import *

from ClientObjects import Message, User


if __name__ == '__main__':
    # I want to implement a thread pool later

    HEADER = 64 # For each beginning of the message, this header will contain the len of the bytes to be expected from a client request

    PORT = 9000
    SERVER = socket.gethostbyname(socket.gethostname()) # IP of host (this comp)
    ADDR = (SERVER, PORT)


    server_online = True # flag for server to accept connections
    registries = dict() # client_addr: [client_socket, client_user]

    _socket = socket.socket(
        socket.AF_INET, # socket address family, what device family is permitted to connect
        socket.SOCK_STREAM # streaming data through the socket
    )
    _socket.bind(ADDR) # Bind socket to the server address


    _messages = [] #[Message(User(username=f"TESTER{i}"),"TEXT"*randint(1,5),None) for i in range(1,10)] # Message[]

    def getMessages(user):
        return [message for message in _messages if message.target in (user.username, None)]




    def fireClients(msg, exclude_addrs=[]):
        # NOTE: client_socket = registries[key][0]
        for key in filter(lambda key: key not in exclude_addrs, registries.keys()):
            try: # socket could be closed
                if isinstance(msg, (str, int, float)):
                    sendStr(registries[key][0], msg, CLIENT_SERVER_MSG_FORMAT)
                else:
                    sendPickle(registries[key][0], msg, CLIENT_SERVER_MSG_FORMAT)
            except:
                pass


    def findAddrFromUsername(username):
        for key in registries.keys():
            user = registries[key][1]
            if user.username == username:
                return key

    def handle_client(conn, addr):
        global sent
        print(f"[CONNECTION] {addr}")

        offline_ref = None
        connected = True
        try:
            while connected:
                incoming = acceptIncoming(conn, CLIENT_SERVER_MSG_FORMAT)
                if incoming:
                    if isinstance(incoming, str):
                        if incoming == DISCONNECT_CLIENT:
                            connected = False
                        elif incoming == REGISTER_USER:
                            user = pickle.loads(acceptIncoming(conn, CLIENT_SERVER_MSG_FORMAT))
                            registries[addr] = [conn, user] # socket, User obj
                            offline_ref = (addr, user.username)

                            fireClients(SERVER_MSG)
                            sendStr(conn, f"WELCOME {user.username}!", CLIENT_SERVER_MSG_FORMAT) # Welcome the new user
                            fireClients(f"{user.username} joined", exclude_addrs=[addr]) # Inform other clients that user has joined
                        elif incoming == GET_MESSAGES:
                            # this sends all chat messages from this server to the client
                            sendPickle(conn, getMessages(registries[addr][1]), CLIENT_SERVER_MSG_FORMAT)

                    elif isinstance(incoming, bytes):
                        obj = pickle.loads(incoming)

                        if isinstance(obj, Message) and obj.text:
                            exclude = [addr]

                            if obj.target:
                                target_addr = findAddrFromUsername(obj.target)
                                if target_addr and obj.target != "UNKNOWN":
                                    exclude += list(filter(lambda key: key != target_addr, registries))
                                else:
                                    sendStr(conn, SERVER_MSG, CLIENT_SERVER_MSG_FORMAT)
                                    sendStr(conn, "User does not exist!", CLIENT_SERVER_MSG_FORMAT)
                                    continue

                            _messages.append(obj) # append this message to message list

                        fireClients(obj, exclude_addrs=exclude) # Fire obj to client

                # Handle web requests using seperate server?
                # else: # web request
                #     conn.send(bytes('HTTP/1.0 200 OK\n', "utf-8"))
                #     conn.send(bytes('Content-Type: text/html\n', "utf-8"))
                #     conn.send(bytes('\n', "utf-8")) # header and body should be separated by additional newline
                #     conn.send(bytes("""
                #         <html>
                #         <body>
                #         <h1>Hello World</h1> this is my server!
                #         </body>
                #         </html>
                #     """, "utf-8")) # Use triple-quote string.
                #     sleep(2)
                #     conn.close()

        except Exception as e:
            print(e)

        conn.close()
        if addr in registries:
            registries.pop(addr)

        if offline_ref:
            fireClients(SERVER_MSG)
            fireClients(f"{offline_ref[1]} left")

        print(f"[CONNECTION LOST] {addr}")

    def messageCleaner(t:int):
        """Removes oldest message every t seconds"""

        while server_online:
            sleep(60)

            if _messages and len(registries) == 0:
                _messages.pop(0) # remove oldest



    def start(): # Start server, socket will begin listening to client connections to handle
        _socket.listen()
        print(f"Ears on [{ADDR[0]}:{ADDR[1]}]")

        mc_thread = threading.Thread(target=messageCleaner, args=[60])
        mc_thread.start()

        while server_online:
            conn, addr = _socket.accept() # accept a connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


        # tell clients server is offline
        fireClients(SERVER_DISCONNECT)

    start()