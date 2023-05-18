import logging
import socket
import time
import json
import sys
from threading import Thread

logging.basicConfig(level=logging.DEBUG,format="[%(levelname)s][%(asctime)s]%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)
connlist = [] # 用来存放套接字对象的列表
online = [] #存放在线用户以及连接
conline = [] #存放在线用户以及连接(连接为键)
exitt = 0

with open("./config.json","r") as f:
    global ip,port,ndlg
    a = json.load(f)
    ip = a["ip"]
    port = a["port"]
    ndlg = a["needlogin"]

class ServerClass(object):
    def __init__(self):
        self.__HOST = ip
        self.__PORT = port
        self.ADDR = (self.__HOST, self.__PORT)
        self.__TCP_SOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # 设置非阻塞
        # self.__TCP_SOCKET.setblocking(False)
        self.__TCP_SOCKET.settimeout(0.0)
        self.nedlog = ndlg
        # self.connlist = [] # 用来存放套接字对象的列表
        # self.online = [] #存放在线用户以及连接
        # self.conline = [] #存放在线用户以及连接(连接为键)
        self.changeon = False
        self.pdlist=["200","201","202","203","205","210","300","301","310","313","311","312","313","314","315","316","317","400","410","411"]

    def start_server(self):
        global connlist,conline,online
        with self.__TCP_SOCKET as sock:
            sock.bind(self.ADDR)
            sock.listen(20)
            logger.info("Server is Running")
            if self.nedlog: #need login
                while exitt == 0:
                    time.sleep(0.00001)
                    if self.changeon:
                        self.send_onus()#;print("wow")
                        self.changeon=False

                    try:
                        conn, addr = sock.accept()
                        # logger.info(conn)
                        conn.setblocking(False)
                        logger.info(('connect by '+str(addr)))
                        # conn.sendall('Welcome to Chat'.encode('gbk'))
                        # 添加到列表
                        connlist.append(conn)
                    # 如果没有连接进来需要捕获BlockingIOError异常
                    except BlockingIOError as e:
                        pass
                        # logger.debug("没有新的客户端连接")
                    
                    for conn in connlist:
                        msg = self.recv_data(conn)
                        datam = str(msg).split('^')
                        if len(datam) <= 1 or datam[0] not in self.pdlist:
                            # logger.warn("unknown datagram")
                            pass
                        # elif datam[0] == '204' and datam[1] == 'onus':
                        #     print("ok")
                            # onus = ""
                            # for us in self.online:
                            #     onus = onus + "^" + list(us.keys())[0]
                            # self.send_data(conn, str("205"+onus))
                        elif datam[0] == '200' and datam[1] == 'conn':
                            self.send_data(conn, "201^accp")
                            continue
                        elif datam[0] == '202' and datam[1] == 'ndl':
                            self.send_data(conn, "203^yes")
                            continue
                        elif datam[0] == '300':
                            uspw = self.getuspw()
                            try:
                                if self.pdcoonl(conn):
                                    self.send_data(conn, "317^conl")
                                    continue
                                elif datam[1] not in uspw.keys():
                                    self.send_data(conn, "310^rst")
                                    # self.rmonline(conn)
                                    # self.rmclose(conn)
                                    continue
                                    # conn.close()
                                elif datam[2] != uspw[datam[1]]:
                                    self.send_data(conn, "313^erro")
                                    continue
                                    # self.rmonline(conn)
                                    # self.rmclose(conn)
                                # elif datam[1]:
                                #     for ii in self.online:
                                #         print(ii)
                                #         if datam[1] == ii.keys():
                                #             self.send_data(conn, "311^onli")
                                #         else:
                                #             pass
                                elif self.pdusonl(datam[1]):
                                    self.send_data(conn, "311^onli")
                                    continue
                                    # self.rmonline(conn)
                                    # self.rmclose(conn)
                                else:
                                    online.append({datam[1]:conn})
                                    conline.append({conn:datam[1]})
                                    self.changeon = True
                                    self.send_data(conn, "312^accp")
                                    logger.info("log by "+str(addr)+" for "+str(datam[1]))
                                    continue
                                    # self.send_onuss(conn)
                                    # print(self.online)
                                    # print(list(self.online[0].keys())[0])
                                    # print(self.pdusonl(datam[1]))
                                    # print(self.connlist)
                            except:
                                self.send_data(conn, "310^rst")
                                self.rmonline(conn)
                                self.rmclose(conn)
                                continue
                                
                        elif datam[0] == '301':
                            uspw = self.getuspw()
                            try:
                                if datam[1] in list(uspw.keys()):
                                    self.send_data(conn, "315^alu")
                                    continue
                                    # self.rmonline(conn)
                                    # self.rmclose(conn)
                                elif len(datam[1]) <= 12 and len(datam[2]) <= 16:
                                    self.putuspw(datam[1],datam[2])
                                    self.send_data(conn, "316^accp")
                                    logger.info("reg by "+str(addr)+" for "+str(datam[1]))
                                    continue
                                else:
                                    self.send_data(conn, "314^rege")
                                    self.rmonline(conn)
                                    self.rmclose(conn)
                                continue
                            except:
                                self.send_data(conn, "314^rege")
                                self.rmonline(conn)
                                self.rmclose(conn)
                                continue
                        elif datam[0] == '400':
                            if self.pdusonl(datam[2]) != True or self.checkcon(conn,datam[2]) == False:
                                logger.warning("410^error msgdata")
                                self.rmonline(conn)
                                self.rmclose(conn)
                                continue
                            else:
                                for connn in connlist:
                                    self.send_data(connn, ("411^"+datam[1]+"^"+datam[2]))
                                logger.info("from:"+str(datam[2])+" recv:"+str(datam[1]))
                                continue
                                # print(self.online)
                        else:
                            continue
                            # logger.warn("unknown datagram")
            else:
                while exitt == 0: #not need login
                    time.sleep(0.00001) #防止占用过高
                    if self.changeon:
                        self.send_onus()#;print("wow")
                        self.changeon=False

                    try:
                        conn, addr = sock.accept()
                        # logger.info(conn)
                        conn.setblocking(False)
                        logger.info(('connect by '+str(addr)))
                        # conn.sendall('Welcome to Chat'.encode('gbk'))
                        # 添加到列表
                        connlist.append(conn)
                    # 如果没有连接进来需要捕获BlockingIOError异常
                    except BlockingIOError as e:
                        pass
                        # logger.debug("没有新的客户端连接")
                    for conn in connlist:
                        msg = self.recv_data(conn)
                        datam = str(msg).split('^')
                        if len(datam) <= 1 or datam[0] not in self.pdlist:
                            # logger.warn("unknown datagram")
                            continue
                        elif datam[0] == '200' and datam[1] == 'conn':
                            self.send_data(conn, "201^accp")
                            continue
                        elif datam[0] == '202' and datam[1] == 'ndl':
                            self.send_data(conn, "203^no")
                            continue
                        # elif datam[0] == '204' and datam[1] == 'onus':
                        #     onus = ""
                        #     for us in self.online:
                        #         onus = onus + "^" + list(us.keys())[0]
                        #     self.send_data(conn, str("205"+onus))
                        elif datam[0] == '300':
                            # uspw = self.getuspw()
                            if self.pdcoonl(conn):
                                self.send_data(conn, "317^conl")
                                continue
                            elif len(datam[1]) > 12:
                                self.send_data(conn, "310^rst")
                                self.rmonline(conn)
                                self.rmclose(conn)
                                continue
                                # conn.close()
                            # elif datam[2] != uspw[datam[1]]:
                            #     self.send_data(conn, "313^erro")
                            #     self.rmonline(conn)
                            #     self.rmclose(conn)
                            # elif datam[1]:
                            #     for ii in self.online:
                            #         print(ii)
                            #         if datam[1] == ii.keys():
                            #             self.send_data(conn, "311^onli")
                            #         else:
                            #             pass
                            elif self.pdusonl(datam[1]):
                                self.send_data(conn, "311^onli")
                                continue
                                # self.rmonline(conn)
                                # self.rmclose(conn)
                            else:
                                online.append({datam[1]:conn})
                                conline.append({conn:datam[1]})
                                self.changeon = True
                                self.send_data(conn, "312^accp")
                                logger.info("log by "+str(addr)+" for "+str(datam[1]))
                                continue
                                # self.send_onuss(conn)
                                # print(self.online)
                                # print(list(self.online[0].keys())[0])
                                # print(self.pdusonl(datam[1]))
                                # print(self.connlist)
                        # elif datam[0] == '301':
                        #     uspw = self.getuspw()
                        #     if datam[1] in list(uspw.keys()):
                        #         self.send_data(conn, "315^alu")
                        #         self.rmonline(conn)
                        #         self.rmclose(conn)
                        #     elif len(datam[1]) <= 12 and len(datam[2]) <= 16:
                        #         self.putuspw(datam[1],datam[2])
                        #         self.send_data(conn, "312^accp")
                        #         logger.info("reg by "+str(addr)+" for "+str(datam[1]))
                        #     else:
                        #         self.send_data(conn, "314^rege")
                        #         self.rmonline(conn)
                        #         self.rmclose(conn)
                        elif datam[0] == '301':
                            self.send_data(conn, "314^rege")
                            self.rmonline(conn)
                            self.rmclose(conn)
                        elif datam[0] == '400':
                            if self.pdusonl(datam[2]) != True or self.checkcon(conn,datam[2]) == False:
                                logger.warning("410^error msgdata")
                                self.rmonline(conn)
                                self.rmclose(conn)
                                continue
                            else:
                                for connn in self.connlist:
                                    self.send_data(connn, ("411^"+datam[1]+"^"+datam[2]))
                                logger.info("from:"+str(datam[2])+" recv:"+str(datam[1]))
                                continue
                                # print(self.online)
                        else:
                            continue
                            # logger.warn("unknown datagram")

    def recv_data(self, conn):
        try:
            msg = conn.recv(10240).decode("utf-8")
            if not msg:
                logger.debug("Disconnect by "+str(conn))
                connlist.remove(conn)
                self.rmonline(conn)
            else:
                # logger.debug(msg)
                return msg
        except IOError as e:
            pass
            # logger.debug("没有接收到数据")

    def send_data(self, conn, msg):
        try:
             conn.send(str(msg).encode("utf-8"))
        except ConnectionResetError as e:
            logger.info("Connection Lost, cannot send data")
            connlist.remove(conn)
            self.rmonline(conn)
        except:
            logger.info("Connection Lost, cannot send data")
            connlist.remove(conn)
            self.rmonline(conn)

    def rmclose(self, conn):
        connlist.remove(conn)
        conn.close()

    def getuspw(self):
        with open("./user.json","r") as f:
            a = json.load(f)
            return a

    def rmonline(self, conn):
        try:
            for iii in conline:
                if conn == list(iii.keys())[0]:
                    conline.remove(iii)
                    online.remove({iii[conn]: conn})
                    self.changeon = True
        except:
            pass

    def pdusonl(self,user):
        try:
            for ii in online:
                if user == list(ii.keys())[0]:
                    # print("changed")
                    return True
                else:
                    pass
        except:
                pass
        
    def pdcoonl(self,conn):
            try:
                for ii in conline:
                    if conn == list(ii.keys())[0]:
                        # print("changed")
                        return True
                    else:
                        pass
            except:
                    pass

    def checkcon(self,conn,user):
        try:
            for iii in online:
                if user == list(iii.keys())[0]:
                    if conn == list(iii.values())[0]:
                        # print("ture")
                        return True
                    else:
                        # print("false")
                        return False
        except:
            pass

    def putuspw(self,us,pw):
        a = self.getuspw()
        aa = {us:pw}
        a.update(aa)
        with open("./user.json","w+") as f:
            json.dump(a ,f ,indent=4 ,ensure_ascii=False)

    def send_onus(self):
        onus = ""
        for us in online:
            onus = onus + "^" + list(us.keys())[0]
        for connn in connlist:
            self.send_data(connn, ("205"+onus))
    
    def send_onuss(self,conn):
        onus = ""
        for us in online:
            onus = onus + "^" + list(us.keys())[0]
        self.send_data(conn, ("205"+onus))

    def cli(self):
        global connlist,online,conline
        while True:
            get = input()
            if get == 'exit':
                global exitt
                exitt = 1
                sys.exit(0)
            elif get[:3] == 'say':
                for connn in connlist:
                    self.send_data(connn,("411^"+get[4:]+"^[Server]"))
                logger.info(str("from:self recv:"+get[4:]))
            elif get[:4] == 'list':
                onus = ""
                # print(onlineuser)
                for us in online:
                    onus = onus + "," + list(us.keys())[0]
                print("online:"+onus[1:])
            elif get[:4] == 'eval':
                eval(get[5:])
            else:
                continue

if __name__ == '__main__':
    Thread(target=ServerClass().start_server).start()
    Thread(target=ServerClass().cli).start()