import sys
from socket import *
import threading,pickle
from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMainWindow

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080))
form_class = uic.loadUiType("chatting.ui")[0]


#data.decode('utf-8')

#messageByteCnt.encode('utf-8')

#clientSock.send(message)

# 수신시  : 크기전송 -> 실제전송
# 송신시  : 크기수신 -

class socketMsg:
    nickname="익명"
    message="없음"
    mode=0
    '''
    normal send Msg 0
    nickname  1
    log out 2   
    '''
    def __init__(self,nickname="익명",message="",mode=1):
        self.nickname = nickname
        self.message = message
        self.mode = mode


def utf8len(s):#utf-8 형태의 바이트 갯수를 반환합니다.
    return len(s.encode('utf-8'))



def recvMsg(myWindow):
        recvMsgSizeLoop = True
        recvMsgSize = -1
        recvMsg = False
        print('recv msg thread on')
        while recvMsgSizeLoop:
            recvMsgSize = clientSock.recv(10)  # 원리는 서버와 같다. 10자리면 용량 한계를 거의 100억단위로 표시 가능하고,
            # 사실상 10기가 까지는 용량을 표기하고 전송가능하다.
            recvMsgSize = recvMsgSize.decode('utf-8')
            if (recvMsgSize.isdecimal()):  # 올바르게 숫자크기값 이 돌아왔는지 확인합니다.
                print("data size returned", recvMsgSize)

                recvMsgSize = int(recvMsgSize)  # 이거 안해줬다가 str고쳐달라고 오류 나온다.  당연히 수신 사이즈는 정수여야 합니다.

                recvMsg = clientSock.recv(recvMsgSize * 10)  # 아까 받아온 사이즈를 기반으로 수신한다. 10배정도 넉넉히주면
                # 알아서 완전한 클래스가 들어오더라......  recvMsgSize를 그대로 곧이 곧대로 쓰면 이유는 모르겠지만 바이트로 변환된 클래스가 잘려서 왔음
                recvMsg = pickle.loads(recvMsg)  # 전송받은 바이트를 다시 클래스로 변환해줍시다.

                print("msg received ",recvMsg.message)  # 클래스 정보 표시.
                #self.listView_chatting.append()

                #myWindow.listView_chatting.add(recvMsg.message)
                # QListView obejct has no attirbute add
                myWindow.listView_chatting.append(str(recvMsg.message)+"\n")
                myWindow.lineEdit_chatting.clear()







class WindowClass(QMainWindow,form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("조찬익.")
        self.button_chatting.clicked.connect(self.sendBtnClick)
        self.listView_chatting.clear()

    '''
    listView_chatting : QListView
    lineEdit_chatting : QLineEdit
    button_chatting : QPushButton
    '''



    def sendBtnClick(self):
        text = self.lineEdit_chatting.text()
        self.sendMsg(text,"닉네임1")#여기 위치에 닉네임을 집어넣으시오.
        print("text widget text",text)

    def sendMsg(self,msg,nickname):
        print("sendMsg btn clicked")
        #msg = input("input message you want to send\n")
        msg = "[ "+nickname+" ] "+msg
        a = socketMsg(nickname="익명1", message=msg, mode=0)  # 통째로 전송할 클래스.
        # 닉네임.
        #print(a)
        msgLen = sys.getsizeof(a)  # 아까 그 클래스의 크기를 따옵니다.
        #print(a.message, "\n", msgLen)


        clientSock.send(
            str(msgLen).encode('utf-8'))  # 파이썬 소켓에서 encode decode는 필수입니다.  한글호환성 문제를 방지하기위해 utf-8을 권장합니다.
        #print("send real message ")

        # 0.3초 기다렸다가 보낼까 말까 싶다. 상대방 PC에서 통신이 밀릴수도 있으니.  안해도 아직까지는 충분히 가능하다.
        a = pickle.dumps(a)  # 그 클래스를 바이트로 변환합니다.
        # print("pickled byte data", a)
        clientSock.send(a)  # 크기를 전송해서 서버측에서 데이터의 크기가 입력된 상태이니 이제 변환한 클래스를 보내줍시다.
        print("send finish")


if __name__ == "__main__":
    # 여기는 클라이언트 입니다.
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    recvThread = threading.Thread(target=recvMsg, args=(myWindow,))
    # sendThread = threading.Thread(target=sendMsg, args=())
    recvThread.start()
    # sendThread.start()
    app.exec_()









