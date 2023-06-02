import sys,socket,os,warnings,ssl,time,json
import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, Qt
# from qt_material import apply_stylesheet

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

username = ""
password = ""
mainlinefou = 1
canre = False

class myqlineedit(QtWidgets.QLineEdit):
    def focusInEvent(self, e):
        global mainlinefou
        # print("foucsin")
        mainlinefou = 0
        return super().focusInEvent(e)
    
    def focusOutEvent(self, e):
        global mainlinefou
        # print("foucsout")
        mainlinefou = 1
        return super().focusOutEvent(e)

class Ui_Chat03Beta(QtWidgets.QMainWindow):
    def setupUi(self, Chat03Beta):
        Chat03Beta.setObjectName("Chat03Beta")
        Chat03Beta.resize(783, 559)
        self.centralwidget = QtWidgets.QWidget(Chat03Beta)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 90, 541, 321))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(630, 460, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = myqlineedit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 460, 541, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(630, 91, 131, 321))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Small")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(630, 40, 131, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.activated.connect(self.setgroup)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 40, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Variable Text")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        Chat03Beta.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Chat03Beta)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 783, 26))
        self.menubar.setObjectName("menubar")
        self.menuoptions = QtWidgets.QAction(self.menubar)
        self.menuoptions.setObjectName("menuoptions")
        self.menuoptions.triggered.connect(self.showcon)
        self.menuabout = QtWidgets.QAction(self.menubar)
        self.menuabout.setObjectName("menuabout")
        self.menuabout.triggered.connect(self.showabo)
        self.menuexit = QtWidgets.QAction(self.menubar)
        self.menuexit.setObjectName("menuexit")
        self.menuexit.triggered.connect(self.exit)
        Chat03Beta.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Chat03Beta)
        self.statusbar.setObjectName("statusbar")
        Chat03Beta.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuoptions)
        self.menubar.addAction(self.menuabout)
        self.menubar.addAction(self.menuexit)

        self.setFixedSize(self.width(), self.height())

        self.retranslateUi(Chat03Beta)
        QtCore.QMetaObject.connectSlotsByName(Chat03Beta)

    def retranslateUi(self, Chat03Beta):
        _translate = QtCore.QCoreApplication.translate
        Chat03Beta.setWindowTitle(_translate("Chat03Beta", "Chat03Beta"))
        self.pushButton.setText(_translate("Chat03Beta", "Send"))
        self.pushButton.clicked.connect(self.saymsg)
        self.label.setText(_translate("Chat03Beta", "Chat 0.3 Beta"))
        self.label_2.setText(_translate("Chat03Beta", "Group"))
        self.menuoptions.setText(_translate("Chat03Beta", "contorl"))
        self.menuabout.setText(_translate("Chat03Beta", "about"))
        self.menuexit.setText(_translate("Chat03Beta", "exit"))
        reth.textbs.connect(self.uponli)
        reth.clearts.connect(self.textBrowser_2.clear)

    def closeEvent(self, a):
        self.exitt(a)

    def setgroup(self ,a):
        senddata(("{\"type\":\"401\",\"gp\":\""+self.comboBox.currentText()+"\"}"))

    def uponli(self ,a):
        self.textBrowser_2.clear()
        self.textBrowser_2.setText(a)

    def saymsg(self,a):
        if pdcon():
            if mainwin.lineEdit.text() == "":
                pass
            else:
                try:
                    if mainwin.lineEdit.text() == "":
                        pass
                    else:
                        say(mainwin.lineEdit.text())
                        mainwin.lineEdit.clear()
                except:
                    pass
        else:
            pass

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Return or QKeyEvent.key() == QtCore.Qt.Key_Enter:
            if mainlinefou == 0:
                # print('enterok')
                if pdcon():
                    if mainwin.lineEdit.text() == "":
                        pass
                    else:
                        try:
                            if mainwin.lineEdit.text() == "":
                                pass
                            else:
                                say(mainwin.lineEdit.text())
                                mainwin.lineEdit.clear()
                        except:
                            pass
                else:
                    pass
            else:
                # print('nothing')
                pass

    def exit(self,a):
        result = QtWidgets.QMessageBox.question(None, "Exit?", "Do you want to exit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if(result == QtWidgets.QMessageBox.Yes):
            global disconn
            disconn = True
            control.close()
            about.close()
            sys.exit(app.exec_())
        else:
            pass

    def exitt(self, a):
        result = QtWidgets.QMessageBox.question(None, "Exit?", "Do you want to exit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if(result == QtWidgets.QMessageBox.Yes):
            global disconn
            disconn = True
            control.close()
            about.close()
            a.accept()
        else:
            a.ignore()

    def showcon(self,a):
        control.show()

    def showabo(self,a):
        about.show()

class Ui_contorl(QtWidgets.QWidget):
    def setupUi(self, contorl):
        contorl.setObjectName("contorl")
        contorl.resize(595, 200)
        self.lineEdit = QtWidgets.QLineEdit(contorl)
        self.lineEdit.setGeometry(QtCore.QRect(170, 40, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.reg = QtCore.QRegExp("^[0-9.]{15}$")
        self.vail = QtGui.QRegExpValidator(None)
        self.vail.setRegExp(self.reg)
        self.lineEdit.setValidator(self.vail)
        self.lineEdit_2 = QtWidgets.QLineEdit(contorl)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 80, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setPlaceholderText("6999")
        self.reg2 = QtCore.QRegExp("^[0-9]{5}$")
        self.vail2 = QtGui.QRegExpValidator(None)
        self.vail2.setRegExp(self.reg2)
        self.lineEdit_2.setValidator(self.vail2)
        self.lineEdit_3 = QtWidgets.QLineEdit(contorl)
        self.lineEdit_3.setGeometry(QtCore.QRect(410, 40, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.reg3 = QtCore.QRegExp("^[a-zA-Z0-9\u4e00-\u9fa5_]{12}$")
        self.vail3 = QtGui.QRegExpValidator(None)
        self.vail3.setRegExp(self.reg3)
        self.lineEdit_3.setValidator(self.vail3)
        self.lineEdit_4 = QtWidgets.QLineEdit(contorl)
        self.lineEdit_4.setGeometry(QtCore.QRect(410, 80, 113, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reg4 = QtCore.QRegExp("^[^\"\'\u4e00-\u9fa5]{16}$")
        self.vail4 = QtGui.QRegExpValidator(None)
        self.vail4.setRegExp(self.reg4)
        self.lineEdit_4.setValidator(self.vail4)
        self.label = QtWidgets.QLabel(contorl)
        self.label.setGeometry(QtCore.QRect(80, 40, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(contorl)
        self.label_2.setGeometry(QtCore.QRect(80, 80, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(contorl)
        self.label_3.setGeometry(QtCore.QRect(320, 40, 72, 15))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(contorl)
        self.label_4.setGeometry(QtCore.QRect(320, 80, 72, 15))
        self.label_4.setObjectName("label_4")
        self.checkBox_2 = QtWidgets.QCheckBox(contorl)
        self.checkBox_2.setGeometry(QtCore.QRect(80, 120, 91, 19))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(self.swbut)
        self.pushButton_4 = QtWidgets.QPushButton(contorl)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 120, 93, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(contorl)
        self.pushButton_5.setGeometry(QtCore.QRect(290, 120, 93, 28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton = QtWidgets.QPushButton(contorl)
        self.pushButton.setGeometry(QtCore.QRect(400, 120, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(contorl)
        self.label_5.setGeometry(QtCore.QRect(150, 160, 301, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")

        self.setFixedSize(self.width(), self.height())

        self.retranslateUi(contorl)
        QtCore.QMetaObject.connectSlotsByName(contorl)

    def retranslateUi(self, contorl):
        _translate = QtCore.QCoreApplication.translate
        contorl.setWindowTitle(_translate("contorl", "Control"))
        self.label.setText(_translate("contorl", "Serverip:"))
        self.label_2.setText(_translate("contorl", "Port:"))
        self.label_3.setText(_translate("contorl", "Username"))
        self.label_4.setText(_translate("contorl", "Password"))
        self.checkBox_2.setText(_translate("contorl", "register"))
        self.pushButton_4.setText(_translate("contorl", "Connect"))
        self.pushButton_4.clicked.connect(self.connser)
        self.pushButton_5.setText(_translate("contorl", "Disconnect"))
        self.pushButton_5.clicked.connect(self.disconser)
        self.pushButton.setText(_translate("contorl", "Login"))
        self.pushButton.clicked.connect(self.lorebt)
        self.label_5.setText(_translate("contorl", ""))

    def lorebt(self,a):
        global username,password
        username = self.lineEdit_3.text()
        password = self.lineEdit_4.text()
        if pdcon():
            if self.checkBox_2.isChecked():
                senddata(("{\"type\":\"301\",\"us\":\""+username+"\",\"pw\":\""+password+"\"}"))
            else:
                senddata(("{\"type\":\"300\",\"us\":\""+username+"\",\"pw\":\""+password+"\"}"))
        else:
            pass

    def warmsg(self,text):
        self.label_5.setStyleSheet("color:red")
        self.label_5.setText(str(text))
    
    def nonemsg(self,msg):
        self.label_5.setStyleSheet("color:black")
        self.label_5.setText(str(msg))

    def swbut(self,a):
        if self.checkBox_2.isChecked():
            self.pushButton.setText("Reg")
        else:
            self.pushButton.setText("Login")

    def disconser(self, a):
        global canre,s,sock
        if pdcon():
            mainwin.textBrowser.append("Disconnect from server")
            canre = False
            s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
            sock = context.wrap_socket(s)
            mainwin.comboBox.clear()
            getonusth.terminate()
            mainwin.textBrowser_2.clear()
        else:
            pass

    def connser(self, a):
        global canre
        ip = self.lineEdit.text()
        port = self.lineEdit_2.text()
        ipc = ip.split(".")
        if port == "":
            if len(ipc) < 4 or int(ipc[0]) > 225 or int(ipc[1]) > 255 or int(ipc[2]) > 255 or int(ipc[3]) > 255:
                self.warmsg("IP address is illegal")
            else:
                sock.setblocking(True)
                try:
                    sock.connect((ip,6999))
                    canre = True
                    senddata('{\"type\":\"201\"}')
                except OSError as e:
                    self.warmsg("Failed to connect the server")
                except ValueError as e:
                    if str(e) == 'attempt to connect already-connected SSLSocket!':
                        self.warmsg("Already connect to server")
                    else:
                        self.warmsg("Error:"+str(e))
        else:
            if int(port) > 65535 or len(ipc) < 4 or int(ipc[0]) > 225 or int(ipc[1]) > 255 or int(ipc[2]) > 255 or int(ipc[3]) > 255:
                self.warmsg("IP address is illegal")
            else:
                sock.setblocking(True)
                try:
                    sock.connect((ip,port))
                    canre = True
                    senddata('{\"type\":\"201\"}')
                except OSError as e:
                    self.warmsg("Failed to connect the server")
                except ValueError as e:
                    if str(e) == 'attempt to connect already-connected SSLSocket!':
                        self.warmsg("Already connect to server")
                    else:
                        self.warmsg("Error:"+e)
        
class Ui_about(QtWidgets.QWidget):
    def setupUi(self, about):
        about.setObjectName("about")
        about.resize(400, 300)
        self.pushButton = QtWidgets.QPushButton(about)
        self.pushButton.setGeometry(QtCore.QRect(150, 220, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close)
        self.textBrowser = QtWidgets.QTextBrowser(about)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.raise_()
        self.pushButton.raise_()

        self.setFixedSize(self.width(), self.height())

        self.retranslateUi(about)
        QtCore.QMetaObject.connectSlotsByName(about)

    def retranslateUi(self, about):
        _translate = QtCore.QCoreApplication.translate
        about.setWindowTitle(_translate("about", "About"))
        self.pushButton.setText(_translate("about", "Close"))
        self.textBrowser.setHtml(_translate("about", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Chat 0.3 Beta by Win11inVMware</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A good chat <a name=\"textarea-bg-text\"></a>application</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">made on 2023/05/07</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

def senddata(msg):
    sock.send(str(msg).encode('utf-8'))

def say(msg):
    sock.send(str("{\"type\":\"402\",\"msg\":\""+str(msg)+"\",\"us\":\""+str(username)+"\"}").encode('utf-8'))

def recvdata():
        global sock,s,canre
        try:
            msg = sock.recv(2048).decode("utf-8")
            if not msg:
                mainwin.textBrowser.append("Disconnect from server")
                canre = False
                s = socket.socket(family=socket.AF_INET,type=socket.SOCK_STREAM)
                sock = context.wrap_socket(s)
                mainwin.comboBox.clear()
                getonusth.terminate()
                reth.clearts.emit("a")
            else:
                return msg
        except IOError as e:
            pass
        except UnicodeDecodeError as e:
            pass
        except OSError:
            pass

class recvthread(QtCore.QThread):
    textbs = QtCore.pyqtSignal(str)
    clearts = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            time.sleep(0.0001)
            if canre:
                sock.setblocking(False)
                msg = recvdata()
                try:
                    datam = json.loads(msg)
                    if datam['type'] == '202':
                        control.nonemsg("Connected to server")
                    elif datam['type'] == '206':
                        mainwin.comboBox.addItems(datam['data'].split(","))
                    elif datam['type'] == '208':
                        temu = ""
                        for i in datam['data'].split(','):
                            temu += i + "\n"
                        temu = "online:\n" + temu
                        # print(temu)
                        self.textbs.emit(temu)
                    elif datam['type'] == '317':
                        control.warmsg("You already login")
                    elif datam['type'] == '310':
                        control.warmsg("User not found")
                    elif datam['type'] == '313':
                        control.warmsg("Incorrect password")
                    elif datam['type'] == '311':
                        control.warmsg("User is online")
                    elif datam['type'] == '312':
                        senddata(("{\"type\":\"205\",\"data\":\"ndgp\"}"))
                        control.nonemsg("Login successful")
                    elif datam['type'] == '315':
                        control.warmsg("User already exists")
                    elif datam['type'] == '316':
                        control.nonemsg("Register successful")
                    elif datam['type'] == '314':
                        control.warmsg("Error during register")
                    elif datam['type'] == '411':
                        mainwin.textBrowser.append("Not logged in")
                    elif datam['type'] == '413':
                        mainwin.textBrowser.append("Group not found")
                    elif datam['type'] == '412':
                        mainwin.textBrowser.append("Already in this group")
                    elif datam['type'] == '416':
                        mainwin.textBrowser.append("Group permission denied")
                    elif datam['type'] == '415':
                        mainwin.textBrowser.append("Not in group")
                    elif datam['type'] == '414':
                        getonusth.start()
                        mainwin.textBrowser.append("Successful choose group:"+mainwin.comboBox.currentText())
                    elif datam['type'] == '420':
                        if datam['us'] == "[Server]":
                            mainwin.textBrowser.append("[Server]"+datam['msg'])
                        elif datam['us'] == "[Server*]":
                            mainwin.textBrowser.append("[Server*]"+datam['msg'])
                        else:
                            mainwin.textBrowser.append("<"+datam['us']+">"+datam['msg'])
                    elif datam['type'] == '0':
                        pass
                    else:
                        pass
                        # print('error msg')
                except json.JSONDecodeError:
                    pass
                except TypeError:
                    pass
                except KeyError:
                    pass
            else:
                pass

class getonus(QtCore.QThread):
    def run(self):
        while True:
            # print("running")
            senddata("{\"type\":\"207\",\"data\":\"ndus\"}")
            time.sleep(3.8)
            
def pdcon():
    try:
        sock.getpeername()
        return True
    except socket.error:
        return False

if True:
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("./icon.ico"))
    # apply_stylesheet(app, theme='light_blue.xml')
    getonusth = getonus()
    reth = recvthread()
    reth.start()
    mainwin = Ui_Chat03Beta()
    control = Ui_contorl()
    about = Ui_about()
    mainwin.setupUi(mainwin)
    control.setupUi(control)
    about.setupUi(about)
    mainwin.show()
    # control.show()
    # about.show()
    sys.exit(app.exec_())