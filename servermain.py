import logging
import socket

logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s]%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)


class ServerClass(object):
    def __init__(self):
        self.__HOST = "127.0.0.1"
        self.__PORT = 6999
        self.ADDR = (self.__HOST, self.__PORT)
        self.__TCP_SOCKET = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # 设置非阻塞
        # self.__TCP_SOCKET.setblocking(False)
        self.__TCP_SOCKET.settimeout(0.0)
        # 用来存放套接字对象的列表
        self.connlist = []

    def start_server(self):
        with self.__TCP_SOCKET as sock:
            sock.bind(self.ADDR)
            sock.listen(10)
            logger.info("Server is Running")
            while True:
                try:
                    conn, addr = sock.accept()
                    # logger.info(conn)
                    conn.setblocking(False)
                    logger.info(('connect by '+str(addr)))
                    conn.sendall('Welcome to Chat'.encode('gbk'))
                    # 添加到列表
                    self.connlist.append(conn)
                # 如果没有连接进来需要捕获BlockingIOError异常
                except BlockingIOError as e:
                    pass
                    # logger.debug("没有新的客户端连接")
                for conn in self.connlist:
                    msg = self.recv_data(conn)
                    if msg:
                        for connn in self.connlist:
                            self.send_data(connn, msg)

    def recv_data(self, conn):
        try:
            msg = conn.recv(1024).decode("gbk")
            if not msg or msg in ["quit"]:
                logger.debug("断开连接")
                self.connlist.remove(conn)
            else:
                logger.info(msg)
                return msg
        except IOError as e:
            pass
            # logger.debug("没有接收到数据")

    def send_data(self, conn, msg):
        try:
             conn.sendall(str(msg).encode("gbk"))
        except ConnectionResetError as e:
            logger.debug("连接已断开，无法再发送信息")
            self.connlist.remove(conn)

if __name__ == '__main__':
    ServerClass().start_server()