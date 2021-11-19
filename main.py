import pickle
from socket import *
import threading
import sys

from struct import unpack
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 8080))
serverSock.listen(1)
def utf8len(s):#utf-8 형태의 바이트 갯수를 반환합니다.
    return len(s.encode('utf-8'))

class socketMsg:#인자는 순서대로 닉네임,메세지,함수기능 입니다.  함수기능(노멀 문자전송,닉네임 변경기능,비활성화)
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


class userLst:  #인자들은 순서대로 디스크립터,아이피주소,유저넘버,유저닉네임,활성화 여부.
    fd=0
    addr=""
    userNum=1
    userNickName=""
    isActive=False
    def __init__(self,fd,addr,userNum,isActive=False):
        self.fd=fd
        self.addr=addr
        self.userNum=userNum
        self.isActive=isActive

def newClientThread(connectionSock):
    print("new Client Thread starts")



    # 수신파트

    dataByteSize = None
    recvLoop = True
    while recvLoop:
        dataByteSize = connectionSock.recv(10)  # 바이트 수가 아니고 글자수네(utf-8이 한글자당 한바이트....)  그래도 10자리면 백억단위 자릿수는 가능하겠지.
        # 백억다리 자리수면 바이트수로만 따져도... 10기가 까지는 충분히 길이 표기 가능하니까.
        # 물론 이시점에서 오는건 순수하게 10자리수니까.... 10바이트정도만.
        # 아무리 파일이 커도 적어도 압축하지 않는이상 파일 하나가 10기가를 넘을 것 같지는 않고...
        # 어쨋거나 송신은 성공적으로 마쳤다.
        # 소켓 끊기면 exception 뿜어내긴한다.  처리가 필요하다.
        # 근데 용케 프로그램이 끝ㅎ기진 않고 디스크립터도 정상적으로 잡힌다.

        print(dataByteSize)
        dataByteSize = dataByteSize.decode('utf-8')
        #dataByteSize = int(dataByteSize)
        if (dataByteSize.isdecimal()):#정상적으로 숫자가 돌아왔나????
            print("data size received", dataByteSize)
            recvLoop = False






    data = connectionSock.recv(int(dataByteSize)*10)#그냥 주면 클래스가 중간에 잘려서 와서 넉넉하게 *10배 주었다.  이 현상이 일어나는 원인은 잘 모르겠다.
    print("print before Pickle data", data)
    data = pickle.loads(bytes(data))#불러온 바이트값을 클래스로 다시 변환해주고 있다.  엄밀히 말하면 클래스로 변환해주는게 아니라 원래 클래스였던게 바이트로 변환되온걸 다시 클래스로 원상복구해준것이다.
    print("print Pickled data", data)
    #정상 작동여부 확인용.

    if(data.mode ==0):
        for i in userList:
            #if(i.isActive != False) and (connectionSock != i.fd): 첫번 째 조건은 비활성화(로그아웃이나 기타상황으로 비활성화 설정된 유저) 유저를 제외하는 조건이고 두번째는 자기 자신에게 메세지를 보내는것을 방지합니다.
            if(i.isActive != False) :
                print("send msg is ", data.message)
                sendMsgToAnotherClient(data,i.fd)
                #이경우(비활성화된 사용자가 아니다 + 내 자신이 아니다)

        '''
        normal send Msg 0
        nickname  1
        log out 2            
        '''
    elif(data.mode==1):
        for i in userList:
            if(i.fd == connectionSock):
                i.userNickName =data.nickname
    elif(data.mode==2):
        for i in userList:
            if(i.fd==connectionSock):
                i.isActive=False
    else:
        print("You got the msg error or wrong function options.")










def sendMsgToAnotherClient(data,connectionSock):
    # 송신.
    print("send msg is ",data.message)


    sendMsg = data
    sendMsgLen = sys.getsizeof(sendMsg)#메세지 의 길이 여기서 메세지는 아마 메세지를 포함한 "socketMsg" 클래스이다.

    connectionSock.send(str(sendMsgLen).encode('utf-8'))
    print('메시지길이를  보냈습니다.')

    connectionSock.send(pickle.dumps(sendMsg))#바이트로 변환하여 전송.
    #connectionSock.send(sendMsg.encode('utf-8'))
    print('메시지를  보냈습니다.')



#실제 서버 실행파트.
if __name__=="__main__":
    print("server program has been started.")
    userList=[]
    threadList=[]

    while (True):
        #여기는 서버  입니다.
        connectionSock, addr = serverSock.accept()
        print(str(addr),'에서 접속이 확인되었습니다.')

        #나간 유저가 한명이라도 존재할 경우의 수.  만약 active가 아닌 유저가 한명이라도 있으면 거기 덮어씌우는 코드이다.
        isLogoutUserExist=False
        for i in userList:
            if(i.isActive==False):
                i.isActive=True
                i.fd=connectionSock
                i.addr=addr


                isLogoutUserExist=True

        #나간 유저가 없을때. 새로 추가.
        if(isLogoutUserExist==False):
            userList.append(userLst(connectionSock,addr,len(userList)+1,True))

        threadList.append(threading.Thread(target=newClientThread,args=(connectionSock,)).start())#accept에 의해 생성된 디스크립터 정보가 나오면 스레드로 분리해주고 실행.











