import pickle
HEADER = 64


def verify_connection(socket, byteformat) -> bool:
    """Checks for live socket connection"""

    try:
        sendStr(socket, "", byteformat)
        return True
    except:
        return False

def sendStr(socket, text, byteformat):
    try:
        packet = text.encode(byteformat)
        packet_size = bytes(f'{len(packet):<{HEADER}}', byteformat)

        socket.send(packet_size)
        socket.send(packet)
    except:
        pass

def sendPickle(socket, obj, byteformat):
    try:
        packet = pickle.dumps(obj)
        packet_size = bytes(f'{len(packet):<{HEADER}}', byteformat)

        socket.send(packet_size)
        socket.send(packet)
    except:
        pass

def acceptIncoming(conn, byteformat):
    try:
        msg_length = conn.recv(HEADER).decode(byteformat).strip() # decode the expected message length
        if msg_length.isdigit():
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)

            if isinstance(msg, bytes):
                try:
                    msg = msg.decode(byteformat)
                except:
                    pass
                    
            return msg
    except:
        pass

