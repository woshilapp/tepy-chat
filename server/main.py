#encoding utf-8
#Python 3.11.3 by Win11inVMware
#go die needlogin, we must login
import socket,ssl,json,threading,logging,sys,time,warnings
from prompt_toolkit import prompt,print_formatted_text as printf
from prompt_toolkit.history import InMemoryHistory

class myconhandler(logging.StreamHandler): #重写StreamHandler实现切换输出函数的功能
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream(msg)
            # stream(self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)

fliehandler = logging.FileHandler(filename='server.log',mode='a',encoding='utf-8')
fliehandler.setFormatter(logging.Formatter("[%(levelname)s][%(asctime)s]%(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
fliehandler.setLevel(logging.INFO)
consolehandler = myconhandler(printf)
consolehandler.setFormatter(logging.Formatter("[%(levelname)s][%(asctime)s]%(message)s",datefmt="%Y-%m-%d %H:%M:%S"))
consolehandler.setLevel(logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('prompt_toolkit').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG,handlers=[fliehandler,consolehandler])
logger = logging.getLogger(__name__) #日志模块，输出文件为'server.log'

sock = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM) #套接字的初始化
sock.setblocking(False)
with warnings.catch_warnings(): #不显示ssl协议的报警
    warnings.simplefilter("ignore")
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile="./server.crt", keyfile="./server.key")

with open("./config.json","r") as f: #读取配置文件
    global ip,port
    a = json.load(f)
    ip = a["ip"]
    port = a["port"]

connlist = []
clientlist = []
online = {}
conline = {}
group = {}
connaddr = {}
printd = False
exitt = 0

class serverclass():
    def __init__(self):
        global group
        sock.bind((ip,port))
        sock.listen(30)
        sock.settimeout(3)
        logger.info('Listening: '+ip+':'+str(port))
        logger.info("Loading groups...")
        with open('./group.json','r') as f: #init groups
            gp=json.load(f)
            for go in gp.keys():
                group[go] = []

    def start(self):  #此函数用于启动服务端
        threading.Thread(target=self.accpethread).start()
        threading.Thread(target=self.recvthread).start()
        threading.Thread(target=self.recvcthread).start()
        threading.Thread(target=self.clearthread).start()
        logger.info('Server is running')
        self.cli()

    def accpethread(self):
        global connlist,connaddr
        while exitt == 0:
            time.sleep(0.0001)
            try:
                conn, addr = sock.accept()
            # 包装一个现有的 Python socket,并返回一个ssl socket,server_side为true表示为服务器行为，默认为false则表示客户端
                try:
                    sslconn = context.wrap_socket(conn, server_side=True)
                    sslconn.setblocking(False) #设置为非阻塞
                    connlist.append(sslconn)
                    connaddr.update({sslconn:addr})
                    logger.info('Connect by: '+addr[0]+':'+str(addr[1]))
                except ssl.SSLError:
                    logger.warning('Unknown client '+"\""+addr[0]+':'+str(addr[1])+"\"")
                    conn.close()
            except IOError:
                pass

    def clearthread(self):
        while exitt == 0:
            time.sleep(2.5)
            for conn in connlist:
                try:
                    conn.send("{\"type\":\"0\",\"data\":\"keepalive\"}".encode('utf-8'))
                except ssl.SSLEOFError:
                    connlist.remove(conn)
                    logger.info("Disconnect by "+str(connaddr[conn][0]+":"+str(connaddr[conn][1])))
                    connaddr.pop(conn)
                except:
                    connlist.remove(conn)
                    logger.info("Disconnect by "+str(connaddr[conn][0]+":"+str(connaddr[conn][1])))
                    connaddr.pop(conn)
            for conn in clientlist:
                try:
                    conn.send("{\"type\":\"0\",\"data\":\"keepalive\"}".encode('utf-8'))
                except ssl.SSLEOFError:
                    try:
                        clientlist.remove(conn)
                        online.pop(conline[conn])
                        for i in group.keys():
                            try:
                                group[i].remove(conline[conn])
                            except:
                                continue
                        conline.pop(conn)
                        logger.info("Disconnect by "+str(connaddr[conn][0]+":"+str(connaddr[conn][1])))
                        connaddr.pop(conn)
                    except:
                        logger.info("Disconnect by "+str(connaddr[conn][0]+":"+str(connaddr[conn][1])))
                        connaddr.pop(conn)
                except:
                    try:
                        clientlist.remove(conn)
                        online.pop(conline[conn])
                        for i in group.keys():
                            try:
                                group[i].remove(conline[conn])
                            except:
                                continue
                        conline.pop(conn)
                        logger.info("Disconnect by "+str(connaddr[conn][0]+":"+str(connaddr[conn][1])))
                        connaddr.pop(conn)
                    except:
                        logger.info("Disconnect by "+str(connaddr[conn][0]+":"+str(connaddr[conn][1])))
                        connaddr.pop(conn)
    def recvthread(self):
        global connlist
        while exitt == 0:
            time.sleep(0.0001)
            for conn in connlist:
                data = self.recv_data(conn)
                try:
                    datam = json.loads(data)
                    if datam['type'] == '201':
                        self.send_data(conn,"{\"type\":\"202\",\"data\":\"accp\"}")
                        clientlist.append(conn)
                        connlist.remove(conn)
                except UnboundLocalError:
                    pass
                except json.JSONDecodeError:
                    pass
                except TypeError:
                    pass
                except ValueError:
                    pass
                except KeyError:
                    pass

    def recvcthread(self):
        global clientlist,online,conline
        while exitt == 0:
            time.sleep(0.0001)
            for conn in clientlist:
                datam = self.recv_data(conn)
                try:
                    datalm = json.loads(datam)
                    uspw = self.getuspw()
                    if datalm['type'][0] == '2':
                        if datalm['type'] == '205':
                            if self.pdcoonl(conn) == False:
                                self.send_data(conn,"{\"type\":\"411\",\"data\":\"nolo\"}")
                            else:
                                gps = ''
                                for g in group.keys():
                                    gps = gps+","+g
                                self.send_data(conn,"{\"type\":\"206\",\"data\":\""+gps[1:]+"\"}")
                                continue
                        elif datalm['type'] == '207':
                            gpp = ''
                            if self.pdcoonl(conn) == False:
                                self.send_data(conn,"{\"type\":\"411\",\"data\":\"nolo\"}")
                            elif self.pdconig(conn) == False:
                                self.send_data(conn,"{\"type\":\"415\",\"data\":\"nigp\"}")
                            else:
                                for i in group.keys():
                                    if conline[conn] in group[i]:
                                        for gus in group[i]:
                                            gpp = gpp+","+gus
                                        self.send_data(conn,"{\"type\":\"208\",\"data\":\""+gpp[1:]+"\"}")
                                        continue
                    elif datalm['type'][0] == '3':
                        if datalm['type'] == '300':
                            if self.pdcoonl(conn):
                                self.send_data(conn,"{\"type\":\"317\",\"data\":\"conl\"}")
                            elif datalm['us'] not in list(uspw.keys()):
                                self.send_data(conn,"{\"type\":\"310\",\"data\":\"nofu\"}")
                            elif datalm['pw'] != uspw[datalm['us']]:
                                self.send_data(conn,"{\"type\":\"313\",\"data\":\"erro\"}")
                            elif self.pdusonl(datalm['us']):
                                self.send_data(conn,"{\"type\":\"311\",\"data\":\"onli\"}")
                            else:
                                online[datalm["us"]] = conn
                                conline[conn] = datalm["us"]
                                self.send_data(conn,"{\"type\":\"312\",\"data\":\"accp\"}")
                                logger.info("Log by "+conn.getpeername()[0]+":"+str(conn.getpeername()[1])+" for "+str(datalm['us']))
                        elif datalm["type"] == '301':
                            if self.pdusal(datalm['us']):
                                self.send_data(conn,"{\"type\":\"315\",\"data\":\"alu\"}")
                            elif len(str(datalm['us'])) > 12 or len(str(datalm['pw'])) > 16:
                                self.send_data(conn,"{\"type\":\"314\",\"data\":\"rege\"}")
                            else:
                                self.putuspw(datalm['us'],datalm['pw'])
                                self.send_data(conn,"{\"type\":\"316\",\"data\":\"accp\"}")
                                logger.info("Reg by "+conn.getpeername()[0]+":"+str(conn.getpeername()[1])+" for "+str(datalm['us']))
                    elif datalm['type'][0] == '4':
                        if datalm['type'] == '401':
                            if self.pdcoonl(conn) == False:
                                self.send_data(conn,"{\"type\":\"411\",\"data\":\"nolo\"}")
                            elif datalm['gp'] not in group.keys():
                                self.send_data(conn,"{\"type\":\"413\",\"data\":\"nofu\"}")
                            elif self.pdconper(conn,datalm["gp"]) == False:
                                self.send_data(conn,"{\"type\":\"416\",\"data\":\"perd\"}")
                            elif self.pdconit(conn,datalm['gp']):
                                self.send_data(conn,"{\"type\":\"412\",\"data\":\"alig\"}")
                            else:
                                for ii in group.keys():
                                    if conline[conn] in group[ii]:
                                        group[ii].remove(conline[conn])
                                group[datalm['gp']].append(conline[conn])
                                self.send_data(conn,"{\"type\":\"414\",\"data\":\"accp\"}")
                                logger.info("Choose group:"+str(datalm['gp']+" by:"+conline[conn]))
                        elif datalm['type'] == '402':
                            if self.pdcoonl(conn) == False:
                                self.send_data(conn,"{\"type\":\"411\",\"data\":\"nolo\"}")
                            elif self.pdusigp(conline[conn]) == False:
                                self.send_data(conn,"{\"type\":\"415\",\"data\":\"nigp\"}")
                            elif self.checkcon(conn,datalm['us']) == False:
                                self.send_data(conn,"{\"type\":\"0\",\"data\":\"nmsl\"}")
                            else:
                                for i in group.keys():
                                    if conline[conn] in group[i]:
                                        for us in group[i]:
                                            self.send_data(online[us],"{\"type\":\"420\",\"msg\":\""+datalm['msg']+"\",\"us\":\""+datalm["us"]+"\"}")
                                        for ii in group.keys():
                                            if conline[conn] in group[ii]:
                                                gpt = ii
                                        logger.info("from:"+datalm['us']+" recv:"+datalm['msg']+" to:"+gpt)
                                        continue
                    elif datalm['type'] == '0':
                        pass
                    else:
                        logger.warning("Unknown data: "+datam+" by: "+conn.getpeername()[0]+":"+str(conn.getpeername()[1]))
                # except UnboundLocalError:
                #     pass
                except json.JSONDecodeError:
                    pass
                except TypeError:
                    pass
                except KeyError:
                    pass
                except Exception as e:
                    logger.error("Unexception Error: "+str(e))

    def cli(self):  #线程部分，此函数后的都是方法
        global connlist,printd,clientlist
        history = InMemoryHistory()
        while True:
            try:
                get = prompt('>',history=history)
            except KeyboardInterrupt:
                printf("^C")
            if get == '':
                continue
            elif get == 'exit':
                global exitt
                exitt = 1
                logger.info("Server stopped")
                sys.exit(0)
            elif get[:4] == 'saya':
                for i in group.keys():
                    for ii in group[i]:
                        self.send_data(online[ii],("{\"type\":\"420\",\"msg\":\""+get[5:]+"\",\"us\":\""+"[Server*]"+"\"}"))
                logger.info(str("from:self recv:"+get[4:]+" to:*"))
            elif get[:3] == 'say':
                a = get.split(' ')
                for i in a:
                    if i == '':
                        a.remove(i)
                try:
                    for i in group[a[1]]:
                        self.send_data(online[i],("{\"type\":\"420\",\"msg\":\""+a[2]+"\",\"us\":\""+"[Server]"+"\"}"))
                    logger.info(str("from:self recv:"+a[2])+" to:"+a[1])
                except:
                    logger.info("say:Send failed")
            elif get[:4] == 'list':
                gps = ''
                for g in group.keys():
                    gps = gps+","+g
                logger.info("group:"+gps[1:])
                for gg in group.keys():
                    gpp = ''
                    for gus in group[gg]:
                        gpp = gpp+","+gus
                    logger.info(gg+":"+gpp)
            elif get[:4] == 'eval':
                try:
                    eval(get[5:])
                except Exception as e:
                    logger.warning("eval:Error during execution: "+str(e))
            elif get[:6] == 'addper':
                add = get.split(' ')
                for i in add:
                    if i == '':
                        add.remove(i)
                with open("./group.json","r+") as f:
                    try:
                        ddp = json.load(f)
                    except:
                        logger.info("addper:Set failed")
                    if add[1] in ddp.keys():
                        if add[2] in ddp[add[1]]:
                            logger.info("addper:Alrealy in")
                        else:
                            with open("./group.json","w+") as f:
                                ddp[add[1]].append(add[2])
                                json.dump(ddp ,f ,indent=4 ,ensure_ascii=False)
                    else:
                        logger.info("addper:Set failed")
                        continue
            elif get[:6] == 'delper':
                rem = get.split(' ')
                for i in rem:
                    if i == '':
                        rem.remove(i)
                with open("./group.json","r+") as f:
                    try:
                        ddp = json.load(f)
                    except:
                        logger.info("delper:Set failed")
                    if rem[1] in ddp.keys():
                        if rem[2] not in ddp[rem[1]]:
                            logger.info("delper:Not in")
                        else:
                            with open("./group.json","w+") as f:
                                ddp[rem[1]].remove(rem[2])
                                json.dump(ddp ,f ,indent=4 ,ensure_ascii=False)
                    else:
                        logger.info("delper:Set failed")
                        continue
            elif get[:6] == 'setgpp':
                with open("./group.json","r") as f:
                    ddc = json.load(f)
                aa = get.split(' ')
                for i in aa:
                    if i == '':
                        aa.remove(i)
                try:
                    if 'w' == aa[2]:
                        if ddc[aa[1]][0] == '*':
                            ddc[aa[1]].pop(0)
                            with open("./group.json",'w+') as f:
                                json.dump(ddc ,f ,indent=4 ,ensure_ascii=False)
                        else:
                            continue
                    elif 'b' == aa[2]:
                        if ddc[aa[1]][0] == '*':
                            continue
                        else:
                            ddc[aa[1]].insert(0,"*")
                            with open("./group.json",'w+') as f:
                                json.dump(ddc ,f ,indent=4 ,ensure_ascii=False)
                except:
                    logger.info("setgpp:Set failed")
            elif get[:4] == 'setp':
                if printd:
                    printd = False
                else:
                    printd = True
            else:
                logger.info("Unknown Command")

    def recv_data(self, conn):
        try:
            msg = conn.recv(10240).decode("utf-8")
            if not msg:
                pass
            elif msg:
                if printd:
                    logger.debug("from"+str(conn.getpeername())+":"+msg)
                return msg
        except IOError as e:
            pass
        except UnicodeDecodeError as e:
            pass

    def send_data(self, conn, msg):
        try:
             conn.send(str(msg).encode("utf-8"))
        except Exception as e:
            logger.error("Error during sending data: " + e)

    def getuspw(self):
        with open("./user.json","r") as f:
            a = json.load(f)
            return a

    def rmclear(self, conn):
        try:
            for iii in conline:
                if conn == list(iii.keys())[0]:
                    conline.remove(iii)
                    online.remove({iii[conn]:conn})
        except:
            pass

    def pdconig(self,conn):
        try:
            for ii in group.keys():
                if conline[conn] in group[ii]:
                    return True
            return False
        except:
            pass

    def pdconit(self,conn,gp):
        try:
            for ii in group.keys():
                if conline[conn] in group[ii]:
                    if ii == gp:
                        return True
            return False
        except:
            pass

    def pdconper(self,conn,gp):
        try:
            conus = conline[conn]
            with open("./group.json","r") as f:
                te = json.load(f)[gp]
                if "*" in te:
                    te.remove("*")
                    if conus in te:
                        return False
                    else:
                        return True
                else:
                    if conus in te:
                        return True
                    else:
                        return False
        except:
            pass

    def pdusonl(self,user):
        try:
            ii = online.keys()
            if user in ii:
                return True
            else:
                return False
        except:
                pass
        
    def pdusigp(self,user):
        try:
            ii = group.keys()
            for i in ii:
                if user in group[i]:
                    return True
            return False
        except:
            pass

    def pdcoonl(self,conn):
        try:
            ii = conline.keys()
            if conn in ii:
                return True
            else:
                return False
        except:
                pass

    def checkcon(self,conn,user):
        try:
            if user == conline[conn]:
                return True
            else:
                return False
        except:
            pass

    def pdusal(self,us):
        a = self.getuspw()
        if us in a:
            return True
        else:
            return False
            
    def putuspw(self,us,pw):
        a = self.getuspw()
        aa = {us:pw}
        a.update(aa)
        with open("./user.json","w+") as f:
            json.dump(a ,f ,indent=4 ,ensure_ascii=False)

    def deluspw(self,us):
        a = self.getuspw()
        aa = str(us)
        a.pop(aa)
        with open("./user.json","w+") as f:
            json.dump(a,f,indent=4,ensure_ascii=False)
    
if __name__ == '__main__':
    with open("./server.log","a+") as f:
        f.write("---------------Server Starting---------------\n")
    printf("---------------Server Starting---------------")
    main = serverclass()
    main.start()