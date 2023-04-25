import socket
# import time
import getpass
import threading
import sys
import os

sock =socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

def usage():
    print('An Internet talk application by Win11inVMware')
    print('usage: $./xxx <serverip:port> <nickname>')
    print('example: $./xxx 10.0.0.15:6999 HaLao_1')

def sendmsg(msg):
    sock.send(('<'+nickname+'>'+msg).encode('gbk'))

def recvdata():
    while True:
        recv=sock.recv(1024)
        print(recv.decode('gbk'))

if __name__ == "__main__":
    nickname = '_'
    ip = ()
    if len(sys.argv) != 3:
        usage()
        sys.exit(0)
    else:
        ipch=sys.argv[1].split(":")
        ipchh=ipch[0].split(".")
        if int(ipch[1]) > 65535 or len(ipchh) < 4 or int(ipchh[0]) > 225 or int(ipchh[1]) > 255 or int(ipchh[2]) > 255 or int(ipchh[3]) > 255:
            print('ip address is illegal')
        else:
            nickname = sys.argv[2]
            ip = (ipch[0],int(ipch[1]))

    sock.connect(ip)
    threading.Thread(target=recvdata).start()

    while True:
        # get = getpass.getpass('')
        get = input()
        # try:
        if get == '':
            continue
        if get == '/exit':
            os.system('taskkill /f /pid '+str(os.getpid())+" >nul")
            break
        elif get[:2] == '//':
            sendmsg(get[1:])
        elif get == '/help':
            print("Commands:")
            print('help       exit       /')
        elif get[0] == '/':
            print('Unknown command,type \'help\' to get help')
        else:
            sendmsg(get)
        # except:
        #     continue