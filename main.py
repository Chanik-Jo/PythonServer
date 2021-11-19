from socket import *
import threading
from struct import unpack
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', 8080))
serverSock.listen(1)


def utf8len(s):#utf-8 형태의 바이트 갯수를 반환합니다.
    return len(s.encode('utf-8'))

if __name__=="__main__":
    print("server program has been started.")


    while (True):

        #여기는 서버  입니다.


        connectionSock, addr = serverSock.accept()
        print(str(addr),'에서 접속이 확인되었습니다.')


        #수신파트
        dataByteSize=0
        data=""
        recvLoop = True
        while recvLoop:
            dataByteSize=connectionSock.recv(10)#바이트 수가 아니고 글자수네 ㅅㅂ 그래도 10자리면 백억단위 자릿수는 가능하겠지.
            #백억다리 자리수면 바이트수로만 따져도... 10기가 까지는 충분히 길이 표기 가능하니까.
            #물론 이시점에서 오는건 순수하게 10자리수니까.... 10바이트정도만.
            #아무리 파일이 커도 적어도 압축하지 않는이상 파일 하나가 10기가를 넘을 것 같지는 않고...
            #어쨋거나 송신은 성공적으로 마쳤다.
            print(dataByteSize)
            dataByteSize =dataByteSize.decode('utf-8')
            if(dataByteSize.isdecimal()):
                print("data size received",dataByteSize)
                recvLoop=False


        data = connectionSock.recv(int(dataByteSize))
        data =data.decode('utf-8')





        print('받은 데이터 : ', data)



        #여기까지 수신 끝.

        #송신.
        sendMsg = 'I am a server.'
        sendMsgLen = utf8len(sendMsg)

        connectionSock.send(str(sendMsgLen).encode('utf-8'))
        print('메시지길이를  보냈습니다.')
        connectionSock.send(sendMsg.encode('utf-8'))
        print('메시지를  보냈습니다.')