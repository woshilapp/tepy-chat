#encoding utf-8
#write on 2023/5/1,by win11invmware
import warnings
import socket
import json
import time
import ssl
import re
import os
from prompt_toolkit import prompt,print_formatted_text as printf
from prompt_toolkit.completion import Completer,Completion
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.shortcuts import CompleteStyle
from threading import Thread

s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# 创建了一个 SSL上下文,ssl.PROTOCOL_TLS表示选择客户端和服务器均支持的最高协议版本
with warnings.catch_warnings(): #不显示ssl协议的报警
    warnings.simplefilter("ignore")
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# 设置模式为CERT_REQUIRED，在此模式下，需要从套接字连接的另一端获取证书；如果未提供证书或验证失败则将引发 SSLError
context.verify_mode = ssl.CERT_REQUIRED
# 加载一组用于验证服务器证书的CA证书
context.load_verify_locations("./ca.crt")
sock = context.wrap_socket(s)

canre = False
setg = ''
setgg = ''

class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        words = ['/help','/say','/list','/login','/exit','/reg','/listg','/group','/connect','/disconnect'] #添加以/开头的命令
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
        global sock,s,canre,setg
        try:
            msg = sock.recv(2048).decode("utf-8")
            if not msg:
                printf("Disconnect from server")
                s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                sock = context.wrap_socket(s)
                canre = False
                setg = ''
            else:
                return msg
        except IOError as e:
            pass
        except UnicodeDecodeError as e:
            pass
        except OSError:
            pass

    def recvthread(self):
        global setg
        while True:
            time.sleep(0.0001)
            if canre:
                try:
                    sock.setblocking(False)
                    msg = self.recvdata()
                except OSError:
                    pass
                try:
                    datam = json.loads(msg)
                    if datam['type'] == '202':
                        printf("Connected to server")
                    elif datam['type'] == '206':
                        temg = ""
                        for i in datam['data'].split(','):
                            temg += ','+i
                        printf("groups:"+temg[1:])
                    elif datam['type'] == '208':
                        temu = ""
                        for i in datam['data'].split(','):
                            temu += ","+i
                        printf("online:"+temu[1:])
                    elif datam['type'] == '317':
                        printf("SERVER:You already login")
                    elif datam['type'] == '310':
                        printf("SERVER:User not found")
                    elif datam['type'] == '313':
                        printf("SERVER:Incorrect password")
                    elif datam['type'] == '311':
                        printf("SERVER:User is online")
                    elif datam['type'] == '312':
                        printf("Login successful")
                    elif datam['type'] == '315':
                        printf("SERVER:User already exists")
                    elif datam['type'] == '316':
                        printf("Register successful")
                    elif datam['type'] == '314':
                        printf("SERVER:Error during register")
                    elif datam['type'] == '411':
                        printf("SERVER:Not logged in")
                    elif datam['type'] == '413':
                        printf("SERVER:Group not found")
                    elif datam['type'] == '412':
                        printf("SERVER:Already in group")
                    elif datam['type'] == '416':
                        printf("SERVER:Permission denied")
                    elif datam['type'] == '415':
                        printf("SERVER:Not in group")
                    elif datam['type'] == '414':
                        setg = setgg
                        printf("Choose group successful")
                    elif datam['type'] == '420':
                        if datam['us'] == "[Server]":
                            printf("[Server]"+datam['msg'])
                        elif datam['us'] == "[Server*]":
                            printf("[Server*]"+datam['msg'])
                        else:
                            printf("<"+datam['us']+">"+datam['msg'])
                    elif datam['type'] == '0':
                        pass
                except json.JSONDecodeError:
                    pass
                except TypeError:
                    pass
                except KeyError:
                    pass
                else:
                    pass
                    # print('error msg')
            else:
                pass

    def cli(self):
        global sock,s,setg,setgg,canre
        commands = MyCompleter()
        history = InMemoryHistory()
        helpitem = "{0:<30}\t{1:<30}\t{2:<30}"
        printf("Welcome to Chat 0.3 Beta")
        printf("Type \'/help\' to get help")
        printf("Made on 2023/05/01 by Win11inVMware")
        while True:
            try:
                get = prompt(setg+'$',completer=commands,history=history,complete_style=CompleteStyle.READLINE_LIKE,auto_suggest=False)
            except KeyboardInterrupt as e:
                print('^C')
                os._exit(0)

            if get == '':
                continue

            elif get[:1] == '/':
            #     if get[1:5] == 'eval': #debugging code
            #         eval(get[6:])
            #         continue

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
                    printf(helpitem.format("listg","/listg","Print all groups"))
                    printf(helpitem.format("group","/group <gp>","Switch groups"))
                    printf(helpitem.format("connect","/connect <ip>:<port>","Connect to server(If no port,default port is 6999)"))
                    printf(helpitem.format("disconnect","/disconnect","Disconnect from server"))
                    printf(helpitem.format("exit","/exit","Exit from this program"))
                    continue
                    
                # elif get[1:4] == 'set':
                #     pass

                elif get[1:4] == 'say':
                    self.sendmsg(str(get[5:]))
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
                            self.senddata(("{\"type\":\"300\",\"us\":\""+username+"\",\"pw\":\""+password+"\"}"))
                            self.username = username
                            continue
                    else:
                        printf("login:Not connected to server")
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
                        if re.match('^[^\"\'\u4e00-\u9fa5]{1,16}$',str(rusdata[1])):
                            password = str(rusdata[1])
                        else:
                            printf("reg:Exceeding the password character limit of 16 or containing illegal characters")
                            continue
                        if username and password:
                            self.senddata(("{\"type\":\"301\",\"us\":\""+username+"\",\"pw\":\""+password+"\"}"))
                            continue
                    else:
                        printf("reg:Not connected to server")
                        continue

                elif get[1:6] == 'listg':
                    if pdcon():
                        self.senddata(("{\"type\":\"205\",\"data\":\"ndgp\"}"))
                        continue
                    else:
                        printf("listg:Not connected to server")
                        continue

                elif get[1:5] == 'list':
                    if pdcon():
                        self.senddata(("{\"type\":\"207\",\"data\":\"ndus\"}"))
                        continue
                    else:
                        printf("list:Not connected to server")
                        continue

                elif get[1:6] == 'group':
                    if pdcon():
                        datagg = get.split(' ')
                        for i in datagg:
                            if i == '':
                                datagg.remove(i)
                        if len(datagg) > 2 or len(datagg) <= 1:
                            printf("group:Incorrect parameter")
                            continue
                        else:
                            self.senddata(("{\"type\":\"401\",\"gp\":\""+datagg[1]+"\"}"))
                            setgg = str(datagg[1])
                            time.sleep(0.1)
                            continue
                    else:
                        printf("group:Not connected to server")
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
                    for i in ipch:
                        if i == '':
                            ipch.remove(i)
                    ipchh = ipch[0].split(".")
                    try:
                        if len(ipch) == 1:
                            if len(ipchh) < 4 or int(ipchh[0]) > 225 or int(ipchh[1]) > 255 or int(ipchh[2]) > 255 or int(ipchh[3]) > 255:
                                printf('connect:IP address is illegal')
                                continue
                            else:
                                ipch.append(6999)
                                sock.setblocking(True)
                                try:
                                    sock.connect((ipch[0],int(ipch[1])))
                                except OSError as e:
                                    printf(e)
                                    printf("connect:Failed to connect the server")
                                    continue
                                except ValueError as e:
                                    if str(e) == 'attempt to connect already-connected SSLSocket!':
                                        printf("connect:Already connect to server")
                                        continue
                                    else:
                                        printf(e)
                                except ssl.SSLError as e:
                                    printf("connect:Failed to connect unknown server")
                                except ssl.SSLCertVerificationError as e:
                                    printf("connect:Failed to connect not certified server")
                                self.senddata('{\"type\":\"201\"}')
                                canre = True
                                continue
                        elif int(ipch[1]) > 65535 or len(ipchh) < 4 or int(ipchh[0]) > 225 or int(ipchh[1]) > 255 or int(ipchh[2]) > 255 or int(ipchh[3]) > 255:
                            printf('connect:IP address is illegal')
                            continue
                        else:
                            sock.setblocking(True)
                            try:
                                sock.connect((ipch[0],int(ipch[1])))
                            except OSError as e:
                                printf(e)
                                printf("connect:Failed to connect the server")
                                continue
                            except ValueError as e:
                                if str(e) == 'attempt to connect already-connected SSLSocket!':
                                    printf("connect:Already connect to server")
                                else:
                                    printf(e)
                            except ssl.SSLError as e:
                                printf("connect:Failed to connect unknown server")
                            except ssl.SSLCertVerificationError as e:
                                printf("connect:Failed to connect not certified server")
                            except IOError as e:
                                pass
                    except IndexError as e:
                        printf('connect:IP address is illegal')
                        continue
                    self.senddata('{\"type\":\"201\"}')
                    canre = True
                    continue

                elif get[1:11] == 'disconnect':
                    sock.close()
                    s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                    sock = context.wrap_socket(s)
                    canre = False
                    setg = ''
                    printf("Disconnect from server")
                    continue

                elif get[1:5] == 'exit':
                    os._exit(0)

                else:
                    printf('Invalid command,type \'/help\' to get help')
                    continue

            elif len(get) >= 1:
                self.sendmsg(str(get))
                continue
        
    def senddata(self,msg):
        sock.send(str(msg).encode('utf-8'))
    
    def sendmsg(self,msg):
        if re.match('^.{1,200}$',msg):
            if pdcon():
                sock.send(str("{\"type\":\"402\",\"msg\":\""+str(msg)+"\",\"us\":\""+str(self.username)+"\"}").encode('utf-8'))
            else:
                printf('say:Not connect to server')
        else:
            printf('say:The length is too long')

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