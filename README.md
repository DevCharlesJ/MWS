# MWS
MWS incorporates a tkinter client application that displays current and historic text messages to that client. 

## Python modules used
    socket
    tkinter
    pickle

## Features
    Message identification and timestamping

    Private messages
    
    
## Example Setup:
  1) run 'server.py'
        A terminal should appear with the following text: "Ears on [<host.ip>:<port>]". If you see this, your server started successfully.
        <host.ip> is your machine ip by default, while the default <port> is 9000. Which is the same for clients as well.
        Please note that running multiple servers is untested.
  2) run 'client.py'
        This will launch another terminal to register a new client to connect to the server.
        After you assign a username to the this client, a graphical interface with a white textbox and green "Send" button located at the bottom should appear.
        Looking back at the server terminal, you should also see that a [CONNECTION] to the server was made.
        If you don't see either of these, an error occurred its details should described in the client or server terminal.

        You can create multiple clients by simply repeating the process.
        
## Messages:
  1. Afer connecting to a server, open the graphical interface respective to a client.
  2. Type the message you want to send into the white textbox located at the bottom of the interface.
  3. Press the green "Send" button to send the message
  4. You and other connected (and permitted) clients should see this message!
  5. Oldest messages are deleted every minute while no clients are connected.
  
## Send a Private Message:
  Private messaging was added to simply test "client targetting", instead of just broadcasting a message to all targets. There's no real secrecy/security for this as of now. 
  
  1. To send a private message, type " --> " right after the message you want to send, then type the username of the recipient.
  2. After pressing "Send", you should notice new details were included above the sent message that denote it as private.
  
### More documentation will be released following later releases.
  
        
