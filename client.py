#encoding utf-8
#write on 2023/4/5,by win11invmware
#not done:recv,say
import socket
import time
import re
import os
from prompt_toolkit import prompt,print_formatted_text as printf
from prompt_toolkit.completion import Completer,Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import CompleteStyle
from threading import Thread

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
ndlg = True
logind = False
onlineuser = []

class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        words = ['/help','/say','/list','/login','/exit','/reg','/connect','/disconnect'] #添加以/开头的命令
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        for word in words:
            if word.startswith(word_before_cursor):
                yield Completion(word, start_position=-len(word_before_cursor))

class mainclient(object):
    def __init__(self):
        self.recvthreadd = Thread(target=self.recvthread,daemon=True)
        self.username = ''

    def start(self):
        self.recvthreadd.start()
        self.cli()

    def recvdata(self):
        global sock,logind
        sock.setblocking(False)
        try:
            msg = sock.recv(2048).decode("utf-8")
            if not msg:
                printf("Disconnect from server")
                sock = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                logind = False
            else:
                return msg
        except IOError as e:
            pass

    def recvthread(self):
        global ndlg,logind,onlineuser
        while True:
            time.sleep(0.0001)
            msg = self.recvdata()
            datam = str(msg).split('^')
            if datam[0] == '201' and datam[1] == 'accp':
                printf('Connected to server')
                continue
            elif datam[0] == '203':
                if datam[1] == 'yes':
                    ndlg = True
                    printf("Server requires login")
                    continue
                else:
                    ndlg = False
                    printf("Server doesn\'t requires login")
                    continue
            elif datam[0] == '205':
                datam.remove('205')
                onlineuser = datam
                continue
            elif datam[0] == '310' and datam[1] == 'rst':
                printf('User doesn\'t exist')
                continue
            elif datam[0] == '313' and datam[1] == 'erro':
                printf('Incorrect password')
                continue
            elif datam[0] == '311' and datam[1] == 'onli':
                printf('User is already online')
                continue
            elif datam[0] == '317' and datam[1] == 'conl':
                printf('Already logged')
                continue
            elif datam[0] == '312' and datam[1] == 'accp':
                logind = True
                printf('Successfully logged in')
                continue
            elif datam[0] == '315' and datam[1] == 'alu':
                printf('User already exists,register has failed')
                continue
            elif datam[0] == '316' and datam[1] == 'accp':
                printf('Successfully registered')
                continue
            elif datam[0] == '314' and datam[1] == 'rege':
                printf('Register error')
                continue
            elif datam[0] == '411':
                # printf(datam)
                if datam[2] == '[Server]':
                    printf(('[Server]'+datam[1]))
                    continue
                else:
                    printf(('<'+datam[2]+'>'+datam[1]))
                    continue
            else:
                pass
                # print('error msg')

    def cli(self):
        global sock,logind
        commands = MyCompleter()
        history = InMemoryHistory()
        helpitem = "{0:<25}\t{1:<25}\t{2:<25}"
        printf("Welcome to Chat 0.2 Beta")
        printf("Type \'/help\' to get help")
        printf("Made on 2023/04/05 by Win11inVMware")
        while True:
            try:
                get = prompt('>',completer=commands,history=history,complete_style=CompleteStyle.READLINE_LIKE,auto_suggest=False)
            except KeyboardInterrupt as e:
                print('^C')
                os._exit(0)

            if get == '':
                continue

            elif get[:1] == '/':
                # if get[1:5] == 'eval': #debugging code
                #     eval(get[6:])

                if get[1:5] == 'help':
                    printf(helpitem.format("command:","usage:","comment:"))
                    printf(helpitem.format("help","/help","Print command help"))
                    printf(helpitem.format("say","/say <text>","Send message to server"))
                    # printf(helpitem.format("set","/set <p1> <p2>","set some parameter"))
                    # printf(helpitem.format("      parameters:","",""))
                    # printf("      server      <ip>:<port>")
                    printf(helpitem.format("login","/login <username> <passwd>","Login in server"))
                    printf(helpitem.format("reg","/reg <username> <passwd>","Register on server"))
                    printf(helpitem.format("list","/list","Print online user"))
                    printf(helpitem.format("connect","/connect <ip>:<port>","Connect to server"))
                    printf(helpitem.format("disconnect","/disconnect","Disconnect from server"))
                    printf(helpitem.format("exit","/exit","Exit from this program"))
                    continue
                    
                # elif get[1:4] == 'set':
                #     pass

                elif get[1:4] == 'say':
                    if logind:
                        self.sendmsg(str(get[5:]))
                        continue
                    else:
                        printf('say:Not logged in')
                        continue

                elif get[1:6] == 'login':
                    usdata = get.split(' ')
                    usdata.remove('/login')
                    for i in usdata:
                        if i == '':
                            usdata.remove(i)
                        else:
                            pass
                    if pdcon():
                        if ndlg:
                            if len(usdata) <= 1:
                                printf("login:Too few parameters")
                                continue
                            elif len(usdata) > 2:
                                printf("login:Too many parameters")
                                continue
                            if re.match('^[a-zA-Z0-9\u4e00-\u9fa5_]{1,12}$',str(usdata[0])):
                                username = str(usdata[0])
                            else:
                                printf("login:Exceeding the username character limit of 12 or containing illegal characters")
                                continue
                            if re.match('^[^^\u4e00-\u9fa5]{1,16}$',str(usdata[1])):
                                password = str(usdata[1])
                            else:
                                printf("login:Exceeding the password character limit of 16 or containing illegal characters")
                                continue
                            if username and password:
                                self.senddata(("300^"+username+"^"+password))
                                self.username = username
                                continue
                        else:
                            if len(usdata) < 1:
                                printf("login:Too few parameters")
                                continue
                            elif len(usdata) > 1:
                                printf("login:Too many parameters")
                                continue
                            if re.match('^[a-zA-Z0-9\u4e00-\u9fa5_]{1,12}$',str(usdata[0])):
                                username = str(usdata[0])
                            else:
                                printf("login:Exceeding the username character limit of 12 or containing illegal characters")
                                continue
                            if username:
                                self.senddata(("300^"+username))
                                self.username = username
                                continue
                    else:
                        printf("reg:Not connected to server")
                        continue
                    
                elif get[1:4] == 'reg':
                    rusdata = get.split(' ')
                    rusdata.remove('/reg')
                    for i in rusdata:
                        if i == '':
                            rusdata.remove(i)
                        else:
                            pass
                    if pdcon():
                        if ndlg:
                            if len(rusdata) <= 1:
                                printf("reg:Too few parameters")
                                continue
                            elif len(rusdata) > 2:
                                printf("reg:Too many parameters")
                                continue
                            if re.match('^[a-zA-Z0-9\u4e00-\u9fa5_]{1,12}$',str(rusdata[0])):
                                username = str(rusdata[0])
                            else:
                                printf("reg:Exceeding the username character limit of 12 or containing illegal characters")
                                continue
                            if re.match('^[^^\u4e00-\u9fa5]{1,16}$',str(rusdata[1])):
                                password = str(rusdata[1])
                            else:
                                printf("reg:Exceeding the password character limit of 16 or containing illegal characters")
                                continue
                            if username and password:
                                self.senddata(("301^"+username+"^"+password))
                                continue
                        else:
                            printf("reg:The server does not require login")
                    else:
                        printf("reg:Not connected to server")
                        continue

                elif get[1:5] == 'list':
                    onus = ""
                    for us in onlineuser:
                        onus = onus + "," + us
                    printf(("online:"+onus[1:]))
                    continue

                elif get[1:8] == 'connect':
                    data = get.split(' ')
                    data.remove('/connect')
                    for i in data:
                        if i == '':
                            data.remove(i)
                        else:
                            pass
                    if len(data) == 0:
                        printf("connect:Too few parameters")
                        continue
                    elif len(data) > 1:
                        printf("connect:Too many parameters")
                        continue
                    ipch = data[0].split(":")
                    ipchh=ipch[0].split(".")
                    try:
                        if int(ipch[1]) > 65535 or len(ipchh) < 4 or int(ipchh[0]) > 225 or int(ipchh[1]) > 255 or int(ipchh[2]) > 255 or int(ipchh[3]) > 255:
                            printf('connect:IP address is illegal')
                            continue
                        else:
                            sock.setblocking(True)
                            try:
                                sock.connect((ipch[0],int(ipch[1])))
                            except OSError as e:
                                # print(e,type(e))
                                # if IOError:
                                #     pass
                                if '10056' in str(e):
                                    printf("connect:Already connect to server")
                                    continue
                                else:
                                    printf("connect:Can't not connect to server")
                                    continue
                            # except IOError as e:
                            #     pass
                    except IndexError as e:
                        printf('connect:IP address is illegal')
                        continue
                    # self.recvthreadd.start()
                    self.senddata('200^conn')
                    time.sleep(0.05)
                    self.senddata('202^ndl')
                    continue

                elif get[1:11] == 'disconnect':
                    sock.close()
                    sock = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                    logind = False
                    continue

                elif get[1:5] == 'exit':
                    os._exit(0)
                else:
                    printf('Invalid command,type \'/help\' to get help')
                    continue

            elif len(get) >= 1:
                if logind:
                    self.sendmsg(str(get))
                    continue
                else:
                    printf('say:Not logged in')
                    continue
        
    def senddata(self,msg):
        sock.send(str(msg).encode('utf-8'))
    
    def sendmsg(self,msg):
        if re.match('^[^^]{1,100}$',msg):
            if pdcon():
                sock.send(str('400^'+msg+'^'+self.username).encode('utf-8'))
            else:
                printf('say:Not connect to server')
        else:
            printf('say:The length is too long or contains illegal characters')

def pdcon():
    try:
        sock.getpeername()
        return True
    except socket.error:
        return False

if __name__ == '__main__':
    mainclient().start()
    # mainclient().cli()
    # os._exit(0)