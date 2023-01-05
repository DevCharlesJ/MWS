import socket
import threading # Might be better to use custom threads
import pickle
from time import sleep

from socketTools import *
from COMMCODES import *


from ClientObjects import Message, User
from app import chatInstance

try:
    username = None
    while True:
        username = input("Display name: ").strip()
        if username:
            if len(username) <= 30:
                break
            else:
                print("Username is too long (30 character max). Try again!\n")
        else:
            print("Invalid username, Try again!\n")

    HEADER = 64

    PORT = 9000
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER,PORT)

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client_socket.connect(ADDR)
    client_socket.settimeout(5)

    client_user = None


    connected = True

    chat_instance = None


    def handle_disconnect():
        global chat_instance
        # chat_instance.destroy()
        # print("Out")
        chat_instance = None
        

    def listen():
        global connected, chat_instance
        try:
            while connected:
                try:
                    incoming = acceptIncoming(client_socket, CLIENT_SERVER_MSG_FORMAT)
                except Exception as e:
                    if verify_connection(client_socket, CLIENT_SERVER_MSG_FORMAT):
                        continue
                    else:
                        print("Lost connection to server")
                        raise e

                        


                if incoming:
                    if isinstance(incoming, str):
                        if incoming == DISCONNECT_CLIENT:
                            break
                        elif incoming == SERVER_MSG:
                            msg = acceptIncoming(client_socket, CLIENT_SERVER_MSG_FORMAT)
                            msg = "[SERVER] " + str(msg)

                            if chat_instance:
                                chat_instance.setSpecial(msg)
                                chat_instance.update()
                            else:
                                print(msg)
                        elif incoming == SERVER_DISCONNECT:
                            break

                    elif isinstance(incoming, bytes):
                        try:
                            obj = pickle.loads(incoming)

                            if isinstance(obj,list) and obj != []:
                                head = obj[0]
                                if isinstance(head, Message):
                                    if chat_instance:
                                        chat_instance.setMessages(obj)
                                        chat_instance.update()

                            elif chat_instance and isinstance(obj, Message):
                                chat_instance.pushMessage(obj)
                        except:
                            pass

        except Exception as e:
            print(1)
            raise e
        finally:
            connected = False
            handle_disconnect()
            print("[DISCONNECTED]")


    listenThread = threading.Thread(target=listen)

    #-------FIRST-UPS
    client_user = User(username)

    # Register user to server
    sendStr(client_socket, REGISTER_USER, CLIENT_SERVER_MSG_FORMAT)
    sendPickle(
        client_socket,
        client_user,
        CLIENT_SERVER_MSG_FORMAT
    )

    # Init chat application
    chat_instance = chatInstance(
        socket=client_socket,
        user=client_user,
        messages=[],
        sendFormat=CLIENT_SERVER_MSG_FORMAT)

    # Request existing messages
    sendStr(client_socket, GET_MESSAGES, CLIENT_SERVER_MSG_FORMAT)

    # If chat instance is ready, execute listener
    print("Awaiting chat application...")
    while not chat_instance.isReady():
        pass
    print("Starting!")
    
    listenThread.start()
    #-----------



    # possibly have to explicitly handle disconnect
except Exception as e:
    print(e)
    input("...")

