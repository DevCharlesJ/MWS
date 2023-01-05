from tkinter import *
import threading
from time import sleep

from ClientObjects import Message
from socketTools import *
from COMMCODES import *

class chatInstance():
    def destroy(self):
        self.__isReady = False
        if self.root:
            print(1)
            self.root.destroy()


    def __start(self):
        root = Tk()
        self.root = root

        root.title("Chat V1")

        root.geometry("350x500")
        root.minsize(350, 500)

        root.configure(bg="gray", padx=5, pady=5)

        chatContainer = Frame(master=root, bg="gray", width=340, height=440)
        chatContainer.pack(side="top")
        chatContainer.pack_propagate(False)

        self.frameChat = Frame(master=chatContainer, bg="darkgray", width=340, height=440)
        self.frameChat.pack(side="left")
        self.frameChat.grid_propagate(False)
        self.frameChat.pack_propagate(False)

        # self.scrollbarChat = Scrollbar(master=self.frameChat, orient="vertical")
        # self.scrollbarChat.pack(side="right", fill="y")
        # self.scrollbarChat.configure(command=self.frameChat)


        bottom_frame = Frame(master=root, bg="gray", width=340, height=40)
        bottom_frame.pack(side="bottom")
        bottom_frame.pack_propagate(False)

        self.varSpecial = StringVar()
        self.varSpecial.set('')

        self.lblSpecial = Label(master=bottom_frame, width=50, height=1, textvariable=self.varSpecial, bg="gray")
        self.lblSpecial.pack(side="top")

        self.txtChat = Text(master=bottom_frame, width=30, height=2, bg="white", fg="gray")
        self.txtChat.pack(side="left")

        btnChat = Button(master=bottom_frame, text="Send", width=20, height=2, command=self.sendChat, bg="green", fg="white")
        btnChat.pack(side="right")



        self.update()
        self.__isReady = True
        root.mainloop()
        self.__isReady = False
        return

    def __init__(self, socket, user, messages=None, sendFormat=None):
        self.socket = socket
        self.user = user
        self.sendFormat = sendFormat
        self.__messages = messages or []
        self.__special_message = ""
        self.__isReady = False

        chat_instance_thread = threading.Thread(target=self.__start)
        chat_instance_thread.start()

    def isReady(self):
        return self.__isReady == True



    def sendChat(self):
        text = self.txtChat.get("1.0",'end-1c').strip()

        self.txtChat.delete('1.0', END)

        target = None
        to = text.find("-->")
        if to != -1:
            target = text[to+3:].strip()
            text = text[:to].strip()
            target = target if target else None

        if text:
            message = Message(self.user, text, target=target)
            sendPickle(self.socket, message, self.sendFormat or CLIENT_SERVER_MSG_FORMAT)
            self.pushMessage(message)


    def pushMessage(self, message):
        if isinstance(message, Message):
            self.__messages.append(message)
            self.update()

    def clearMessages(self):
        self.__messages.clear()

    def setMessages(self, messages:list):
        self.__messages = messages

    def setSpecial(self, txt:str):
        self.__special_message = txt

    def timedSpecial(self, t: float):
        self.varSpecial.set(self.__special_message)
        self.root.update_idletasks()
        sleep(t)
        self.varSpecial.set('')
        self.root.update_idletasks()
        self.setSpecial("")

    def update(self):
        if self.__special_message:
            ts_thread = threading.Thread(target=self.timedSpecial, args=[3])
            ts_thread.start()


        self.__updateMessages()

    def __updateMessages(self):
        for widget in self.frameChat.children.values():
            # if widget == self.scrollbarChat:
            #     continue

            widget.grid_forget()
            widget.pack_forget()

        # NOTE: Server-sided message security
        # Private messages which do not target the user were pre-filtered out of __messages

        for i,message in enumerate(self.__messages):
            frameSpeech = Frame(master=self.frameChat, bg="darkgray", width=340)
            frameSpeech.grid(column=0, row=i, sticky=W)

            lblAuthor = Label(master=frameSpeech, bg="darkgray") # custom fg colors later
            lblAuthor.grid(column=0, row=0, sticky=W)
            lblAuthor.configure(font="Lucida 11 bold")

            lblMsgType = Label(master=frameSpeech, bg="darkgray") # custom fg colors later
            lblMsgType.grid(column=1, row=0, sticky=W)

            lblDate = Label(master=frameSpeech, text=message.created, bg="darkgray") # custom fg colors later
            lblDate.grid(column=2, row=0, sticky=W)

            lblSpeech = Label(master=frameSpeech, text=message.text, bg="darkgray", wraplength=300) # custom formatting later
            lblSpeech.grid(column=0, row=1, columnspan=4, rowspan=10, sticky=W)
            lblSpeech.configure(font="ArialS 10")

            # (frameAttachment, typeAttach) later

            if message.author == self.user:
                lblAuthor.configure(text="You")
                if message.target:
                    lblMsgType.configure(text=f" --> {message.target} ")

            else:
                lblAuthor.configure(text=message.author.username)
                if message.target:
                    lblMsgType.configure(text="(PRIVATE)")



        self.frameChat.update()
        